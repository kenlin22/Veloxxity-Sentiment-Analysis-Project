from utils import (
    youtube_authenticate,  
    get_video_details,
    print_video_infos,
    search
)

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
        print("="*50)
    
    print(time)
    neg = pnn[1]
    pos = pnn[0]
    neu = pnn[2]
    fig = go.Figure(data=[go.Pie(labels=['Positive Comments','Negative Comments','Neutral Comments'], values=[pos, neg, neu])])
    fig.update_layout(title_text="Proportion of Positive and Negative Tweets on the South China Sea")
    fig.show()