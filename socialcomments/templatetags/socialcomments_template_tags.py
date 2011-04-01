from django import template

register = template.Library()

@register.filter
def can_comment(context, request):
    return context.can_comment(request)
