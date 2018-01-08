{% extends "settings_base.js" %}

{% block document_domain %}
{% endblock %}

{% block extra_window_settings %}
window.settings['URL_ID_JOB_OFFER'] = "{{ URL_ID_JOB_OFFER|default:"job" }}";
window.settings['URL_ID_JOB_OFFERS'] = "{{ URL_ID_JOB_OFFERS|default:"jobs" }}";

window.settings['FACEBOOK_APP_ID'] = "{{ FACEBOOK_APP_ID }}";
window.settings['FACEBOOK_APP_REQUIRED_PERMISSIONS'] = "{{ FACEBOOK_APP_REQUIRED_PERMISSIONS }}";

{% endblock %}

