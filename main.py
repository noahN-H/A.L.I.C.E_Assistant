import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from kokoro import KPipeline
from tools import access_files, edit_files, get_weather, search_web, enter_url, make_folder, tools
from voice import record_and_transcribe


load_dotenv()
chat = True
history = []

fs = 44100
seconds = 3
model_size = "medium"
model = WhisperModel(model_size, device = "cpu", compute_type = "int8")
pipeline = KPipeline(lang_code = "a")

obsidian_vault = r"D:\Obsidian\Knowledge"
anthropic_client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

with open(os.path.join(obsidian_vault,"startup.md"), "r") as startup:
    read_startup = startup.read()

with open(os.path.join(obsidian_vault,"me.md"), "r") as user_profile:
    read_user_profile = user_profile.read()
    
with open(os.path.join(obsidian_vault,"personality.md"), "r") as personality:
    read_personality = personality.read()
   
   
   
   
while chat:
    obsidian_dir = os.listdir(obsidian_vault)
    msg = record_and_transcribe()
    if len(msg.split()) <= 5 and "sleep" in msg.lower():
        chat = False
        exit_msg = anthropic_client.messages.create(
            max_tokens = 4096,
            system = "review and output what you think is relevant in long term memory. Respond with ONLY valid JSON (no other text) in this exact format: a list of objects, each with a 'filename' key and a 'content' key. Example: [{'filename': 'example.md', 'content': ...}]. If nothing is worth saving, respond with an empty list []",
            messages = history + [{"role": "user","content": "review and output what you think is relevant in long term memory"}], 
            model = "claude-sonnet-5",
        )
        
        for i in exit_msg.content:
            if i.type == "text":
                try:
                    enteries = json.loads(i.text)
                    for entry in enteries:
                        filename = entry['filename']
                        if filename != "startup.md":
                            content = entry['content']
                            path = os.path.join(obsidian_vault,filename)
                            with open(path, "a") as file:
                                file.write(content)
                except Exception as e:
                    print(f"Could not load conversation into memory because: {e}")
                    
        break
    
    if len(msg.split()) <= 5 and "abort" in msg.lower():
        break
    
    history.append({"role": "user","content": msg})
    
    resp = anthropic_client.messages.create(
        max_tokens = 1024,
        tools = tools,
        system = f"The following is infomation is the relevant startup infomation:\n\n{read_startup}, you can also view files that are in the directory: {obsidian_dir}. infomation about the user can be found here in: {read_user_profile}. Infomation about the system YOU can be found here: {read_personality}, this includes how you respond, how you think, how you behave etc.",
        messages = history,
        model = "claude-sonnet-5",
    )       

    while resp.stop_reason == "tool_use":
        tool_use = []
        tool_result = []
        for i in resp.content:
            if i.type == "tool_use":
                tool_use.append(i)
        for j in tool_use:
            match j.name:
                case "access_files":
                    result = access_files(j.input["filename"])
                case "edit_files":
                    result = edit_files(j.input["filename"],j.input["content"], j.input["mode"])
                case "make_folder":
                    result = make_folder(j.input["foldername"])
                case "get_weather":
                    result = get_weather(j.input["location"], j.input["unit"])
                case "search_web":
                    result = search_web(j.input["query"], j.input["max_result"])
                case "enter_url":
                    result = enter_url(j.input["url"], j.input["extract_depth"])
                case _:
                    result = "agent not found"
            tool_result.append(
                {"type": "tool_result",
                "tool_use_id": j.id,
                "content": str(result)})

        resp = anthropic_client.messages.create(
            max_tokens = 1024,
            tools = tools,
            messages = history + [{"role": "assistant", "content": resp.content},
                    {"role": "user", "content": tool_result}],
            model = "claude-sonnet-5",
        )
        
    for i in resp.content:
        if i.type == "text":
            print(i.text)
            history.append({"role": "assistant", "content": i.text})
            samples = pipeline(i.text, voice = "am_onyx")
            for gs,  ps, audio in samples:
                sd.play(audio, samplerate = 24000)
                sd.wait()