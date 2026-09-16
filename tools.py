import os
import json
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from tavily import TavilyClient, AsyncTavilyClient

load_dotenv()

tavily_client = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)

obsidian_vault = r"D:\Obsidian\Knowledge"
obsidian_dir = os.listdir(obsidian_vault)

def access_files(filename):
    try:
        with open(os.path.join(obsidian_vault,filename), "r") as open_file:
            read_file = open_file.read()
            return read_file
    except Exception as e:
        return f"file {filename} not found. Files in directory are: {obsidian_dir}. Error: {e}"
    
def preview_file(filename, mode):
    try:
        with open(os.path.join(obsidian_vault, filename), "r") as file_preview:
            return file_preview.readline()
    except Exception as e:
        return f"could not load preview. Error: {e}"
def edit_files(filename, content, mode):
    try:
        if filename != "startup.md":
            with open(os.path.join(obsidian_vault, filename), mode) as edit_file:
                edit_file.write(content)
            return f"Successfully wrote to {filename} in {mode} mode. Content written: {content}"
        else:
            return "Cannot modify startup.md - can only be modified by user"
    except Exception as e:
        return f"could not make or edit file: {filename} in mode: {mode}. Error: {e}"
    
def make_folder(foldername):
    try:
        newpath = os.path.join("obsidian_vault", foldername)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    except Exception as e:
        return f"folder: {foldername} could not be made. Error: {e}"
    
def get_weather(location, unit):
    try:
        geolocator = Nominatim(user_agent = "Assistant")
        location_coords = geolocator.geocode(location)
        weather_params = {
            "latitude": location_coords.latitude,
            "longitude": location_coords.longitude,
            "current": "temperature_2m",
            "temperature_unit": unit,
        }
        response = requests.get("https://api.open-meteo.com/v1/forecast", params = weather_params)
        data = response.json()
        return f"The weather in {location} is {data['current']['temperature_2m']}"
    except Exception as e:
        return f"Weather could not be returned: {e}"
    
def search_web(query, max_result):
    try:
        response = tavily_client.search(
        query = query,
        max_results = max_result,
        )
        all_results = []
        for result in response["results"]:
            all_results.append(f"{result['title']} \n {result['url']}\n")
        return "\n".join(all_results)
    except Exception as e:
        return f"could not search web. Error: {e}"    
def enter_url(url, extract_depth):
    try:
        response = tavily_client.extract(
        urls = url,
        extract_depth = extract_depth,
    )
        result = response["results"][0]
        return f"URL: {result['url']} \n Content length: {len(result['raw_content'])} chars \n {result['raw_content'][:500]}"
    except Exception as e:
        return f"url not found: {e}"



    
tools = [
    {
        "name": "access_files",
        "description": "Reads and returns the contents of a specific file from the user's memory vault, given its filename. Use this when a file mentioned in the file index seems relevant to the current conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The exact filename to read, as it appears in the file index (e.g. 'eeg_project.md').",
                }
            },
            "required": ["filename"]
        }
    },
    
    {
        "name": "read_summary",
        "description": "Reads the first line of a specific file iun the users memory vault. The first line of everyfile contains a summery of that file",
        "input_schema": {
            "type": "",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The exact filename to read, as it appears in the file index (e.g. 'eeg_project.md').",
                }
            },
            "required": ["filename"]
        }
    },
    
    {
        "name": "edit_files",
        "description": "Creates and/or edits the contents of a specific file from the user's memory vault, given its filename. Use this when a file mentioned in the file index or not in the index but seems relevant to the current conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The exact filename that will either created or the exact filename of the file as it appears in the the file index (e.g. 'eeg_project.md'). Where relevant when content in the note clearly relates to another existing note in the vault using the [[note_name]] syntax",
                },
                "content": {
                    "type": "string",
                    "description": "the content of which either will be appended to the file or overwrite in the file",
                },
                "mode": {
                    "type": "string",
                    "description": "the mode either 'a' for append where a file is created, or 'w' where a file is written to.",
                    "enum": ["a", "w"],
                },
            },
         "required": ["filename", "content", "mode"],
        }
    },
    
    {
        "name": "make_folder",
        "description": "Allows the creation of new folders in the directory with a name that is relevant based on the user and conversation",
        "input_schema": {
            "type": "object",
            "properties": {
                "foldername": {
                    "type": "string",
                    "description": "The exact foldername that will be created",
                }
            },
            "required": ["foldername"]
        }
    },
    
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The unit of temperature",
                },
            },
            "required": ["location"],
        },
        "input_examples": [
            {"location": "San Francisco, CA", "unit": "fahrenheit"},
            {"location": "Tokyo, Japan", "unit": "celsius"},
            {"location": "New York, NY"},
        ],
    },
    
    {
        "name": "search_web",
        "description": "Search the web for a users query",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What the user is request is to be searched on the web",
                },
                "max_result": {
                    "type": "integer",
                    "description": "the maximum number of results the user is given",
                },
            },
            "required": ["query", "max_result"],
        },
    },
    
    {
        "name": "enter_url",
        "description": "Once the web has been searched, used to enter and return the contents of the url",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url that the contents will be retured",
                },
                "extract_depth": {
                    "type": "string",
                    "description": "determins the level of depth returned by the url",
                    "enum": ["basic", "advanced"],
                },
                
            },
            "required": ["url", "extract_depth"],
        },
    },
]