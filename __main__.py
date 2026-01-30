from sys import exit
if __name__ != "__main__": exit()

from os.path import join

from discord import Interaction, Member

from Library.EverburnBot import EverburnBot as EB
from Library.DB import DB
from Bots.Crucible import Crucible as C
from Bots.Crucible.Panels.Challenge import Challenge
from Bots.Crucible.Pit import Pit
from Bots.Crucible.Panels.Fighters import Fighters


Crucible:C = C()


@Crucible.tree.command(name="_challenge" if Crucible.Testing else "challenge", description="Challenge another player to a fight")
async def challenge(Interaction:Interaction, challengee:Member, wager:float):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	Challenge(Interaction, challengee, wager, Crucible)


@Crucible.tree.command(name="_arena" if Crucible.Testing else "arena", description="Invoke Crucible's Arena (Admin Only)")
async def arena(Interaction:Interaction, action:str):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	if Interaction.user.id not in Crucible.Admins: return
	if action == "begin":
		await Interaction.response.send_message("Beginning arena tournament!", ephemeral=True)
	else:
		await Interaction.response.send_message("Invalid action", ephemeral=True, delete_after=5)


@Crucible.tree.command(name="_fighters" if Crucible.Testing else "fighters", description="Manage your Crucible fighters")
async def fighters(Interaction:Interaction):
	if Crucible.Testing:
		if not await Crucible.Dev_Channel_Gate(Interaction): return
	Fighters(Interaction, Crucible)


Crucible.run(Crucible.Token)
Crucible.Pit.Alive = False
Crucible.DB.Connection.close()
Crucible.DB.Alive = False
exit() # Send rational exit code, no matter. We output any errors to Everburn already