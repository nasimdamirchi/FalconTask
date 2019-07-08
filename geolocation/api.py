import json
import http

from flask import Flask, request

from celery_config import geocode, reverse_geocode, celery

app = Flask(__name__)


@app.route('/geocode', methods=['POST'])
def start_geocode():
    address = request.get_json(force=True).get('address')
    try:
        result = geocode.delay(address)
        return result.id, http.HTTPStatus.ACCEPTED
    except Exception as e:
        return 'Some error occurred ... {}'.format(e), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/reverse', methods=['POST'])
def start_reverse_geocode():
    lat = request.get_json(force=True).get('lat')
    lon = request.get_json(force=True).get('lon')
    try:
        result = reverse_geocode.delay(lat, lon)
        return result.id, http.HTTPStatus.ACCEPTED
    except Exception as e:
        return 'Some error occurred ... {}'.format(e), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/geo_result/<job_id>', methods=['GET'])
def geocode_result(job_id):
    job = celery.AsyncResult(job_id)
    response_obj = {'status': job.state, 'result': job.result}
    return json.dumps(response_obj, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
