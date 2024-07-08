from discord import Intents, Game
from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from discord import Interaction, Member
from discord.ext.commands import Bot, Context
from sys import argv
from os.path import join
from Player import Player
from Arena import Arena
from HorseRacing import HorseRacing
from Activites import Activities


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
        Self.AttackMoves = []
        Self.DefensiveMoves = []

        with open(join("MainEvent", "Attack_Moves.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.AttackMoves.append(Line.strip())

        with open(join("MainEvent", "Defence_Moves.txt"), 'r') as File:
            Lines = File.readlines()
            for Line in Lines:
                Self.DefensiveMoves.append(Line.strip())

        Self.ActivitiesList = [
            "Arena",
            "Horse Racing",
        ]

        Self.AllChallenges = {}

        Self.ProtectedGuildIDs = [
            1127838810097594438, # DeForrest Studios
            1219494686369255444, # Odysseus Strike Force
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


    async def Select_Activity(Self, User:Member, Interaction:Interaction, Selection:str) -> None:
        if Interaction.user != User: return
        
        Mapping = {
            "Arena":Arena,
            "Horse Racing":HorseRacing,
        }

        Mapping[Selection](User, Interaction, Self)


global ME
ME:MainEvent = MainEvent()


# This initial player load will take all of the server members, and turn them into players
def Populate_Players():
    for Member in ME.Bot.get_all_members():
        ME.Players.update({Member.name:Player(Member, ME)})


# This load will load all of the saved challenges
def Load_All_Challenges():
    for MEPlayer in ME.Players.values():
        MEPlayer.Load_Challenges()


@ME.Bot.event
async def on_ready() -> None:
    Message = f"{ME.Bot.user} has connected to Discord!"
    print(Message)
    ME.MainEventLogger.log(20, Message)
    await ME.Bot.change_presence(activity=Game('.me'))


    if ME.Bot.guilds[0].id == 1127838810097594438: # Dev
        ME.DataPath = "DevData"
        ME.Channels.update({"Lounge":ME.Bot.get_channel(1255299478408265808),
                            "Arena":ME.Bot.get_channel(1255299515297169428), 
                            "TrainingGrounds": ME.Bot.get_channel(1255663997718368256)})
    elif ME.Bot.guilds[0].id == 1219494686369255444: # Official
        ME.DataPath = "Data"
        ME.Channels.update({"Lounge":ME.Bot.get_channel(1255673883554484428),
                            "Arena":ME.Bot.get_channel(1255673917545386014), 
                            "TrainingGrounds": ME.Bot.get_channel(1255673944111976509),
                            "HorseRacing": ME.Bot.get_channel(1255673942505689188)})

    Populate_Players()

    Load_All_Challenges()

    ME.MainEventLogger.log(20, ME.Players)


@ME.Bot.command(aliases=["me"])
async def Main_Event(InitialContext:Context) -> None:
    if InitialContext.guild.id not in ME.ProtectedGuildIDs or InitialContext.channel not in ME.Channels.values(): return
    User = InitialContext.message.author
    Activities(User, InitialContext, ME)


ME.Bot.run(ME.Token)