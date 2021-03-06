from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # url(r'^login2/$', views.CustomLogin.as_view(), name='login2'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^register/$', views.register_page, name="register"),
    url(r'^success/$', views.SuccessPage.as_view(), name="success")
]
