import re

from django import template
from django.template.base import VariableNode

register = template.Library()


@register.tag(name='addmark')
def add_mark(parser, token):
    nodelist = parser.parse(('end_add_mark','endaddmark'))
    parser.delete_first_token()
    return MarkDown(nodelist)


class MarkDown(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        outputs = []
        for node in self.nodelist:
            if not isinstance(node, VariableNode):
                outputs.append(node.render(context))
                continue

            obj = node.filter_expression.resolve(context)
            star_re = re.compile("\*([A-Za-z]+)\*")
            for item in obj.split():
                if star_re.search(item):
                    text = f'<b>{item}</b>'
                    outputs.append(text)
                outputs.append(node.render(context))
        return ''.join(outputs)
