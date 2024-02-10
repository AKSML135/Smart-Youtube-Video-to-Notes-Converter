import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

prompt= '''Consider yourself as a youtube video summarizer. You will be provided with a transcript of
the youtube video. You need to read the transcript and provide a good summary of the transcript, including
important points , topics , details in maximum 250 words.

The transcript text will be appended here : '''

def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel(model_name='gemini-pro')
    response = model.generate_content(prompt+transcript_text)
    return response.text

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('=')[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ''
        for i in transcript_text:
            transcript+= " " + i['text']
        return transcript
    except Exception as e:
        raise e
    
st.title("Youtube🎬 Transcript to Detailed Notes📝 Converter !")
youtube_link = st.text_input("Paste your Youtube video link here ...")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes."):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown('## Detailed Notes')
        st.write(summary)