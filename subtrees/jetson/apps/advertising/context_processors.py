def source_features(request):
    import re
    bot_names = re.compile(
        r'\b(googlebot|slurp|twiceler|msnbot|kaloogabot|yodaobot|baiduspider|speedy spider|dotbot)\b',
        re.IGNORECASE
    )
    features = {}
    if request.META.has_key('REMOTE_ADDR'):
        features['from_ip'] = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    features['is_crawler'] = bool(bot_names.match(user_agent))
    return features
