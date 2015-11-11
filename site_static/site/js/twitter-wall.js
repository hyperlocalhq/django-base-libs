/**
 * Provides the functionality for the twitter wall.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function TwitterWall($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$tweets = $('.tweet', me.$main);
        me.username = me.$main.attr('data-username');
        
        $.getJSON('/tweets/' + me.username + '/', function(data) {
        
            for (var i=0, length = data.length; i<length; i++) {
                
                if (i >= me.$tweets.length) {
                    break;
                }
                
                var tweet = data[i];
                
                var  html = [];
                html.push('<p>'+tweet.text_urlized_atlinked+'</p>');
                html.push('<p class="tweet-time"><a href="http://twitter.com/#!/'+tweet.user.screen_name+'/status/'+tweet.id_str+'" target="_blank">'+tweet.created_timesince+'</a></p>');
                
                $(me.$tweets.get(i)).html(html.join('\n'));
            }
        
            $('a', me.$main).attr('target', '_blank');
        });
        
    }
    
    $('.twitter-wall').each(function() {
        new TwitterWall($(this)); 
    });
    
    
})();