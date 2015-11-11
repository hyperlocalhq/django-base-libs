$(document).ready(function() {
    $.getJSON('/' + settings.lang + '/kreativarbeiten/newsfeed/', function(data) {
        for (num=data.length-1; num>=0; num--) {
            article = data[num];
            //$('#newsfeed').prepend('<li class="style-' + (num % 3 + 1) + '"><div class="text"><a href="' + article.link + '">' + article.title + '</a></div><div class="created_at">' + article.pubDate + '</div><div>' +  article.description + '</div></li>');
            $('#newsfeed').prepend('<li class="style-' + (num % 3 + 1) + '"><div class="text"><a href="' + article.link + '">' + article.title + '</a></div><div class="created_at">' + article.pubDate + '</div></li>');
        }
    });
});