from django import template

register = template.Library()

@register.filter
def is_open(exhibition, selected):

    if 'selected_date' in selected:
        return exhibition.is_open(selected['selected_date'])
        
    if 'calendar' in selected:
        if selected['calendar'] == 'today':
            return exhibition.is_today()
        if selected['calendar'] == 'tomorrow':
            return exhibition.is_tomorrow()
            
    return True
    
@register.filter
def are_open(object_list, selected):

    if 'selected_date' in selected:
        new_list = []
        for exhibition in object_list:
            if exhibition.is_open(selected['selected_date']):
                new_list.append(exhibition)
        return new_list
        
    if 'calendar' in selected:
        new_list = []
        for exhibition in object_list:
            if selected['calendar'][0] == 'today' and exhibition.is_today():
                new_list.append(exhibition)
            if selected['calendar'][0] == 'tomorrow' and exhibition.is_tomorrow():
                new_list.append(exhibition)
        return new_list
        
    return object_list