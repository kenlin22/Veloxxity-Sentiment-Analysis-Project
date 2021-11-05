import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import plotly.graph_objects as go

from utils import (
    youtube_authenticate,  
    get_video_details,
    print_video_infos,
    search
)


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
        else :
            return 'neutral'

  
    def get_tweets(self, query, count, u):
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count, until = u)
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

def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()

def main():
    # create TwitterClient object 
    tweetapi = TwitterClient()


    # calling function to get tweets
    tweets = tweetapi.get_tweets(query = 'South China Sea', count = 200, u='2021-11-01')
  
    # put positive tweets, negative tweets, and neutral in lists
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    # youtube analysis
    # authenticate to YouTube API
    input = "South China Sea"
    youtube = youtube_authenticate()
    # search for the query 'python' and retrieve 2 items only
    response = search(youtube, q=input, maxResults=5)
    items = response.get("items")
    pnn = [0,0,0]
    time = []
    for item in items:
        # get the video ID
        video_id = item["id"]["videoId"]
        params = {
            'videoId': video_id, 
            'maxResults': 2,
            'order': 'relevance', # default is 'time' (newest)
        }
        # get the video details
        video_response = get_video_details(youtube, id=video_id)
        # print the video details
        print_video_infos(video_response)
        print(video_id)
        # show comments
        n_pages = 2
        for i in range(n_pages):
            response = get_comments(youtube, **params)
            items = response.get("items")
            if not items:
                break
            
            #pnn = [0,0,0]

            for item in items:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                updated_at = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                comment_id = item["snippet"]["topLevelComment"]["id"]
                print(f"""\
                Comment: {comment}
                Likes: {like_count}
                Updated At: {updated_at}
                ==================================\
                """)
                text = TextBlob(comment)
                print(text.sentiment)
                print(text.sentiment.polarity)
                time.append(updated_at)
                if text.polarity < 0:
                    polarity = "Negative"
                    pnn[1] += 1
                elif text.polarity > 0:
                    polarity = "Positive"
                    pnn[0] += 1
                else:
                    polarity = "Neutral"
                    pnn[2] += 1

            if "nextPageToken" in response:
            # if there is a next page
            # add next page token to the params we pass to the function
                params["pageToken"] =  response["nextPageToken"]
            else:
            # must be end of comments!!!!
                break

    posPosts = pnn[0] + len(ptweets)
    negPosts = pnn[1] + len(ntweets)
    neuPosts = pnn[2] + len(neutweets)
    #dislaying them on a plotly pie chart
    pChart = go.Figure(data=[go.Pie(labels=['Positive Posts','Negative Posts', 'Neutral'], values=[posPosts, negPosts, neuPosts])])
    pChart.update_layout(title_text="Proportion of Positive and Negative Posts on the South China Sea")
    pChart.show()

if __name__ == "__main__": main()