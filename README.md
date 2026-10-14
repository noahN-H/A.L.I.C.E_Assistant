# A.L.I.C.E_Assistant
A.L.I.C.E is an Agentic AI assistant that has a custom bottom-up memory system, full speech I/O (TTS and STT), and tool-use/function-calling capable of real-world actions including file manipulation, weather search and general web search.

**A**.rtificial<br>
**L**.earning<br>
**I**.ntelligence<br>
and<br>
**C**.erebral<br>
**E**.nvironment

Featuring: 
- a custom bottom up memory system
- read, write files and folders
- full speech I/O using whisper and Kokoro
- weather access using geopy
- internet access using tavily

# System Overview:
- The system loads its startup file as well as its personality and its own personal profile from the memory vault
- Takes a voice input from the user
- Using Whisper transcribes the audio
- The transcription is then added to a conversation history
- Conversation history is sent to the api as a request
- The api decides if any tools should be used
- The api handles the request and returns an output
- Kokoro then takes the api output and returns an audio out of the result
- Once the conversation has ended, the system makes one more call to summarise all of the conversation history
- The summarised history is then saved in the memory vault to be referenced at a later date

# Setup
Prerequisites:
- [Claude api key](https://platform.claude.com)
- [Tavilly api key](https://app.tavily.com/home)
- Python
<br>To install dependencies run `$ pip install -r requirements.txt` 

Set up `.env` - copy the example and fill it in: `cp .env.example .env`
```
ANTHROPIC_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
MEMORY_VAULT=/path/to/your/vault
```

`ANTHROPIC_API_KEY` is the Claude api <br>
`TAVILY_API_KEY` where the Tavily api key goes <br>
`MEMORY_VAULT` is the path to the memory vault

To run 
`$ python main.py`

# Sources
Anthropic Claude API (the model and SDK powering ALICE): https://docs.claude.com

faster-whisper (speech-to-text): https://github.com/SYSTRAN/faster-whisper

Kokoro (text-to-speech): https://github.com/hexgrad/kokoro

sounddevice (microphone capture and audio playback): https://python-sounddevice.readthedocs.io/

Tavily (web search and URL extraction): https://tavily.com

geopy (geocoding): https://geopy.readthedocs.io/

Nominatim (geocoding backend used by geopy): https://nominatim.org/

Open-Meteo (weather data API): https://open-meteo.com/

NumPy (audio array handling): https://numpy.org/

SciPy (WAV file I/O): https://scipy.org/
