from django.views.generic import TemplateView
from counter.views import CookieRenewerMixin

class HomePage(CookieRenewerMixin,TemplateView):
    template_name = 'index.html'

    # def render_to_response(self, context, **response_kwargs):
    #     response = super(HomePage, self).render_to_response(context, **response_kwargs)
    #     print ("response")
    #     response.set_cookie("visited","visited",max_age=30)
    #     return response
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cookie = self.request.COOKIES.get("visited")
    #     if cookie:
    #         context['visited'] = cookie
    #     return context
