/**
 * Handles the functionality of the media upload page.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function MediaUpload($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$link = $('.link_to_media_file', me.$main);
        me.$upload = $('.upload_media_file', me.$main);
        me.$link_switch = $('.link_to_media_file_switcher', me.$main);
        me.$upload_switch = $('.upload_media_file_switcher', me.$main);
        me.$objects = $('object, .media-file', me.$main);
        
        me.$link_switch.click(function() {me.toggle(me.$link);});
        me.$upload_switch.click(function() {me.toggle(me.$upload);});
        me.$current_section = me.$upload;
        
        var hash = document.location.hash;
        if (hash == "#link_to_media_file" || (!hash && $("#id_external_url").val())) {
            me.$current_section = me.$link;
        }
        
        
        $('<input type="button" class="button" value="' + trans['Cancel'] + '">').click(function () {
            var path = location.href.split('/');
            var old = parseInt(path[path.length-2]);
            if (old) redirect("../manage/");
            else redirect("../../manage/");
        }).prependTo(
            $(".prepend-cancel").parent()
        );
        
        
        me.$objects.each(function() {
            
            var $object = $(this);
            $object.attr('data-width', $object.width());
            $object.attr('data-height', $object.height());
            $object.css('width', '100%');
        });
        
        $(window).resize(function() {me.onResize();});
        
        me.onResize();
    }
    
    MediaUpload.prototype.toggle = function($section) {
        
        var me = this;        
        
        me.$current_section = $section;
        
        me.$link.css('display', 'none');
        me.$upload.css('display', 'none');
        
        $section.css('display', 'block');
    }
    
    MediaUpload.prototype.onResize = function() {
        
        var me = this;
        
        me.$link.css('display', 'block');
        me.$upload.css('display', 'block');
        
        me.$objects.each(function() {
            
            var $object = $(this);
            
            var width = $object.width();
            var height = $object.attr('data-height') * width / $object.attr('data-width');
            
            $object.height(height);
        });
        
        me.toggle(me.$current_section);
    }
    
    $('.media-upload').each(function() {
        new MediaUpload($(this)); 
    });
    
    
})();