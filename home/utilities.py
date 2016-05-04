import os

from cassiopeia.type.api.exception import APIError
import urllib.request

import urllib.parse
import re


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
    print (search_results)
    return search_results[0:count]
