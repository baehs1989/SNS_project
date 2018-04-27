from django.shortcuts import render
from .models import Visitor

# Create your views here.
class CookieRenewerMixin:
    def dispatch(self, *args, **kwargs):
        visitor_counter,created = Visitor.objects.get_or_create(name="total")
        print (visitor_counter)
        print (created)
        cookie = self.request.COOKIES.get("visited")
        if cookie:
            print ("cookie exists")
        else:
            visitor_counter.count_up()
        return super(CookieRenewerMixin, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super(CookieRenewerMixin, self).render_to_response(context, **response_kwargs)
        print ("mixin response")
        max_age = 10 * 60
        response.set_cookie("visited","visited",max_age=max_age)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cookie = self.request.COOKIES.get("visited")
        visitor_counter,created = Visitor.objects.get_or_create(name="total")
        context['visitor_count'] = visitor_counter.visitors
        if cookie:
            context['visited'] = cookie
        return context
