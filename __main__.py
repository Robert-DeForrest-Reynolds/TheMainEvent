from sys import exit
if __name__ != "__main__": exit()

from discord.ext.commands import Context as DiscordContext
from discord import SelectOption, Interaction, Member, Embed
from discord.ui import Select, View

from Library.EverburnBot import EverburnBot
from Bots.MainEvent import MainEvent
from Bots.MainEvent.Panels.Pit import Pit
from Bots.MainEvent.Panels.SeeFighters import SeeFighters
from Bots.MainEvent.Entities.Fighter import Fighter


MainEventBot:EverburnBot = EverburnBot()
ME = MainEvent(MainEventBot)

async def Setup() -> None:
	MainEventBot.Send("Post setup")
	ME.Channels.update({"Lounge":MainEventBot.Bot.get_channel(1462614581678706739),
						"Pit":MainEventBot.Bot.get_channel(1462614973741137953),
						"Arena":MainEventBot.Bot.get_channel(1462615216733818943)})


@MainEventBot.Bot.tree.command(name="challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member):
	ChallengeView = View(timeout=900)
	ChallengeEmbed = Embed(title="Select the fighters")

	# get all fighters of challenger, and challengee
	# get wager, and ensure the challenger has enough for it
	# send it to the database, and to the other player

	Challenger = ME.Players[Interaction.user]
	Opponent = ME.Players[challengee]

	ChallengerFighters = [SelectOption(label=Fighter.Name) for Fighter in Challenger.Fighters]
	OpponentFighters = [SelectOption(label=Fighter.Name) for Fighter in Opponent.Fighters]

	ChallengerFightersSelect = Select(placeholder="Select your fighter", options=ChallengerFighters)
	OpponentFightersSelect = Select(placeholder="Who are they fighting?", options=OpponentFighters)

	ChallengeView.add_item(ChallengerFightersSelect)
	ChallengeView.add_item(OpponentFightersSelect)

	await Interaction.response.send_message("What is your challenge?", view=ChallengeView, embed=ChallengeEmbed)


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