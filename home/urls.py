from django.conf.urls import url
from .views import Home, SummonerMain
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  url(r'^summoner$', SummonerMain.as_view(), name='summonerMain'),
                  url(r'^$', Home.as_view(), name='home')
              ] + staticfiles_urlpatterns()
# TODO fix warning about this
