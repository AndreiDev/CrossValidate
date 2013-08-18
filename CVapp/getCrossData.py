from twython import Twython, TwythonError, TwythonRateLimitError
import time

def twitter_retry(func):
    howmany = 5 # maximum retires
    simple_timeout = 5 # seconds
    rate_limit_timeout = 300 # seconds
    def tryIt(*fargs, **fkwargs):
        for _ in xrange(howmany):
            try: return func(*fargs, **fkwargs)
            except (TwythonError, TwythonRateLimitError, Exception) as e:
                if "Rate limit" in str(e): 
                    print e
                    print fkwargs['limit_rate_string']
                    print 'sleeping for ' + str(rate_limit_timeout) + ' seconds'
                    time.sleep(rate_limit_timeout)
                else:
                    print e
                    print 'sleeping for ' + str(simple_timeout) + ' seconds'
                    time.sleep(simple_timeout)
    return tryIt  
    
@twitter_retry
def twitterGetFollowersIds(twitter,**params):
    return twitter.get_followers_ids(**params)

@twitter_retry
def twitterGetFriendsIds(twitter,**params):
    return twitter.get_friends_ids(**params)    
    
@twitter_retry
def twitterLookupUser(twitter,**params):
    return twitter.lookup_user(**params)

def getFollowersIds(twitter,subjectScreenName):
    print '*** getting the followers of ' + subjectScreenName
    ii = 1
    print 'page ' + str(ii) 
    followersIds_raw = twitterGetFollowersIds(twitter,limit_rate_string='xxx',screen_name=subjectScreenName,cursor=-1,count=5000)
    followersIds_next_cursor = followersIds_raw['next_cursor']
    followersIds_ids = followersIds_raw['ids']
    while followersIds_next_cursor:
        ii += 1
        print 'page ' + str(ii) 
        followersIds_raw = twitterGetFollowersIds(twitter,limit_rate_string='xxx',screen_name=subjectScreenName,cursor=followersIds_next_cursor,count=5000)
        followersIds_next_cursor = followersIds_raw['next_cursor']
        followersIds_ids = followersIds_ids + followersIds_raw['ids']    
    return followersIds_ids
    
def getFriendsIds(twitter,subjectScreenName):
    print '*** getting the friends of ' + subjectScreenName
    ii = 1
    print 'page ' + str(ii) 
    friendsIds_raw = twitterGetFriendsIds(twitter,screen_name=subjectScreenName,cursor=-1,count=5000)
    friendsIds_next_cursor = friendsIds_raw['next_cursor']
    friendsIds_ids = friendsIds_raw['ids']
    while friendsIds_next_cursor:
        ii += 1
        print 'page ' + str(ii)     
        friendsIds_raw = twitterGetFriendsIds(twitter,screen_name=subjectScreenName,cursor=friendsIds_next_cursor,count=5000)
        friendsIds_next_cursor = friendsIds_raw['next_cursor']
        friendsIds_ids = friendsIds_ids + friendsIds_raw['ids']    
    return friendsIds_ids    


    