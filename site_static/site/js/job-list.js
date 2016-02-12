/**
 * Provides functionality and styles for the job list.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function JobList($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$elements = $('.col-xs-12', $main);
        me.$body = $('body');
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt(200);});
        me.styleIt();
    }
    
    JobList.prototype.styleIt = function(delay) {
     
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $content = $('.content', $element);
            var $website = $('.website', $element);
            
            if ($('.bubble', $content).length) {
                $element.addClass('has-bubble');   
            }
            
            if ($website.length) {
            
                var $p = $('p', $content);
                var $ul = $('ul', $content);
                
                var margin = 5;
                
                $website.css('top', ($p.position().top + $p.height()) + margin + 'px');
                $p.css('margin-bottom', ($website.height() + margin) + 'px');
                $ul.css('margin-top', ($website.height() + margin) + 'px');
                
            }
            
        });
    }
    
    $('.job-list').each(function() {
        new JobList($(this)); 
    });    
    
})();