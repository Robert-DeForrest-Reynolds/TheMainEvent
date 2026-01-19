from sys import exit
if __name__ != "__main__": exit()


from os.path import join

from discord.abc import GuildChannel
from discord import app_commands
from discord import SelectOption, Interaction, ForumChannel
from discord.ui import Select
from discord.ext.commands import Context as DiscordContext

from EverburnLauncher.Library.EverburnBot import EverburnBot
from EverburnLauncher.Library.Panel import Panel
from Bots.MainEvent.Pit import Pit


class MainEvent:
	def __init__(Self, Bot:EverburnBot):
		Self.Forums:dict[str:ForumChannel] = {}
		Self.Channels:dict[str:GuildChannel] = {}
		Self.Players = {}
		Self.Weapons = []
		Self.AttackMoves = []
		Self.DefensiveMoves = []
		Self.Bot:EverburnBot = Bot

		with open(join("Bots", "MainEvent", "Data", "Weapons.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.Weapons.append(Line.strip())

		with open(join("Bots", "MainEvent", "Data", "AttackMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.AttackMoves.append(Line.strip())

		with open(join("Bots", "MainEvent", "Data", "DefensiveMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.DefensiveMoves.append(Line.strip())


async def Setup(Self:EverburnBot) -> None:
	MainEventBot.Output("Post setup")
	ME.Channels.update({"Lounge":MainEventBot.Bot.get_channel(1462614581678706739),
						"Pit":MainEventBot.Bot.get_channel(1462614973741137953),
						"Arena":MainEventBot.Bot.get_channel(1462615216733818943)})


async def Select_Activity(Interaction:Interaction, Selection:str):
	if Selection == "Pit":
		Pit(Interaction.user, Interaction, ME)


MainEventBot:EverburnBot = EverburnBot()
ME = MainEvent(MainEventBot)
MainEventBot.Setup = Setup

Activities = [SelectOption(label=Activity) for Activity in ["Pit"]]

ActivityChoice = Select(placeholder="👣 Select an Activity 👣",
						options=Activities,
						row=2,
						custom_id=f"ActivityChoice")
ActivityChoice.callback = lambda Interaction: Select_Activity(Interaction, Interaction.data["values"][0])

MainEventBot.ViewContent.append(ActivityChoice)

MainEventBot.ProtectedGuildIDs.append(1457557663562072138) # CounterFource Casino


@MainEventBot.Bot.tree.command(name="arena", description="Invoke Main Event's Arena (Admin Only)")
async def arena(Interaction:Interaction, action:str):
	if Interaction.user.id not in MainEventBot.Admins: return
	if action == "begin":
		await Interaction.response.send_message("Beginning arena tournament!")
	else:
		await Interaction.response.send_message("Invalid action")


MainEventBot.Bot.run(MainEventBot.Token)

MainEventBot.Output("stopped")
exit()