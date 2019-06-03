from rest_framework import serializers

from tweets.models import Tweet

from django.utils.timesince import timesince

from accounts.api.serializers import UserSerializer



class ParentTweetSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only = True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()
	class Meta:
		model = Tweet
		fields = ('user','content','time','date_display','timesince','id',"likes","did_like")

	def get_did_like(self,obj):
		try:
			request = self.context.get("request")
			user = request.user
			if user.is_authenticated:
				if user in obj.liked.all():
					return True
			return False	
		except:
			pass		

	def get_date_display(self, obj):
		return obj.time.strftime("%b %d, %Y | %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.time) + " ago"	

	def get_likes(self,obj):
		return obj.liked.all().count()	



class TweetSerializer(serializers.ModelSerializer):
	parent_id = serializers.CharField(write_only = True,required= False)
	user = UserSerializer(read_only = True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	parent = ParentTweetSerializer(read_only = True)
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()
	reply = serializers.BooleanField(default= True)
	
	class Meta:
		model = Tweet
		fields = ('user','content','time','date_display','timesince','parent','id',"likes","did_like",'reply',"parent_id")


	def get_did_like(self,obj):
		try:
			request = self.context.get("request")
			user = request.user
			if user.is_authenticated:
				if user in obj.liked.all():
					return True
			return False	
		except:
			pass	


	def get_date_display(self, obj):
		return obj.time.strftime("%b %d, %Y | %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.time) + " ago"	

	def get_likes(self,obj):
		return obj.liked.all().count()


