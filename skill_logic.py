import datetime
from operator import itemgetter
import requests
import iso8601


stop_board_url = 'https://tfe-opendata.com/api/v1/live_bus_times/{stop_id}'


def get_departures():
    stop_id = '36237949'
    response = requests.get(stop_board_url.format(stop_id=stop_id))
    response.raise_for_status()
    route_departures = response.json()

    now = datetime.datetime.now(datetime.timezone.utc)
    departures = []
    for route in route_departures:
        for departure in route['departures']:
            departure['routeName'] = route['routeName']
            minutes_to_departure = int((iso8601.parse_date(departure['departureTime']) - now).total_seconds() / 60)
            departure['minutesToDeparture'] = minutes_to_departure
            departures.append(departure)

    departures.sort(key=itemgetter('departureTime'))
    return departures


if __name__ == '__main__':
    print(get_departures())
