import json
import sys
import time
import azure.cognitiveservices.speech as speechsdk
import asyncio
import os
import openai
import discord

class Globals:
    botKey = "DiscordBotKey"

    '''
    !!!
        If the scipt is telling you that the settings file was not found:

        1. Make sure you alredy launched the save at least once.

        2. Change everything after the = on the line below (path = <>)
        To your script-output path. Use the format 'Disk:\\folder1\\folder2\\so_on'. 
        For example, 'C:\\Users\\IKEA\\AppData\\Roaming\\Factorio\\script-output'
    !!!
    '''

    home_dir = os.path.expanduser("~")
    path = os.path.join(home_dir, "AppData", "Roaming", "Factorio", "script-output")

    filename = os.path.join(path, "events.txt")
    settings = os.path.join(path, "settings.txt") 

    prompt = "a very sarcastic engineer who dislikes how everyone else builds factories and can only talk with sarcasm"
    voice = "Aria"
    mood = "Unfriendly"
    interval = 45
    max_words = 40

    openaiKey = "OpenAIKey"
    speech_key = "AzureKey"
    service_region = "AzureRegion"

    openai.api_key = openaiKey
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    play = False

    if sys.platform == "win32":
        ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")
    elif sys.platform == "linux":
        ffmpeg_path = "/usr/bin/ffmpeg"

    def read_settings():
        try:
            with open(Globals.settings) as f:
                json_str = f.read()
                data = json.loads(json_str)
            
            Globals.prompt = data["prompt"]
            Globals.voice = data["voice"]
            Globals.mood = data["mood"]
            Globals.interval = data["interval"]
            Globals.max_words = data["max_words"]
            Globals.openaiKey = data["openAI"]
            Globals.speech_key = data["azure"]
            Globals.service_region = data["azureRegion"]

            openai.api_key = Globals.openaiKey
            Globals.speech_config = speechsdk.SpeechConfig(subscription=Globals.speech_key, region=Globals.service_region)
            Globals.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=Globals.speech_config)

            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print("The settings file was not found. Make sure you already launched the save at least once. If that does not help, open the script with any text editor and read the text marked by exclamation marks (at the top).")
            return False   
            
class Voice:
    def __init__(self, name, language, styles):
        self.name = name
        self.language = language
        self.styles = styles

