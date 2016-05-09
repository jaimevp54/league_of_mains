from cassiopeia import riotapi
from cassiopeia.core import leagueapi
from cassiopeia.type.api.exception import APIError

from .models import Summoner, ChampionData

import os
import re
import urllib.parse
import urllib.request


def setup_cassiopeia(region="NA", print_calls=True, key="development"):
    from cassiopeia import riotapi
    riotapi.set_region(region)
    riotapi.print_calls(print_calls)
    key = key.lower()
    riotapi.set_load_policy('lazy')
    if key in ("d", "dev", "development"):
        key = os.environ['DEV_KEY']
    elif key in ("p", "prod", "production"):
        key = os.environ["PROD_KEY"]
        riotapi.set_rate_limits((3000, 10), (180000, 600))
    riotapi.set_api_key(key)
    riotapi.set_locale(locale="en_US")


def get_related_videos(query, count):
    # return ids of videos from last week
    query_string = urllib.parse.urlencode({"search_query": query})
    html_content = urllib.request.urlopen("https://www.youtube.com/results?sp=EgIIAw%253D%253D&" + query_string)

    search_results = re.findall(r'<a href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results[0:count]


def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """

    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
            # Try Again Once
            if error.error_code in [500]:
                try:
                    print("Got a 500, trying again...")
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 400, 404]:
                        pass
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                print("Got a 400 or 404")
                pass

            # Fatal
            else:
                raise error

    return call_wrapper
