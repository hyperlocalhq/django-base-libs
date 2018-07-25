(function($, undefined) {
    function AutocompleteManagerClass(){
        var registered_selectors = {};
        var dynamic = [];
        var that = this;
        this.init = function() {
            var i, iLen=dynamic.length; 
            for(i=0; i<iLen; i++) {
                var oEl = dynamic[i];
                this.set_autocomplete(
                    $(oEl.selector),
                    oEl.urlOrData,
                    oEl.options
                );
            }
        };
        this.reinit = function($oRow) {
            var i, iLen=dynamic.length; 
            for(i=0; i<iLen; i++) {
                var oEl = dynamic[i];
                this.set_autocomplete(
                    $oRow.find(oEl.selector),
                    oEl.urlOrData,
                    oEl.options
                );
            }
        };
        this.register = function(selector, urlOrData, options) {
            var dynamic_selector = selector.replace(/^#(id_.+?)-.+?-(.+)$/, ":input[id$=$2][id^=$1]")
            if (dynamic_selector != selector) {
                if (!registered_selectors[selector]) {
                    dynamic.push({
                        selector: dynamic_selector,
                        urlOrData: urlOrData,
                        options: options
                    });
                    registered_selectors[dynamic_selector] = true;
                }
            } else {
                this.set_autocomplete($(selector), urlOrData, options);
                registered_selectors[selector] = true;
            }
        };
        this.set_autocomplete = function($oField, urlOrData, options) {
            if ($oField.length) {
                $oField.autocomplete(urlOrData, options).result(that.result);
                $oField.click(function(){
                    $(this).select();
                }).blur(function(){
                    var $oField = $(this);
                    var $oHidden = $("#" + $oField.attr("id").replace(/_text$/, ""));
                    if (!$oField.val()) {
                        $oHidden.val("");
                    }
                });
            }
        };
        this.result = function(oEvent, aData, sFormatted) {
            var $oField = $(this);
            var $oHidden = $("#" + $oField.attr("id").replace(/_text$/, ""));
            if (aData) {
                $oHidden.val(aData[1]);
            } else { 
                $oHidden.val("");
            }
            $oHidden.change();
            $oHidden.blur();
        };
            
        this.formatItem = function(aRow) {
            var sHtml = '<span class="ac_title">' + aRow[0] + '</span>';
            if (aRow[2]) {
                sHtml += '<br /><span class="ac_description">' + aRow[2] + '</span>';
            }
            return sHtml;
        };
            
        this.test = function() {
            console.log(registered_selectors);
        };
    }
    self.AutocompleteManager = new AutocompleteManagerClass();

    function AutocompleteMultipleManagerClass() {
        var that = this;
        
        this.remove_item = function() {
            var $oLI = $(this).parent("li");
            var sFieldID = $oLI.attr("id");
            var aParts = sFieldID.split("-");
            var $oHidden = $("#" + aParts[0].replace(/_value_pk$/, ""));
            var aPKs = $oHidden.val().split(",");
            var aNewPKs = [];
            for (i=0; i<aPKs.length; i++) {
                if (aPKs[i] != aParts[1]) {
                    aNewPKs.push(aPKs[i]);
                }
            }
            $oHidden.val(aNewPKs.join(","));
            $oLI.slideUp("fast", function() {
                $(this).remove();
                $oHidden.change();
            });
            return false;
        };
        
        this.set_autocomplete = function($oField, urlOrData, options) {
            if ($oField.length) {
                $oField.unautocomplete().autocomplete(urlOrData, options).result(that.result);
                $oField.click(function(){
                    $(this).select();
                }).blur(function(){
                    $(this).val("");
                });
                var $oList = $("#" + $oField.attr("id").replace(/_text$/, "_value_list"));
                $oList.find("li").each(function() {
                    var $oClosing = $('<a href="#"><span>×</span></a>').click(that.remove_item);
                    $(this).append($oClosing);
                });
            }
        };
        this.result = function(oEvent, aData, sFormatted) {
            var $oField = $(this);
            var sFieldID = $oField.attr("id");
            var $oHidden = $("#" + sFieldID.replace(/_text$/, ""));
            var sPKs = "," + $oHidden.val() + ",";
            var aPKs = $oHidden.val()? $oHidden.val().split(","): [];
            if (aData && sPKs.indexOf("," + aData[1] + ",") == -1) {
                var $oList = $("#" + sFieldID.replace(/_text$/, "_value_list"));
                if (!$oList.length) {
                    $oList = $('<ul id="'+sFieldID.replace(/_text$/, "_value_list")+'" class="ac_value_list"></ul>').insertBefore($oField);
                }
                var $oLI = $('<li id="'+sFieldID.replace(/_text$/, "_value_pk-" + aData[1])+'"><span>'+aData[0]+' </span></li>');
                var $oClosing = $('<a href="#"><span>×</span></a>').click(that.remove_item);
                $oLI.hide();
                $oList.append($oLI);
                $oLI.append($oClosing);
                aPKs.push(aData[1]);
                $oHidden.val(aPKs.join(","));
                $oField.val("").focus();
                $oLI.slideDown("fast", function() {
                    $oHidden.change();
                    $oField.focus();
                });
            }
        };
    }
    /* inherits from AutocompleteManagerClass */
    AutocompleteMultipleManagerClass.prototype = new AutocompleteManagerClass();
    AutocompleteMultipleManagerClass.prototype.constructor = AutocompleteMultipleManagerClass;
    
    self.AutocompleteMultipleManager = new AutocompleteMultipleManagerClass();
    
    $(document).ready(function() {
        self.AutocompleteManager.init();
        self.AutocompleteMultipleManager.init();
    });
    
    $(window).unload(function() {
        self.AutocompleteManager = null;
        self.AutocompleteMultipleManager = null;
    });
    
}(jQuery));
