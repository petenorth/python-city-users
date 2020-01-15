import json
import requests
from haversine import haversine,Unit

api_url_base = 'https://bpdts-test-app.herokuapp.com/'
headers = {'Content-Type': 'application/json'}
london = (51.5074, 0.1278) # (lat, lon)

def get_users_within_distance_of(distance, location):

    api_url = '{0}users'.format(api_url_base)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        filtered_users = []
        for user in response.json():
           if check_distance(distance, location, user):
               filtered_users.append(user)
        return filtered_users
    else:
        return None

def get_users_in_city(city):

    api_url = '{0}city/{1}/users'.format(api_url_base, city)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_distance(distance, location, user):

    user_location = (float(user.get('latitude')),float(user.get('longitude')))

    if haversine(location, user_location, unit=Unit.MILES) < distance:
        return True
    else: 
        return False

def get_users_in_city_or_within_distance_of(city, distance, location):
    users1 = get_users_within_distance_of(distance, location)
    users2 = get_users_in_city(city)
    for user1 in users1:
        if user1 not in users2:
            users2.append(user1)
    return users2

if __name__ == "__main__":
    import sys
    if (len(sys.argv) != 5):
      print("""
      An API that returns people who are listed as either living in a city, or whose current coordinates are within a certain distance in miles of a city (supplied as latitude and longitude)
     
      Usage:  python user_by_distance.py <city> <distance> <latitude> <Longitude>

      Example: user_by_distance.py London 50 51.5074 0.1278
      """)
      sys.exit(1)

    city = (float(sys.argv[3]), float(sys.argv[4])) # (lat, lon)
    for user in get_users_in_city_or_within_distance_of(sys.argv[1],float(sys.argv[2]), city):
        print(user)
