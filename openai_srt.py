from openai import OpenAI
import subprocess
import os

# Set up your OpenAI API key 
client = OpenAI(api_key='your-api-key') 


def time_to_seconds(time_str):
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2].replace(',', '.'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def transcribe_video(audio_file):  
    audio_file= open(audio_file, "rb")
    response = client.audio.transcriptions.create(
        file=audio_file,
        response_format = "srt",  
        model="whisper-1"
    )
 
    transcription = response
    
    text_list = transcription.split("\n")
    temp = len(text_list)%4
    text_list = text_list[:-temp]

    srt_text = []
    for i in range(0,len(text_list),4):
        start_second = time_to_seconds(text_list[i+1].split("-->")[0])
        end_second = time_to_seconds(text_list[i+1].split("-->")[1])
        srt_text.append(((start_second,end_second),text_list[i+2]))

    return srt_text

def translate(content, input_language="English", target_language = 'Vietnamese'):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {
            "role": "system",
            "content": f"You will be provided with a sentence in {input_language}, and your task is to translate it into {target_language}. If it's too short, just translate it, or return it blank"
            },
            {
            "role": "user",
            "content": content
            }
        ],
        temperature=0.7,
        max_tokens=100,
        top_p=1
    )
    
    return response.choices[0].message.content

