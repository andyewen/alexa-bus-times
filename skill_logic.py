import datetime
import hashlib
import pytz
import requests
import settings


def get_departures():
    now = datetime.datetime.now(pytz.utc)
    api_key = settings.BUSTRACKER_API_KEY
    key_with_time = (
        f'{api_key}{now.year:04}{now.month:02}{now.day:02}{now.hour:02}'
    )
    md5_api_key = hashlib.md5(key_with_time.encode('utf-8')).hexdigest()

    response = requests.get(
        settings.BUSTRACKER_API_URL,
        params={
            'module': 'json',
            'key': md5_api_key,
            'function': 'getBusTimes',
            'stopId': settings.BUSTRACKER_STOP_ID
        }
    )
    response.raise_for_status()

    data = response.json()

    departures = []
    for service in data['busTimes']:
        for departure in service['timeDatas']:
            departures.append({
                'routeName': service['mnemoService'],
                'minutesToDeparture': departure['minutes']
            })
    departures.sort(key=lambda d: d['minutesToDeparture'])
    return departures


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_departures())
