{% extends "settings_base.js" %}
{% load i18n %}

{% block document_domain %}
//"{{ cookie_domain }}";
{% endblock %}

{% block extra_window_settings %}
window.settings.frontend_languages = { {% for lang in FRONTEND_LANGUAGES %}'{{ lang.0|escapejs }}': '{{ lang.1|escapejs }}'{% if not forloop.last %},{% endif %}{% endfor %} };

window.WEEKDAYS = ['{% trans "Sunday" %}', '{% trans "Monday" %}', '{% trans "Tuesday" %}', '{% trans "Wednesday" %}', '{% trans "Thursday" %}', '{% trans "Friday" %}', '{% trans "Saturday" %}'];
window.WEEKDAYS_SHORT = [
    '{% filter slice:":2" %}{% trans "Sunday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Monday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Tuesday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Wednesday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Thursday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Friday" %}{% endfilter %}',
    '{% filter slice:":2" %}{% trans "Saturday" %}{% endfilter %}'
];
window.MONTHS = [
    '{% trans "January" %}', '{% trans "February" %}', '{% trans "March" %}', '{% trans "April" %}',
    '{% trans "May" %}', '{% trans "June" %}', '{% trans "July" %}', '{% trans "August" %}',
    '{% trans "September" %}', '{% trans "October" %}', '{% trans "November" %}', '{% trans "December" %}'
];
window.MONTHS_SHORT = [
    '{% filter slice:":3" %}{% trans "January" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "February" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "March" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "April" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "May" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "June" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "July" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "August" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "September" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "October" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "November" %}{% endfilter %}',
    '{% filter slice:":3" %}{% trans "December" %}{% endfilter %}'
];

{% endblock %}
