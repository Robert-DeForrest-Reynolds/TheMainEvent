from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from discord import Interaction, Member, Intents
from discord.ext.commands import Bot, Context
from sys import argv
from os.path import join


class MainEventBot:
    def __init__(Self) -> None:
        # Setup
        Self.Token = argv[1]
        intents = Intents.all()
        intents.message_content = True
        Self.Bot = Bot(command_prefix='.', intents=intents, help_command=None, description='description', case_insensitive=True)
        Self.Members = []
        Self.Logger:Logger = getLogger('discord')
        Self.Logger.setLevel(DEBUG)
        getLogger('discord.http').setLevel(INFO)
        Self.Channels = {}
        Self.Players = {}
        Self.Weapons = []
        Self.AttackMoves = []
        Self.DefensiveMoves = []
        Self.KeySelection = argv[2]

        Self.Admins = [
            713798389908897822, # Zach
            897410636819083304, # Cavan
        ]

        with open(join("MainEvent", "Data", "Weapons.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.Weapons.append(Line.strip())

        with open(join("MainEvent", "Data", "AttackMoves.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.AttackMoves.append(Line.strip())

        with open(join("MainEvent", "Data", "DefensiveMoves.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.DefensiveMoves.append(Line.strip())

        Self.AllChallenges = {}

        Self.ProtectedGuildIDs = [
            1457557663562072138, # CounterForce Casino
        ]

        # Logging
        Handler = RotatingFileHandler(
            filename='MainEvent.log',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        DateTimeFormat = '%Y-%m-%d %H:%M:%S'
        MainEventFormatter = Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', DateTimeFormat, style='{')
        Handler.setFormatter(MainEventFormatter)
        Self.Logger.addHandler(Handler)
        Self.Logger.info("Logger is setup")