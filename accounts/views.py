from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView
from django.views import View 
from .models import Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms

# Create your views here.

User = get_user_model()

class UserProfile(DetailView):
    model = User.objects.all()
    template_name = 'accounts/user_detail.html'

    def get_object(self):
        return get_object_or_404(User,username__iexact = self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfile, self).get_context_data(*args, **kwargs)
        following = Profile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recommended'] = Profile.objects.recommended(self.request.user)
        return context




class UserFollow(View):
    def get(self,request,username,*args,**kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = Profile.objects.toggle_follow(request.user, toggle_user)
        return redirect("accounts:user_profile",username=username)          
                    


from django.views.generic.edit import FormView

class SignUp(FormView):
    template_name = 'registration/signup.html'
    form_class = forms.SignUpForm
    success_url = '/login/'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username = username,email= email)
        new_user.set_password(password)  
        new_user.save()
        return super().form_valid(form)