unparsed = [{"name":"en-US-NancyNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-JaneNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-SaraNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-AriaNeural", "language":"English", "styles":['Default', 'Chat', 'Customer-service', 'Narration-professional', 'Newscast-casual', 'Newscast-formal', 'Cheerful', 'Empathetic', 'Angry', 'Sad', 'Excited', 'Friendly', 'Terrified', 'Shouting', 'Unfriendly', 'Whispering', 'Hopeful']},
            {"name":"en-US-JennyNeural", "language":"English", "styles":['Default', 'Assistant', 'Chat', 'Customer-service', 'Newscast', 'Angry', 'Cheerful', 'Sad', 'Excited', 'Friendly', 'Terrified', 'Shouting', 'Unfriendly', 'Whispering', 'Hopeful']},
            {"name":"en-US-DavisNeural", "language":"English", "styles":["Default", "Chat", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-GuyNeural", "language":"English", "styles":["Default", "Newscast", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-TonyNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-JasonNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]}]

voices = [Voice(voice["name"], voice["language"], voice["styles"]) for voice in unparsed]

all_styles = ["Angry",
"Assistant",
"Chat",
"Cheerful",
"Customer-service",
"Default",
"Empathetic",
"Excited",
"Friendly",
"Hopeful",
"Narration-professional",
"Newscast",
"Newscast-casual",
"Newscast-formal",
"Sad",
"Shouting",
"Terrified",
"Unfriendly",
"Whispering"]

async def get_response(prompt):
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=prompt
)

  response = json.loads(json.dumps(response))
  return response


def make_ssml(voice, style, text_to_speak):
    return f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{voice}">
        <mstts:express-as style="{style.lower()}">
        {text_to_speak}
        </mstts:express-as>
    </voice>
    </speak>
    """

async def text_to_speech(ssml):
    def synthesize_speech():
        return Globals.speech_synthesizer.speak_ssml_async(ssml).get()

    result = await asyncio.get_event_loop().run_in_executor(None, synthesize_speech)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        if not os.path.exists("log"):
            os.makedirs("log")

        file_name = f"{int(time.time())}.mp3"
        file_path = os.path.join("log", file_name)
        with open(file_path, "wb") as audio_file:
            audio_file.write(result.audio_data)
        return file_path
    else:
        cancellation_details = result.cancellation_details
        error_message = f"Speech synthesis canceled. Reason: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        raise Exception(error_message)

class Summary:
    class Player:
        def __init__(self, name):
            self.name = name
            self.crafted = {}
            self.built = {}
            self.picked = {}
            self.cancelled = {}
            self.marked = {}
            self.marked = {}
            self.flushed = {}
            self.surface = []
            self.died = {}
            self.console = 0
            self.left = 0
            self.joined = 0
        
        def __hash__(self):
            return hash(self.name)
        
        def __str__(self):
            string = ""
            if self.any_value():
                string += f"{self.name} has: "

                if self.crafted:
                    string += f"Crafted {parse_numeric_dict(self.crafted)}; "
                
                if self.built:
                    string += f"Built {parse_numeric_dict(self.built)}; "
                
                if self.picked:
                    string += f"Picked up {parse_numeric_dict(self.picked)}; "

                if self.cancelled:
                    string += "Cancelled: "
                    string += parse_special_dict(self.cancelled, " of ", "")
                    string += "\n"

                if self.marked:
                    string += "Marked: "
                    string += parse_special_dict(self.marked, "", "for ", True)
                    string += "\n"

                if self.flushed:
                    string += f"Flushed {parse_numeric_dict(self.flushed, 'liters of ')}; "

                if self.died:
                    string += f"Died {parse_numeric_dict(self.died), 'times due to '}; "
                
                if self.surface:
                    string += "Changed surfaces: "
                    for pair in self.surface:
                        string += f"from {pair[0]} to {pair[1]}, "
                    string = string[:-2]
                    string += "; "
                
                if self.console:
                    string += f"Used console commands {self.console} times; "
                
                if self.left:
                    string += f"Left the game {self.left} times; "

                if self.joined:
                    string += f"Joined the game {self.joined} times; "

            if string:
                string += "\n"

            return string

        def any_value(self):
            return self.crafted or self.built or self.picked or self.cancelled or self.marked or self.flushed or self.surface or self.died or self.console or self.left or self.joined

    class Robots:
        def __init__(self):
            self.built = {}
            self.picked = {}
        
        def __str__(self):
            string = ""
            if self.built:
                string += "Robots have built "
                string += parse_numeric_dict(self.built)
                string += "\n"
            if self.picked:
                string += "Robots have picked up "
                string += parse_numeric_dict(self.picked)
                string += "\n"
            return string

    class Special:
        def __init__(self):
            self.expired = 0
            self.charted = {}
            self.rocket = 0
            self.research = []
            self.trains = 0
        
        def __str__(self):
            string = ""
            if self.expired:
                string += f"{self.expired} corpses have expired\n"
            if self.rocket:
                string += f"{self.rocket} rockets have been launched\n"
            if self.trains:
                string += f"{self.trains} trains have been built\n"
            if self.charted:
                string += "New areas discovered on these surfaces: "
                string += parse_numeric_dict(self.charted)
                string += "\n"
            if self.research:
                string += "New technology researched: "
                string += ", ".join(self.research)
                string += "\n"
            return string

                

    def __init__(self):
        self.players = {}
        self.deaths = {}
        self.robots = self.Robots()
        self.biters = 0
        self.special = self.Special()

    def __str__(self):
        parsed = ""

        parsed += self.parse_players()
        parsed += str(self.robots)
        parsed += self.parse_deaths()
        parsed += str(self.special)

        if self.biters:
            parsed += f"{self.biters} biters have migrated to a new location\n"

        return parsed 
    
    def parse_players(self):
        string = ""
        for value in self.players.values():
            string += str(value)
            string += "\n"
        return string

    def parse_deaths(self):
        string = ""
        if self.deaths:
            string += "Entities died: "
            string += parse_special_dict(self.deaths, "", "due to ", True)
            string += "\n"
        return string

    def add(self, event_type, event_data):
        if event_type == "on_built_entity":
            player_name = event_data["player"]
            entity = f'[{event_data["entity"]}]'
            
            player = self.players.setdefault(player_name, self.Player(player_name)) # Get the player, adding them if they are not in the dict
            player.built[entity] = player.built.get(entity, 0) + 1 # Increment the entity by 1
            
        elif event_type == "on_build_base_arrived":
            self.biters += 1
            
        elif event_type == "on_cancelled":
            player_name = event_data["player"]
            entity = f'[{event_data["entity"]}]'
            cancel = event_data["cancel"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            if cancel in player.cancelled:
                inner_dict = player.cancelled[cancel]
                if entity in inner_dict:
                    inner_dict[entity] += 1
                else:
                    inner_dict[entity] = 1
            else:
                player.cancelled[cancel] = {entity: 1}

        elif event_type == "on_marked":
            player_name = event_data["player"]
            entity = f'[{event_data["entity"]}]'
            marked = event_data["marked"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            if marked in player.marked:
                inner_dict = player.marked[marked]
                if entity in inner_dict:
                    inner_dict[entity] += 1
                else:
                    inner_dict[entity] = 1
            else:
                player.marked[marked] = {entity: 1}

        elif event_type == "on_character_corpse_expired":
            self.special.expired += 1

        elif event_type == "on_chunk_generated":
            surface_name = event_data["surface"]
            
            if surface_name in self.special.charted:
                self.special.charted[surface_name] += 1
            else:
                self.special.charted[surface_name] = 1

        elif event_type == "on_console_command":
            player_name = event_data["player"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.console += 1
            
        elif event_type == "on_entity_died":
            entity_name = f'[{event_data["entity"]}]'
            cause = f'[{event_data["cause"]}]'

            if cause in self.deaths:
                inner_dict = self.deaths[cause]
                if entity_name in inner_dict:
                    inner_dict[entity_name] += 1
                else:
                    inner_dict[entity_name] = 1
            else:
                self.deaths[cause] = {entity_name: 1}

        elif event_type == "on_player_changed_surface":
            player_name = event_data["player"]
            old_surface_name = event_data["old_surface"]
            new_surface_name = event_data["new_surface"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.surface.append([old_surface_name, new_surface_name])

        elif event_type == "on_player_died":
            player_name = event_data["player"]
            cause = f'[{event_data["cause"]}]'

            player = self.players.setdefault(player_name, self.Player(player_name))
            if cause in player.died:
                player.died["cause"] += 1
            else:
                player.died["cause"] = 1

        elif event_type == "on_player_flushed_fluid":
            player_name = event_data["player"]
            fluid = f'[{event_data["fluid"]}]'
            amount = int(event_data["amount"])

            player = self.players.setdefault(player_name, self.Player(player_name))
            if fluid in player.flushed:
                player.flushed[fluid] += amount
            else:
                player.flushed[fluid] = amount

        elif event_type == "on_player_left_game":
            player_name = event_data["player"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.left += 1

        elif event_type == "on_robot_built_entity":
            entity = f'[{event_data["entity"]}]'
            
            self.robots.built[entity] = self.robots.built.get(entity, 0) + 1

        elif event_type == "on_robot_mined":
            entity = f'[{event_data["entity"]}]'

            self.robots.picked[entity] = self.robots.picked.get(entity, 0) + 1

        elif event_type == "on_rocket_launched":
            self.special.rocket += 1

        elif event_type == "on_player_mined_entity":
            player_name = event_data["player"]
            entity = f'[{event_data["entity"]}]'

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.picked[entity] = player.picked.get(entity, 0) + 1

        elif event_type == "on_research_finished":
            research = f'[{event_data["research"]}]'

            self.special.research.append(research)

        elif event_type == "on_player_joined_game":
            player_name = event_data["player"]

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.joined += 1

        elif event_type == "on_player_crafted_item":
            player_name = event_data["player"]
            item = f'[{event_data["item"]}]'

            player = self.players.setdefault(player_name, self.Player(player_name))
            player.crafted[item] = player.crafted.get(item, 0) + 1
            
        else:
            return

def parse_numeric_dict(dictionary, extra = ""):
    string = ""
    for name, value in dictionary.items():
        string += f"{value} {extra}{name}, "
    return string[:-2]

def parse_special_dict(dictionary, extra1 = "", extra2 = "", at_start = False):
    parsed_string = ""
    for cause_param, inner_dict in dictionary.items():
        for entity_param, count in inner_dict.items():
            parsed_string += f"{cause_param if not at_start else ''}{extra1}{count} {entity_param} {extra2}{cause_param if at_start else ''}, "
    return parsed_string[:-2]

def make_prompt(player_prompt, max_words, summary):
    if not str(summary).strip():
        summary = "Nothing happened"

    prompt = ""
    prompt += f"You play the role of {player_prompt}. Your comments must be meaningful and insightful without summarizing the events.\n"
    prompt += f"Your input is a summary of in-game events of the game Factorio. System names are in square brackets. All system names must be translated to human English."
    prompt += f"Your output should consist of a single json with a 'response' field that contains a meaningful and original comment about one of the event, chosen by you."
    prompt += f"Limit your response to a maximum of {max_words} words."
    prompt += f"The summary is:"
    prompt += f"{summary}"

    corrected = []
    corrected.append({"role": "system", "content":prompt})

    return corrected

def summarize_events(events):
    summary = Summary()
    for event in events:
        event = json.loads(event)
        #print(event)
        event_type = event["type"]
        event_data = event["data"]
        summary.add(event_type, event_data)

    return summary

def read_file(filename):
    try:
        events = []
        with open(filename) as f:
            for line in f:
                events.append(line.strip())
        return events
    except FileNotFoundError:
        print("Event file was not found. Make sure you already launched the save at least once. If that does not help, open the script with any text editor and read the text marked by exclamation marks (at the top).")
        return False

def clear_file(filename):
    try:
        with open(filename, 'w') as f:
            f.truncate(0)
    except FileNotFoundError:
        print("Event file was not found. Make sure you already launched the save at least once. If that does not help, open the script with any text editor and read the text marked by exclamation marks (at the top).")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    try:
        if message.content == "!factorio":
            Globals.play = True
            await message.channel.send("Execution has started.")
            print("Execution has started.")
            while Globals.play:
                await play_audio(message)
                await asyncio.sleep(Globals.interval)
    except:
        await message.channel.send("An error happened that the script was not able to handle. The script will continue to function, skipping this iteration.")
        print("An error happened that the script was not able to handle. The script will continue to function, skipping this iteration.")

    if message.content == "!stop":
        Globals.play = False
        await message.channel.send("Execution has stopped.")
        print("Execution has stopped.")


async def play_audio(message):
    canContinue = Globals.read_settings()
    events = read_file(Globals.filename)

    if canContinue and (events != False): 

        voice_state = message.author.voice
        if not voice_state:
            await message.channel.send("Please join a voice channel.")
            print("Please join a voice channel.")
            return

        voice_channel = voice_state.channel
        voice_client = message.guild.voice_client
        if voice_client and voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
        elif not voice_client:
            voice_client = await voice_channel.connect()

        if not voice_channel.members:
            await voice_client.disconnect()
            return
        
        summary = summarize_events(events)

        prompt = make_prompt(Globals.prompt, Globals.max_words, summary)


        try:
            response = await get_response(prompt)
        except openai.error.AuthenticationError:
            await message.channel.send("OpenAI key you specified is incorrect.")
            print("OpenAI key you specified is incorrect.")

        try:
            response = response["choices"][0]["message"]["content"]
            response = json.loads(response)["response"]
            await message.channel.send(response)
            ssml = make_ssml(Globals.voice, Globals.mood, response)
        except Exception as e:
            await message.channel.send(f"Something went wrong: {e}. Most probably, the response GPT provided was incorrectly formatted.")
            print(f"Something went wrong: {e}. Most probably, the response GPT provided was incorrectly formatted.")

        try:
            audio = await text_to_speech(ssml)
            source = discord.FFmpegPCMAudio(executable=Globals.ffmpeg_path, source=audio)
            voice_client.play(source)
            clear_file(Globals.filename)
        except Exception as e:
            await message.channel.send(f"Azure key or region you specified is incorrect: {e}")
            print(f"Azure key or region you specified is incorrect: {e}")


        while voice_client.is_playing():
            await asyncio.sleep(1)

        
    else:
        await message.channel.send("Settings or events file was not found. Make sure you already launched the save at least once. If that does not help, open the script with any text editor and read the text marked by exclamation marks (at the top).")
        print("Settings or events file was not found. Make sure you already launched the save at least once. If that does not help, open the script with any text editor and read the text marked by exclamation marks (at the top).")

client.run(Globals.botKey)