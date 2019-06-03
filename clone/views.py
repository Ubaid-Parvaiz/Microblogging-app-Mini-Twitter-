from django.shortcuts import render
from django.views import View

from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class Search(View):
	def get(self,request,*args,**kwargs):
		query = request.GET.get('q')
		queryset = None
		if query:
			queryset = User.objects.filter(
				Q(username__icontains = query)			
				)

		context = {"user":queryset}

		return render(request,"search.html",context)			


