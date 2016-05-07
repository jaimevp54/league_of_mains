from django import forms


class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField(label='Summoner Name', max_length=100)
    region = forms.CharField(max_length=5)


class CompareSummonersForm(forms.Form):
    summoner_b_name = forms.CharField(label='Second Summoner', max_length=100)


class ContactForm(forms.Form):
    contact_summoner_name = forms.CharField(required=False)
    contact_region = forms.CharField(required=False)
    contact_email = forms.EmailField()
    contact_message = forms.CharField()
