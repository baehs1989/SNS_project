from django import forms
from . import models


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'description',)
