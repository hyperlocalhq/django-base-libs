from django import template

register = template.Library()

@register.filter
def get_selected_date(workshop, selected_date):
    return workshop.get_closest_workshop_time(selected_date)