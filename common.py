import os
import time
import tweepy
import pickle

def authenticate():
    """
    Reads keys from a file, it's glorious.
    """
    # extract keys
    with open('twitter.txt', 'r') as f:
        keys = f.read().split()
    assert len(keys) == 4, "sorry to interupt, but there should be 4 lines in this file."
    # authenticate
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)
    return api

def api_iter(api_func, user, limit):
    """
    Iterates API while error fetching correct. can't believe I have to do this manually and that
    it is not supported by tweepy. It claims to have it, but when I tried it crashed with an error.
    """
    if limit == 0: 
        return [] # fast escape when applicable
    
    it = tweepy.Cursor(api_func, id=user).items(limit)
    elements = []
    while True:
        try:
            f = it.next()
            elements.append(f)
        except tweepy.TweepError:
            print("got a tweepy error. collected %d/%d so far. waiting 15 minutes..." % (len(elements), limit))
            time.sleep(60 * 15 + 10)
            continue
        except StopIteration:
            break

    return elements

class LOLDB:
    """
    This class is a "database". haha
    """
    def __init__(self, dbpath):
        self.dbpath = dbpath
        if not os.path.isdir(dbpath):
            print("creating directory", dbpath)
            os.makedirs(dbpath)
    
    def _key_to_path(self, key):
        return os.path.join(self.dbpath, key+'.p')
    
    def __setitem__(self, key, item):
        with open(self._key_to_path(key), 'wb') as fp:
            pickle.dump(item, fp)

    def __getitem__(self, key):
        with open(self._key_to_path(key), 'rb') as fp:
            item = pickle.load(fp)
        return item
    
    def __contains__(self, key):
        pp = self._key_to_path(key)
        return os.path.isfile(pp)
    