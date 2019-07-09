import json
import time
import unittest

from api import app

DTU_ADDRESS = "DTU, Anker Engelunds Vej, Lundtofte, Stampen, Lyngby-Taarbæk Kommune, Region Hovedstaden, 2800, Danmark"

DTU_LAT_1 = 55.78541445
DTU_LON_1 = 12.5202151444421


DTU_LAT_2 = 55.7860293
DTU_LON_2 = 12.5201872

DTU_RESPONSE_GEOCODE = {"status": "SUCCESS", "result": [{"address": DTU_ADDRESS, "lat": DTU_LAT_1, "lon": DTU_LON_1},
                                                        {"address": DTU_ADDRESS, "lat": DTU_LAT_2, "lon": DTU_LON_2}]}


DTU_RESPONSE_REVERSE = {"status": "SUCCESS", "result": [{"address": DTU_ADDRESS, "lat": DTU_LAT_1, "lon": DTU_LON_1}]}


class TestGeoLocation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.address = "Denmark"

    def test_geocode(self):
        response = self.app.post('/geolocation/geocode', data=json.dumps(dict(address=DTU_ADDRESS)))
        self.assertEqual(response.status_code, 202)

    def test_reverse(self):
        response = self.app.post('/geolocation/reverse', data=json.dumps(dict(lat=DTU_LAT_1, lon=DTU_LON_1)))
        self.assertEqual(response.status_code, 202)

    def test_geocode_result(self):
        create_response = self.app.post('/geolocation/geocode', data=json.dumps(dict(address=DTU_ADDRESS)))
        time.sleep(2)
        answer_response = self.app.get('/geolocation/geo_result/{}'.format(create_response.data.decode('utf8')))
        self.assertEqual(answer_response.status_code, 200)
        self.assertDictEqual(json.loads(answer_response.data.decode('utf8')), DTU_RESPONSE_GEOCODE)

    def test_reverse_result(self):
        create_response = self.app.post('/geolocation/reverse', data=json.dumps(dict(lat=DTU_LAT_1, lon=DTU_LON_1)))
        time.sleep(2)
        answer_response = self.app.get('/geolocation/geo_result/{}'.format(create_response.data.decode('utf8')))
        self.assertEqual(answer_response.status_code, 200)
        self.assertDictEqual(json.loads(answer_response.data.decode('utf8')), DTU_RESPONSE_REVERSE)


if __name__ == '__main__':
    unittest.main()
