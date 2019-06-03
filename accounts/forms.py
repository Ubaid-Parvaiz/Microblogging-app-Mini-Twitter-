from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class SignUpForm(forms.ModelForm):
	password = forms.CharField(max_length=30,widget = forms.PasswordInput)
	password2 = forms.CharField(max_length=30,label = "Confirm Password",widget = forms.PasswordInput)


	class Meta:
		model  = User
		fields = ('username', 'email', 'password', 'password2', )



	def clean_username(self):
		username =  self.cleaned_data.get("username")
		if User.objects.filter(username__icontains = username):
			raise forms.ValidationError("Username is already taken!")
		return username	

	
	def clean_email(self):
		email =  self.cleaned_data.get("email")
		if User.objects.filter(email__icontains = email):
			raise forms.ValidationError("Email is already taken!")
		return email


	
	def clean_password(self):
		password =  self.cleaned_data.get("password")
		password2 =  self.cleaned_data.get("password")
		print(password  + "Password")
		print(password2 + "Password2")
		if password != password2:
			raise forms.ValidationError("Password should be same!")
		return password


	




