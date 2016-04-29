import os
from cassiopeia.type.api.exception import APIError


def process_data(summoner, champion, champion_mastery):
    data = dict()
    match_list = summoner.match_list(champions=champion)
    data['summoner_name'] = summoner.name
    data['champion_name'] = champion.name
    data['mastery_level'] = champion_mastery.level
    data['mastery_points'] = champion_mastery.points
    data['highest_grade'] = champion_mastery.highest_grade
    data['games'] = len(match_list)
    data['wins'] = 0
    data['kills'] = 0
    data['deaths'] = 0
    data['assists'] = 0
    data['cs_count'] = 0
    data['penta_kills'] = 0
    data['quadra_kills'] = 0
    data['triple_kills'] = 0
    data['double_kills'] = 0
    data['time_played'] = 0
    data['largest_killing-spree'] = 0
    data['largest_cs'] = 0

    for match_reference in match_list:
        try:
            match = match_reference.match(include_timeline=False)
        except APIError as e:
            continue
        for p in match.participants:
            if p.summoner_name == summoner.name:
                participant = p
                break

        data['wins'] += 1 if participant.stats.win else 0
        data['kills'] += participant.stats.kills
        data['deaths'] += participant.stats.deaths
        data['assists'] += participant.stats.assists
        data['cs_count'] += participant.stats.cs
        data['first_blood_count'] += 1 if participant.stats.first_blood else 0
        data['turret_kills'] += participant.stats.turret_kills
        data['penta_kills'] += participant.stats.penta_kills
        data['quadra_kills'] += participant.stats.quadra_kills
        data['triple_kills'] += participant.stats.triple_kills
        data['double_kills'] += participant.stats.double_kills
        # data['time_played'] += match.duration
        data['largest_killing-spree'] = max(data['largest_killing-spree'], participant.stats.largest_killing_spree)
        data['largest_cs'] = max(data['largest_cs'], participant.stats.cs)

    data['losses'] = len(match_list) - data['wins']
    data['kda'] = round(((data['kills'] + data['assists']) / (data['deaths'] if data['deaths'] else 1)), 3)

    return data


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
