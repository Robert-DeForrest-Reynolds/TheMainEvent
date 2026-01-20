from sys import exit
if __name__ != "__main__": exit()


from discord import SelectOption, Interaction, Member, Embed
from discord.ui import Select, View

from EverburnLauncher.Library.EverburnBot import EverburnBot
from Bots.MainEvent import MainEvent
from Bots.MainEvent.Panels.Pit import Pit


MainEventBot:EverburnBot = EverburnBot()
ME = MainEvent(MainEventBot)


async def Setup(Self:EverburnBot) -> None:
	MainEventBot.Send("Post setup")
	ME.Channels.update({"Lounge":MainEventBot.Bot.get_channel(1462614581678706739),
						"Pit":MainEventBot.Bot.get_channel(1462614973741137953),
						"Arena":MainEventBot.Bot.get_channel(1462615216733818943)})


async def Select_Activity(Interaction:Interaction, Selection:str):
	if Selection == "Pit":
		Pit(Interaction.user, Interaction, ME)


@MainEventBot.Bot.tree.command(name="challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member):
	ChallengeView = View(timeout=900)
	ChallengeEmbed = Embed(title="Select the fighters")

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


MainEventBot.Setup = Setup

Activities = [SelectOption(label=Activity) for Activity in ["Pit"]]

ActivityChoice = Select(placeholder="👣 Select an Action 👣",
						options=Activities,
						row=2,
						custom_id=f"ActivityChoice")
ActivityChoice.callback = lambda Interaction: Select_Activity(Interaction, Interaction.data["values"][0])

MainEventBot.ViewContent.append(ActivityChoice)

MainEventBot.ProtectedGuildIDs.append(1457557663562072138) # CounterFource Casino

MainEventBot.Bot.run(MainEventBot.Token)

MainEventBot.Send("stopped")
exit()