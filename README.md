# AI_Assistant
A Assistant based of of Claude api, used to monitor programs and assist the user]

A.rtifical
L.earning
I.ntellegance
and
C.erebral
E.nvironemnt


A.L.I.C.E is an agentic AI assistant based on the Claude api. 

Featuring: 
- a custom bottom up memory system
- read, write files and folders
- full speech I/O using whisper and Kokoro
- weather access using geopy
- internet access using tavily



# imports needed to run main:
    from anthropic import Anthropic
    from dotenv import load_dotenv
    import json
    from faster_whisper import WhisperModel
    import sounddevice as sd
    from scipy.io.wavfile import write
    import numpy as np
    from kokoro import KPipeline
    from tools import access_files, read_summary, edit_files, get_weather, search_web, enter_url, make_folder, tools
    from voice import record_and_transcribe

# imports needed to run tools:
    import os
    import json
    import requests
    from dotenv import load_dotenv
    from geopy.geocoders import Nominatim
    from tavily import TavilyClient, AsyncTavilyClient

# imports needed to run voice:
    from faster_whisper import WhisperModel
    import sounddevice as sd
    from scipy.io.wavfile import write
    import numpy as np
    from kokoro import KPipeline
