$(document).ready(function() {
    var $tweets = $('#tweets');
    var twitter_username = $tweets.data('twitter-username');
    $.getJSON('/tweets/' + twitter_username + '/', function(data) {
        for (num=data.length-1; num>=0; num--) {
            tweet = data[num];
            $tweets.prepend('<li class="style-' + (num % 3 + 1) + '"><div class=" text">' + tweet.text_urlized_atlinked + '</div><div class="created_at"><a href="http://twitter.com/#!/' + tweet.user.screen_name + '/status/' + tweet.id_str + '">' + tweet.created_timesince + '</a></div></li>');
        }
    });
});