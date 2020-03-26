"""
    This is a configuration file you can store here all the variables.
"""
# Edit these Fields
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
ENVNAME = ""
WEBHOOK_URL = ""


# Do not edit these Fields unless and until API version change.
BOT_ACCOUNT_ID = str(ACCESS_TOKEN.split("-")[0])
DM_URL = "https://api.twitter.com/1.1/direct_messages/events/new.json"
TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"
CREATE_WEBHOOK = "https://api.twitter.com/1.1/account_activity/all/{}/webhooks.json"
SUBSCRIBE_WEBHOOK = "https://api.twitter.com/1.1/account_activity/all/{}/subscriptions.json"
RETRIEVE_WEBHOOK = "https://api.twitter.com/1.1/account_activity/all/webhooks.json"
DELETE_WEBHOOK = "https://api.twitter.com/1.1/account_activity/all/{}/webhooks/{}.json"
