import json
from os import getenv

TOKEN = getenv('TOKEN')


class Guild:
    ID = int(getenv('GUILD'))
    SESSION_LISTINGS = int(getenv('SESSION_LISTINGS'))
    DUNGEON_MASTER = int(getenv('DUNGEON_MASTER'))


class Staging:
    ID = int(getenv('STAGING'))


class Postgres:
    DSN = 'postgres://postgres@database:5432/postgres'


rewards = {
    "player": (100, 100),
    "ondeck": (50, 50),
    "spectator": (25, 0)
}

roleshop = \
        {"true": (25, 0),
         "chaotic": (25, 0),
         "lawful": (25, 0),
         "good": (25, 0),
         "evil": (25, 0),
         "neutral": (25, 0),

         "monk": (50, 0),
         "fighter": (50, 0),
         "bard": (50, 0),
         "druid": (50, 0),
         "rogue": (50, 0),
         "ranger": (50, 0),
         "paladin": (50, 0),
         "warlock": (50, 0),
         "barbarian": (50, 0),
         "cleric": (50, 0),
         "sorcerer": (50, 0),
         "wizard": (50, 0),

         "occult priest": (300, 0),
         "sea urchin": (300, 0),
         "chaotic dumbass": (300, 0),
         "dragon seducer": (300, 0),
         "fireball flinger": (300, 0),
         "dungeon crawler": (300, 0),
         "knife swallower": (300, 0),
         "lady of the night": (300, 0),
         "lord of the night": (300, 0),
         "tiger king": (300, 0),
         "clueless god": (300, 0),

         "tis just a flesh wound": (750, 500),
         "i don't know where i am, and i don't care": (750, 500),
         "i've got a fuckin knife, bitch": (750, 500),
         "probably an npc": (750, 500),
         "kill first, ask questions later": (750, 500),
         "will sell soul for gold": (750, 500),

         "all my 20s are natural": (1000, 750),
         "fuck you, i'm the dm": (1000, 750),

         "fuck you, i was here in the beta": (200, 0)
        }

with open('/static/tags.json') as file:
    tags = json.load(file)
