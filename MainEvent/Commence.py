from timeit import timeit
from time import perf_counter
from discord import Intents, Game
from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from discord import Interaction, Member
from discord.ext.commands import Bot, Context
from sys import argv
from os.path import join
from Dashboard import Dashboard
from sys import argv


class MainEvent:
    def __init__(Self) -> None:
        # Setup
        Self.Token = argv[1]
        intents = Intents.all()
        intents.message_content = True
        Self.Bot = Bot(command_prefix='.', intents=intents, help_command=None, description='description', case_insensitive=True)
        Self.Members = []
        Self.MainEventLogger:Logger = getLogger('discord')
        Self.MainEventLogger.setLevel(DEBUG)
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

        with open(join("MainEvent", "Weapons.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.Weapons.append(Line.strip())

        with open(join("MainEvent", "Attack_Moves.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.AttackMoves.append(Line.strip())

        with open(join("MainEvent", "Defence_Moves.txt"), 'r') as File:
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
        Self.MainEventLogger.addHandler(Handler)
        Self.MainEventLogger.info("Logger is setup")


Initalization = perf_counter()
global ME
ME:MainEvent = MainEvent()
FinishedInitializing = perf_counter()

print(f"Initialized at {Initalization}, and finished at {FinishedInitializing}")



@ME.Bot.event
async def on_ready() -> None:
    Message = f"{ME.Bot.user} has connected to Discord!"
    ME.MainEventLogger.log(20, Message)
    await ME.Bot.change_presence(activity=Game('.me'))

    
    if ME.KeySelection == "test": # Dev
        ME.DataPath = "DevData"
        ME.Channels.update({"Lounge":ME.Bot.get_channel(1459244861835186247),
                            "Arena":ME.Bot.get_channel(1459244861835186247), 
                            "HorseRacing": ME.Bot.get_channel(1459244861835186247)})
    elif ME.KeySelection == "official": # Official
        print("Loading official data path")
        ME.DataPath = "Data"
        ME.Channels.update({"Lounge":ME.Bot.get_channel(1459082586143068202),
                            "Arena":ME.Bot.get_channel(1459082754754084897),
                            "HorseRacing": ME.Bot.get_channel(1255673942505689188)})

    ME.MainEventLogger.log(20, ME.Players)


@ME.Bot.command(aliases=["me"])
async def Main_Event(InitialContext:Context) -> None:
    if InitialContext.guild.id not in ME.ProtectedGuildIDs or InitialContext.channel not in ME.Channels.values(): return
    User = InitialContext.message.author
    Dashboard(User, InitialContext, ME)


ME.Bot.run(ME.Token)