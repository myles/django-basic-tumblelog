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

from django.contrib.contenttypes.models import ContentType
from django import template
from django.template.loader import get_template, TemplateDoesNotExist

register = template.Library()

def render_item(item, template=None):
	app_label = item._meta.app_label
	model_name = item._meta.verbose_name_raw
	
	try:
		if tempalte:
			t = get_template(template)
		else:
			t = get_template('%(app)s/tumblelog/%(model)s.html' % {
				'app': app_label,
				'model': model_name,
			})
	except TemplateDoesNotExist:
		t = get_template('tumblelog/default.html')
	
	return t.render(template.Context({
		'item' : item.content_object,
		'itemid' : item.id,
		'itemclass' : content_type
	}))

register.filter('render_item', render_item)