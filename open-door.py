import requests
import json
from dotenv import load_dotenv
import os
import sys


def login_csb(user, password):
    session = requests.Session()
    url = 'https://www.chalmersstudentbostader.se/wp-login.php'
    data = {
        'log': user,
        'pwd': password,
        'redirect_to': 'https://www.chalmersstudentbostader.se/min-bostad/'
    }
    r = session.post(url, data=data)
    if "Rikard Legge" not in r.text:
        raise Exception("Failed to login to csb")
    return session


def login_aptus(csb_session):
    link_url = "https://www.chalmersstudentbostader.se/widgets/?callback=cb&widgets%5B%5D=aptuslogin@APTUSPORT"
    response = csb_session.get(link_url)
    data = response.text[3:-2]
    j = json.loads(data)
    apt_url = j["data"]["aptuslogin@APTUSPORT"]["objekt"][0]["aptusUrl"]

    apt_session = requests.Session()
    r = apt_session.get(apt_url)
    if "lockUnlockButton" not in r.text:
        raise Exception("Failed to login to aptus")
    return apt_session


def unlock_door(session, door):
    url = "https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock/UnlockEntryDoor/" + door
    r = session.get(url)
    if "Dörren är upplåst" not in r.text:
        raise Exception("Failed to open door")


def main():
    doors = {
        "80-inne": "123641",
        "80-ute": "123640",
        "82": "123518",
        "84": "123596",
        "86": "123597",
        "88": "123599",
        "90": "123612",
        "92": "123613",
        "94": "123626",
    }

    if len(sys.argv) != 2:
        raise Exception("One argument must be provided and should be the door number")

    load_dotenv()
    user = os.getenv("user")
    password = os.getenv("password")
    door_id = sys.argv[1]
    door = doors[door_id]

    s = login_csb(user, password)
    s = login_aptus(s)
    unlock_door(s, door)


main()


