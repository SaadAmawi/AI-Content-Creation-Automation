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
            f"""
            1. Project Title:

A concise and catchy title summarizing the video concept (e.g., "Top 10 EA FC Tips for 2025" or "Behind-the-Scenes with NASR's Pro Gamers").
2. Video Objective:

The main goal of this video (e.g., "Engage gaming enthusiasts by sharing pro tips on new EA FC strategies," or "Highlight the personality and gaming skills of NASR players").
3. Target Audience:

Describe the intended viewers (e.g., "Dedicated EA FC fans looking to improve their gameplay" or "Esports enthusiasts interested in NASR's team culture").
4. Video Structure:

Intro (10-15 seconds): Briefly introduce the concept or hook to grab attention.
Main Content: List the primary points or segments the video should cover (e.g., top 10 tips, reactions, gameplay analysis, behind-the-scenes).
Outro: Include a call-to-action (subscribe, follow on social, leave a comment with tips/questions).
5. Tone & Style:

Outline the expected tone (e.g., "Informative but friendly" or "Energetic and engaging with humor").
Style recommendations (e.g., "High-energy, concise cuts, on-screen graphics for gameplay tips").
6. Key Elements to Include:

Any specific NASR content, terms, or player insights to mention.
B-roll suggestions (e.g., clips of past tournaments, reaction shots, or fan interactions if available).
Suggested questions or prompts if interviewing NASR players or fans.
7. Technical Specifications:

Video length, format requirements, and resolution.
Soundtrack guidelines or any sound effects that fit the brand style.
8. Call to Action:

Encourage viewers to engage (e.g., "Ask viewers to share their favorite EA FC tactics in the comments").
9. Timeline & Deadlines:

Key deadlines (script approval, filming, editing, final video submission).
Any extra notes on urgent release dates or campaign tie-ins.
10. Points of Contact:

List contacts for questions, feedback, or assistance with editing resources.

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

