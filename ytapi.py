from utils import (
    youtube_authenticate,  
    get_video_details,
    print_video_infos,
    get_video_likes,
    get_video_dislikes,
    search
)
import csv
import tweepy
from tweepy import OAuthHandler

from textblob import TextBlob
import plotly.graph_objects as go

def get_comments(youtube, **kwargs):
    
        return youtube.commentThreads().list(
            part="snippet",
            **kwargs
        ).execute()
    

if __name__ == "__main__":
    # authenticate to YouTube API
    input = input("Enter your topic: ")
    # videocount = input("How many videos to analyse")
    youtube = youtube_authenticate()
    # csv file 
    # c = csv.writer(open("youtube.csv", "w"))
    # search for the query 'python' and retrieve 2 items only
    response = search(youtube, q=input, maxResults=5)
    items = response.get("items")
    pnn = [0,0,0]
    positivewords = []
    negativewords = []
    likes = 0
    dislikes = 0
    time = []
    try:
        
            for item in items:
                     
                    # get the video ID
                    video_id = item["id"]["videoId"]
                    if(len(video_id)<12):
                        params = {
                            'videoId': video_id, 
                            'maxResults': 2,
                            'order': 'relevance', # default is 'time' (newest)
                        }
                        # get the video details
                        try:
                            video_response = get_video_details(youtube, id=video_id)
                            #likes = 0
                            
                            likes += get_video_likes(video_response)
                            dislikes += get_video_dislikes(video_response)
                            # print the video details
                            print_video_infos(video_response)
                            print(video_id)
                            # show comments
                            n_pages = 2
                            
                            for i in range(n_pages):
                                if not items:
                                    break
                                elif(len(video_id)<12):
                                        response = get_comments(youtube, **params)
                                        items = response.get("items")
                                
                                
                                #pnn = [0,0,0]

                                # loop for each comments
                                
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

                                    # csv
                                    #c.writerow(comment, like_count, updated_at)

                                    text = TextBlob(comment)
                                    print(text.sentiment)
                                    # print(text.sentiment.polarity)
                                    print(text.sentiment_assessments)
                                    # words = text.sentiment_assessments[2].split(",")
                                    # print(words)
                                    empty = " assessments=[]"
                                    # if (text.sentiment_assessments[2]!=empty):
                                    #     print(text.sentiment_assessments[2][0])
                                    #     positivewords.append(text.sentiment_assessments[2][0])
                                    time.append(updated_at)

                                    #likes.append(like_count)
                                    #dislikes.append()

                                    if text.sentiment.polarity < 0:
                                        polarity = "Negative"
                                        pnn[1] += 1
                                    elif text.sentiment.polarity > 0:
                                        polarity = "Positive"
                                        pnn[0] += 1
                                    else:
                                        polarity = "Neutral"
                                        pnn[2] += 1
                                fields = ['positive','negative','neutral']
                                rows = [pnn[0], pnn[1], pnn[2]]
                                with open(youtube.csv,'w') as csvfile:
                                    csvwriter.writerow(rows)
                                if "nextPageToken" in response:
                                # if there is a next page
                                # add next page token to the params we pass to the function
                                    params["pageToken"] =  response["nextPageToken"]
                                else:
                                # end of comments
                                    break
                        except:
                            print("Error403")
                        
                    print("="*50)
    except AttributeError:
        print("Error occured")
    
    print(time)
    # print("positive words: "+positivewords)
    # print("negative words: "+negativewords)
    neg = pnn[1]
    pos = pnn[0]
    neu = pnn[2]
    
    
    ## graph
    fig1 = go.Figure(data=[go.Pie(labels=['Likes','Dislikes'], values=[likes,dislikes])])
    fig1.update_layout(title_text="Pie chart of "+input)
    fig1.show()

    fig = go.Figure(data=[go.Pie(labels=['Positive Comments','Negative Comments','Neutral Comments'], values=[pos, neg, neu])])
    fig.update_layout(title_text="Pie chart of "+input)
    fig.show()
