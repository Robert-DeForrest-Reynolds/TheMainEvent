from sys import exit
if __name__ != "__main__": exit()

from os.path import join

from discord import Interaction, Member
from discord import Game as DiscordGame

from Library.EverburnBot import EverburnBot as EB
from Library.DB import DB
from Bots.Crucible import Crucible as C
from Bots.Crucible.Panels.Challenge import Challenge
from Bots.Crucible.Pit import Pit
from Bots.Crucible.Panels.Fighters import Fighters


Crucible:C = C()


async def Setup() -> None:
	Crucible.Send("Post setup")
	Crucible.DB = DB(join("Data", "Crucible.db"), Crucible)
	Crucible.Channels.update({"Lounge":Crucible.Bot.get_channel(1462614581678706739),
						"Pit":Crucible.Bot.get_channel(1462614973741137953),
						"Arena":Crucible.Bot.get_channel(1462615216733818943),
						"Challenges":Crucible.Bot.get_channel(1464681901775392768)})
	Crucible.Pit = Pit(Crucible)
	await Crucible.Bot.change_presence(activity=DiscordGame(f'/{"_" if Crucible.Testing else ""}fighters'), status="Tending the fights.")



@Crucible.Bot.tree.command(name="_challenge" if "Testing" in Crucible.Name else "challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member, wager:float):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	Challenge(Interaction, challengee, wager, Crucible)


@Crucible.Bot.tree.command(name="_arena" if "Testing" in Crucible.Name else "arena", description="Invoke Crucible's Arena (Admin Only)")
async def arena(Interaction:Interaction, action:str):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	if Interaction.user.id not in Crucible.Admins: return
	if action == "begin":
		await Interaction.response.send_message("Beginning arena tournament!", ephemeral=True)
	else:
		await Interaction.response.send_message("Invalid action", ephemeral=True, delete_after=5)


@Crucible.Bot.tree.command(name="_fighters" if "Testing" in Crucible.Name else "fighters", description="Manage your Crucible fighters")
async def fighters(Interaction:Interaction):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	Fighters(Interaction, Crucible)


Crucible.Setup = Setup

Crucible.Bot.run(Crucible.Token)
Crucible.Pit.Alive = False
Crucible.Send("stopped")
Crucible.DB.close()
# Shutdown
# await Self.DBWorker.Queue.put(None)
# Self.DBWorker.Alive = False
exit()