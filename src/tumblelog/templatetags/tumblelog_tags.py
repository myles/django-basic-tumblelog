"""
Copyright 2009 Myles Braithwaite <me@mylesbraithwaite.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
from django.contrib.contenttypes.models import ContentType
from django import template
from django.conf import settings
from django.template.loader import select_template

from tumblelog.models import Post

register = template.Library()

def render_item(item, template_name=None):
    model_name = item.content_object._meta.verbose_name_raw

    template_list = [template_name,] if template_name else []
    template_list.extend([
        'tumblelog/includes/%(model)s.html' % {'model': model_name },
        'tumblelog/includes/default.html'
    ])

    t = select_template(template_list)

    return t.render(template.Context({
        'object' : item.content_object,
        'object_id' : item.id,
        'content_type' : item.content_type,
        'item': item,
        'MEDIA_URL': settings.MEDIA_URL
    }))

register.filter('render_item', render_item)

class LatestPosts(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name

    def render(self, context):
        posts = Post.objects.published()[:int(self.limit)]
        if posts and (int(self.limit) == 1):
            context[self.var_name] = posts[0]
        else:
            context[self.var_name] = posts
        return ''


@register.tag
def get_latest_posts(parser, token):
    """
    Gets any number of latest posts and stores them in a varable.

    Syntax::

        {% get_latest_posts [limit] as [var_name] %}

    Example usage::

        {% get_latest_posts 10 as latest_post_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestPosts(format_string, var_name)
