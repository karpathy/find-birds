# find-birds

![user interface](https://raw.github.com/karpathy/find-birds/master/ui.png)

The goal is to find people on Twitter ("birds", haha) who you should follow.

The source of signal is that the people you follow follow other people you probably should follow but so far do not.

## installation

The code base uses tweepy library to interact with the Twitter API:

`pip install -r requirements.txt`

You will have to set up oauth access to Twitter API. Follow [this great tutorial](https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04) to set that up. You'll then want to enter your consumer key, consumer secret, access token, access token secret as 4 lines in a file `twitter.txt` in the root directory of this project.


## usage

The typical usage for me (username "karpathy") looks as follows:

1. Run `fetch.py karpathy --depth 1`, which fetches information about who I follow, and who everyone I follow follows. Everything is saved to a super lightweight "database" as pickle files. This part can take many days because the Twitter API access is heavily rate limited. For example, I follow about 400 people and it took about 2 weeks to download all of the information. Therefore, I'd run this script in a screen session and come back later.
2. Run `report.py --from-user karpathy`, which finds the most commonly occurring people and then renders the results into an `html` page (by default `report.html`), for pretty consumption. You'll be able to use this script before the `fetch.py` script above fully finishes to see preliminary results if you like.

These two scripts have some more bells and whistles - don't be afraid to read & modify the code, it's relatively short.

## ugh, so much work

If we are very good friends I'd be happy to run all of this code for you on a first-come-first-serve basis, get in touch.


# license
MIT
