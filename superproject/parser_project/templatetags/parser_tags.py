from django import template

from parser_project.models import Resources

register = template.Library()


@register.inclusion_tag("parser_project/list_resources.html")
def show_resources():
    resources = Resources.objects.exclude(title = "Другие ресурсы")
    return {"resources": resources}
