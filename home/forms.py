from django import forms


class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField(label='Summoner Name', max_length=100)
    region = forms.CharField(max_length=5)


class CompareSummonersForm(forms.Form):
    summoner_b_name = forms.CharField(label='Second Summoner', max_length=100)


class ContactForm(forms.Form):
    messages = {
        'required': "This is a required field"
    }
    contact_summoner_name = forms.CharField()
    contact_region = forms.CharField()
    contact_email = forms.EmailField(error_messages={'required': messages['required']})
    contact_message = forms.CharField(error_messages={'required': messages['required']})
