#!/usr/bin/env python3

import os
import time
import telepot
import check_mail
import utils


def handle_email(sender, receiver, subject, message_lines):
    if subject.startswith('Ingress Damage Report: '):
        agent, portals = utils.parse_email_lines(message_lines)
        print(agent)
        for p in portals:
            print(p)


def handle_telegram_message(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        text = message['text']
        print(text)


if __name__ == '__main__':
    # Run mail checker
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    check_mail.run(USERNAME, PASSWORD, callback=handle_email)

    # Run telepot
    if 'TELEGRAM_TOKEN' in os.environ:
        bot = telepot.Bot(os.environ['TELEGRAM_TOKEN'])
        bot.message_loop(handle_telegram_message)

    # Do not end process
    while True:
        time.sleep(60)
