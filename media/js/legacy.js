/**
 *  Cancel the default event behaviour and event propagation
 *  Example:
 *      <a href="#" onclick="cancelEvent(event)">Inactive Link</a>
 */
window.cancelEvent = function(e) {
    if (!e) var e = window.event;
    e.cancelBubble = true;
    e.returnValue = false;
    if (e.stopPropagation) e.stopPropagation();
    if (e.preventDefault) e.preventDefault();
};

/**
 *  Get the html node which caused the event
 */
window.getCausingElement = function(e) {
    if (!e) var e = window.event;
    return e.target || e.srcElement;
};

/**
 *  Open current link in a new window
 *  Example:
 *      <a href="#" onclick="open_new_window(event)">Open</a>
 *  Use it instead of
 *      <a href="#" target="_blank">Open</a>
 */
window.open_new_window = function(e) {
    oLink = window.getCausingElement(e);
    while(oLink && oLink.tagName !== 'A') {
        oLink = oLink.parentNode;
    }
    window.open(oLink.href, '_blank', 'scrollbars=1,menubar=1,toolbar=1,location=1,resizable=1,status=1');
    window.cancelEvent(e);
};

/**
 *  Open the specified url
 *  Example:
 *      <div onclick="redirect('#')">Open</div>
 */
window.redirect = function(sURL) {
    document.location.href = sURL;
};

/**
 *  Open the specified url
 *  Example:
 *      <a href="javascript:submit_form('my_form')">Send</a>
 */
window.submit_form = function(sFormId) {
    document.getElementById(sFormId).submit();
};

/**
 *  Add CSS rules dynamically
 *  Example:
 *      dyn_css_rule("#menu li:hover", "color: red")
 */
window.dyn_css_rule = function(sSelector, sCssText) {
    try {
        var aSS = document.styleSheets;
        var i;
        for (i=aSS.length-1; i>=0; i--) {
            var oCss = document.styleSheets[i];
            var sMedia = (typeof(oCss.media) === 'string')?
                oCss.media:
                oCss.media.mediaText;
            if (!sMedia
                || sMedia.indexOf('screen') !== -1
                || sMedia.indexOf('all') !== -1
            ) {
                break;
            }
        }
        if (oCss.insertRule) {
            oCss.insertRule(sSelector + ' {' + sCssText + '}', oCss.cssRules.length);
        } else if (oCss.addRule) {
            oCss.addRule(sSelector, sCssText);
        }
    } catch(err) {
        var tag = document.createElement('style');
        tag.setAttribute('type', 'text/css');
        try {
            tag.innerHTML = sSelector + ' {' + sCssText + '}';
        } catch(err) {
            tag.innerText = sSelector + ' {' + sCssText + '}';
        }
        document.getElementsByTagName('head')[0].appendChild(tag);
    }
    return sSelector + '{' + sCssText + '}';
};

/**
 *  Adds or replaces GET parameters or hash parameters and redirects to that view.
 *  @sParams - string of params with leading "?" or "#"
 *  @oDict - a dictionary of parameters to add or replace.
 *  @bReturn - true if params string should be returned, false if page should be redirected
 *  If null is passed as a value for a parameter, the parameter will be removed.
 *  Example:
 *      append_to_get({paginate_by: 2, page: null}) will change
 *      "/?cat=3&page=5" to /?cat=3&paginate_by=2"
 *      append_to_hash({paginate_by: 2, page: null}) will change
 *      "/#cat=3&page=5" to /#cat=3&paginate_by=2"
 *      append_to_hash({paginate_by: 2, page: null}, true) will return
 *      "cat=3&paginate_by=2" from "/#cat=3&page=5"
 */
window.append_to_params = function(sParams, oDict, bReturn) {
    var oParams = {};
    var aPairs = sParams.slice(1).split('&');
    var sSep = sParams.slice(0, 1); // "?" or "#"
    var iLen = aPairs.length;
    for (i=0; i<iLen; i++) {
        aPair = aPairs[i].split('=');
        if (aPair[1]) {
            oParams[aPair[0]] = aPair[1];
        }
    }
    for (sKey in oDict) {
        oParams[sKey] = oDict[sKey];
    }
    var aParams = [];
    for (sKey in oParams) {
        if (oParams[sKey]) {
            aParams.push(sKey + '=' + encodeURI(oParams[sKey]));
        }
    }
    var sPath = '';
    sParams = aParams.join('&');
    sPath = sSep + sParams;

    if (bReturn) {
        return sParams;
    } else {
        location.href = sPath;
    }
};
window.append_to_get = function(oDict, bReturn) {
    return append_to_params(location.search || '?', oDict, bReturn);
};
window.append_to_hash = function(oDict, bReturn) {
    return append_to_params(location.hash || '#', oDict, bReturn);
};
