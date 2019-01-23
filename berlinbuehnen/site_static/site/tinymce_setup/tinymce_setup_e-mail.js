/**
 TinyMCE settings for administration.
 If a checkbox with id "id_is_rte" doesn't exist or is checked, adds rich-text widgets for all textareas but with a class "vPlainTextField".
 */
 
oTinyMCEConfig.content_css = window.settings.STATIC_URL + "site/css/tinymce_email.css";

oTinyMCEConfig.remove_script_host = false;
oTinyMCEConfig.convert_urls = true;
oTinyMCEConfig.relative_urls = false;
oTinyMCEConfig.document_base_url = settings.WEBSITE_URL;

oTinyMCEConfig.template_templates = [];

tinyMCE.init(oTinyMCEConfig);

