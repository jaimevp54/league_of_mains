from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import get_template

from django.views.generic import View
from .forms import SummonerSearchForm, CompareSummonersForm, ContactForm
from .models import Summoner, ChampionData

from cassiopeia.type.api.exception import APIError
from cassiopeia import riotapi
from .utilities import setup_cassiopeia, get_related_videos


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        search_form = SummonerSearchForm(request.POST)
        compare_form = CompareSummonersForm(request.POST)

        if search_form.is_valid() and "searchBtn" in search_form.data:
            summoner_name = search_form.cleaned_data['summoner_name']
            region = search_form.cleaned_data['region']
            return redirect('summonerMain', summoner_name=summoner_name, region=region)

        if compare_form.is_valid() and "compareBtn" in compare_form.data:
            summoner_a_name = compare_form.cleaned_data['summoner_a_name']
            summoner_b_name = compare_form.cleaned_data['summoner_b_name']
            region = compare_form.cleaned_data['region']
            return redirect('compareSummoners', region=region, summoner_a_name=summoner_a_name,
                            summoner_b_name=summoner_b_name)

        return handle_contact_form(request)


class SummonerMain(View):
    def get(self, request, region, summoner_name):
        setup_cassiopeia(region=region)
        try:
            summoner = riotapi.get_summoner_by_name(summoner_name)
        except APIError as e:
            if e.error_code in [404]:
                from_url = request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else ""
                context = {
                    'summoner_name': summoner_name,
                    'region': region,
                    '404_summoner_not_found': True,
                    'from_url': from_url,
                }
                return render(request, 'notification.html', context=context)
            raise e

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
            'champion_data_averages': champion_data.averages,
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
        return handle_contact_form(request)


class CompareSummoners(View):
    def get(self, request, region, summoner_a_name, summoner_b_name):
        setup_cassiopeia(region=region)
        try:
            summoner_a = riotapi.get_summoner_by_name(summoner_a_name)
            summoner_b = riotapi.get_summoner_by_name(summoner_b_name)
        except APIError as e:
            if e.error_code in [404]:
                summoner_name = summoner_a_name if ("by-name/" + summoner_a_name) in e.message else summoner_b_name
                from_url = request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else ""
                context = {
                    'summoner_name': summoner_name,
                    'region': region,
                    '404_summoner_not_found': True,
                    'from_url': from_url,
                }
                return render(request, 'notification.html', context=context)
        champion_mastery_a = summoner_a.top_champion_masteries()[0]
        champion_mastery_b = summoner_b.top_champion_masteries()[0]

        champion_a = champion_mastery_a.champion
        champion_b = champion_mastery_b.champion

        champion_data_a = ChampionData.get_champion_data(summoner_a, champion_a, champion_mastery_a)
        champion_data_b = ChampionData.get_champion_data(summoner_b, champion_b, champion_mastery_b)

        if not champion_data_a.games or not champion_data_b.games:
            from_url = request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else ""
            context = {
                'cant_compare_summoners': True,
                'from_url': from_url,
            }
            return render(request, 'notification.html', context=context)

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
            'champion_data_a_averages': champion_data_a.averages,
            'champion_data_b': champion_data_b,
            'champion_data_b_averages': champion_data_b.averages,
            'region': region,
        }
        return render(request, 'compare.html', context=context)

    def post(self, request):
        return handle_contact_form()


def error404(request):
    return render(request, 'notification.html')


def handle_contact_form(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        summoner_name = form.cleaned_data['contact_summoner_name']
        region = form.cleaned_data['contact_region']
        email = form.cleaned_data['contact_email']
        subject = "Contact Form - " + (summoner_name if summoner_name else email)
        message = form.cleaned_data['contact_message']
        context = {
            'summoner_name': summoner_name,
            'region': region,
            'email': email,
            'message': message
        }

        message = get_template('contact.email.html').render(context=context)
        recipient_list = ['leagueofmains.contact@gmail.com']
        msg = EmailMessage(subject, message, to=recipient_list)
        msg.content_subtype = 'html'
        msg.send()
        context = {
            'contact_us_success': True,
            'from_url': request.META['HTTP_REFERER'],
        }
        return render(request, 'notification.html', context=context)
        # return render(request, "error", {'form': form})
