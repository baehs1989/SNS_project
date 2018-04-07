from django import template

register = template.Library()

@register.filter
def next_page(value):
    print ("value: ", value == "")
    if value == '/accounts/signup/' or value=="":
        return "/"
    return value
