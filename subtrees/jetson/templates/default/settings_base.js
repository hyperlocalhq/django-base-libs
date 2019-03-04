{% load base_tags cache %}{% cache 600 jssettings LANGUAGE_CODE %}

{% block document_domain %}
domain_bits = document.location.hostname.split('.');
if (!(domain_bits.length === 4 && !isNaN(domain_bits[3]))) {
    document.domain = domain_bits.slice(-2).join('.');
}
{% endblock %}

window.settings = {
    // SOLID
    STATIC_URL: '{{ STATIC_URL }}',
    UPLOADS_URL: '{{ UPLOADS_URL }}',
    FILEBROWSER_ROOT_DIR: '{{ FILEBROWSER_ROOT_DIR }}',

    // NEW
    ROOT_DIR: '/',
    MEDIA_URL: '{{ MEDIA_URL }}',
    MEDIA_HOST: '{{ MEDIA_HOST }}',
    JETSON_MEDIA_URL: '{{ JETSON_MEDIA_URL }}',
    WEBSITE_URL: '{{ WEBSITE_URL }}',
    WEBSITE_SSL_URL: '{{ WEBSITE_SSL_URL }}',
    LANGUAGE_CODE: '{{ LANGUAGE_CODE }}',
    LANGUAGES: JSON.parse('{{ LANGUAGES_JSON }}'),

    // DEPRECATED
    root_dir: '/',
    media_url: '{{ MEDIA_URL }}',
    media_host: '{{ MEDIA_HOST }}',
    jetson_media_url: '{{ JETSON_MEDIA_URL }}',
    css_url: '{{ css_url }}',
    img_url: '{{ img_url }}',
    website_url: '{{ WEBSITE_URL }}',
    lang: '{{ LANGUAGE_CODE }}',
    languages: JSON.parse('{{ LANGUAGES_JSON }}')
};

{% block extra_window_settings %}{% endblock %}

window.website = {
    path: window.location.pathname.replace(
        new RegExp('^/(' + Object.keys(window.settings.LANGUAGES).join('|') + ')/'),
        '/'
    )
};

{% endcache %}
