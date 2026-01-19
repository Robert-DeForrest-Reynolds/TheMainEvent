from sys import exit
if __name__ != "__main__": exit()


from os.path import join

from EverburnLauncher.Library.EverburnBot import EverburnBot
from EverburnLauncher.Library.Panel import Panel

from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Bots.MainEvent.Pit import Pit

class MainEvent:
	def __init__(Self, Bot:EverburnBot):
		Self.Channels = {}
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


async def Select_Activity(Interaction:Interaction, Selection:str):
	print(Selection)
	if Selection == "Pit":
		Pit(Interaction.user, Interaction, ME)



async def Setup(Self:EverburnBot) -> None:
	MainEventBot.Output("Post setup")


MainEventBot:EverburnBot = EverburnBot()
ME = MainEvent(MainEventBot)
MainEventBot.Setup = Setup

Activities = [SelectOption(label=Activity) for Activity in ["Arena", "Pit"]]

ActivityChoice = Select(placeholder="👣 Select an Activity 👣",
						options=Activities,
						row=2,
						custom_id=f"ActivityChoice")
ActivityChoice.callback = lambda Interaction: Select_Activity(Interaction, Interaction.data["values"][0])

MainEventBot.ViewContent.append(ActivityChoice)

MainEventBot.ProtectedGuildIDs.append(1457557663562072138) # CounterFource Casino

MainEventBot.Bot.run(MainEventBot.Token)

MainEventBot.Output("stopped")
exit()