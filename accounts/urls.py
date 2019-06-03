from django.conf.urls import url
from . import views


app_name = 'accounts'

urlpatterns = [

url(r'^(?P<username>[\w.@+-]+)/$',views.UserProfile.as_view(),name = 'user_profile'),
url(r'^follow/(?P<username>[\w.@+-]+)$',views.UserFollow.as_view(),name = 'follow'),

]