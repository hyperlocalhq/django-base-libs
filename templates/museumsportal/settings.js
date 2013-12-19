{% extends "settings_base.js" %}

{% block document_domain %}
//"{{ cookie_domain }}";
{% endblock %}

{% block extra_window_settings %}
window.settings.frontend_languages = { {% for lang in FRONTEND_LANGUAGES %}'{{ lang.0|escapejs }}': '{{ lang.1|escapejs }}'{% if not forloop.last %},{% endif %}{% endfor %} };
{% endblock %}
