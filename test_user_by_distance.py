import requests
import unittest
import user_by_distance
from unittest import mock

class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

class TestUserByDistance(unittest.TestCase):

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get')
    def test_get_users_within_distance_of(self, mock_get):
        mock_get.return_value = MockResponse([{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}], 200)
        user_list = user_by_distance.get_users_within_distance_of(50, user_by_distance.london)
        self.assertEqual(user_list, [{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}])
        self.assertIn(mock.call(user_by_distance.api_url_base + 'users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('requests.get')
    def test_get_users_within_distance_of_outside_london(self, mock_get):
        mock_get.return_value = MockResponse([{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 61.6553959, 'longitude': 0.0572553}], 200)
        user_list = user_by_distance.get_users_within_distance_of(50, user_by_distance.london)
        self.assertEqual(user_list, [])
        self.assertIn(mock.call(user_by_distance.api_url_base + 'users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('requests.get')
    def test_get_users_within_distance_of_server_error(self, mock_get):
        mock_get.return_value = MockResponse(None, 500)
        user_list = user_by_distance.get_users_within_distance_of(50, user_by_distance.london)
        self.assertEqual(user_list, None)
        self.assertIn(mock.call(user_by_distance.api_url_base + 'users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('requests.get')
    def test_get_users_in_city_success(self, mock_get):
        mock_get.return_value = MockResponse([{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}], 200)
        user_list = user_by_distance.get_users_in_city('London')
        self.assertEqual(user_list, [{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}])
        self.assertIn(mock.call(user_by_distance.api_url_base + 'city/London/users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('requests.get')
    def test_get_users_in_city_empty(self, mock_get):
        mock_get.return_value = MockResponse([], 200)
        user_list = user_by_distance.get_users_in_city('London')
        self.assertEqual(user_list, [])
        self.assertIn(mock.call(user_by_distance.api_url_base + 'city/London/users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('requests.get')
    def test_get_users_in_city_server_error(self, mock_get):
        mock_get.return_value = MockResponse(None, 500)
        user_list = user_by_distance.get_users_in_city('London')
        self.assertEqual(user_list, None)
        self.assertIn(mock.call(user_by_distance.api_url_base + 'city/London/users', headers=user_by_distance.headers) , mock_get.call_args_list)

    @mock.patch('user_by_distance.get_users_within_distance_of')
    @mock.patch('user_by_distance.get_users_in_city')
    def test_get_users_in_city_or_within_distance_of(self, mock_get_city, mock_get_distance):

        mock_get_city.return_value = [{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}, {'id': 322, 'first_name': 'Hugo', 'last_name': 'Lynd', 'email': 'hlynd8x@merriam-webster.com', 'ip_address': '109.0.153.166', 'latitude': 51.6710832, 'longitude': 0.8078532}]

        mock_get_distance.return_value=[{'id': 658, 'first_name': 'Stephen', 'last_name': 'Mapstone', 'email': 'smapstonei9@bandcamp.com', 'ip_address': '187.79.141.124', 'latitude': -8.1844859, 'longitude': 113.6680747}]
        combined_list = user_by_distance.get_users_in_city_or_within_distance_of('London', 50, user_by_distance.london)

        self.assertEqual(combined_list, [{'id': 266, 'first_name': 'Ancell', 'last_name': 'Garnsworthy', 'email': 'agarnsworthy7d@seattletimes.com', 'ip_address': '67.4.69.137', 'latitude': 51.6553959, 'longitude': 0.0572553}, {'id': 322, 'first_name': 'Hugo', 'last_name': 'Lynd', 'email': 'hlynd8x@merriam-webster.com', 'ip_address': '109.0.153.166', 'latitude': 51.6710832, 'longitude': 0.8078532},{'id': 658, 'first_name': 'Stephen', 'last_name': 'Mapstone', 'email': 'smapstonei9@bandcamp.com', 'ip_address': '187.79.141.124', 'latitude': -8.1844859, 'longitude': 113.6680747}])
        self.assertIn(mock.call('London') , mock_get_city.call_args_list)
        self.assertIn(mock.call(50, user_by_distance.london) , mock_get_distance.call_args_list)


    @mock.patch('user_by_distance.get_users_within_distance_of')
    @mock.patch('user_by_distance.get_users_in_city')
    def test_get_users_in_city_or_within_distance_of_empty_empty(self, mock_get_city, mock_get_distance):

        mock_get_city.return_value = []

        mock_get_distance.return_value=[]
        combined_list = user_by_distance.get_users_in_city_or_within_distance_of('London', 50, user_by_distance.london)

        self.assertEqual(combined_list, [])
        self.assertIn(mock.call('London') , mock_get_city.call_args_list)
        self.assertIn(mock.call(50, user_by_distance.london) , mock_get_distance.call_args_list)


if __name__ == '__main__':
    unittest.main()
