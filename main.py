#!/usr/bin/env python3

import check_mail

USERNAME = 'user@example.com'
PASSWORD = 'yourpassword'

def dosomething(agent, portals):
    print(agent)
    print(portals)

check_mail.run(USERNAME, PASSWORD, callback=dosomething)
