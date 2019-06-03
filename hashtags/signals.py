from django.dispatch import Signal

parsed_hashtags = Signal(providing_args = ["hashtags_list"])


#  I just made a signal which needs to have hastags in order to function.