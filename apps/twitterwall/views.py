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
        ).order_by("-creation_date")[5:50]
    tweets_from_search = Tweet.objects.filter(
        from_search=True,
        status="published",
        sites=current_site,
        ).order_by("-creation_date")[5:50]
    return render(request, "twitterwall/index.html", locals())
    
def load_tweets(request):
    params = {
        'status': "published",
        'sites': Site.objects.get_current(),
        }
    if request.REQUEST.get('by_user', False):
        params['by_user'] = True
    if request.REQUEST.get('from_search', False):
        params['from_search'] = True
    since_id = request.REQUEST.get('since_id', "")
    if since_id:
        try:
            since = Tweet.objects.get(id=since_id)
        except:
            pass
        else:
            params['creation_date__gt'] = since.creation_date
    before_id = request.REQUEST.get('before_id', "")
    if before_id:
        try:
            before = Tweet.objects.get(id=before_id)
        except:
            pass
        else:
            params['creation_date__lt'] = before.creation_date
    try:
        count = int(request.REQUEST.get('count', "0"))
    except:
        count = 0
    
    tweets = Tweet.objects.filter(**params).order_by("-creation_date")
    if count:
        tweets = tweets[:count]
        
    return render(request, "twitterwall/tweets.html", {'tweets': tweets})
