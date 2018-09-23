import slack, drive

pins = slack.get_general_channel_pins()
print('The pins:')
for pin in pins:
    text = pin['message']['text']
    user = pin['message']['user']
    print(user)
    print(text)
