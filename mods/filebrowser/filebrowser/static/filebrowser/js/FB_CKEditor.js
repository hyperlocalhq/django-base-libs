function ProtectPath(path) {
    path = path.replace( /\\/g,'\\\\');
    path = path.replace( /'/g,'\\\'');
    return path ;
}

function gup( name ) {
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.href);
  if(results == null)
    return "";
  else
    return results[1];
}

function OpenFile(fileUrl, fileAuthor, fileDescription) {

    if (typeof fileAuthor === "undefined") fileAuthor = '';
    if (typeof fileDescription === "undefined") fileDescription = '';
    window.top.opener.fb_fileAuthor = fileAuthor;
    window.top.opener.fb_fileDescription = fileDescription;

    var CKEditorFuncNum = gup('CKEditorFuncNum');
    var host = (window.top.opener.CKEDITOR.config.media_host) ? window.top.opener.CKEDITOR.config.media_host : "";
    window.top.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum, host+fileUrl);
    window.top.close();
    window.top.opener.focus();
}
