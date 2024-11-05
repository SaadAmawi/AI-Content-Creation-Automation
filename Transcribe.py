from youtube_transcript_api import YouTubeTranscriptApi
from Top10 import Top10

class Transcript:
    
    fileName = "Transcript.txt"
    @staticmethod
    def transcription():
        top = Top10()
        IDs = top.get_top_gaming_videos()
        print(IDs)
        VIDEO_ID = IDs # Replace with the actual video ID
        file = open(Transcript.fileName,'w')
        counter = 1
        for id in VIDEO_ID:
            file.write(f'Video {counter} Transcript \n')
            try:
                # Fetch the transcript
                transcript = YouTubeTranscriptApi.get_transcript(id)
                for entry in transcript:
                    file.write(f"{entry['text']} ")
                    # print(f"{entry['text']} ")
            except Exception as e:
                file.write("No Transcript Available")
                print("Error fetching transcript:", e)
            file.write('\n\n\n\n\n\n\n\n')
            counter += 1
        return open(Transcript.fileName,'r')
        

if __name__ == '__main__':
    transcript = Transcript()
    transcript.transcription()

