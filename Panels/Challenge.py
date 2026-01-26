from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Bots.Crucible.__main__ import Crucible

from discord import Interaction as DiscordInteraction
from discord import Member as DiscordMember
from discord import Embed, SelectOption, ButtonStyle, TextChannel
from discord.ui import Button, Select
from Library.Panel import Panel
from asyncio import create_task


class Challenge(Panel):
	def __init__(Self, Interaction:DiscordInteraction, Opponent:DiscordMember, Wager:float, CrucibleReference:Crucible) -> None:
		super().__init__(Interaction.user, CrucibleReference.Bot)
		Self.Crucible = CrucibleReference
		Self.Opponent = Opponent
		Self.Fighters:dict = None
		Self.Fighter = None
		Self.OpponentFighter = None
		Self.Wager = Wager
		Self.OriginInteraction = Interaction
		Self.Task = create_task(Self.Send_Panel(Interaction))


	async def Send_Panel(Self, Interaction:DiscordInteraction, Edit=False):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title="Select the fighters")
		
		Self.Funds = Self.Bot.Get_Wallet(Interaction.user)

		ChallengerFighters = Self.Crucible.Get_Fighters(Interaction.user)
		Opponentfighters = Self.Crucible.Get_Fighters(Self.Opponent)

		if not Self.Check_Challenges(Self.User):
			Self.Embed.add_field(name="Challenge Error:", value="You have max challenges already (25).")
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed)
			return
		if not Self.Check_Challenges(Self.Opponent):
			Self.Embed.add_field(name="Challenge Error:", value=f"{Self.Opponent.name} has max challenges already (25).")
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed)
			return
		
		if Self.Wager <= 10:
			Self.Embed.title = "Challenge Error"
			Self.Embed.add_field(name="Error:", value="Must have a minimum wager of $10 to submit a challenge.")
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)
			return
		if len(ChallengerFighters) == 0:
			Self.Embed.title = "Challenge Error"
			Self.Embed.add_field(name="Error:", value=f"You have no fighters.")
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)
			return
		if len(Opponentfighters) == 0:
			Self.Embed.title = "Challenge Error"
			Self.Embed.add_field(name="Error:", value=f"{Self.Opponent.name} has no fighters.")
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)
			return

		if Self.Fighter and Self.OpponentFighter:
			Details = f"You have selected **{Self.Fighter}** to fight **{Self.OpponentFighter}** for **${Self.Wager:,.2f}**\n\n"
			Details += "Confirm your challenge now!"
			Self.Embed.add_field(name="May luck be in your favor!", value=Details)

			Confirm = Button(label="Confirm Challenge", style=ButtonStyle.red, row=4)
			Confirm.callback = Self.Confirm_Fight
			Self.View.add_item(Confirm)
		else:
			Details = "Select your fighter.\n\n\n"
			# Details += "Then select the fighter you want to challenge,\n"
			# Details += "or leave it blank to allow them to choose.\n\n"
			Details += "*⁽ᶠᵘʳᵗʰᵉʳ ʳᵉᵍᵘˡᵃᵗᶦᵒⁿˢ ᵒⁿ ᶜʰᵃˡˡᵉⁿᵍᵉˢ ᵃʳᵉ ᵗᵒ ᶜᵒᵐᵉ⁾*"
			Self.Embed.add_field(name="Welcome to the Main Event challenger!", value=Details)

			ChallengerFightersOptions = [SelectOption(label=Name) for Name in ChallengerFighters.keys()]
			OpponentFightersOptions = [SelectOption(label=Name) for Name in Opponentfighters.keys()]

			Self.ChallengerFightersSelect = Select(placeholder="Your fighter...", options=ChallengerFightersOptions, row=0)
			if Self.Fighter: Self.ChallengerFightersSelect.placeholder = Self.Fighter
			Self.ChallengerFightersSelect.callback = Self.Set_Fighter
			Self.View.add_item(Self.ChallengerFightersSelect)

			Self.OpponentFightersSelect = Select(placeholder="Opponent's fighter...", options=OpponentFightersOptions, row=1)
			if Self.OpponentFighter: Self.OpponentFightersSelect.placeholder = Self.OpponentFighter
			Self.OpponentFightersSelect.callback = Self.Set_Opponent_Fighter
			Self.View.add_item(Self.OpponentFightersSelect)


		if Edit:
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		else:
			Self.Message = await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)

	
	def Check_Challenges(Self, Member:DiscordMember) -> bool:
		Self.Crucible.DBCursor.execute(
			"SELECT COUNT(*) FROM Challenges WHERE ChallengerID = ? OR ChallengeeID = ?",
			(Member.id, Member.id)
		)
		ChallengeCount = Self.Crucible.DBCursor.fetchone()[0]
		if ChallengeCount >= 25:
			return False
		else:
			return True
		

	async def Set_Fighter(Self, Interaction:DiscordInteraction):
		Self.Fighter = Self.ChallengerFightersSelect.values[0]
		await Self.Send_Panel(Interaction, Edit=True)
		

	async def Set_Opponent_Fighter(Self, Interaction:DiscordInteraction):
		Self.Fighter = Self.OpponentFightersSelect.values[0]
		await Self.Send_Panel(Interaction, Edit=True)


	async def Confirm_Fight(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title="Challenge Sent")
		Data = [Self.Fighter, Self.OpponentFighter, Self.Wager]
		Self.Crucible.Save_New_Challenge(Self.User, Self.Opponent, Data)
		Self.Embed.add_field(name="Challenge:", value=f"**{Self.Fighter}** vs. **{Self.OpponentFighter}** for **${Self.Wager:,.2f}**")
		await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		ChallengesChannel:TextChannel = Self.Crucible.Channels["Challenges"]
		ChallengeEmbed = Embed(title=f"{Self.User.name} has challenged {Self.Opponent.name}")
		ChallengeEmbed.add_field(name=f"**{Self.Fighter}** vs. **{Self.OpponentFighter}** for ${Self.Wager:,.2f}\n", value="")
		await ChallengesChannel.send(f"{Self.User.mention} ⚔️ {Self.Opponent.mention}\n",embed=ChallengeEmbed)
