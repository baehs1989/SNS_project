from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login

from . import forms
# Create your views here.

from django.template import TemplateDoesNotExist
from django.http import Http404



class SuccessPage(generic.TemplateView):
    template_name = "accounts/success.html"


#lets test with different class name
class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class CustomLogin(auth_views.LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context.get('form')
        return context


from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()
def register_page(request):
    form = forms.RegisterForm(request.POST or None)
    context = {
        'form':form,
    }
    if form.is_valid():
        # print (form.cleaned_data)
        # print (form.cleaned_data.get('username'))
        # print (form.cleaned_data.get('email'))
        # print (form.cleaned_data.get('password'))
        # print (form.cleaned_data.get('password2'))
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username,email,password)
        new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],)
        login(request, new_user)
        return redirect('/accounts/success')
    return render(request,'accounts/register.html', context )
