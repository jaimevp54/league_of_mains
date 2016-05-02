from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SummonerSearch
from .models import Summoner, ChampionData

from cassiopeia import riotapi
from .utilities import setup_cassiopeia


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class SummonerMain(View):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        print(request.POST)
        form = SummonerSearch(request.POST)
        if form.is_valid():
            setup_cassiopeia(region=form.cleaned_data['region'])
            summoner = riotapi.get_summoner_by_name(form.cleaned_data['summoner_name'])
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

            return render(request, 'summoner.html', context=context)
