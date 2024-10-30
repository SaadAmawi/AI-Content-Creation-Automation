from docx import Document
from openai import OpenAI
from transcribe import Transcript
import Config 

Trans = Transcript()
file = Transcript.transcription()
# file = open('Transcript.txt','r')

client = OpenAI(
  organization=Config.organization,
  project=Config.project,
  api_key=Config.gpt_api_key
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",  
            "content": 
            f"""I have gone and found the top 10 most popular YouTube videos under the EA FC game genre in the past week.
                            I will now give you the transcripts of the top 10 videos, and I want you to do the following:
                            -understand the context from the transcript
                            -create a summary for each video
                            -create a summary of the top 10 videos of the week, explaining common themes and things we can incorporate into our ideas for content creation this week
                            -include any other information you think might be useful or that might give us insight
                            -put this all into a brief that will be sent to our content creation director for him to use for the content creation this week.

                            This is the format of the brief:

                            GAME TITLE

                            Video Title - View Count - Channel Name - Channel Subscriber Amount
                            Transcript 1 : [transcripts can be found at the bottom of this document]
                            Video Summary

                            Video Title - View Count - Channel Name - Channel Subscriber Amount
                            Transcript 2: [transcripts can be found at the bottom of this document]
                            Video Summary detailing what the video was about, what kind of methods the content creator used to increase audience retention,
                            and other things that may be useful to know about the contents of the video (ENSURE THIS SUMMARY IS A SHORT PARAGRAPH OF AROUND 300-400 WORDS) 
                            .
                            .
                            .
                            Transcript 10.

                            1. LONGER Summary of all the videos and any common themes, common strategies used to increase audience
                            2. key findings

                            3. Any other relevant information that our content creation director (Darshan) might find useful

                            below are the transcripts of the videos:
                            {file.read()}
                                        """
        }
    ]
)

reply = completion.choices[0].message.content
try:
    transcript_file = open('transcript.txt','r')
    # Create a Word document and add the reply
    document = Document()
    document.add_paragraph(reply)
    document.add_paragraph("----BELOW ARE THE FULL TRANSCRIPT FOR ALL THE VIDEOS----")
    document.add_paragraph(transcript_file.read())
    document.add_paragraph("Prepared By: Saad Amawi")


    # Save the document
    document.save("ChatGPT_Reply3.docx")

    print("The reply has been saved to ChatGPT_Reply.docx")
except Exception as e:
    print("error adding transcriptions to document",e)

