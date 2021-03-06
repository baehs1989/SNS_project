from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse

from django.http import Http404
from django.views import generic

#pip install django-braces
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Prefetch
from counter.views import CookieRenewerMixin

from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden

class PostList(CookieRenewerMixin, SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user', 'group')

class UserPosts(CookieRenewerMixin, generic.ListView):
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

class PostDetail(CookieRenewerMixin, SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'posts/post_detail.html'

    # read documents on queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(CookieRenewerMixin, LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    # fields = ('message', 'group')
    select_related = ('user', 'group')
    form_class = forms.PostForm
    model = models.Post

    def get_success_url(self):
        return reverse_lazy('groups:single', kwargs={'slug': self.object.group.slug})

    def get_form_kwargs(self):
        kwargs = super(CreatePost, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # print (self.object.get_absolute_url())
        return super().form_valid(form)


class CreatePost2(CookieRenewerMixin, LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    # fields = ('message', 'group')
    select_related = ('user', 'group')
    form_class = forms.PostForm2
    model = models.Post

    def get_success_url(self):
        return reverse_lazy('groups:single', kwargs={'slug': self.object.group.slug})

    def get_form_kwargs(self):
        kwargs = super(CreatePost2, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self,form):
        group = Group.objects.get(slug=self.kwargs.get('slug'))
        self.object = form.save(commit=False)
        if group.is_user_group_member(self.request.user):
            self.object.user = self.request.user
            self.object.group = group
            self.object.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, 'blabla')
            return HttpResponseRedirect(reverse('groups:single', kwargs={'slug': group.slug}))

        # group = Group.objects.get(slug=self.kwargs.get('slug'))
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user
        # self.object.group = group
        # self.object.save()
        # return super().form_valid(form)





class DeletePost(CookieRenewerMixin, LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    # success_url = reverse_lazy('posts:all')

    def get_success_url(self):
        return reverse_lazy('groups:single', kwargs={'slug': self.object.group.slug})
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
