from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Tweet
from .forms import Tweet_Form
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class Retweet(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user, tweet)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())

@login_required
def Tweets_List(request):
	queryset = Tweet.objects.all()
	query = request.GET.get('q',None)

	if query is not None:
			queryset = queryset.filter(
				Q(user__username__icontains = query)|
				Q(content__icontains = query)
				)


	
	form = Tweet_Form(request.POST or None)

	if request.method == 'POST':
		form = Tweet_Form(request.POST)
		if form.is_valid():
			form = form.save(commit = False)
			form.user = request.user
			form.save()
	
	return render(request,'tweets/tweets_list.html',{'tweets_list':queryset,'form':form,})




class Tweet_Detail(generic.DetailView,LoginRequiredMixin):
	model = Tweet
	fields = '__all__'
	template_name = 'tweets/tweets_detail.html'


