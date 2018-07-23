import slack, drive

pins = slack.get_general_channel_pins()
print('The pins:')
for pin in pins:
    print(pin['message']['text'])
slack.remove_all_general_channel_pins()
