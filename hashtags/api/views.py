from rest_framework import generics

from hashtags.models import HashTag

from rest_framework.permissions import IsAuthenticated,AllowAny

from django.db.models import Q

from tweets.api.pagination import StandardResultsPagination

from rest_framework.views import APIView

from rest_framework.response import Response

from tweets.api.serializers import TweetSerializer


class TagSerializer_view(generics.ListAPIView):
	serializer_class = TweetSerializer
	pagination_class = StandardResultsPagination

	def get_seraializer_count(self,*args,**kwargs):
		context = super(TagSerializer_view,self).get_seraializer_count(*args,**kwargs)
		context["request"] = self.request
		return context


	def get_queryset(self,*args,**kwargs):
		hashtag = self.kwargs.get("hashtag")
		hashtag_obj = None

		try:
			hashtag_obj = HashTag.objects.get_or_create(tag = hashtag)[0]
		except:
			pass	

		if hashtag_obj:
			queryset = hashtag_obj.tweet_contains()
			return queryset	

	

		