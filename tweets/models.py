from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from hashtags.signals import parsed_hashtags

import re
# Create your models here.


class TweetManager(models.Manager):
	def retweet(self,user,parent_obj):

		if parent_obj.parent:
			obj_parent = parent_obj.parent
			# print(obj.parent  ,"This is a parent" ,Object.parent.id)
		else:
			obj_parent = parent_obj
			# print(obj.parent ,"This is  a parent",)			

		qs = self.get_queryset().filter(user = user, parent = obj_parent)
		if qs.exists():
			return None

		obj = self.model(
			user = user,
			parent = obj_parent,
			content = parent_obj.content

			)

		obj.save()

		return obj		

	def like_toggle(self,user,tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.liked.remove(user)
		else:
			is_liked = True
			tweet_obj.liked.add(user)
		return is_liked	
				
		
				


class Tweet(models.Model):
	parent = models.ForeignKey("self",blank = True,null = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.TextField(max_length = 130)
	reply = models.BooleanField(verbose_name = "Is a Reply ?" , default = False)
	liked = models.ManyToManyField(settings.AUTH_USER_MODEL,blank = True,related_name = "liked")
	time = models.DateTimeField(auto_now_add = True)
	objects = TweetManager()

	def __str__(self):
		return self.content

	class Meta:
		ordering = ['content']	

# Getting the parent
    
	def get_parent(self):
		the_parent = self
		if self.parent:
			parent = self.parent
		return the_parent

#  Getting the children  and the getting the parent too
	def get_children(self):
		parent = self.get_parent()
		qs = Tweet.objects.filter(parent = parent)	
		qs_parent = Tweet.objects.filter(pk = parent.pk)	
		return (qs | qs_parent)




def tweet_save_receiver(sender,instance,created,*args,**kwargs):
	if created and not instance.parent:

		user_regex = r'@(?P<username>[\w.@+-]+)'

		username = re.findall(user_regex,instance.content)

		hashtag_regex = r'#(?P<username>[\w\d-]+)'

		hashtags = re.findall(hashtag_regex,instance.content)

		print(instance.__class__)

		parsed_hashtags.send(hashtags_list = hashtags,sender = instance.__class__)

		




post_save.connect(tweet_save_receiver,sender = Tweet)



