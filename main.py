from moviepy.editor import *
from edit import VideoEditor
import generate_srt
import openai_srt
import os


editor = VideoEditor('./video/video1.mp4')

audio = editor.get_audio(download=True)
# srt_text = generate_srt.transcribe_video("./audio.mp3")
srt_text = openai_srt.transcribe_video("./audio.mp3")
for i in range(len(srt_text)):
    srt_text[i] = (srt_text[i][0],openai_srt.translate(srt_text[i][1],input_language="Vietnamese", target_language = 'English'))
editor.add_subtitle(srt_text,y=900)

editor.animate_image('./image/logoo.png',x1=10, y1=10, x2=100, y2=100,width_img=100, height_img=100) 

editor.save('./output/output.mp4')

editor.close()
os.remove('audio.mp3')