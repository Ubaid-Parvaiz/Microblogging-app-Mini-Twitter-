from django.conf.urls import url
from . import views

app_name = 'tweets'

urlpatterns = [

url(r'^(?P<pk>\w+)/$',views.Tweet_Detail.as_view(),name = 'detail'),
url(r'^(?P<pk>\w+)/retweet/$',views.Retweet.as_view(),name = 'retweet')


]