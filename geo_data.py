from collections import namedtuple
from datetime import datetime
from typing import NamedTuple
from geopy.geocoders import Nominatim
from astral import LocationInfo
from astral.sun import sun
import sys


def lat_log_data(city: str, country: str) -> NamedTuple:
    """
    Fetch latitude and longitude data for specified city.

    Args:
        city (str): Name of desired city.
        country (str): Country where city is located.

    Returns:
        NamedTuple City's latitude and longitude.
    """
    locator = Nominatim(user_agent='my_user_agent')
    Coordinates = namedtuple('Coordinates', ('latitude', 'longitude'))
    data = locator.geocode(city + ',' + country)
    try:
        return Coordinates(data.latitude, data.longitude)
    except AttributeError:
        print('Invalid city or country!\n Aborting!')
        sys.exit(-1)


def sunrise_sunset(latitude: float, longitude: float, **kwargs) -> NamedTuple:
    """
    Fetch sunrise and sunset datetime.

    Args:
        latitude (float): Desired latitude.
        longitude (float): Desired longitude.

    Returns:
        NamedTuple : Today's sunrise and sunset datetime.
    """
    loc = LocationInfo(latitude=latitude,
                       longitude=longitude,
                       **kwargs)
    try:
        Sun = sun(loc.observer, date=datetime.today(), tzinfo=loc.timezone)
        Sun_data = namedtuple('SunData', ('sunrise', 'sunset'))

        return Sun_data(Sun['sunrise'], Sun['sunset'])
    except ValueError as e:
        print(f'Invalid coordinates!\n{e}')
        sys.exit(-1)


if __name__ == '__main__':
    x = sunrise_sunset(*lat_log_data('Słopnice', 'Poland'),
                         name='Słopnice',
                         region='Poland',
                         timezone='Europe/Warsaw')
    # print(tzinfo())
    print(x.sunrise.replace(tzinfo=None) > datetime.now().replace(tzinfo=None))