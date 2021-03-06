#!/usr/bin/env python3

import os
import re
import sqlite3
import json


INGRESS_SQLITE_PATH = 'data/ingress.db'

def mkdirp(path):
    try:
        os.makedirs(path, exist_ok=True)
    except IOError as e:
        if e.errno == errno.EACCES:
            print('No permission to create folder "%s"' % path)
        print(e)

def create_database():
    # Create if database not found
    if not os.path.isfile(INGRESS_SQLITE_PATH):
        mkdirp(os.path.dirname(INGRESS_SQLITE_PATH))
        conn = sqlite3.connect(INGRESS_SQLITE_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE log (agent TEXT, portal TEXT, attacker TEXT, timestamp INTEGER, latitude REAL, longitude REAL)')
        c.execute('CREATE TABLE notification (agent TEXT, portal TEXT, address TEXT, nick TEXT, receivers TEXT)')
        conn.commit()
        conn.close()

def insert_log(agent, portal, attacker, timestamp, latitude, longitude):
    # Make sure database exists
    create_database()

    # Insert
    conn = sqlite3.connect(INGRESS_SQLITE_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?)",
            (agent, portal, attacker, timestamp, latitude, longitude))
    conn = sqlite3.connect(INGRESS_SQLITE_PATH)
    conn.commit()
    conn.close()

def insert_notification(agent, portal, address, nick, receivers):
    # Make sure database exists
    create_database()

    # Insert
    conn = sqlite3.connect(INGRESS_SQLITE_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO notification VALUES (?, ?, ?, ?, ?)",
            (agent, portal, address, nick, json.dumps(receivers)))
    conn.commit()
    conn.close()

def get_notifications():
    # Make sure database exists
    create_database()

    # Insert
    conn = sqlite3.connect(INGRESS_SQLITE_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM notification")
    portals = cur.fetchall()
    s = portals[0][4]
    portals = [(p[0], p[1], p[2], p[3], json.loads(p[4])) for p in portals]
    conn.commit()
    conn.close()
    return portals


def parse_email_lines(lines):
    agent = {}
    portals = []

    # Parse message.
    conn = sqlite3.connect(INGRESS_SQLITE_PATH)
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
