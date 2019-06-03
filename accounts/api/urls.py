from django.conf.urls import url
from tweets.api import views


urlpatterns = [

url(r'^(?P<username>[\w.@+-]+)/tweet/$',views.TweetSerializer_view.as_view(),name = 'tweet_list'),


]