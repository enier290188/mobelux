from django.views.generic.base import RedirectView


class IndexView(RedirectView):
    pattern_name = 'security.dj:profile:index'
    permanent = False
    query_string = True
