from rest_framework import serializers

from django.contrib.auth.models import User

from django.urls import reverse_lazy

class UserSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = [
		'username',
		'url'
		]

	def get_url(self,obj):
		return reverse_lazy("accounts:user_profile",kwargs = {"username":obj.username})
