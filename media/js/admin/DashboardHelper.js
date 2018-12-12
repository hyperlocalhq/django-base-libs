(function($, undefined) {
    var location_hash = window.location.hash;
    
    $(document).ready(function() {
        $(window).bind('hashchange', function(e) {
            $('#link-to-' + window.location.hash.substring(6)).not('.active').find('a').click();
        });
        
        window.setInterval(function() {
            if (window.location.hash != location_hash) {
                $(window).trigger('hashchange');
                location_hash = window.location.hash;
            }
        }, 500);
        
        
        if ($('#content-main .app-group').length == 0) return;
        var ul = $('#content-main').prepend('<ul id="appgroup-nav"></ul>');
        $('#content-main .app-group').each(function() {
            $('#appgroup-nav').append('<li id="link-to-' + $(this).attr('id') + '"><a href="#' + $(this).attr('id') + '">' + $('h4',this).text() + '</a></li>');
        });
        $('#content-main .app-group').hide();
        $('#content-main .app-group h4').hide();
        $('#appgroup-nav li a').click(function() {
            $('#content-main .app-group').hide();
            $('#' + $(this).attr('href').substring(1)).show();
            $('#appgroup-nav li.active').removeClass('active');
            $(this).parent('li').addClass('active');
            window.location.hash = 'show-' + $(this).attr('href').substring(1);
            return false;
        });
        
        var matches;
        if (window.location.hash && (matches = window.location.hash.match(/^#show\-(.*)$/))) {
            $('#link-to-' + matches[1] + ' a').trigger('click');
        } else {
            $('#appgroup-nav a:first').trigger('click');
        }
        
    });
}(django.jQuery));
