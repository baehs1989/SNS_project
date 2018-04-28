from django import template
import re


register = template.Library()

@register.filter
def next_page(value):
    print ("value: ", value == "")
    if value == '/accounts/register/' or value == '/accounts/signup/' or value=="":
        return "/"
    if re.match(r'^/posts/new2/', value):
        return ("/groups/posts/in/{}".format(value.split('/')[-2]))
    return value
