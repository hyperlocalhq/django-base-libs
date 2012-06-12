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
  
oTinyMCEConfig.template_templates = [
    {
        title: "2 Columns ( 164px / 338px )",
        src:  window.settings.STATIC_URL+"site/tiny_mce-templates/2_columns_2-4.html",
        description: "Golden ratio"
    },
    {
        title: "2 Columns ( 338px / 164px )",
        src:  window.settings.STATIC_URL+"site/tiny_mce-templates/2_columns_4-2.html",
        description: "Golden ratio"
    },
    {
        title: "2 Columns ( 251px / 251px )",
        src:  window.settings.STATIC_URL+"site/tiny_mce-templates/2_columns.html",
        description: "50 / 50"
    },
    {
        title: "3 Columns ( 164px / 164px / 164px )",
        src:  window.settings.STATIC_URL+"site/tiny_mce-templates/3_columns.html",
        description: "3 Columns"
    },
];

tinyMCE.init(oTinyMCEConfig);
