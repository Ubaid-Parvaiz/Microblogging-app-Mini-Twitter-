from django import forms
from .models import Tweet

class Tweet_Form(forms.ModelForm):
	content = forms.CharField(label='', 
				widget=forms.Textarea(
						attrs={'placeholder': "Your tweet", 
								'class':'form-control',
								"rows":"4"

						   }
))

	class Meta:
		model = Tweet
		fields = ('content',)



	# def clean_content(self, *args, **kwargs):
	# 	content = self.cleaned_data.get("content")
	# 	if "fuck" or 'FUCK' or 'Fuck' in content:
	# 		raise forms.ValidationError("Tweet cannot contain Profanity")
	# 	return content	
	# 	