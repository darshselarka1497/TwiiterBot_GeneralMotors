import tweepy
from datetime import datetime
from secret import consumer_key, consumer_secret, access_token, access_secret, handle
from fetch import make_query,request

# get authentication info
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# log into the API
api = tweepy.API(auth)
print('[{}] Logged into Twitter API as @{}\n-----------'.format(
    datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
    handle
))

# string array of words that will trigger the on_status function
trigger_words = [
    '@' + handle # respond to @mentions
]

# override the default listener to add code to on_status
class MyStreamListener(tweepy.StreamListener):

    # listener for tweets
    # -------------------
    # this function will be called any time a tweet comes in
    # that contains words from the array created above
    def on_status(self, status):

        # log the incoming tweet
        print('[{}] Received: "{}" from @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.text,
            status.author.screen_name
        ))

        # get the text from the tweet mentioning the bot.
        # for this bot, we won't need this since it doesn't process the tweet.
        # but if your bot does, then you'll want to use this

        message = status.text #converts tweet to string

        m = message.replace('@'+handle, "") #removes handle along with @ character to process it further
        #print(message)

        # after processing the input, you can build your output
        # into this variable. again, since we're just reply "No.",
        # we'll just set it as that.

        url = make_query(m) #passes the string from the text to the make_query function as title and stores it in url variable.

        response = request(url) #after decoding the url, response variable stores the plot in string format.

        #print(response)
        print(status.author.screen_name)
        # respond to the tweet
        api.update_status(
            status="Hello "+"@"+status.author.screen_name+','+'\n\n'+"Plot:  "+response, #the response to the tweet (title of the movie). Will tweet the plot of the movie/tv show.
            in_reply_to_status_id=status.id
        )

        print('[{}] Responded to @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.author.screen_name
        ))

# create a stream to receive tweets
try:
    streamListener = MyStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(track=trigger_words)
except KeyboardInterrupt:
    print('\nGoodbye')