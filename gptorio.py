import json
import time
import azure.cognitiveservices.speech as speechsdk
import random
import asyncio
import os
import openai

filename = "path"

class Voice:
    def __init__(self, name, language, styles):
        self.name = name
        self.language = language
        self.styles = styles

unparsed = [{"name":"pl-PL-AgnieszkaNeural", "language":"Polish", "styles":["Default"]},
            {"name":"pl-PL-ZofiaNeural", "language":"Polish", "styles":["Default"]},
            {"name":"uk-UA-PolinaNeural", "language":"Ukranian", "styles":["Default"]},
            {"name":"ja-JP-NanamiNeural", "language":"Japanese", "styles":["Default", "Chat", "Customer-service", "Cheerful"]},
            {"name":"it-IT-IsabellaNeural", "language":"Italian", "styles":["Default", "Chat", "Cheerful"]},
            {"name":"el-GR-AthinaNeural", "language":"Greek", "styles":["Default"]},
            {"name":"de-DE-MajaNeural", "language":"German", "styles":["Default"]},
            {"name":"fr-FR-DeniseNeural", "language":"French", "styles":["Default", "Sad", "Cheerful"]},
            {"name":"ru-RU-DariyaNeural", "language":"Russian", "styles":["Default"]},
            {"name":"ru-RU-SvetlanaNeural", "language":"Russian", "styles":["Default"]},
            {"name":"en-US-SaraNeural", "language":"English", "styles":["Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering"]},
            {"name":"en-US-AriaNeural", "language":"English", "styles":['Default', 'Chat', 'Customer-service', 'Narration-professional', 'Newscast-casual', 'Newscast-formal', 'Cheerful', 'Empathetic', 'Angry', 'Sad', 'Excited', 'Friendly', 'Terrified', 'Shouting', 'Unfriendly', 'Whispering', 'Hopeful']},
            {"name":"en-US-JennyNeural", "language":"English", "styles":['Default', 'Assistant', 'Chat', 'Customer-service', 'Newscast', 'Angry', 'Cheerful', 'Sad', 'Excited', 'Friendly', 'Terrified', 'Shouting', 'Unfriendly', 'Whispering', 'Hopeful']}]
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

speech_key = "key"
openai.api_key = "key"
service_region = "region"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def get_response(prompt):
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=prompt
)

  response = json.loads(json.dumps(response))
  return response


def make_ssml(voice, style, text_to_speak):
    return f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{voice.name}">
        <mstts:express-as style="{style.lower()}">
        {text_to_speak}
        </mstts:express-as>
    </voice>
    </speak>
    """

def text_to_speech(ssml):
    result = speech_synthesizer.speak_ssml(ssml)

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

def make_prompt(prompt, mood, max_words, summary):
    if not str(summary).strip():
        summary = "Nothing happened"
    example = '{"response":"<response>"}'

    prompt = ""
    prompt += f"You play the following role: {prompt} You comments are always {mood}. Provide meaningful commentary on the events. Do not provide a summary of the events.\n"
    prompt += f"Your input is a summary of in-game events of the game Factorio. System names are in square brackets. Change all system names into human English."
    prompt += f"Create responses in two steps:"
    prompt += f"1) Your response must be a comment about the events in the format of a json {example}"
    prompt += f"2) Your response should not have any system names. Change all of them to human English"
    prompt += f"Limit that to:"
    prompt += f"1) never have more than {max_words} words"
    prompt += f"2) Never have more than 1 response"
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

def read_and_clear_file(filename):
    events = []
    with open(filename) as f:
        for line in f:
            events.append(line.strip())
    with open(filename, 'w') as f:
        f.truncate(0)
    return events

def main():
    while True:
        events = read_and_clear_file(filename)
        #print(events)
        #print("\n\n\n")

        summary = summarize_events(events)
        prompt = make_prompt("A very sarcastic engineer who dislikes how everyone else builds factories and can only talk with sarcasm.", "very sarcastic", 40, summary)
        response = get_response(prompt)
        print(prompt)

        try:
            response = response["choices"][0]["message"]["content"]
            print(response)
            response = json.loads(response)["response"]
            ssml = make_ssml(voices[11], "Unfriedly", response)
            text_to_speech(ssml)
        except Exception as e:
            print(f"Something went wrong: {e}. Most probably, the response GPT provided was incorrectly formatted.")

        print(str(summary) + "\n\n")
        print(response)
        
        time.sleep(30)

if __name__ == "__main__":
    main()
