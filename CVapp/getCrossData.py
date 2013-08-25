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
                    #print fkwargs['limit_rate_string']
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
def twitterGetFollowingIds(twitter,**params):
    return twitter.get_friends_ids(**params)    
    
@twitter_retry
def twitterLookupUser(twitter,**params):
    return twitter.lookup_user(**params)

@twitter_retry
def twitterCreateFriendship(twitter,**params):
    return twitter.create_friendship(**params)

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
    
def getFollowingIds(twitter,subjectScreenName):
    print '*** getting the following of ' + subjectScreenName
    ii = 1
    print 'page ' + str(ii) 
    followingIds_raw = twitterGetFollowingIds(twitter,screen_name=subjectScreenName,cursor=-1,count=5000)
    followingIds_next_cursor = followingIds_raw['next_cursor']
    followingIds_ids = followingIds_raw['ids']
    while followingIds_next_cursor:
        ii += 1
        print 'page ' + str(ii)     
        followingIds_raw = twitterGetFollowingIds(twitter,screen_name=subjectScreenName,cursor=followingIds_next_cursor,count=5000)
        followingIds_next_cursor = followingIds_raw['next_cursor']
        followingIds_ids = followingIds_ids + followingIds_raw['ids']    
    return followingIds_ids    

def followUser(twitter, subjectName):
    print '*** following ' + subjectName
    return twitterCreateFriendship(twitter,screen_name=subjectName)
    
    