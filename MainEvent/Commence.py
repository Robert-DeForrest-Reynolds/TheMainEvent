from timeit import timeit
from time import perf_counter
from discord import Game
from discord.ext.commands import Bot, Context
from Dashboard import Dashboard
from MainEventBot import MainEventBot


MainEvent:MainEventBot = MainEventBot()


@MainEvent.Bot.event
async def on_ready() -> None:
    Message = f"{MainEvent.Bot.user} has connected to Discord!"
    MainEvent.Logger.log(20, Message)
    await MainEvent.Bot.change_presence(activity=Game('.me'))

    
    if MainEvent.KeySelection == "test": # Dev
        MainEvent.DataPath = "DevData"
        MainEvent.Channels.update({"Lounge":MainEvent.Bot.get_channel(1459244861835186247),
                            "Arena":MainEvent.Bot.get_channel(1459244861835186247), 
                            "HorseRacing": MainEvent.Bot.get_channel(1459244861835186247)})
    elif MainEvent.KeySelection == "official": # Official
        print("Loading official data path")
        MainEvent.DataPath = "Data"
        MainEvent.Channels.update({"Lounge":MainEvent.Bot.get_channel(1459082586143068202),
                            "Arena":MainEvent.Bot.get_channel(1459082754754084897),
                            "HorseRacing": MainEvent.Bot.get_channel(1255673942505689188)})

    MainEvent.Logger.log(20, MainEvent.Players)


@MainEvent.Bot.command(aliases=["me"])
async def Main_Event(InitialContext:Context) -> None:
    if InitialContext.guild.id not in MainEvent.ProtectedGuildIDs or InitialContext.channel not in MainEvent.Channels.values(): return
    User = InitialContext.message.author
    Dashboard(User, InitialContext, MainEvent)


MainEvent.Bot.run(MainEvent.Token)