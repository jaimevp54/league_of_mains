from django.shortcuts import render
from django.views.generic import View
from .models import Summoner, ChampionData

from cassiopeia import riotapi
from .utilities import setup_cassiopeia


# Create your views here.
class Home(View):
    def get(self, request):
        setup_cassiopeia(region="LAN")
        summoner = riotapi.get_summoner_by_name("Kyde")
        champion_mastery = summoner.top_champion_masteries()[0]
        champion = champion_mastery.champion
        if not Summoner.objects.filter(name=summoner.name).exists():
            s = Summoner(name=summoner.name, game_id=summoner.id, profile_icon_id=summoner.profile_icon_id)
            s.save()
        else:
            s = Summoner.objects.filter(name=summoner.name)[0]

        if not ChampionData.objects.filter(summoner=s, name=champion.name).exists():
            champion_data = ChampionData.create(s, champion)
        else:
            champion_data = ChampionData.objects.filter(summoner=s, name=champion.name)[0]
        champion_data.update(summoner, champion, champion_mastery)
        champion_data.save()

        context = {
            'summoner': summoner,
            'champion': champion,
            'champion_data': champion_data,
        }

        return render(request, 'home.html', context=context)
