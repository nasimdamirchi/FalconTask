from celery import Celery

from geopy.geocoders import Nominatim
import config

celery = Celery('celery_config', broker=config.REDIS_BROKER_URL, backend=config.REDIS_BACKEND_URL,
                include=['api', ], )


@celery.task()
def geocode(address):
    geo_locator = Nominatim(user_agent=config.GEOPY_USER_AGENT)
    locations = geo_locator.geocode(address, exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "lon": location.longitude})
    return result


@celery.task()
def reverse_geocode(lat, lon):
    geo_locator = Nominatim(user_agent=config.GEOPY_USER_AGENT)
    locations = geo_locator.reverse((str(lat), str(lon)), exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "lon": location.longitude})
    return result
