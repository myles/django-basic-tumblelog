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