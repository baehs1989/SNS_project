from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.http import Http404
from django.views import generic

#pip install django-braces
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Prefetch

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user', 'group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    # context_object_name = 'schools'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
            # self.post_user = User.objects.prefetch_related(Prefetch('posts')).get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            print (self.post_user.posts.all().first())
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'posts/post_detail.html'

    # read documents on queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    # fields = ('message', 'group')
    select_related = ('user', 'group')
    form_class = forms.PostForm
    model = models.Post

    def get_form_kwargs(self):
        kwargs = super(CreatePost, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user_id = self.request.user.id)

    def get(self, request, *args, **kwargs):
        object_instance = self.get_object()  # Get the object
        object_user = self.request.user  # Get the user who owns the object

        if object_instance.user != object_user:  # See if the object_user is the same as the user
            return HttpResponseForbidden('Permission Error')
        else:
            return super().get(request,*args,**kwargs)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
