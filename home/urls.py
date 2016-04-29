from django.conf.urls import url
from .views import Home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  url(r'^$', Home.as_view(), name='home')
              ] + staticfiles_urlpatterns()
