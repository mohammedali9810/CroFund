from django import template
from Users.models import *
register = template.Library()

@register.filter
def filter_comment_report(comment_id,user_current):
    return not (Reportno.objects.filter(comment_id=comment_id,user_id=user_current).exists() )
    

