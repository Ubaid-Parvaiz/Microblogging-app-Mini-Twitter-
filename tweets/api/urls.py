from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [

url(r'^$',views.TweetSerializer_view.as_view(),name = 'tweet_list'),
url(r'^create/$',views.TweetCreate_view.as_view(),name = 'tweet_create'),
url(r'^(?P<pk>\w+)/retweet/$',views.RetweetApi.as_view(),name = 'retweet'),
url(r'^(?P<pk>\w+)/like/$',views.LikeApi.as_view(),name = 'like-toggle'),
url(r'^(?P<pk>\w+)/$',views.TweetDetail_view.as_view(),name = 'api-detail')





]