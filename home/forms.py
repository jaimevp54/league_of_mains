from django import forms


class SummonerSearch(forms.Form):
    summoner_name = forms.CharField(label='Summoner Name', max_length=100)
    region = forms.CharField(max_length=5)


class CompareSummoners(forms.Form):
    summoner_a_name = forms.CharField(label='First Summoner', max_length=100)
    summoner_b_name = forms.CharField(label='Second Summoner', max_length=100)
