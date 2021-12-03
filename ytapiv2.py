from utils import (
    youtube_authenticate,  
    get_video_details,
    print_video_infos,
    get_video_likes,
    get_video_dislikes,
    get_video_views,
    get_video_title,
    search
)
import csv
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import plotly.graph_objects as go
import pandas as pd

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
    # search for the query 'python' and retrieve 2 items only
    response = search(youtube, q=input, maxResults=4)
    items = response.get("items")
    pnn = [0,0,0]
    positivewords = []
    negativewords = []
    likes = 0
    dislikes = 0
    views = 0
    titles = ""
    time = []
    try:
        #creating csv files for each analysis
        with open('youtubep.csv','w') as csvfilep, open('youtuben.csv','w') as csvfilen, open('youtube.csv','w') as csvfile, open('video.csv','w') as vfile:
        
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
                            likes += get_video_likes(video_response)
                            dislikes += get_video_dislikes(video_response)

                            views = get_video_views(video_response)
                            titles = get_video_title(video_response)
                            dislikecounts = get_video_dislikes(video_response)
                            likecounts = get_video_likes(video_response)
                            video_rows = [titles, views, dislikecounts, likecounts, dislikecounts/likecounts]
                            writerv = csv.writer(vfile)
                            writerv.writerow(video_rows)
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

                                    #csvfile
                                    rows = [comment,updated_at,like_count]
                                    text = TextBlob(comment)
                                    print(text.sentiment)
                                    
                                    # print(text.sentiment.polarity)
                                    print(text.sentiment_assessments)
                                    time.append(updated_at)
                                    if text.sentiment.polarity < 0:
                                        polarity = "Negative"
                                        pnn[1] += 1
                                        writern = csv.writer(csvfilen)
                                        writern.writerow(rows)
                                    elif text.sentiment.polarity > 0:
                                        polarity = "Positive"
                                        pnn[0] += 1
                                        writerp = csv.writer(csvfilep)
                                        writerp.writerow(rows)
                                    else:
                                        polarity = "Neutral"
                                        pnn[2] += 1
                                        writer = csv.writer(csvfile)
                                        writer.writerow(rows)
                                if "nextPageToken" in response:
                                    params["pageToken"] =  response["nextPageToken"]
                                else:
                                # end of comments
                                    break
                        except:
                            print("Error403")
                        
                    print("="*50)
    except AttributeError:
        print("Error occured")
    
    #print(time)
    neg = pnn[1]
    pos = pnn[0]
    neu = pnn[2]
    
    ## most viewed video details
    col_name = ['title','views','dislikes','likes','rate']
    df = pd.read_csv('video.csv', names=col_name, encoding= 'unicode_escape')
    max = df.sort_values(by=['views']).max()
    dismax = df.sort_values(by=['dislikes']).max()
    print("Most viewed video: ")
    print(max)
    print("\n\n")
    print("Most disliked video by numbers: ")
    print(dismax)
    print("\n\n")
    rate = df.sort_values(by=['rate']).max()
    print("Most disliked video by like counts: ")
    print(rate)
    print("\n\n")
    maxlike = df.sort_values(by=['likes']).max()
    print("Most liked video by like counts: ")
    print(maxlike)
    
    data = {'mostviewed': max}
    dfff = pd.DataFrame(data=data)
    dfff.to_csv('max.csv')


    ## graph
    fig1 = go.Figure(data=[go.Pie(labels=['Likes','Dislikes'], values=[likes,dislikes])])
    fig1.update_layout(title_text="Pie chart of "+input)
    fig1.show()

    fig = go.Figure(data=[go.Pie(labels=['Positive Comments','Negative Comments','Neutral Comments'], values=[pos, neg, neu])])
    fig.update_layout(title_text="Pie chart of "+input)
    fig.show()
