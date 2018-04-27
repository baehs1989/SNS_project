from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from groups.models import Group,GroupMember

from django.contrib.auth import get_user_model
User = get_user_model()

from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy

from . import forms

from counter.views import CookieRenewerMixin


class CreateGroup(CookieRenewerMixin, LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    # form_class = forms.GroupCreateForm
    model = Group

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.admin = self.request.user
        self.object.save()
        GroupMember.objects.create(user=self.request.user, group=self.object)
        return super().form_valid(form)

class SingleGroup(CookieRenewerMixin, generic.DetailView):
    model = Group
    template_name = "groups/group_single.html"

class ListGroups(CookieRenewerMixin, generic.ListView):
    model = Group
    # context_object_name = 'group_list'


class JoinGroup(CookieRenewerMixin, LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})


    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request, 'Your are now a member!')
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')
        return super().get(request,*args,**kwargs)

from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden

class DeleteGroup(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Group
    select_related = ('admin',)
    success_url = reverse_lazy('groups:all')

    # def delete(self,*args,**kwargs):
    #     messages.success(self.request,'Group Deleted')
    #     return super().delete(*args,**kwargs)

    def get(self, request, *args, **kwargs):
        object_instance = self.get_object()  # Get the object
        object_user = self.request.user  # Get the user who owns the object

        if object_instance.admin != object_user:  # See if the object_user is the same as the user
            return HttpResponseForbidden('Permission Error')
        else:
            return super().get(request,*args,**kwargs)


    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       if self.object.admin == request.user:
          self.object.delete()
          return HttpResponseRedirect(self.get_success_url())
       else:
          return HttpResponseRedirect(reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')}))

from itertools import chain

class GroupDetail(LoginRequiredMixin,generic.DetailView):
    model = Group

    def get_context_data(self,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['admin'] = self.object.admin
        context['group_users'] = self.object.members.all()
        return context


from groups.forms import GroupUpdateForm
class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model=Group
    fields = ( 'name','description',)
    from_class = GroupUpdateForm
    template_name = "groups/group_update_form.html"

# import . from forms
# class EnterMobileView(ParticipantLoginRequiredMixin, UpdateView):
#     model=Group
#     form_class = forms.G
#     template_name = 'participants/enter_mobile.html'
#     success_url = reverse_lazy('participants:validate_mobile')

    #
    # def get_object(self, queryset=None):
    #     return get_object_or_404(self.model, pk=self.request.user.participant_set.get().pk)
    #
    # def get_form(self, form_class):
    #     return form_class(instance=self.get_object(), data=self.request.POST or None)
    #
    #
    # def get(self, request, *args, **kwargs):
    #     participant=self.get_object()
    #
    #     if participant.mobile_verified is not None or participant.nb_times_phone_checked>3:
    #         return redirect('participants:home')
    #
    #     participant.nb_times_phone_checked+=1
    #     participant.save()
    #     return render(request, self.template_name, {'form': self.get_form(self.form_class)}
