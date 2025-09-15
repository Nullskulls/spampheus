from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json, sys, random, time

users = []

def save_config(filename="config.json", cfg={}):
    if not cfg:
        sys.exit("Hey! It looks like cfg somehow got corrupted? try restarting if that doesn't work delete the config.json file and restart the bot!")
    try:
        with open(filename, 'w') as file:
            file.write(json.dumps(cfg, indent=1))
    except Exception as e:
        sys.exit(f"Error occurred whilst saving config file, Please restart the bot if the error occurs please raise a github issue, ERROR: {e}")

def get_config(filename="config.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write(json.dumps({
                "Max_Messages": 15,
                "Spam_Bot_API_Keys": [""],
                "Bot_API_Key": "",
                "Bot_Signing_Secret": "",
                "Socket_ID": "",
                "Allowed_Channels": [],
                "Spam_Phrases": ["I like cats!", "I really love cats", "Cats are the best!", "Cats rule!", "Cats are purrfect!"],
                "Delay_Seconds": 1,
                "Debugging": "False",
                "Multi_Instance": "True"
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
        cfg = get_config()
        if cfg["Debugging"] == "True":
            respond("Hey there! Since this is in a public channel i set the wait between each message to 6 seconds, no you can't change it.")
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
            if cfg["Multi_Instance"] == "False":
                if command["user_id"] in users:
                    respond("Hey looks like your last spam instance isn't over.. Please wait!")
                    return
                else:
                    users.append(command["user_id"])
            while True:
                for api_key in cfg["Spam_Bot_API_Keys"]:
                    client = WebClient(token=api_key)
                    try:
                        client.chat_postMessage(
                            channel=user_slack_id,
                            text=random.choice(cfg["Spam_Phrases"])
                        )
                        message_number += 1
                        time.sleep(cfg["Delay_Seconds"]/len(cfg["Spam_Bot_API_Keys"]))
                    except SlackApiError as e:
                        respond(f"Oops! Ran into an issue... {e}")
                    if message_number >= cfg["Max_Messages"]:
                        break
                break
            respond(f"{message_number} messages have been sent to {user_slack_id} to hehehe with {len(cfg['Spam_Bot_API_Keys'])} bots!")
            if command["user_id"] in users:
                users.remove(command["user_id"])
        else:
            respond("Hey! Looks like this isn't a valid channel to use this :(")

    @app.command("/spset")
    def spset_user(ack, respond, command):
        ack()
        cfg = get_config()
        if cfg["Debugging"] == "True":
            respond("Hey there! Since this is in a public channel i blocked this command sorry...")
            return
        user_input = command.get("text").strip(' ').split(' ') or "None"
        if command["channel_id"] in cfg["Allowed_Channels"]:
            if user_input == "None":
                respond("Whoopse you forgot to enter an argument! Please use `/spset help` to learn valid commands.")
                return
            if user_input[0] == "help" and len(user_input) == 1:
                respond("Okay so far there are a few arguments available... `max, channels, phrases, spam_api_keys, set_delay` to learn more specify which in the help command!")
            elif user_input[0] == "help" and len(user_input) == 2:
                if user_input[1] == "max":
                    respond("This command is used to set the maximum amount of messages to be sent. usage is `/spset max <number>`.")
                elif user_input[1] == "channels":
                    respond("Okay so you've got 3 options add or remove simple enough eh? works via `spset channels <add/remove/list> <channel_id>` this is used to configure the channel whitelist! channel id is optional when listing btw!")
                elif user_input[1] == "spam_api_keys":
                    respond("So.. 2 options add or remove simple enough eh? works via `/spset spam_api_keys <add/remove> <api_key>` This is used to manage the spam bots keys!")
                elif user_input[1] == "phrases":
                    respond("Three options again... add, remove or list usage as such `/spset phrases <add/remove/list> <phrase>` this is used to add or remove possible things sent! the phrase parameter is optional when listing btw!")
                elif user_input[1] == "set_delay":
                    respond("Pretty self explanatory usage as such `/spset set_delay <delay in seconds>`")
                else:
                    respond("Yeah sorry... Invalid arguments :/")
                return
            elif user_input[0] == "max":
                if len(user_input) == 2:
                    cfg["Max_Messages"] = user_input[1]
                    save_config(cfg=cfg)
                    respond(f"Max Messages has been set to {user_input[1]}")
                else:
                    respond("Hey! It looks like you passed in too many or too few arguments :( To learn more please use `/spset help max`")
                    return
            elif user_input[0] == "channels":
                if user_input[1] == "add":
                    if not len(user_input) == 3:
                        respond("So it looks like you passed in too many or too few params :/ Please use `/spset help channels` for instructions!")
                        return
                    if user_input[1] in cfg["Allowed_Channels"]:
                        respond("Hey... So that channel is already white listed :)")
                        return
                    cfg["Allowed_Channels"].append(user_input[2])
                    save_config(cfg=cfg)
                    return
                elif user_input[1] == "remove":
                    if not len(user_input) == 3:
                        respond("Hey so it looks like you passed in too little or too few params :/ Please use `/spset help channels` for instructions!")
                        return
                    if not user_input[1] in cfg["Allowed_Channels"]:
                        respond("Okay so you're currently trying to remove a channel not even in the white list :(")
                        return
                    cfg["Allowed_Channels"].remove(user_input[1])
                    respond("Removed successfully :)")
                elif user_input[1] == "list":
                    message = "*ALLOWED CHANNELS*\n"
                    for channel in cfg["Allowed_Channels"]:
                        message += f"{channel}\n"
                    message += "~That's all~"
                    respond(message)
                else:
                    respond("Soo yeah... Invalid arguments :/")
            elif user_input[0] == "spam_api_keys":
                if not len(user_input) == 3:
                    respond("Hey.. So you either added too many or too few params :/ please view `/spset help spam_api_keys` for instructions!")
                    return
                if user_input[1] == "add":
                    if user_input[2] in cfg["Spam_Bot_API_Keys"]:
                        respond("Hey.. so That bot is already in the legion...")
                        return
                    cfg["Slack_Bot_API_Keys"].append(user_input[2])
                    save_config(cfg=cfg)
                    respond("Added successfully :D")
                elif user_input[1] == "remove":
                    if not user_input[2] in cfg["Spam_Bot_API_Keys"]:
                        respond("Hey so yeah... You're trying to remove a bot that isn't in the legion...")
                        return
                    cfg["Slack_Bot_API_Keys"].remove(user_input[2])
                    save_config(cfg=cfg)
                    respond("Removed successfully :)")
                elif user_input[1] == "list":
                    respond("sorry ye i'm not leaking my keys :/")
                else:
                    respond("Sorry invalid arguments :( Please use `/spset help spam_api_keys` for instructions!")
            elif user_input[0] == "set_delay":
                if not len(user_input) == 2:
                    respond("Too many or too few arguments :/ Please use `/spset help set_delay` for instructions!")
                    return
                cfg["Delay_Seconds"] = user_input[1]
                save_config(cfg=cfg)
                respond(f"Delay seconds has been set to {user_input[1]}!")
            elif user_input[0] == "phrases":
                respond("Ye i dont feel like doing this rn sorry lol")
            else:
                respond("Invalid arguments :/ please use `/spset help` for instructions!")
        else:
            respond("Hey! yeah sorry you're not allowed to do that.. :(")
    return app


if __name__ == "__main__":
    cfg = get_config()
    app = build_app(cfg["Bot_API_Key"], cfg["Bot_Signing_Secret"], cfg)
    handler = SocketModeHandler(app, cfg["Socket_ID"])
    handler.start()