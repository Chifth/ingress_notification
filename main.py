#!/usr/bin/env python3

import os
import check_mail

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

def dosomething(agent, portals):
    print(agent)
    print(portals)

check_mail.run(USERNAME, PASSWORD, callback=dosomething)
