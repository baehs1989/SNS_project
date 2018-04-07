from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# GROUPS MODELS.PY FILE
# Create your models here.

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through='GroupMember')
    admin = models.ForeignKey(User, related_name="admin", null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    def get_users_counts(self):
        count = self.members.all().count() + 1
        return count

    class Meta:
        ordering = ['-created_at']
        unique_together = ['admin', 'name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')
