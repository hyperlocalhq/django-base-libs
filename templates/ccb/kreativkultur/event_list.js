(function() {
{% autoescape off %}
    var rendered_event_list = '{{ rendered_event_list|escapejs }}';
{% endautoescape %}
    if (window.event_list_loaded) {
        window.event_list_loaded(rendered_event_list);
    }
})();