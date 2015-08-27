{% load base_tags %}
{% if media_file %}
{
    "file_type": "{{ media_file.file_type }}",
    "token": "{{ media_file.get_token }}",
    "html": "{{ media_file.get_representation|escapejs }}",
    "description": "{% filter escapejs %}
        {% if media_file.title %}
            <h5>{{ media_file.title }}</h5>
        {% endif %}
        {% if media_file.description %}
            {{ media_file.description|decode_entities|striptags|linebreaks }}
        {% endif %}
    {% endfilter %}"
}
{% else %}
false
{% endif %}
