#!/usr/bin/env python
import requests
import os
import util
from util import io

TOKEN_LOCATION = 'api-token.txt'
API_TOKEN = ''

# Access the API token if it exists
if os.path.exists(TOKEN_LOCATION):
    API_TOKEN = util.io.read_text(TOKEN_LOCATION)
# Otherwise prompt for the API token and store it
else:
    API_TOKEN = input('Please enter the API token: ').strip()
    util.io.write_text(TOKEN_LOCATION, API_TOKEN)

def get_all_channels():
    """Returns all channels in the workspace"""
    payload = {'token': API_TOKEN}
    r = requests.get('https://slack.com/api/channels.list', payload)
    json_data = r.json()
    if (not json_data['ok']):
        print('Couldn\'t get all channels')
        print('Reason: ' + json_data['error'])
        return []
    return json_data['channels']

def get_general_channel():
    """Returns just the general channel of the workspace"""
    channels = get_all_channels()
    for channel in channels:
        if (channel['is_general']):
            return channel

def get_general_channel_id():
    """Returns the id of the general channel of the workspace"""
    general_channel = get_general_channel()
    return general_channel['id']

def get_pins_from_channel(id):
    """Returns the pins of the given channel"""
    payload = {'token': API_TOKEN, 'channel': id}
    r = requests.get('https://slack.com/api/pins.list', payload)
    json_data = r.json()
    if (not json_data['ok']):
        print('Couldn\'t get pins from channel id = ' + id)
        print('Reason: ' + json_data['error'])
        return []
    return json_data['items']

def get_general_channel_pins():
    """Returns the pins of the general channel"""
    return get_pins_from_channel(get_general_channel_id())

def remove_pin(channel_id, item):
    """Removes the given pin from the given channel"""
    payload = {'token': API_TOKEN, 'channel': channel_id}
    if (item['type'] == 'message'):
        payload['timestamp'] = item['message']['ts']
    else:
        return False
    r = requests.post('https://slack.com/api/pins.remove', payload)
    json_data = r.json()
    if (not json_data['ok']):
        print('Couldn\'t remove pin')
        print('Reason: ' + json_data['error'])
    return json_data['ok']

def remove_all_pins(channel_id, items):
    """Removes all of the given pins from the given channel"""
    successes = 0
    failures = 0
    for item in items:
        if (remove_pin(channel_id, item)):
            successes += 1
        else:
            failures += 1
    print('Successfully removed ' + str(successes) + ' pins')
    print('Unsuccessfully removed ' + str(failures) + ' pins')

def remove_all_pins_from_channel(id):
    """Removes all of the pins from the given channel"""
    remove_all_pins(id, get_pins_from_channel(id))

def remove_all_general_channel_pins():
    """Removes all of the pins from the general channel"""
    remove_all_pins_from_channel(get_general_channel_id())


remove_all_general_channel_pins()
