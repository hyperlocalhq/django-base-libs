$(document).ready(function() {
	var $tweets = $('#tweets');
	var twitter_username = $tweets.data('twitter-username');
	$.getJSON('/tweets/' + twitter_username + '/', function(data) {
		for (num=data.length-1; num>=0; num--) {
			tweet = data[num];
			if (num==0) {
				$tweets.prepend('<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 hidden-md style-' + (num % 3 + 1) + '"><div class="tweet"><p><small>' + tweet.text_urlized_atlinked + '</small></p><p class="created_at"><a href="http://twitter.com/#!/' + tweet.user.screen_name + '/status/' + tweet.id_str + '">' + tweet.created_timesince + '</a></p></div></div>');
			} else {
				$tweets.prepend('<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 style-' + (num % 3 + 1) + '"><div class="tweet"><p><small>' + tweet.text_urlized_atlinked + '</small></p><p class="created_at"><a href="http://twitter.com/#!/' + tweet.user.screen_name + '/status/' + tweet.id_str + '">' + tweet.created_timesince + '</a></p></div></div>');
			}
		}
	});
});

