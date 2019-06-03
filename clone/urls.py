"""clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home'),
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home'),
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls')),
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings 
from tweets import views
from hashtags.views import HashtagView
from .views import Search 
from tweets.api.views import SearchSerializer_view
from hashtags.api.views import TagSerializer_view
from django.contrib.auth import views as auth_views
from accounts.views import SignUp


urlpatterns = [
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
	url(r'^signup/$',SignUp.as_view(),name = 'signup'),
	url(r'^login/$',auth_views.login,name = 'login'),
	url(r'^logout/$',auth_views.logout,{'next_page': '/login/'},name = 'logout'),
	url(r'^admin/', admin.site.urls),
	url(r'^$',views.Tweets_List,name = 'tweet_list'),
	url(r'^tweet/',include('tweets.urls'),name = 'tweets'),
	url(r'^search/$',Search.as_view(),name = 'search'),
	url(r'^api/tweet/',include('tweets.api.urls'),name = 'tweets-api'),
	url(r'^api/',include('accounts.api.urls'),name = ''),
	url(r'^tags/(?P<hashtag>.*)/$',HashtagView.as_view(),name = 'tag'),
	url(r'^',include('accounts.urls'),name = 'profile'),
	url(r'^api/search/$',SearchSerializer_view.as_view(),name = 'search'),
	url(r'^api/tags/(?P<hashtag>.*)/$',TagSerializer_view.as_view(),name = 'tags'),



]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += staticfiles_urlpatterns() 
	import debug_toolbar
	urlpatterns = [
		url('__debug__/', include(debug_toolbar.urls)),

	] + urlpatterns