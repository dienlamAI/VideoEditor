from faster_whisper import WhisperModel 
import os

#config
task = "transcribe" # tasks: translate, transcribe
 
def transcribe_video(input_file):
    model_size = "large-v2"  # other models: small, medium, large-v2, tiny

    # Run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", cpu_threads=12, compute_type="int8")

    # Remove task="translate" if you want the original language
    segments, info = model.transcribe(input_file, beam_size=5, task=task, vad_filter=True)

    print("Detected language '{}' with probability {:.2f}".format(info.language, info.language_probability))

    srt_text = []
 
    for segment in segments: 
        srt_text.append(((segment.start, segment.end), segment.text))
    return srt_text

def translate(content, input_language="English", target_language = 'Vietnamese'):
    model_size = "large-v2"  # other models: small, medium, large-v2, tiny

    # Run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", cpu_threads=12, compute_type="int8")

    response = model.translate(content, input_language, target_language)

    return response
