# GROUPS URLS.PY
from django.conf.urls import url
from . import views

app_name = 'groups'

urlpatterns = [
    url(r'^$', views.ListGroups.as_view(), name='all'),
    url(r'^new/$', views.CreateGroup.as_view(), name='create'),
    url(r'posts/in/(?P<slug>[-\w]+)/$', views.SingleGroup.as_view(), name='single'),
    url(r'join/(?P<slug>[-\w]+)/$', views.JoinGroup.as_view(), name='join'),
    url(r'leave/(?P<slug>[-\w]+)/$', views.LeaveGroup.as_view(), name='leave'),
    url(r'delete/(?P<slug>[-\w]+)/$', views.DeleteGroup.as_view(), name='delete'),
    url(r'detail/(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='detail'),
    url(r'update/(?P<slug>[-\w]+)/$', views.GroupUpdateView.as_view(), name='update'),
]
