from django.contrib.contenttypes.models import ContentType
from django import template
from django.template.loader import get_template
from django.utils.html import escape

register = template.Library()

@register.filter
def render_item(item, template_directory="items"):
	content_type = item.content_type.model
	t = get_template('tumblelog/%s/%s.html' % (template_directory, content_type,))
	return t.render(template.Context({'item' : item.content_object, 'itemid' : item.id, 'itemclass' : content_type}))

@register.filter
def format_code(code, lexer_name):
	"""
	Attempts to format the given code using Pygments - if Pygments is not
	available or a lexer with the given name cannot be found, falls back to
	displaying the code in a plain <pre> element.
	
	code
		a snippet of code
	
	lexer_name
		the name of a Pygments lexer, to be used to format the given code
	"""
	try:
		from pygments import highlight
		from pygments.lexers import get_lexer_by_name
		from pygments.formatters import HtmlFormatter
		
		lexer = get_lexer_by_name(lexer_name, stripall=True)
		formatter = HtmlFormatter(style='native', cssclass='source', noclasses=True, nowrap=False)
		return highlight(code, lexer, formatter)
	except (ImportError, ValueError):
		return '<div class="source"><pre>%s</pre></div>' % (escape(code),)

register.filter('format_code', format_code)
register.filter('render_item', render_item)