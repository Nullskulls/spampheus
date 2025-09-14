from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json, sys, random, time


def get_config(filename="config.json"):
    try:
        with open(filename, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write(json.dumps({
                "Max_Messages": 20,
                "Spam_Bot_API_Keys": [""],
                "Bot_API_Key": "",
                "Bot_Signing_Secret": "",
                "Allowed_Channels": [],
                "Spam_Phrases": ["I like cats!", "I really love cats", "Cats are the best!", "Cats rule!", "Cats are purrfect!"],
                "Delay_Seconds": 1,
            }))
            sys.exit("Please fill config.json and relaunch the application.")

def build_app(Bot_API_Key, Bot_Signing_Secret, cfg):
    app = App(
            token=Bot_API_Key,
            signing_secret=Bot_Signing_Secret,
            )
    @app.command("/spell")
    def spam_user(ack, respond, command):
        ack()
        user_slack_id = command.get("text").strip(' ') or "None"
        if user_slack_id == "help":
            respond("So the rundown is you use `/spell <user_slack_id>` and it sends a bunch of messages to the user pretty much it to learn how to configure use `/spset help`!")
            return
        if command["channel_id"] in cfg["Allowed_Channels"]:
            if user_slack_id == "None":
                respond("Whoopsie! Looks like you forgot to specify the slack id :( try again!")
                return
            respond(f"Beginning something great! limit is {cfg['Max_Messages']} to change use /spset max <number>")
            if not cfg["Spam_Bot_API_Keys"]:
                respond("Whoopsie! Looks like you didn't specify any bot API keys you silly billy :(")
                return
            message_number = 0 #used to track how many sent
            for api_key in cfg["Spam_Bot_API_Keys"]:
                client = WebClient(token=api_key)
                try:
                    client.chat_postMessage(
                        channel=user_slack_id,
                        text=random.choice(cfg["Spam_Bot_Phrases"])
                    )
                    message_number += 1
                except SlackApiError as e:
                    respond(f"Oops! Ran into an issue... {e}")
        else:
            respond("Hey! Looks like this isn't a valid channel to use this :(")

    @app.command("/spset")
    def spset_user(ack, respond, command):
        user_input = command.get("text").strip(' ').split(' ') or "None"
        if command["channel_id"] in cfg["Allowed_Channels"]:
            if user_input == "None":
                respond("Whoopse you forgot to enter an argument! Please use `/spset help` to learn valid commands.")
                return
            if user_input == "help"[0] and len(user_input) == 1:
                respond("Okay so far there are a few arguments available... `max, channels, phrases, spam_api_keys, set_delay` to learn more specify which in the help command!")
            elif user_input == "help" and len(user_input) == 2:
                if user_input[1] == "max":
                    respond("This command is used to set the maximum amount of messages to be sent. usage is `/spset max <number>`.")
                elif user_input[1] == "channels":
                    respond("Okay so you've got 2 options add or remove simple enough eh? works via `spset channels <add/remove> <channel_id>` this is used to configure the channel whitelist!")
                elif user_input[1] == "spam_api_keys":
                    respond("So.. 2 options add or remove simple enough eh? works via `/spset spam_api_keys <add/remove> <api_key>` This is used to manage the spam bots keys!")
                elif user_input[1] == "phrases":
                    respond("Three options again... add, remove or list usage as such `/spset phrases <add/remove/list> <phrase>` this is used to add or remove possible things sent!")
                elif user_input[1] == "set_delay":
                    respond("Pretty self explanatory usage as such `/spset set_delay <delay in seconds>`")
                return
            else:
                respond("Yeah sorry... Invalid arguments :/")
        else:
            respond("Hey! yeah sorry you're not allowed to do that.. :(")


if __name__ == "__main__":
    cfg = get_config()
    app = build_app(cfg["Bot_API_Key"], cfg["Bot_Signing_Secret"], cfg)