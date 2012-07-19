# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.db import models

Tweet = models.get_model("twitterwall", "Tweet")
Site = models.get_model("sites", "Site")

def twitterwall(request):
    current_site = Site.objects.get_current()
    selected_user_tweets = Tweet.objects.filter(
        by_user=True,
        status="published",
        sites=current_site,
        )[:50]
    tweets_from_search = Tweet.objects.filter(
        from_search=True,
        status="published",
        sites=current_site,
        )[:50]
    return render(request, "twitterwall/index.html", locals())
