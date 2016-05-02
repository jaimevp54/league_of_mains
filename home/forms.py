from django import forms


class SummonerSearch(forms.Form):
    summoner_name = forms.CharField(label='Summoner Name', max_length=100)
    region = forms.CharField(max_length=5)
