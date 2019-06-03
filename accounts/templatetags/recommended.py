from django import template
from django.contrib.auth import get_user_model

from accounts.models import Profile

register = template.Library()


User = get_user_model()

@register.inclusion_tag("accounts/snippets/recommend.html") # Check the template
def recommended(user):
    if isinstance(user, User):
        qs = Profile.objects.recommended(user) # Perform the function
        return {"recommended": qs}
