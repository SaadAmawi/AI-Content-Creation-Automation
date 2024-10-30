from googleapiclient.discovery import build 
from datetime import datetime, timedelta  
import isodate  
import config

class Top10:



    API_KEY = config.YT_API_KEY


    @staticmethod
    def isEnglish(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
    @staticmethod
    def get_top_gaming_videos():
    
        youtube = build('youtube', 'v3', developerKey=config.YT_API_KEY)  

        one_week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'  

        keywords = ['Black Ops 6']  

        counter = 0

        videos = [] 
        videoIDs = []
        for word in keywords: 
            request = youtube.search().list(  
                part='snippet',  
                maxResults=20,  
                q=word, 
                type='video',  
                videoDuration="medium",
                order='viewCount',  
                relevanceLanguage="en",
                publishedAfter=one_week_ago,  
                fields='items(id(videoId),snippet(title,publishedAt,channelTitle,channelId))'  
            )

            response = request.execute() 

            for item in response.get('items', []): 
                video_id = item['id']['videoId']  
                channel_id = item['snippet']['channelId']  
                title = item['snippet']['title']

                video_response = youtube.videos().list(  
                    part='contentDetails,statistics',  
                    id=video_id,  
                ).execute()  

                if video_response['items']:  
                    duration = isodate.parse_duration(video_response['items'][0]['contentDetails']['duration'])  
                    view_count = int(video_response['items'][0]['statistics']['viewCount'])  

                    channel_response = youtube.channels().list(  
                        part='statistics',  
                        id=channel_id  
                    ).execute()  

                    if channel_response['items']:  
                        subscriber_count = int(channel_response['items'][0]['statistics'].get('subscriberCount', 0))  
                    
                        if  Top10.isEnglish(title):
                            videos.append({  
                                'title': item['snippet']['title'],  
                                'url': f'https://www.youtube.com/watch?v={video_id}',  
                                'channel': item['snippet']['channelTitle'],  
                                'published_at': item['snippet']['publishedAt'],  
                                'duration': str(duration),  
                                'view_count': view_count,  
                                'subscriber_count': subscriber_count,  
                                'vidID': item['id']['videoId']  
                            })
                            videoIDs.append(str(video_id))

            top_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)[:10]  
            IDs = []
        
            print(f"TOP VIDEOS SINCE {one_week_ago} for {keywords[counter]}:")  
            for video in top_videos:  
                print(f"Title: {video['title']}")  
                print(f"URL: {video['url']}")  
                print(f"Channel: {video['channel']}")  
                print(f"Published: {video['published_at']}")  
                print(f"Duration: {video['duration']}")  
                print(f"Views: {video['view_count']:,}")  
                print(f"Subscribers: {video['subscriber_count']:,}") 
                print(f"ID: {video['vidID']}")  
                print() 
                IDs.append(str(video['vidID']))
            counter+=1
            print(IDs)
            return(IDs)
if __name__ == '__main__': 
    Top10.get_top_gaming_videos()  