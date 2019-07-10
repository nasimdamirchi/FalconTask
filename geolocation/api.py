import json
import http

from flask import Flask, request
from flasgger import Swagger

from celery_config import geocode, reverse_geocode, celery

app = Flask(__name__)
Swagger(app)


@app.route('/geolocation/geocode', methods=['POST'])
def start_geocode():
    """
        Address to Coordinates
        Call this api, passing a address and get back id for checking result in /geo_result
        ---
        tags:
          - Geocode API
        parameters:
            - in: body
              name: Address
              description: Address of location
              schema:
                type: object
                properties:
                  address:
                    type: string
        responses:
          500:
            description: Internal Server Error
          202:
            description: id for checking result in /geo_result
            schema:
              id: geocode
              properties:
                id:
                  type: string
                  description: geocode id
        """

    address = request.get_json(force=True).get('address', '')
    try:
        job = geocode.delay(address)
        result_obj = {"id": job.id}
        return json.dumps(result_obj), http.HTTPStatus.ACCEPTED
    except Exception as e:
        return 'Some error occurred ... {}'.format(e), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/geolocation/reverse', methods=['POST'])
def start_reverse_geocode():
    """
        Coordinates to Address
        Call this api, passing a latitude and longitude and get back id for checking result in /geo_result
        ---
        tags:
          - Reverse Geocode API
        parameters:
            - in: body
              name: Coordinates
              description: Coordinates of location
              schema:
                type: object
                properties:
                  lat:
                    type: string
                  lon:
                    type: string

        responses:
          500:
            description: Internal Server Error
          202:
            description: id for checking result in /geo_result
            schema:
              id: reverse
              properties:
                id:
                  type: string
                  description: geocode id
        """

    lat = request.get_json(force=True).get('lat', '')
    lon = request.get_json(force=True).get('lon', '')
    try:
        job = reverse_geocode.delay(lat, lon)
        result_obj = {"id": job.id}
        return json.dumps(result_obj), http.HTTPStatus.ACCEPTED
    except Exception as e:
        return 'Some error occurred ... {}'.format(e), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/geolocation/geo_result/<job_id>', methods=['GET'])
def geocode_result(job_id):
    """
        Result of Geocode
        Call this api, pass id and get result of geocode or reverse geocode
        ---
        tags:
          - Geo Result
        parameters:
          # - name: id
          #   type: string
          #   in: path
          #   required: True
          #   description: returned id of /geocode or /reverse

          - in: path
            name: job_id
            schema:
                type: integer
            required: true

        responses:
          200:
            description: result of geocode or reverse geocode
            schema:
              id: address
              properties:
                status:
                  type: string
                  description: status of request
                result:
                  type: object
                  description: address
        """

    job = celery.AsyncResult(job_id)
    response_obj = {'status': job.state, 'result': job.result}
    return json.dumps(response_obj, ensure_ascii=False), http.HTTPStatus.OK


if __name__ == '__main__':
    app.run()
