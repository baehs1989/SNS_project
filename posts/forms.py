from django import forms
from posts.models import Post
from groups.models import Group
from django.db.models import Q


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = self.fields['group'].queryset.filter(Q(members__username=user.username) | Q(admin__username=user.username))

    class Meta():
        model = Post
        fields = ('message', 'group')
