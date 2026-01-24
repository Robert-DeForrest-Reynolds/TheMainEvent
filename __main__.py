from sys import exit
if __name__ != "__main__": exit()

from discord.ext.commands import Context as DiscordContext
from discord import SelectOption, Interaction, Member, Embed
from discord.ui import Select, View

from Library.EverburnBot import EverburnBot
from Bots.MainEvent import MainEvent
from Bots.MainEvent.Panels.Pit import Pit
from Bots.MainEvent.Panels.Challenge import Challenge
from Bots.MainEvent.Panels.SeeFighters import SeeFighters
from Bots.MainEvent.Entities.Fighter import Fighter


MainEventBot:EverburnBot = EverburnBot()
ME = MainEvent(MainEventBot)

async def Setup() -> None:
	MainEventBot.Send("Post setup")
	ME.Channels.update({"Lounge":MainEventBot.Bot.get_channel(1462614581678706739),
						"Pit":MainEventBot.Bot.get_channel(1462614973741137953),
						"Arena":MainEventBot.Bot.get_channel(1462615216733818943),
						"Challenges":MainEventBot.Bot.get_channel(1464681901775392768)})


@MainEventBot.Bot.tree.command(name="challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member, wager:float):
	Challenge(Interaction, challengee, wager, ME)


@MainEventBot.Bot.tree.command(name="arena", description="Invoke Main Event's Arena (Admin Only)")
async def arena(Interaction:Interaction, action:str):
	if Interaction.user.id not in MainEventBot.Admins: return
	if action == "begin":
		await Interaction.response.send_message("Beginning arena tournament!", ephemeral=True)
	else:
		await Interaction.response.send_message("Invalid action", ephemeral=True, delete_after=5)


@MainEventBot.Bot.tree.command(name="fighters", description="Manage your Main Event fighters")
async def fighters(Interaction:Interaction):
	SeeFighters(Interaction.user, Interaction, ME)


MainEventBot.Setup = Setup

MainEventBot.Bot.run(MainEventBot.Token)

MainEventBot.Send("stopped")
ME.DB.close()
exit()