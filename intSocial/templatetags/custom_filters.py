from django import template
from intSocial.models import Likes

register = template.Library()

@register.filter(name='user_has_liked')
def user_has_liked(request, publicacion, valor):
    # request = template.context.get('request')
    if not request.user.is_authenticated:
        return False

    return Likes.objects.filter(usuario=request.user, ref=publicacion, valor=valor).exists()
