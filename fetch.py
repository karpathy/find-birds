import os
import time
import logging
import argparse

import tweepy

from common import authenticate, api_iter, LOLDB

# -----------------------------------------------------------------------------
parser = argparse.ArgumentParser()
# required arguments
parser.add_argument('user', type=str, help='The user to get information about')
# options
parser.add_argument('-d', '--depth', type=int, default=0, help='Fetch just the single user, or also all of their friends recurisvely.')
parser.add_argument('-n', '--max-friends', type=int, default=1000, help='Maximum number of latest friends we fetch per any user.')
parser.add_argument('-m', '--max-tweets', type=int, default=200, help='Maximum number of latest tweets we fetch per any user.')
parser.add_argument('-x', '--cache', type=int, default=1, help='If we already have the user in database, skip? 1/0')
parser.add_argument('-i', '--db-dir', type=str, default="db", help='Folder where we store all of the information')
args = parser.parse_args()
# -----------------------------------------------------------------------------

assert args.depth in [0,1], "for now depth should be either 0 or 1. Anything else is likely to take way too long."

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = authenticate()
db = LOLDB(args.db_dir)

def download_user(user):
    if args.cache and user in db:
        return # nothing to be done
    # hit the Twitter API to get the information
    friends = api_iter(api.friends, user, args.max_friends)
    tweets = api_iter(api.user_timeline, user, args.max_tweets)
    blob = { 'time':time.time(), 'friends': friends, 'tweets': tweets }
    # back the information up in database for later
    db[user] = blob

logging.info("fetching user %s" % (args.user, ))
download_user(args.user)
b = db[args.user]
if args.depth == 1:
    for i,f in enumerate(b['friends']):
        logging.info("%d/%d fetching a friend %s" % (i+1, len(b['friends']), f.screen_name))
        download_user(f.screen_name)
