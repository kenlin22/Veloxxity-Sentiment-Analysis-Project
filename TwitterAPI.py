import pickle
import pandas as pd
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import plotly.graph_objects as go
  
class TwitterClient(object):
    def __init__(self):
        # attempt authentication
        try:

            apiKey = '1oILHQ7zAdvdu1XaJoAZkvUY7'
            apiSecret = 'j449aCLnyKJhqTU84PB2AarTdAw9CWhLcUc0iBMZjm2veKfk8o'

            accessToken = '1214015320395960320-CQBr65Cno6XjDL2wlnSThYx7R516BZ'
            accessSecret = 'I63R3znoVQLPEM79i1laSJzjbmLOKLlKP97hN0VvvzLkI'

            # create OAuthHandler object
            self.auth = OAuthHandler(apiKey, apiSecret)
            # set access token and secret
            self.auth.set_access_token(accessToken , accessSecret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
   
    def getSentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
  
    def get_tweets(self, query, count = 10):
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q = query, count = count)
  
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
  
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.getSentiment(tweet.text)
  
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.TweepError as e:
            print("Error : " + str(e))
  
def main():
    # create TwitterClient object 
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'South China Sea', count = 200)
  
    # put positive tweets and negative tweets in lists
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    #dislaying them on a plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=['Positive Tweets','Negative Tweets'], values=[len(ptweets), len(ntweets)])])
    fig.update_layout(title_text="Proportion of Positive and Negative Tweets on the South China Sea")
    fig.show()
    df = pd.DataFrame(tweets)
    df.to_csv('new_file.csv')
    print(df.shape)
    print(df)

if __name__ == "__main__": main()