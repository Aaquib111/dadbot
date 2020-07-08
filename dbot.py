from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import json
import os
import re

tokens = {}
with open('tokens.json') as json_data:
    tokens = json.load(json_data)

slack_events_adapter = SlackEventAdapter(tokens.get("slack_signing_secret"), "/slack/events")
slack_client = SlackClient(tokens.get("slack_bot_token"))

print(tokens.get("slack_signing_secret"))
print(tokens.get("slack_bot_token"))

REGEX = "(I'm|Im|im|i am|I am) ([^.\,]*)"

HAIL = [
    'all hail dad bot',
    'All hail dad bot',
    'ALL HAIL DAD BOT',
    'all hail dad',
    'All hail dad',
    'ALL HAIL DAD',
    'all hail the creator',
    'All hail the creator',
    'ALL HAIL THE CREATOR'
]

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    reg_match = re.search(REGEX, str(message.get('text')))
    if reg_match != None:
        mes = reg_match.group(2).strip()
    else:
        mes = "Dad!"
    channel = message["channel"]
    if message.get("subtype") is None and mes != "Dad!":
        if mes in HAIL:
            send_message =  "ALL HAIL THE CREATOR, BOW DOWN TO ME CHILDREN"
            slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
        else:
            send_message =  "Hi " + mes + ", I am Dad!"
            slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)
