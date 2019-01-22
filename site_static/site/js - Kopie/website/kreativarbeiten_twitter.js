$(document).ready(function() {
    $.getJSON('/' + settings.LANGUAGE_CODE + '/kreativarbeiten/tweets/', function(data) {
        for (num=data.length-1; num>=0; num--) {
            tweet = data[num];
            $('#tweets').prepend('<li class="style-' + (num % 3 + 1) + '"><div class=" text">' + tweet.text_urlized_atlinked + '</div><div class="created_at"><a href="http://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id + '">' + tweet.created_timesince + '</a></div></li>');
        }
    });
});