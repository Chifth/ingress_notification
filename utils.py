#!/usr/bin/env python3

import re

def parse_email_lines(lines):
    agent = {}
    portals = []

    # Parse message.
    line = lines.pop(0)
    if line !=  '** Ingress - Begin Transmission**':
        return (agent, portals)

    # Name
    line = lines.pop(0)
    m = re.match('Agent Name:(.*)', line)
    if m:
        agent['name'] = m.group(1)

    # Faction
    line = lines.pop(0)
    m = re.match('Faction:(.*)', line)
    if m:
        agent['faction'] = m.group(1)

    # Level
    line = lines.pop(0)
    m = re.match('Current Level:L(.*)', line)
    if m:
        agent['level'] = m.group(1)

    line = lines.pop(0)
    if line != 'DAMAGE REPORT':
        return (agent, portals)

    while lines[0] !=  '** Ingress - End Transmission **':
        portal = {}
        portal['name'] = lines.pop(0)
        portal['address'] = ''

        # Loop for address
        while True:
            line = lines.pop(0)
            if line.startswith('Portal - '):
                break
            portal['address'] += line

        # Map
        line = lines.pop(0)

        # LINK(S) DESTROYED
        line = lines.pop(0)
        if line == 'LINK DESTROYED' or line == 'LINKS DESTROYED':
            portal['links'] = []
            while True:
                line = lines.pop(0)
                m = re.match('Portal - (.*)', line)
                if m:
                    portal['links'].append(m.group(1))
                if line == 'DAMAGE:':
                    break

        # DAMAGE
        portal['remain'] = '0'
        while True:
            line = lines.pop(0)

            # attacker
            m = re.match('.* destroyed by (.*) at ', line)
            if m:
                portal['attacker'] = m.group(1)

            # remain
            m = re.match('(\d+) Resonators? remaining', line)
            if m:
                portal['remain'] = m.group(1)

            # Break on STATUS
            if line == 'STATUS:':
                break

        # STATUS:
        line = lines.pop(0)
        m = re.match('Level (\d*)', line)
        if m:
            portal['level'] = m.group(1)
        line = lines.pop(0)
        m = re.match('Health: (\d*)%', line)
        if m:
            portal['health'] = m.group(1)
        line = lines.pop(0)
        m = re.match('Owner: (.*)', line)
        if m:
            portal['owner'] = m.group(1)

        # Add portal.
        portals.append(portal)

    return (agent, portals)
