(function($,undefined){self.CategoryManager={init:function(){var oF=self.CategoryManager;
var $oLi=$("div.categories li");
var aChecks=$oLi.find(":checkbox").each(function(){var $oCheck=$(this);
if($oCheck.attr("id").match(/^id_[A-Z]{2}_\d+$/)){var $oLabel=$oCheck.parents("label");
var $oUl=$oLabel.nextAll("ul");
var $oA=$oLabel.prevAll("a");
if($oUl.length){$oCheck.click(oF.toggle);
$oA.click(oF.toggle);
$oA.removeClass("no-children").removeClass("children-opened").addClass("children-closed").children("span").html("&rarr;");
$oUl.hide()
}else{$oA.click(function(){return false
});
$oCheck.click(function(){$(this).parents("li").children("label").children(":checkbox").not(this).attr("checked",true)
})
}if($oCheck.attr("checked")){oF.expand($oUl)
}}})
},toggle:function(){var oF=self.CategoryManager;
var $aFields=$(this).parents("li").children("label, ul");
var $oCheck=$($aFields[0]).children(":checkbox");
var $oUl=$($aFields[1]);
var bBubble=true;
if($(this).is(":checkbox")){$oCheck.parent().parents("li").children(":checkbox").attr("checked",true)
}if($(this).is("a")){if($oUl.is(":hidden")){oF.expand($oUl)
}else{oF.collapse($oUl)
}bBubble=false
}else{if($oCheck.attr("checked")){oF.expandAndCheck($oUl)
}else{oF.collapseAndUncheck($oUl)
}}return bBubble
},collapseAndUncheck:function(oUl){var oF=self.CategoryManager;
oUl.slideUp("normal");
oUl.find(":checkbox").attr("checked",false);
oA=oUl.siblings("a");
if(!oA.is(".no-children")){oA.removeClass("children-opened").addClass("children-closed").children("span").html("&rarr;")
}},expandAndCheck:function(oUl){var oF=self.CategoryManager;
oUl.slideDown("normal");
oA=oUl.siblings("a");
if(!oA.is(".no-children")){oA.removeClass("children-closed").addClass("children-opened").children("span").html("&darr;")
}},collapse:function(oUl){var oF=self.CategoryManager;
oUl.slideUp("normal");
oA=oUl.siblings("a");
if(!oA.is(".no-children")){oA.removeClass("children-opened").addClass("children-closed").children("span").html("&rarr;")
}},expand:function(oUl){var oF=self.CategoryManager;
oUl.slideDown("normal");
oA=oUl.siblings("a");
if(!oA.is(".no-children")){oA.removeClass("children-closed").addClass("children-opened").children("span").html("&darr;")
}},destruct:function(){self.CategoryManager=null
}};
$(document).ready(function(){self.CategoryManager.init()
});
$(window).unload(self.CategoryManager.destruct)
}(jQuery));
(function($,undefined){self.ContactDetailsManager={iEmailCount:3,iURLCount:3,iIMCount:3,init:function(){var oSelf=self.ContactDetailsManager;
for(i=1;
i<3;
i++){var $oF=$("#id_email"+i);
if(!$oF.length){return
}if(!$oF.val()){$oF.parents(".ctrlHolder").css("display","none");
oSelf.iEmailCount--
}$oF=$("#id_url"+i+"_link");
if(!$oF.val()){$oF.parents(".ctrlHolder").css("display","none");
oSelf.iURLCount--
}$oF=$("#id_im"+i+"_address");
if(!$oF.val()){$oF.parents(".ctrlHolder").css("display","none");
oSelf.iIMCount--
}}var $oLi=$('<p class="dyn_contact_managing">').appendTo($("#id_email0").parents(".ctrlHolders"));
$('<a href="#Remove-Email" id="email_remover">'+gettext("Remove email")+"</a> ").css("display",oSelf.iEmailCount>1?"inline":"none").click(oSelf.remove_email).appendTo($oLi);
$(document.createTextNode(" ")).appendTo($oLi);
$('<a href="#Add-Email" id="email_adder">'+gettext("Add email")+"</a>").css("display",oSelf.iEmailCount<3?"inline":"none").click(oSelf.add_email).appendTo($oLi);
var $oLi=$('<p class="dyn_contact_managing">').appendTo($("#id_url0_link").parents(".ctrlHolders"));
$('<a href="#Remove-URL"  id="url_remover">'+gettext("Remove URL")+"</a>").css("display",oSelf.iURLCount>1?"inline":"none").click(oSelf.remove_url).appendTo($oLi);
$(document.createTextNode(" ")).appendTo($oLi);
$('<a href="#Add-URL"  id="url_adder">'+gettext("Add URL")+"</a>").css("display",oSelf.iURLCount<3?"inline":"none").click(oSelf.add_url).appendTo($oLi);
var $oLi=$('<p class="dyn_contact_managing">').appendTo($("#id_im0_address").parents(".ctrlHolders"));
$('<a href="#Remove-IM" id="im_remover">'+gettext("Remove IM")+"</a>").css("display",oSelf.iIMCount>1?"inline":"none").click(oSelf.remove_im).appendTo($oLi);
$(document.createTextNode(" ")).appendTo($oLi);
$('<a href="#Add-IM" id="im_adder">'+gettext("Add IM")+"</a> ").css("display",oSelf.iIMCount<3?"inline":"none").click(oSelf.add_im).appendTo($oLi)
},add_email:function(){var oSelf=self.ContactDetailsManager;
$("#id_email"+oSelf.iEmailCount).parents(".ctrlHolder").css("display","block");
oSelf.iEmailCount++;
if(oSelf.iEmailCount>1){$("#email_remover").css("display","inline");
$("#email_adder").addClass("separated")
}if(oSelf.iEmailCount>=3){$("#email_adder").css("display","none")
}return false
},remove_email:function(){var oSelf=self.ContactDetailsManager;
oSelf.iEmailCount--;
$("#id_email"+oSelf.iEmailCount).val("").parents(".ctrlHolder").css("display","none").find("p.error").remove();
if(oSelf.iEmailCount<=1){$("#email_remover").css("display","none");
$("#email_adder").removeClass("separated")
}if(oSelf.iEmailCount<3){$("#email_adder").css("display","inline")
}return false
},add_url:function(){var oSelf=self.ContactDetailsManager;
$("#id_url"+oSelf.iURLCount+"_link").parents(".ctrlHolder").css("display","block");
oSelf.iURLCount++;
if(oSelf.iURLCount>1){$("#url_remover").css("display","inline");
$("#url_adder").addClass("separated")
}if(oSelf.iURLCount>=3){$("#url_adder").css("display","none")
}return false
},remove_url:function(){var oSelf=self.ContactDetailsManager;
oSelf.iURLCount--;
$("#id_url"+oSelf.iURLCount+"_link").val("").parents(".ctrlHolder").css("display","none").find("p.error").remove();
$("#id_url"+oSelf.iURLCount+"_type").val("");
if(oSelf.iURLCount<=1){$("#url_remover").css("display","none");
$("#url_adder").removeClass("separated")
}if(oSelf.iURLCount<3){$("#url_adder").css("display","inline")
}return false
},add_im:function(){var oSelf=self.ContactDetailsManager;
$("#id_im"+oSelf.iIMCount+"_address").parents(".ctrlHolder").css("display","block");
$("#id_im"+oSelf.iIMCount+"_type").val("");
oSelf.iIMCount++;
if(oSelf.iIMCount>1){$("#im_remover").css("display","inline");
$("#im_adder").addClass("separated")
}if(oSelf.iIMCount>=3){$("#im_adder").css("display","none")
}return false
},remove_im:function(){var oSelf=self.ContactDetailsManager;
oSelf.iIMCount--;
$("#id_im"+oSelf.iIMCount+"_address").val("").parents(".ctrlHolder").css("display","none").find("p.error").remove();
$("#id_im"+oSelf.iIMCount+"_type").val("");
if(oSelf.iIMCount<=1){$("#im_remover").css("display","none");
$("#im_adder").removeClass("separated")
}if(oSelf.iIMCount<3){$("#im_adder").css("display","inline")
}return false
},destruct:function(){self.ContactDetailsManager=null
}};
$(document).ready(function(){self.ContactDetailsManager.init()
});
$(window).unload(function(){self.ContactDetailsManager.destruct()
})
}(jQuery));
(function($,undefined){self.ProfileManager={sContextItemType:"",sSlug:"",oCachedDefaults:{},sSelected:"",sInProgress:'<span class="section_in_progress"><img alt="'+gettext("in progress...")+'" src="'+settings.STATIC_URL+'site/js/jquery/indicator.gif" /></span>',bInProgress:false,oIndexedRe:/^(.+)_(\d+)$/,init:function(){var oSelf=self.ProfileManager;
var aUrlBits=window.website.path.substr(1).split("/");
oSelf.sContextItemType=aUrlBits[0];
oSelf.sSlug=aUrlBits[1];
$('<iframe src="/helper/edit-'+oSelf.sContextItemType+"-profile/"+oSelf.sSlug+'/" name="hidden_iframe" id="hidden_iframe" />').addClass("hidden").appendTo($(document.body));
$("div.dyn_section").each(function(){sSection=$(this).attr("id").substr(4);
$('<a href="#edit_'+sSection+'" id="but_edit_'+sSection+'"><span><span>'+gettext("edit")+"</span></span></a>").addClass("but_edit").click(new Function('return self.ProfileManager.edit_section("'+sSection+'")')).insertAfter($("#dyn_"+sSection))
});
if((settings.URL_ID_PERSON+"|"+settings.URL_ID_INSTITUTION+"|"+settings.URL_ID_EVENT+"|"+settings.URL_ID_JOB_OFFER).indexOf(oSelf.sContextItemType)!=-1){if(self.GMapManager){self.GMapManager.init()
}}if($("#dyn_contacts").length&&(oSelf.sContextItemType=="person"||oSelf.sContextItemType=="institution")){$('<span class="contact_modifiers"><a href="#" class="but_add_contact"><span><span>'+gettext("add contact")+"</span></span></a></span>").appendTo(".dyn_contact_new");
$(".but_add_contact").click(oSelf.add_contact)
}if(document.location.hash.indexOf("#edit_")==0){sCurrentSection=document.location.hash.substr(6);
oSelf.edit_section(sCurrentSection)
}else{if(document.location.hash.indexOf("#view_")==0){sCurrentSection=document.location.hash.substr(6);
$("#dyn_"+sCurrentSection).autoscroll()
}}},clear_current_section:function(){var oSelf=self.ProfileManager;
if(oSelf.sSelected){$("#dyn_"+oSelf.sSelected).html(oSelf.oCachedDefaults[oSelf.sSelected]);
$("#but_edit_"+oSelf.sSelected).removeClass("hidden");
$(".but_add_contact").removeClass("hidden")
}},cancel_current_section:function(){var oSelf=self.ProfileManager;
if(oSelf.sSelected){$("#dyn_"+oSelf.sSelected).html(oSelf.oCachedDefaults[oSelf.sSelected]);
$("#but_edit_"+oSelf.sSelected).removeClass("hidden");
$(".but_add_contact").removeClass("hidden");
document.location.href=document.location.pathname+"#view_"+oSelf.sSelected;
$("#dyn_"+oSelf.sSelected).autoscroll()
}},edit_section:function(sSection){var oSelf=self.ProfileManager;
if(!oSelf.bInProgress){oSelf.bInProgress=true;
oSelf.clear_current_section();
oSelf.sSelected=sSection;
oSelf.oCachedDefaults[sSection]=$("#dyn_"+sSection).html();
$("#but_edit_"+sSection).prepend(oSelf.sInProgress);
var sPostfix="";
var oM=sSection.match(oSelf.oIndexedRe);
if(oM){sSection=oM[1];
sPostfix=oM[2]+"/"
}frames.hidden_iframe.location.href="/helper/edit-"+oSelf.sContextItemType+"-profile/"+oSelf.sSlug+"/"+sSection+"/"+sPostfix
}},add_contact:function(){var oSelf=self.ProfileManager;
if(!oSelf.bInProgress){oSelf.bInProgress=true;
oSelf.clear_current_section();
$(".but_add_contact").addClass("hidden");
oSelf.sSelected=sSection="contact_new";
oSelf.oCachedDefaults[sSection]="";
if(!$("#dyn_"+sSection).length){$('<div class="dyn_section" id="dyn_'+sSection+'"></div>').appendTo($("#dyn_contacts"))
}$("#dyn_"+sSection).html(oSelf.sInProgress);
frames.hidden_iframe.location.href="/helper/edit-"+oSelf.sContextItemType+"-profile/"+oSelf.sSlug+"/contact/new/"
}return false
},delete_contact:function(iIndex){var oSelf=self.ProfileManager;
if(!oSelf.bInProgress){var oM=$(this).parents(".dyn_section").attr("id").match(oSelf.oIndexedRe);
var sIndex="";
if(oM){sSection=oM[1];
sIndex=oM[2]
}open_popup(gettext("Delete Contact"),584,"auto","/helper/popup-window/delete-contact/?type="+oSelf.sContextItemType+"&slug="+oSelf.sSlug+"&index="+sIndex,true)
}return false
},section_loaded:function(sHtml,bUpdate){var oSelf=self.ProfileManager;
var sSection=oSelf.sSelected;
$("#but_edit_"+sSection).addClass("hidden");
$("#dyn_"+sSection).html(sHtml).autoscroll();
if(bUpdate){if(sSection.match(/^(identity|event_times|details|contact_)/)){document.location.href=document.location.pathname
}else{oSelf.oCachedDefaults[sSection]=$("#dyn_"+sSection).html();
$("#but_edit_"+sSection).removeClass("hidden");
oSelf.sSelected=""
}document.location.href=document.location.pathname+"#view_"+sSection;
$("#dyn_"+sSection).html(sHtml).autoscroll()
}else{self.ContactPrepopulationManager.init();
$(":button[name=cancel]").click(oSelf.cancel_current_section);
if("categories"==sSection){if(self.CategoryManager){self.CategoryManager.init()
}if(self.CollapsableNavigationBlocks){self.CollapsableNavigationBlocks.init()
}}else{if("avatar"==sSection){$('<input type="button" class="button_delete button_bad" />').val(gettext("Delete").toUpperCase()).insertBefore(".buttons").click(oSelf.delete_avatar)
}else{if("event_times"==sSection){if(self.FormsetsManager){self.FormsetsManager.init()
}if(self.EventTimesManager){self.EventTimesManager.init()
}}else{if("opening_hours"==sSection||"fees_opening_hours"==sSection){if(self.OpeningHoursManager){self.OpeningHoursManager.init()
}}else{if("fees"==sSection){if(self.EventFeeManager){self.EventFeeManager.init()
}}else{if("contact"==sSection){if(self.ContactManager){self.ContactManager.init()
}if(self.ContactDetailsManager){self.ContactDetailsManager.init()
}if(self.GMapManager){self.GMapManager.init()
}}else{if(sSection.match(/^contact_/)){if(self.ContactManager){self.ContactManager.init()
}if(self.ContactDetailsManager){self.ContactDetailsManager.init()
}if(self.GMapManager){self.GMapManager.init()
}$("#id_location_type").change(function(){if($(this).val()=="work"){$("#dyn_contact_institution").slideDown("normal").removeClass("hidden")
}else{$("#dyn_contact_institution").slideUp("normal").addClass("hidden");
$("#id_institution").val("")
}}).change();
if(sSection!="contact_new"){$('<input type="button" class="button_delete button_bad" />').val(gettext("Delete").toUpperCase()).insertBefore(".buttons").click(oSelf.delete_contact)
}}else{if("additional_info"==sSection){MutipleSelectAutoCompleteManager.init()
}}}}}}}}}$("#but_edit_"+sSection+" .section_in_progress").remove();
oSelf.bInProgress=false
},delete_avatar:function(){var oSelf=self.ProfileManager;
if(!oSelf.bInProgress){open_popup(gettext("Delete Avatar"),584,"auto","/helper/popup-window/delete-avatar/?type="+oSelf.sContextItemType+"&slug="+oSelf.sSlug,true)
}return false
},destruct:function(){self.ProfileManager=null
}};
self.ContactManager={init:function(){var oSelf=self.ContactManager;
$("#id_institution_enter").click(function(){$("#id_institution").val("");
$("#id_institution_text").val("");
$("#id_institution_enter").parents("fieldset:first").addClass("hidden");
$("#id_institution_select").parents("fieldset:first").removeClass("hidden");
return false
});
$("#id_institution_select").click(function(){$("#id_institution_title").val("");
$("#id_institution_select").parents("fieldset:first").addClass("hidden");
$("#id_institution_enter").parents("fieldset:first").removeClass("hidden");
return false
});
if($("#id_institution_title").val()){$("#id_institution_enter").click()
}$("#id_institution").blur(oSelf.prepopulateContact);
$("#id_venue").blur(oSelf.prepopulateContact)
},prepopulateContact:function(){var oSelf=self.ContactManager;
if($(this).val()){$j.get("/helper/accounts/"+settings.URL_ID_INSTITUTION+"_attrs/"+$(this).val()+"/",self.ContactManager.fillInInstitutionContactData);
return false
}},fillInInstitutionContactData:function(sData){var oSelf=self.ContactManager;
eval("var oData = "+sData);
if(oData.street_address&&!$("#id_street_address").val()){$("#id_street_address").val(oData.street_address)
}if(oData.street_address2&&!$("#id_street_address2").val()){$("#id_street_address2").val(oData.street_address2)
}if(oData.postal_code&&!$("#id_postal_code").val()){$("#id_postal_code").val(oData.postal_code)
}if(oData.country&&!$("#id_country").val()){$("#id_country").val(oData.country.iso2_code)
}if(oData.latitude&&!$("#id_latitude").val()){$("#id_latitude").val(oData.latitude)
}if(oData.longitude&&!$("#id_longitude").val()){$("#id_longitude").val(oData.longitude)
}var aTextFields=[["email0_address","email0"],["email1_address","email1"],["email2_address","email2"],["phone0_country","phone_country"],["phone0_area","phone_area"],["phone0_number","phone_number"],["phone1_country","fax_country"],["phone1_area","fax_area"],["phone1_number","fax_number"],["phone2_country","mobile_country"],["phone2_area","mobile_area"],["phone2_number","mobile_number"],["url0_link","url0_link"],["url1_link","url1_link"],["url2_link","url2_link"],["im0_address","im0_address"],["im1_address","im1_address"],["im2_address","im2_address"]];
var aSelectFields=["url0_type","url1_type","url2_type","im0_type","im1_type","im2_type"];
$(aTextFields).each(function(iIndex,aNames){if(oData[aNames[0]]&&!$("#id_"+aNames[1]).val()){$("#id_"+aNames[1]).val(oData[aNames[0]])
}});
$(aSelectFields).each(function(iIndex,sName){$("#id_"+sName).val(oData[sName+"_id"])
});
if(typeof(oData.latitude)!="undefined"&&typeof(oData.longitude)!="undefined"){self.GMapManager.markGeoposition(oData.latitude,oData.longitude)
}},destruct:function(){self.ContactManager=null
}};
self.ContactPrepopulationManager={aTextFields:["location_title","street_address","street_address2","postal_code","city","state","neighborhood","district","latitude","longitude","phone0_country","phone0_area","phone0_number","phone1_country","phone1_area","phone1_number","phone2_country","phone2_area","phone2_number","url0_link","url1_link","url2_link","im0_address","im1_address","im2_address"],aSelectFields:["country","phone0_type","phone1_type","phone2_type","url0_type","url1_type","url2_type","im0_type","im1_type","im2_type"],aBoolFields:[],init:function(){var oSelf=self.ContactPrepopulationManager;
$("#id_institution").change(oSelf.get_contact_details)
},destruct:function(){self.ContactPrepopulationManager=null
},get_contact_details:function(){var oSelf=self.ContactPrepopulationManager;
var sValue=$(this).val();
if(sValue){$j.get("/admin/institutions/institution/"+sValue+"/json/",oSelf.prepopulate)
}},prepopulate:function(sData){var oSelf=self.ContactPrepopulationManager;
eval("var oData ="+sData);
$(oSelf.aTextFields).each(function(iKey,sVal){var oNode=$("#id_"+sVal);
if(!oNode.val()&&oData[sVal]){oNode.val(oData[sVal])
}});
$(oSelf.aBoolFields).each(function(iKey,sVal){var oNode=$("#id_"+sVal);
oNode.get(0).checked=oData[sVal]
});
$(oSelf.aSelectFields).each(function(iKey,sVal){var oNode=$("#id_"+sVal);
oNode.val(oData[sVal+"_id"])
})
}};
self.EventFeeManager={iFeeCount:6,init:function(){var oSelf=self.EventFeeManager;
for(i=1;
i<6;
i++){var oF=$("#id_fee"+i+"_amount");
if(!oF.val()){$("#id_fee"+i+"_label_en").parent().hide();
$("#id_fee"+i+"_label_de").parent().hide();
oF.parent().hide();
oSelf.iFeeCount--
}}var $oLi=$('<li class="dyn_contact_managing">').appendTo($("#id_fee0_label_en").parents("ul:first"));
$('<a href="#Remove-Fee" id="fee_remover">'+gettext("Remove Fee")+"</a>").css("display",oSelf.iFeeCount>1?"inline":"none").click(oSelf.remove_fee).appendTo($oLi);
$(document.createTextNode(" ")).appendTo($oLi);
$('<a href="#Add-Fee" id="fee_adder">'+gettext("Add Fee")+"</a>").css("display",oSelf.iFeeCount<6?"inline":"none").click(oSelf.add_fee).appendTo($oLi);
if(oSelf.iFeeCount>1){$("#fee_adder").addClass("separated")
}},destruct:function(){self.EventFeeManager=null
},add_fee:function(){var oSelf=self.EventFeeManager;
$("#id_fee"+oSelf.iFeeCount+"_label_en").parent().show();
$("#id_fee"+oSelf.iFeeCount+"_label_de").parent().show();
$("#id_fee"+oSelf.iFeeCount+"_amount").parent().show();
oSelf.iFeeCount++;
if(oSelf.iFeeCount>1){$("#fee_remover").css("display","inline");
$("#fee_adder").addClass("separated")
}if(oSelf.iFeeCount>=6){$("#fee_adder").hide()
}return false
},remove_fee:function(){var oSelf=self.EventFeeManager;
oSelf.iFeeCount--;
$("#id_fee"+oSelf.iFeeCount+"_label_en").val("").parent().hide().find("p.error").remove();
$("#id_fee"+oSelf.iFeeCount+"_label_de").val("").parent().hide().find("p.error").remove();
$("#id_fee"+oSelf.iFeeCount+"_amount").val("").parent().hide().find("p.error").remove();
if(oSelf.iFeeCount<=1){$("#fee_remover").hide();
$("#fee_adder").removeClass("separated")
}if(oSelf.iFeeCount<6){$("#fee_adder").css("display","inline")
}return false
}};
self.JobOfferManager={init:function(){var oSelf=self.JobOfferManager;
$("#link_enter_institution").click(function(){oSelf.manageBlocks("enter institutions manually");
return false
});
$("#link_select_institution").click(function(){oSelf.manageBlocks("select institution");
return false
});
$("#id_contact_person_ind_0").change(function(){oSelf.manageBlocks("contact person myself");
return false
});
$("#id_contact_person_ind_1").change(function(){oSelf.manageBlocks("enter contact person name");
return false
});
if($("#id_offering_institution_title").val()!=""){oSelf.manageBlocks("enter institutions manually")
}else{oSelf.manageBlocks("select institution")
}if($("input[name='contact_person_ind']:checked").val()==1){oSelf.manageBlocks("enter contact person name")
}else{oSelf.manageBlocks("contact person myself")
}},manageBlocks:function(sCase){switch(sCase){case"select institution":$("#block_institution_title_input").addClass("hidden");
$("#id_offering_institution_title").val("");
$("#block_institution_select").removeClass("hidden to_hide");
break;
case"enter institutions manually":$("#block_institution_select").addClass("hidden");
$("#id_offering_institution").val("");
$("#id_offering_institution_text").val("");
$("#block_institution_title_input").removeClass("hidden to_hide");
break;
case"contact person myself":$("#block_contact_input").addClass("hidden");
$("#id_contact_person_name").val("");
break;
case"enter contact person name":$("#block_contact_input").removeClass("hidden to_hide");
break;
default:break
}}};
$(document).ready(function(){self.ProfileManager.init()
});
$(window).unload(function(){self.ProfileManager.destruct();
self.ContactPrepopulationManager.destruct()
})
}(jQuery));
(function($,undefined){self.FormsetsManager={init:function(){var oSelf=self.FormsetsManager;
$('<div class="buttonHolder"><input type="button" class="add-formset primaryAction" value="'+gettext("Add another entry")+'" /></div>').insertAfter(".formset-form:last");
$("input:hidden.form_hidden[id$=TOTAL_FORMS]").each(function(){var totalField=this;
var $totalField=$(this);
var $fieldset=$totalField.nextAll(".formset-form");
$fieldset.find("input:checkbox[id$=DELETE]").parent().each(function(){var $deleteLink=$('<a href="#delete_event_time" class="deletebutton"><span>'+gettext("Delete")+"</span></a>");
$(this).hide();
$(this).before($deleteLink);
$deleteLink.click(function(){if(parseInt($(totalField).val())>1){$(this).closest(".formset-form").remove();
$totalField.val(parseInt($(totalField).val())-1);
$fieldset.find(".formset-form").each(function(index,form){oSelf.set_index_for_fields($(form),index)
})
}return false
})
});
$fieldset.parent().find("input:button.add-formset").click(function(e){var $newForm=$totalField.nextAll(".formset-form").filter(":last").clone(true);
oSelf.set_index_for_fields($newForm,parseInt($totalField.val(),10));
$newForm.insertAfter(".formset-form:last",this);
$totalField.val(parseInt($totalField.val(),10)+1)
})
})
},set_index_for_fields:function($formset_form,index){$formset_form.find(":input").each(function(){var $field=$(this);
if($field.attr("id")){$field.attr("id",$field.attr("id").replace(/-(\d+)-/,"-"+index+"-"))
}if($field.attr("name")){$field.attr("name",$field.attr("name").replace(/-(\d+)-/,"-"+index+"-"))
}});
$formset_form.find("label").each(function(){var $field=$(this);
if($field.attr("for")){$field.attr("for",$field.attr("for").replace(/-(\d+)-/,"-"+index+"-"))
}})
},destruct:function(){self.FormsetsManager=null
}};
$(document).ready(function(){self.FormsetsManager.init()
});
$(window).unload(function(){self.FormsetsManager.destruct()
})
}(jQuery));
self.MutipleSelectAutoCompleteManager={init:function(){$("select[multiple]:visible").each(function(){var valuesList=[];
var valuesIDsMap={};
$("option",this).each(function(){if(!$(this).attr("value")){return
}valuesList.push($(this).text());
valuesIDsMap[$(this).text()]=$(this).attr("value")
});
var selectField=this;
var selectFieldID=$(this).attr("id");
var selectFieldName=$(this).attr("name");
var inputFieldID=selectFieldID+"_autocomplete";
var selectedListID=selectFieldID+"_selected";
$(this).wrap('<div class="autocomplete_container"></div>');
$(this).after('<ul id="'+selectedListID+'" class="autocomplete_selected"/><input type="text" id="'+inputFieldID+'" />');
var $input=$("#"+inputFieldID);
$input.autocomplete(valuesList,{selectFirst:false,highlight:false,max:20,minChars:1,mustMatch:1,matchContains:true});
$input.result(function(event,data,formatted){var id=valuesIDsMap[data];
if(id){$("#"+selectedListID).append("<li>"+data+'<a href="#" class="closebutton" /></li>');
$("option[value="+id+"]",selectField).attr("selected",true);
$(this).val("");
$("#"+selectedListID+" li:last").data("id",id);
$("#"+inputFieldID).focus();
event.preventDefault()
}});
$("option[selected]",this).each(function(){$("#"+selectedListID).append("<li>"+$(this).text()+'<a href="#" class="closebutton" /></li>');
$("#"+selectedListID+" li:last").data("id",$(this).attr("value"))
});
$(this).hide();
$("#"+selectedListID+" a.closebutton").live("click",function(event){var li=$(this).parents("li:first");
var id=li.data("id");
li.remove();
$("option[value="+id+"]",selectField).attr("selected",false);
event.preventDefault()
})
})
},destruct:function(){self.MutipleSelectAutoCompleteManager=null
}};
$(document).ready(function(){self.MutipleSelectAutoCompleteManager.init()
});
$(window).unload(function(){self.MutipleSelectAutoCompleteManager.destruct()
});