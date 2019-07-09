from celery import Celery

from geopy.geocoders import Nominatim

celery = Celery('celery_config', broker='redis://redis:6379/0', backend='redis://redis:6379/1',
                include=['api', ], )


@celery.task()
def geocode(address):
    geo_locator = Nominatim(user_agent='nasim.damirchli89@gmail.com')
    locations = geo_locator.geocode(address, exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "long": location.longitude})
    return result


@celery.task()
def reverse_geocode(lat, lon):
    geo_locator = Nominatim(user_agent='nasim.damirchli89@gmail.com')
    locations = geo_locator.reverse((str(lat), str(lon)), exactly_one=False)
    result = []
    if locations:
        for location in locations:
            result.append({"address": location.address, "lat": location.latitude, "long": location.longitude})
    return result
