from django.db import models

from django.conf import settings

from django.urls import reverse_lazy

from django.db.models.signals import post_save

from django.contrib.auth.models import User


# Create your models here.

class ProfileManager(models.Manager):
	def all(self):
		qs = self.get_queryset().all()
		if self.instance:
			qs = qs.exclude(user = self.instance)
		else:
			pass
		return qs

	def toggle_follow(self, user, to_toggle_user):
		user_profile, created = Profile.objects.get_or_create(user=user) # (user_obj, true)
		if to_toggle_user in user_profile.following.all():
			user_profile.following.remove(to_toggle_user)
			added = False
		else:
			user_profile.following.add(to_toggle_user)
			added = True
		return added

	def is_following(self, user, followed_by_user):
		user_profile, created = Profile.objects.get_or_create(user=user)
		if created:
			return False
		if followed_by_user in user_profile.following.all():
			return True
		return False

	def recommended(self,user,limit_to = 10):
		profile = user.profile
		following = profile.get_follower()	
		queryset = self.get_queryset().exclude(user = following).exclude(id = profile.id)[:limit_to]
		return queryset
	
			

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name = "profile")

	following = models.ManyToManyField(settings.AUTH_USER_MODEL,blank = True,related_name = "followed_by") 

	# user.profile.following - users I follow 

	#  This actually calls profile which means the user itself and then grab the following field of user itself
	#  which in return gives us the following

	# user.followed_by - users that follow me

	#  This happens as user is connected with followed_by and then it simply will get the followed by people
	#  which means the users which are following me 

	objects = ProfileManager()

	def get_follower(self):
		users = self.following.all()
		return users.exclude(username = self.user.username)

	def __str__(self):
		return self.user.username

	def get_follow_url(self):
		return reverse_lazy("accounts:follow", kwargs={"username":self.user.username})	

	def get_absolute_url(self):
		return reverse_lazy("accounts:detail", kwargs={"username":self.user.username})


	
	


def post_save_user(sender,instance,created,*args,**kwargs):
	if created:
		user = Profile.objects.get_or_create(user = instance)


		

post_save.connect(post_save_user,sender = settings.AUTH_USER_MODEL)




class User(User):
	passsword2 = models.CharField(max_length = 201)

	
