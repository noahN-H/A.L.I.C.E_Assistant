from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from kokoro import KPipeline

fs = 44100
seconds = 3
model_size = "medium"
model = WhisperModel(model_size, device = "cpu", compute_type = "int8")

audio_list = []
def audio_callback(indata, frames, time, status):
    audio_list.append(indata.copy())
    
def record_and_transcribe():
    stream = sd.InputStream(samplerate = fs, channels = 1, callback = audio_callback)
    audio_list.clear()
    stream.start()
    audio_in = input("Press 'Enter' to stop Recording... : ")
    stream.stop()
    full_recording = np.concatenate(audio_list)
    stream.close()
    write("output.wav", fs, full_recording) 
    
    segments, info = model.transcribe("output.wav", beam_size = 5, vad_filter = True)
    transcribed_text = " ".join([segment.text for segment in segments])
    return transcribed_text