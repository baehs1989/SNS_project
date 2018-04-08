from django import forms
from . import models


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'description',)

# class GroupCreateForm(forms.Form):
#     name = forms.CharField()
#     description = forms.CharField()
#
#     def clean_name(self):
#         name = self.cleaned_data.get('name').lower()
#         qs = models.Group.objects.filter(name=name)
#         if qs.exists():
#             raise forms.ValidationError("Username is already taken")
#         return name
#
#     def clear(self):
#         data = self.cleaned_data
#
#         return data
