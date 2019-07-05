import json
import http

from flask import Flask, request

from geopy.geocoders import Nominatim

app = Flask(__name__)


def geocode(address):
    geo_locator = Nominatim(user_agent='nasim.damirchli89@gmail.com')
    locations = geo_locator.geocode(address, exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "long": location.longitude})
    return result


def reverse_geocode(lat, lon):
    geo_locator = Nominatim(user_agent='nasim.damirchli89@gmail.com')
    locations = geo_locator.reverse((str(lat), str(lon)), exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "long": location.longitude})
    return result


@app.route('/geocode', methods=['GET'])
def get_geocode():
    address = request.args.get('address', '')
    try:
        response = geocode(address)
        if response:
            return json.dumps(response, ensure_ascii=False)
        else:
            return '', http.HTTPStatus.NO_CONTENT
    except Exception:
        return 'Some error occurred ...', http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/reverse', methods=['GET'])
def get_reverse_geocode():
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    try:
        response = reverse_geocode(lat, lon)
        if response:
            return json.dumps(response, ensure_ascii=False)
        else:
            return '', http.HTTPStatus.NO_CONTENT
    except Exception:
        return 'Some error occurred ...', http.HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run()
