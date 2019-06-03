from rest_framework import generics

from tweets.models import Tweet

from rest_framework.permissions import IsAuthenticated,AllowAny

from .serializers import TweetSerializer

from django.db.models import Q

from .pagination import StandardResultsPagination

from rest_framework.views import APIView

from rest_framework.response import Response

from .serializers import TweetSerializer


class LikeApi(APIView):
	permission_classes = [IsAuthenticated]


	def get(self,request,pk,format= None):
		tweet = Tweet.objects.filter(pk = pk)
		if request.user.is_authenticated:
				is_liked = Tweet.objects.like_toggle(request.user, tweet.first())
				return Response({"liked":is_liked})
			
		return Response({"message":message},status = 400)




class RetweetApi(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		print(tweet_qs)
		message = "Not allowed"

		if tweet_qs.exists() and tweet_qs.count() == 1:
			print(tweet_qs)
			new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())

			new_tweet

			if new_tweet:
				data = TweetSerializer(new_tweet).data
				return Response(data)
				print(data)

			# message = "Cannot retweet the same in 1 day"

		return Response({"message": message}, status=400)


#  Follower Tweets, Tweets 
class TweetSerializer_view(generics.ListAPIView):
	serializer_class = TweetSerializer
	pagination_class = StandardResultsPagination

	def get_seraializer_count(self,*args,**kwargs):
		context = super(TweetSerializer_view,self).get_seraializer_count(*args,**kwargs)
		context["request"] = self.request
		return context




	def get_queryset(self,*args,**kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			queryset = Tweet.objects.filter(user__username = requested_user).order_by("-time")

		else:	
			following = self.request.user.profile.get_follower()
			qs1 = Tweet.objects.filter(user__in = following)
			qs2 = Tweet.objects.filter(user = self.request.user)
			queryset = (qs1 | qs2).distinct().order_by("-time")

		query = self.request.GET.get('q',None)

		if query is not None:
			queryset = queryset.filter(
				Q(user__username__icontains = query)|
				Q(content__icontains = query)
				)

		return queryset	
		

class TweetCreate_view(generics.ListCreateAPIView):
	queryset = Tweet.objects.all()
	serializer_class = TweetSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user = self.request.user)
		


class TweetDetail_view(generics.ListAPIView):
	queryset = Tweet.objects.all()
	serializer_class = TweetSerializer
	pagination_class = StandardResultsPagination
	permission_classes = [AllowAny]

	def get_queryset(self,*args,**kwargs):
		tweet_id = self.kwargs.get("pk")
		qs = Tweet.objects.filter(pk = tweet_id )
		if qs.exists() and qs.count() == 1:
			parent_obj = qs.first()
			qs1 = parent_obj.get_children()
			qs = (qs | qs1).distinct().extra(select = {"parent_id_null":"parent_id IS NULL"})
		return qs.order_by("-parent_id_null","-time")		




class SearchSerializer_view(generics.ListAPIView):
	serializer_class = TweetSerializer
	pagination_class = StandardResultsPagination



	def get_queryset(self,*args,**kwargs):

		if query is not None:
			queryset = queryset.filter(
				Q(user__username__icontains = query)|
				Q(content__icontains = query)
				)

		return queryset	