import requests
from agent import Agent
from json import loads
from threading import Event, Thread
from queue import Queue, Empty
from time import sleep, time
from tweepy import API, OAuthHandler
# from tweepy.streaming import Stream
from dotenv import load_dotenv
from os import environ

load_dotenv()

# API keys for accessing Twitter APIs.
API_KEY = environ["API_KEY"]
API_KEY_SECRET = environ["API_KEY_SECRET"]
BEARER_TOKEN = environ["BEARER_TOKEN"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]


# The user ID of @elonmusk.
MUSK_USER_ID = "44196397"

# The user ID of @giftedsynth.
SYNTH_USER_ID = "1287364596572082179"

# The URL pattern for links to tweets.
TWEET_URL = "https://x.com/%s/status/%s"

# Some emoji.
EMOJI_THUMBS_UP = "\U0001f44d"
EMOJI_THUMBS_DOWN = "\U0001f44e"
EMOJI_SHRUG = "¯\\_(\u30c4)_/¯"

# The maximum number of characters in a tweet.
MAX_TWEET_SIZE = 140

# The number of worker threads processing tweets.
NUM_THREADS = 100

# The maximum time in seconds that workers wait for a new task on the queue.
QUEUE_TIMEOUT_S = 5 * 60

# The number of retries to attempt when an error occurs.
API_RETRY_COUNT = 60

# The number of seconds to wait between retries.
API_RETRY_DELAY_S = 1

# The HTTP status codes for which to retry.
API_RETRY_ERRORS = [400, 401, 500, 502, 503, 504]


class Twitter:
    """A helper for talking to Twitter APIs."""

    def __init__(self):
        self.twitter_auth = OAuthHandler(API_KEY, API_KEY_SECRET)
        self.twitter_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.twitter_api = API(auth=self.twitter_auth, wait_on_rate_limit=True)
        self.streaming_active = False

    def stream_mentions(self):
        """Streams mentions of the authenticated user."""
        
        self.streaming_active = True
        url = "https://api.twitter.com/2/tweets/search/stream"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        # Add rules to filter mentions
        rules_url = f"{url}/rules"
        rules = [{"value": "@giftedsynth"}]  # Replace with your username
        requests.post(rules_url, headers=headers, json={"add": rules})

        # Start streaming
        print("Starting to stream mentions...")
        response = requests.get(url, headers=headers, stream=True)
        for line in response.iter_lines():
            if not self.streaming_active:
                break
            if line:
                tweet = line.decode("utf-8")
                self.handle_mention(loads(tweet))
                print("Mention received:", tweet)

    def handle_mention(self, tweet):
        """Handles a mention by responding to it."""
        try:
            if "data" not in tweet: 
                raise KeyError("Missing 'data' key in tweet response.")
            tweet_id = tweet["data"]["id"]
            username = tweet["includes"]["users"][0]["username"]
            request_txt = tweet["data"]["text"]
            print(f"Mention received from @{username}: {tweet['data']['text']}")

            # Respond to the mention with an llvm agent
            agent_response = Agent().chat(request_txt).answer
            if not agent_response:
                reply_text = f"Thanks for the mention, @{username}, however I have no further comments!" 
            reply_text = agent_response
            self.reply_to_tweet(tweet_id, reply_text)
        except KeyError as e:
            print(f"Malformed tweet: {tweet}, error: {e}")
    
    def strop_stream(self):
        """Stops the streaming of mentions."""
        self.streaming_active = False
        print("Stopped streaming mentions.")
        
    def reply_to_tweet(self, tweet_id, reply_text):
        """Replies to a tweet."""
        try:
            self.twitter_api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True,
            )
            print(f"Replied to tweet ID {tweet_id}: {reply_text}")
        except Exception as e:
            print(f"Failed to reply: {e}")

    def tweet(self, tweet):
        """Posts a tweet listing the target, and quote of the original tweet.
        """
        pass

    def make_tweet_text(self, companies, link):
        """Generates the text for a tweet."""
        pass
       

    def get_sentiment_emoji(self, sentiment):
        """Returns the emoji matching the sentiment."""

        if not sentiment:
            return EMOJI_SHRUG

        if sentiment > 0:
            return EMOJI_THUMBS_UP

        if sentiment < 0:
            return EMOJI_THUMBS_DOWN

        self.logs.warn("Unknown sentiment: %s" % sentiment)
        return EMOJI_SHRUG