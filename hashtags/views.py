from django.shortcuts import render
from django.views import View
from hashtags.models import HashTag
# Create your views here.

class HashtagView(View):
	def get(self,request,hashtag,*args,**kwargs):
		hash_tag , created = HashTag.objects.get_or_create(tag = hashtag)
		return render(request,"hashtags/hashtags_view.html",{"tag":hash_tag})
