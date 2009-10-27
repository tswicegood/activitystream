from django import template
from django.template.loader import render_to_string

register = template.Library()

class ActivityStreamItemNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = template.Variable(item_to_be_rendered)

    def render(self, context):
        item = self.item_to_be_rendered.resolve(context)
        try:
            t = template.loader.get_template("activitystream/fragments/%s_item.html" % item.type.name)
        except template.TemplateDoesNotExist:
            t = template.loader.get_template("activitystream/fragments/default_item.html")
        return t.render(template.Context({"item": item,}))

@register.tag('display_activity')
def do_display_activity(parser, token):
    _tag_name, item_name = token.split_contents()
    return ActivityStreamItemNode(item_name)
