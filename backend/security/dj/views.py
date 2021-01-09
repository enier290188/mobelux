from django.views.generic.base import RedirectView


class SecurityView(RedirectView):
    pattern_name = 'index'
    permanent = False
    query_string = True
