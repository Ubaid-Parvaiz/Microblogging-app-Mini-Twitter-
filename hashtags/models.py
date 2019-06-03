from django.db import models
# Create your models here.
from tweets.models import Tweet

from .signals import parsed_hashtags

class HashTag(models.Model):
	tag = models.CharField(max_length = 120)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.tag


	def tweet_contains(self):
		return Tweet.objects.filter(content__icontains = "#" + self.tag)	


def parsed_hastags_receiver(sender,hashtags_list, *args,**kwargs):
	if len(hashtags_list) > 0:
		for tag in hashtags_list:
			obj, created = HashTag.objects.get_or_create(tag = tag)

parsed_hashtags.connect(parsed_hastags_receiver)	


