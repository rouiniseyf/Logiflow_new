from django import template
from django.template.defaultfilters import stringfilter

register = template.Library() 

@register.filter(name='sliceText') 
@stringfilter
def slice_text(text):
    new_text = (text[:20] + '...')  if len(text) > 20 else text
    return new_text


