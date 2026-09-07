import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from tools import access_files, edit_files, get_weather, search_web, enter_url, tools


chat = True
history = []
load_dotenv()
obsidian_vault = r"D:\Obsidian\Knowledge"
obsidian_dir = os.listdir(obsidian_vault)
anthropic_client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

with open(os.path.join(obsidian_vault,"startup.md"), "r") as startup:
    read_startup = startup.read()

with open(os.path.join(obsidian_vault,"me.md"), "r") as user_profile:
    read_user_profile = user_profile.read()
   
while chat:
    msg = input()
    if msg == "sleep":
        chat = False
        exit_msg = anthropic_client.messages.create(
            max_tokens = 1024,
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
    
    if msg == "abort":
        break
    
    history.append({"role": "user","content": msg})
    
    resp = anthropic_client.messages.create(
        max_tokens = 1024,
        tools = tools,
        system = f"The following is infomation is the relevant startup infomation:\n\n{read_startup}, you can also view files that are in the directory: {obsidian_dir}. infomation about the user can be found here in: {read_user_profile}",
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
                    result = edit_files(j.input["filename"],j.input["content"], j.input["mode"] )
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