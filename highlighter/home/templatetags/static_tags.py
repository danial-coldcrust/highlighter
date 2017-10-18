import time
from django import template
from django.conf import settings
from django.templatetags.static import StaticNode

register = template.Library()

class VersioningStaticNode(StaticNode):
    def url(self, context):
        url = super().url(context)
        if settings.DEBUG:
            t = str(int(time.time()))
            if '?' not in url:
                url += '?_=' + t
            else:
                url += '&_=' + t
        return url

@register.tag('static_t')
def static_t(parser, token):
    return VersioningStaticNode.handle_token(parser, token)