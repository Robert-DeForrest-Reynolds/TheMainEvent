from sys import exit
if __name__ != "__main__": exit()

from discord import Interaction, Member
from discord import Game as DiscordGame

from Library.EverburnBot import EverburnBot
from Bots.Crucible import Crucible
from Bots.Crucible.Panels.Challenge import Challenge
from Bots.Crucible.Pit import Pit
from Bots.Crucible.Panels.Fighters import Fighters


CrucibleBot:EverburnBot = EverburnBot()
C = Crucible(CrucibleBot)


async def Setup() -> None:
	CrucibleBot.Send("Post setup")
	C.Channels.update({"Lounge":CrucibleBot.Bot.get_channel(1462614581678706739),
						"Pit":CrucibleBot.Bot.get_channel(1462614973741137953),
						"Arena":CrucibleBot.Bot.get_channel(1462615216733818943),
						"Challenges":CrucibleBot.Bot.get_channel(1464681901775392768)})
	C.Pit = Pit(C)
	await CrucibleBot.Bot.change_presence(activity=DiscordGame(f'/{"_" if CrucibleBot.Testing else ""}fighters'), status="Tending the fights.")



@CrucibleBot.Bot.tree.command(name="_challenge" if "Testing" in CrucibleBot.Name else "challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member, wager:float):
	if CrucibleBot.Testing:
		if not await CrucibleBot.Dev_Channel_Gate(Interaction): return
	Challenge(Interaction, challengee, wager, C)


@CrucibleBot.Bot.tree.command(name="_arena" if "Testing" in CrucibleBot.Name else "arena", description="Invoke Crucible's Arena (Admin Only)")
async def arena(Interaction:Interaction, action:str):
	if CrucibleBot.Testing:
		if not await CrucibleBot.Dev_Channel_Gate(Interaction): return
	if Interaction.user.id not in CrucibleBot.Admins: return
	if action == "begin":
		await Interaction.response.send_message("Beginning arena tournament!", ephemeral=True)
	else:
		await Interaction.response.send_message("Invalid action", ephemeral=True, delete_after=5)


@CrucibleBot.Bot.tree.command(name="_fighters" if "Testing" in CrucibleBot.Name else "fighters", description="Manage your Crucible fighters")
async def fighters(Interaction:Interaction):
	if CrucibleBot.Testing:
		if not await CrucibleBot.Dev_Channel_Gate(Interaction): return
	Fighters(Interaction, C)


CrucibleBot.Setup = Setup

CrucibleBot.Bot.run(CrucibleBot.Token)
C.Pit.Alive = False
CrucibleBot.Send("stopped")
C.DB.close()
exit()