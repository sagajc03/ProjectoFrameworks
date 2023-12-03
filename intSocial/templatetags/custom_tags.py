# custom_tags.py
from django import template
from intSocial.models import Likes

register = template.Library()

@register.simple_tag(name='user_has_liked', takes_context=True)
def user_has_liked(context, publicacion_id, valor):
    request = context['request']
    if not request.user.is_authenticated:
        return False

    return Likes.objects.filter(usuario=request.user, ref_id=publicacion_id, valor=valor).exists()
