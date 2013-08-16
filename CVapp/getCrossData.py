def getCrossData(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    from twython import Twython, TwythonError, TwythonRateLimitError
    
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    res = twitter.lookup_user(user_id='348664405',include_entities='false')
    return res