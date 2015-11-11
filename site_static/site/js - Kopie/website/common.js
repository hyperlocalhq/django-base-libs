(function($, undefined) {

    if (
        !dyn_css_rule(".to_hide", "display: none")
        || !dyn_css_rule(".to_show", "display: block")
    ) {
        $(document).ready(function() {
            $(".to_hide").hide();
            $(".to_show").show();
        });
    }
    
    (function($){  
        $.fn.autoscroll = function() {
            $('html,body').animate(
                {
                    scrollLeft: this.offset().left,
                    scrollTop: this.offset().top
                },
                500
            );
            return this;
        };  
    })(jQuery);
       
    self.SectorSelectorManager = {
        init: function() {
            var oSelf = self.SectorSelectorManager;
            $("#id_chosen_creative_sector").change(function() {
                var sSector = $(this).val();
                if (sSector) {
                    window.redirect("/creative-sector/" + sSector + "/");
                } else {
                    window.redirect("/");
                }
                return false;
            });
        },
        destruct: function() {
            self.SectorSelectorManager = null;
        }
    };
    
    self.ActivityManager = {
        init: function() {
            var oSelf = self.ActivityManager;
            if ($("#dyn_profiles").children("li").length > 2) {
                var aSelectors = [
                    ".navi_add_portfolio_image_" + window.settings.lang + " a",
                    ".navi_add_new_project_" + window.settings.lang + " a",
                    ".navi_add_profile_image_" + window.settings.lang + " a",
                    ".navi_add_blog_entry_" + window.settings.lang + " a"
                ];
                $(aSelectors.join(",")).click(oSelf.choose_profile);
            }
            var aSelectors = [
                "li.navi_delete_event_" + window.settings.lang + " a",
                "li.navi_delete_job_offer_" + window.settings.lang + " a"
            ];
            $(aSelectors.join(",")).click(oSelf.delete_object);
        },
        choose_profile: function() {
            var oSelf = self.ActivityManager;
            var $oLink = $(this);
            self.open_popup(
                gettext("Choose profile"),
                584, "auto",
                "/helper/popup-window/choose-profile/",
                false,
                false,
                {
                    onsubmit: function() {return oSelf.goto_profile($oLink);}
                }
            );
            return false;
        },
        delete_object: function() {
            var oSelf = self.ActivityManager;
            var $oLink = $(this);
            self.open_popup(
                $oLink.text(),
                584, "auto",
                $oLink.attr("href"),
                true
            );
            return false;
        },
        goto_profile: function($oLink) {
            var oSelf = self.ActivityManager;
            $oProfileLink = $("#dyn_go_to_profile");
            var oM = $oLink.parent().attr("class").match(
                /\bnavi_(\S+?)_\S\S\b/
            );
            if (oM) {
                var sUrl = $oProfileLink.val();
                switch (oM[1]) {
                    case "add_portfolio_image":
                        window.redirect(sUrl + settings.URL_ID_PORTFOLIO + "/manage/");
                        break;
                    case "add_new_project":
                        window.redirect(sUrl + settings.URL_ID_PORTFOLIO + "/album/add/");
                        break;
                    case "add_profile_image":
                        window.redirect(sUrl + "#edit_avatar");
                        break;
                    case "add_blog_entry":
                        window.redirect(sUrl + "blog/new/");
                        break;
                }
            }
            return false;
        },
        destruct: function() {
            self.ActivityManager = null;
        }
    };
    
    self.AboutManager = {
        init: function() {
            var oSelf = self.AboutManager;
            $("li.navi_about_" + window.settings.lang + " a").click(oSelf.show_info);
        },
        show_info: function() {
            var oSelf = self.AboutManager;
            var $oLink = $(this);
            self.open_popup(
                "",
                584, "auto",
                "/about/",
                false,
                false,
                {}
            );
            return false;
        },
        destruct: function() {
            self.AboutManager = null;
        }
    };
    
    self.BookmarkManager = {
        init: function() {
            $("#save_bookmark").click(function() {
                self.BookmarkManager.addBookmark(website.path);
                return false;
            });
            $("#save_list_link a").click(function() {
                self.BookmarkManager.toggleAdding(1);
                return false;
            });
            $("#cancel_bookmark").click(function() {
                self.BookmarkManager.toggleAdding(0);
                return false;
            });
        },
        toggleAdding: function(action) {
            // action == 0 - hide form fields for adding
            // action == 1 - show form fields for adding
            if (action == 1) {
                $("#save_list_link").hide();
                $("#save_list_as").show();
            } else {
                $("#save_list_link").show();
                $("#save_list_as").hide();
                $("#error_msg").hide();
            }
        },
        toggleRenaming: function(counter, action) {
            // action == 0 - hide form fields for renaming
            // action == 1 - show form fields for renaming
            var oLink = $("#bookmark_link_" + counter);
            var oTitle = $("#bookmark_title_" + counter);
            if (action == 1) {
                $("#main_functions_" + counter).hide();
                $("#renaming_functions_" + counter).show();
                oLink.hide();
                oTitle.show().val(oLink.text());
            } else {
                $("#main_functions_" + counter).show();
                $("#renaming_functions_" + counter).hide();
                oLink.show();
                oTitle.hide();
            }
        },
        toggleDeleting: function(counter, action) {
            var sMessage = '<div class=\"errorBox\">' + gettext("Do you really want to delete this bookmark?") + '</div>';
            var oDeletingFuncs = $("#delete_functions_" + counter).get(0);
            var oMainFuncs = $("#main_functions_" + counter).get(0);
            if (action == 1) {
                oMainFuncs.style.display = "none";
                oDeletingFuncs.style.display = "block";
    
                var oRow = $('#bookmark_row_' + counter).get(0);
                var oRowClass = oRow.className;
                oRow.style.borderTop = '0';
                
                var confirmRow = $('#bookmark_management').get(0).insertRow(oRow.rowIndex);
                
                var confirmColumn = document.createElement('td');
                var colspan = document.createAttribute('colspan');
                colspan.nodeValue = '2';
                confirmColumn.setAttributeNode(colspan);
                
                confirmRow.appendChild(confirmColumn);
                confirmColumn.innerHTML = sMessage;
                
                confirmRow.className = oRowClass;
                $(confirmColumn).children("div.errorBox").hide().slideDown("normal");
                
            } else {
                oMainFuncs.style.display = "block";
                oDeletingFuncs.style.display = "none";
    
                var oRow = $('#bookmark_row_' + counter).get(0);
                oRow.style.borderTop = '1px solid #E6ECF0';
                $(oRow).prev("tr:first").find("div.errorBox").slideUp("normal", function() {
                    $(oRow).prev("tr:first").remove();
                });
            }
        },
        addBookmark: function(sUrlPath) {
            var sTitle = $("#bookmark_title").val();
            $.get(
                "/helper/bookmark/",
                {
                    title: sTitle,
                    url_path: sUrlPath,
                    action: "add"
                },
                self.BookmarkManager.showAddingResults
            );
        },
        showAddingResults: function(sData) {
            var oSelf = self.BookmarkManager;
            eval("var oData = " + sData);
            // check for errors ...
            if (oData && oData.error) {
                $("#error_msg").text(oData.error).show();
                oSelf.toggleAdding(1);
            } else {
                var $oLi = $('<li>').addClass("list");
                var $oA = $('<a>').attr("href", oData.url_path).addClass("active");
                $oA.append(
                    '<span class="pic">'
                ).append(
                    document.createTextNode(oData.title)
                );
                $oLi.append($oA).insertBefore("#save_list_link");
                // everything is ok, hide errors
                $("#error_msg").hide();
                oSelf.toggleAdding(0);
            }
        },
        renameBookmark: function(id, counter) {
            var sTitle = $("#bookmark_title_" + counter).val();
            $.get(
                "/helper/bookmark/",
                {
                    title: sTitle,
                    id: id,
                    action: "rename"
                },
                new Function("sData", "self.BookmarkManager.showRenamingResults(sData, "+ counter + ")")
            );
        },
        showRenamingResults: function(sData, counter) {
            var oLink = $("#bookmark_link_" + counter).get(0);
            var oErrorMsg = $("#error_msg_" + counter).get(0);
            eval("oData = " + sData);
            // check for errors ...
            if (oData.error) {
                oErrorMsg.style.display="block";
                if (oErrorMsg.firstChild)
                    oErrorMsg.removeChild(oErrorMsg.firstChild)
                oErrorMsg.appendChild(document.createTextNode(oData.error));
                self.BookmarkManager.toggleRenaming(counter, 1);
            } else {
                oLink.innerHTML = oData.title;
                // everything is ok, hide errors
                oErrorMsg.style.display="none";
                self.BookmarkManager.toggleRenaming(counter, 0);
            }
        },
        deleteBookmark: function(id, counter) {
            $.get(
                "/helper/bookmark/",
                {
                    id: id,
                    action: "delete"
                },
                new Function("sData", "self.BookmarkManager.showDeletingResults(sData, "+ counter + ")")
            );
        },
        showDeletingResults: function(sData, counter) {
            var oBookmarkRow = $("#bookmark_row_" + counter).get(0);
            var oErrorMsg = $("#error_msg_" + counter).get(0);
            eval("oData = " + sData);
            // check for errors ...
            if (oData.error) {
                oErrorMsg.style.display = "block";
                if (oErrorMsg.firstChild)
                    oErrorMsg.removeChild(oErrorMsg.firstChild)
                oErrorMsg.appendChild(document.createTextNode(oData.error));
            } else {
                $(oBookmarkRow).prev("tr:first").find("div.errorBox").slideUp("normal", function() {
                    $(oBookmarkRow).prev("tr:first").andSelf().remove();
                    // everything is ok, hide errors
                    oErrorMsg.style.display="none";
                    var oTable = $('#bookmark_management').get(0);
                    if (oTable.rows.length) {
                        j = 0;
                        for (i=0, l=oTable.rows.length; i<l; i++) {
                            if (i>0 && !oTable.rows[i-1].id) {
                                j++;
                            }
                            if (j%2==0) {
                                oTable.rows[i].className = "list-item odd";
                            } else {
                                oTable.rows[i].className = "list-item even";
                            }
                            j++;
                        }
                    } else {
                        $('#no_bookmarks').css({display: "block"});
                    }
                });
            }
        },
        destruct: function() {
            self.BookmarkManager = null;
        }
    };
    
    if (!dyn_css_rule("#dyn_rotating_banner p", "display: none;")
        || !dyn_css_rule("#dyn_rotating_banner p.first-child", "display: block")
    ) {
        $(document).ready(function() {
            $("#dyn_rotating_banner p").hide();
            $("#dyn_rotating_banner p.first-child").show();
        });
    }
    
    self.RotatingBanner = {
        current: 0,
        $banners: [],
        timeout_handler: null,
        init: function() {
            var oSelf = self.RotatingBanner;
            oSelf.$banners = $(
                "#dyn_rotating_banner .hidable p:has(a)"
            ).addClass("rotating_unit");
            $("#dyn_rotating_banner .hidable a").click(function(e) {
                location.href = "/" + window.settings.lang + "/partner/";
                return false;
                /*
                if (self.open_new_window) {
                    self.open_new_window(e);
                    return false;
                }
                */
            });
            if (oSelf.$banners.length > 1) {
                var $current = $(oSelf.$banners[oSelf.current]);
                $current.addClass("current_rotating_unit");
                oSelf.timeout_handler = setTimeout(
                    "self.RotatingBanner.show_another()",
                    5000
                );
            }
        },
        show_another: function() {
            var oSelf = self.RotatingBanner;
            var $current = $(oSelf.$banners[oSelf.current]);
            oSelf.current++;
            if (oSelf.$banners.length==oSelf.current) {
                oSelf.current = 0;
            }
            var $another = $(oSelf.$banners[oSelf.current]);
            $another.hide().addClass("next_rotating_unit").fadeIn("slow", function() {
                $current.hide().removeClass("current_rotating_unit");
                $another.removeClass("next_rotating_unit").addClass("current_rotating_unit");
            });
            oSelf.timeout_handler = setTimeout("self.RotatingBanner.show_another()", 5000);
        },
        destruct: function() {
            clearTimeout(self.RotatingBanner.timeout_handler);
            self.RotatingBanner = null;
        }
    };
    
    self.SocialProfilesManager = {
        init: function() {
            $("#block_social-profiles_en .hidable a,"
                + "#block_social-profiles_de .hidable a"
            ).click(function(e) {
                if (self.open_new_window) {
                    self.open_new_window(e);
                    return false;
                }
            });
        },
        destruct: function() {
            self.SocialProfilesManager = null;
        }
    };
    
    $(document).ready(function() {
        self.ActivityManager.init();
        self.AboutManager.init();
        self.SectorSelectorManager.init();
        self.BookmarkManager.init();
        self.RotatingBanner.init();
        self.SocialProfilesManager.init();
    });
    
    
    $(window).unload(function() {
        self.SectorSelectorManager.destruct();
        self.ActivityManager.destruct();
        self.AboutManager.destruct();
        self.BookmarkManager.destruct();
        self.RotatingBanner.destruct();
        self.SocialProfilesManager.destruct();
    });
    
    $(document).ready(function() {
        if ($.browser.msie) {
            var version = Number($.browser.version.replace(/\.[0-9\.]+$/gi, ""));
            if (version < 8) {
                if (window.location.href.indexOf("compatibility") == -1) {
                    window.location = "/compatibility/";
                    return;
                }
            }
        } 
            
        var hash = window.location.hash;
        if (hash && $(hash).length) {
            $(hash).addClass('highlight');
        }
        $('a[href^=#]').click(function() {
            if ($(this).attr('href') != '#') {
                $($(this).attr('href')).addClass('highlight');
            }
        });
        
        // init Uni-Form
        $("form.uniForm").uniform();
        
        // specific for this page
        $(".browse a").click(function(e) {
            e.preventDefault();
            $("#formStyle").attr("href",$(this).attr('rel'));
            return false;
        });
        
        $('.nav_menu li:first-child').addClass("first-child");
        $('.nav_menu li:last-child').addClass("last-child");
        
        $("#nav li").live("mouseover", function() {
            $(this).addClass("hover");
        }).live("mouseout", function() {
            $(this).removeClass("hover");
        });
        $(".list-item").live("mouseenter", function() {
            $(this).addClass("hover");
        }).live("mouseleave", function() {
            $(this).removeClass("hover");
        });
        $("ul.list-block").find('li').hover(function() {
            $(this).addClass("hover");
        }, function() {
            $(this).removeClass("hover");
        })
        $(".news-details").hover(function() {
            $(this).addClass("hover");
        }, function() {
            $(this).removeClass("hover");
        })
        /*
        (function update_visitors() {
            $.get("/helper/site-visitors/", function(data) {
                $('#site_visitors').html(data);
            });
            setTimeout(update_visitors, 10000);
        }());
        */
    });
    
}(jQuery));
