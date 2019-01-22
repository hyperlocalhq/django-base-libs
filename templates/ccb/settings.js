{% extends "settings_base.js" %}

{% block document_domain %}
{% endblock %}

{% block extra_window_settings %}

window.settings['URL_ID_PERSON'] = '{{ URL_ID_PERSON|default:"person" }}';
window.settings['URL_ID_PEOPLE'] = '{{ URL_ID_PEOPLE|default:"people" }}';
window.settings['URL_ID_INSTITUTION'] = '{{ URL_ID_INSTITUTION|default:"institution" }}';
window.settings['URL_ID_INSTITUTIONS'] = '{{ URL_ID_INSTITUTIONS|default:"institutions" }}';
window.settings['URL_ID_EVENT'] = '{{ URL_ID_EVENT|default:"event" }}';
window.settings['URL_ID_EVENTS'] = '{{ URL_ID_EVENTS|default:"events" }}';
window.settings['URL_ID_DOCUMENT'] = '{{ URL_ID_DOCUMENT|default:"document" }}';
window.settings['URL_ID_DOCUMENTS'] = '{{ URL_ID_DOCUMENTS|default:"documents" }}';
window.settings['URL_ID_PERSONGROUP'] = '{{ URL_ID_PERSONGROUP|default:"group" }}';
window.settings['URL_ID_PERSONGROUPS'] = '{{ URL_ID_PERSONGROUPS|default:"groups" }}';
window.settings['URL_ID_PORTFOLIO'] = '{{ URL_ID_PORTFOLIO|default:"portfolio" }}';
window.settings['URL_ID_JOB_OFFER'] = '{{ URL_ID_JOB_OFFER|default:"job" }}';
window.settings['URL_ID_JOB_OFFERS'] = '{{ URL_ID_JOB_OFFERS|default:"jobs" }}';

window.settings['FACEBOOK_APP_ID'] = '{{ FACEBOOK_APP_ID }}';
window.settings['FACEBOOK_APP_REQUIRED_PERMISSIONS'] = '{{ FACEBOOK_APP_REQUIRED_PERMISSIONS }}';

{% endblock %}

