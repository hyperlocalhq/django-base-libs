/**
 TinyMCE settings for administration.
 */
oTinyMCEConfig.content_css = window.settings.STATIC_URL+"site/css/tinymce.css";

oTinyMCEConfig.extended_valid_elements = "iframe[align<bottom?left?middle?right?top|class|frameborder|height|id"
    +"|longdesc|marginheight|marginwidth|name|scrolling<auto?no?yes|src|style"
    +"|title|width|webkitAllowFullScreen|allowFullScreen],";
  + "object[align<bottom?left?middle?right?top|archive|border|class|classid"
    +"|codebase|codetype|data|declare|dir<ltr?rtl|height|hspace|id|lang|name"
    +"|onmouseout|onmouseover|onmouseup|standby|style|tabindex|title|type|usemap"
    +"|vspace|width],"
  +"param[id|name|type|value|valuetype<DATA?OBJECT?REF]";

oTinyMCEConfig.style_formats = [
    {title: '[all] clearfix', selector: "*", classes: 'clearfix'},
    {title: 'Paragraph styles'},
    {title: '[p] Image sidebar', selector: 'p', classes: 'img_left'},
    {title: '[p] Image main', selector: 'p', classes: 'img_block'},
    {title: 'Image styles'},
    {title: '[img] Image left-aligned', selector: 'img', classes: 'img_left'},
    {title: '[img] Image left-aligned (no top space)', selector: 'img', classes: 'img_left_nospacetop'},
    {title: '[img] Image right-aligned', selector: 'img', classes : 'img_right'},
    {title: '[img] Image right-aligned (no top space)', selector: 'img', classes: 'img_right_nospacetop'},
    {title: '[img] Image Block', selector: 'img', classes: 'img_block'}
];

tinyMCE.init(oTinyMCEConfig);
