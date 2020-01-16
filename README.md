# python-city-users

An API that returns people who are listed as either living in a city, or whose current coordinates are within a certain distance in miles of a city (supplied as latitude and longitude)
     
Usage:  

The python module requires Python 3 and the `requests` and `haversine` modules installed

    pip install requests
    pip install haversine
    python user_by_distance.py <city> <distance> <latitude> <Longitude>

Example:

    python user_by_distance.py London 50 51.5074 0.1278
    
The tests can be run via

    python test_user_by_distance.py
    
or

    python -m unittest discover
