from django.conf.urls import url
from .views import Home, SummonerMain, CompareSummoners
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  url(r'^$', Home.as_view(), name='home'),
                  url(r'^summoner$', SummonerMain.as_view(), name='summonerMain'),
                  url(r'^compare/([a-z]{3,4})/(\w*)-(\w*)$', CompareSummoners.as_view(), name='compareSummoners'),
              ] + staticfiles_urlpatterns()
# TODO fix warning about this
