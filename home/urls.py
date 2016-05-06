from django.conf.urls import url
from .views import Home, SummonerMain, CompareSummoners, Notification
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  url(r'^$', Home.as_view(), name='home'),
                  url(r'^(?i)summoner/(?P<region>[a-z]{2,4})/(?P<summoner_name>[\w ]*)$', SummonerMain.as_view(),
                      name='summonerMain'),
                  url(r'^(?i)compare/(?P<region>[a-z]{2,4})/(?P<summoner_a_name>[\w ]*)-(?P<summoner_b_name>[\w ]*)$',
                      CompareSummoners.as_view(), name='compareSummoners'),
                  url(r'^notification/$', Notification.as_view(), name='notification'),
              ] + staticfiles_urlpatterns()
# TODO fix warning about this
