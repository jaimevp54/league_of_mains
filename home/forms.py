from django import forms


class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField(label='Summoner Name', max_length=100)
    region = forms.CharField(max_length=5)


class CompareSummonersForm(forms.Form):
    summoner_b_name = forms.CharField(label='Second Summoner', max_length=100)
