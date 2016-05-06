from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SummonerSearchForm, CompareSummonersForm
from .models import Summoner, ChampionData

from cassiopeia import riotapi
from .utilities import setup_cassiopeia, get_related_videos


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        form = SummonerSearchForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            region = form.cleaned_data['region']

            return redirect('summonerMain', summoner_name=summoner_name, region=region)


class SummonerMain(View):
    def get(self, request, region, summoner_name):
        setup_cassiopeia(region=region)
        summoner = riotapi.get_summoner_by_name(summoner_name)
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
            'related_videos_ids': get_related_videos('League of legends ' + champion.name, count=6),
            'region': region,
        }

        return render(request, 'summoner.html', context=context)

    def post(self, request, region, summoner_name):
        form = CompareSummonersForm(request.POST)
        if form.is_valid():
            region = region
            summoner_a_name = summoner_name
            summoner_b_name = form.cleaned_data['summoner_b_name']
        return redirect('compareSummoners', region=region, summoner_a_name=summoner_a_name,
                        summoner_b_name=summoner_b_name)


class CompareSummoners(View):
    def get(self, request, region, summoner_a_name, summoner_b_name):
        setup_cassiopeia(region=region)

        summoner_a = riotapi.get_summoner_by_name(summoner_a_name)
        champion_mastery_a = summoner_a.top_champion_masteries()[0]
        champion_a = champion_mastery_a.champion

        summoner_b = riotapi.get_summoner_by_name(summoner_b_name)
        champion_mastery_b = summoner_b.top_champion_masteries()[0]
        champion_b = champion_mastery_b.champion

        champion_data_a = ChampionData.get_champion_data(summoner_a, champion_a, champion_mastery_a)
        champion_data_b = ChampionData.get_champion_data(summoner_b, champion_b, champion_mastery_b)

        champion_data_a.win_percent = int((champion_data_a.wins / champion_data_a.games) * 100)
        champion_data_b.win_percent = int((champion_data_b.wins / champion_data_b.games) * 100)

        champion_data_a.kda_percent = int(champion_data_a.kda / (champion_data_a.kda + champion_data_b.kda) * 100)
        champion_data_b.kda_percent = 100 - champion_data_a.kda_percent

        context = {
            'summoner_a': summoner_a,
            'summoner_b': summoner_b,
            'champion_a': champion_a,
            'champion_b': champion_b,
            'champion_data_a': champion_data_a,
            'champion_data_b': champion_data_b,
        }
        return render(request, 'compare.html', context=context)
