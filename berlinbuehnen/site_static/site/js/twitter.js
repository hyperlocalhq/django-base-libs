$(document).ready(function() {
	var $tweets = $('#twitter-tweets');
	var twitter_username = $tweets.data('twitter-username');
	$.getJSON('/tweets/' + twitter_username + '/', function(data) {
        
        for (var i=0, length = data.length; i<length; i++) {
            
            var tweet = data[i];
            
            var  html = [];
            html.push('<div class="col-xs-12 col-sm-6 col-md-4 '+((i == 2) ? 'hidden-sm' : '')+'">');
            html.push('<div class="twitter-tweet">');
            html.push('<p>'+tweet.text_urlized_atlinked+'</p>');
            html.push('<p class="twitter-tweet-time"><a href="http://twitter.com/#!/'+tweet.user.screen_name+'/status/'+tweet.id_str+'" target="_blank">'+tweet.created_timesince+'</a></p>');
            html.push('</div>');
            html.push('</div>');
            
            $tweets.append(html.join(''));
            
            if (i == 2) break;
        }
        
	});
});

