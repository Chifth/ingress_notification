#!/usr/bin/env python3 -u

import os
import time
import check_mail
import telepot

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

def dosomething(agent, portals):
    print(agent)
    print(portals)

def handle_telegram_message(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        text = message['text']
        print(text)

# Run telepot
if 'TELEGRAM_TOKEN' in os.environ:
    bot = telepot.Bot(os.environ['TELEGRAM_TOKEN'])
    bot.message_loop(handle_telegram_message)

# Run mail checker
check_mail.run(USERNAME, PASSWORD, callback=dosomething)

# Do not end process
while True:
    time.sleep(60)
