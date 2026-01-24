from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Bots.MainEvent.__main__ import MainEvent

from discord import Interaction as DiscordInteraction
from discord import Member as DiscordMember
from discord import Embed, SelectOption, ButtonStyle, TextChannel
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task
from Bots.MainEvent.Entities.Fighter import Fighter


class Challenge:
	def __init__(Self, Interaction:DiscordInteraction, Opponent:DiscordMember, Wager:float, MEReference:MainEvent) -> None:
		Self.ME = MEReference
		Self.User = Interaction.user
		Self.Opponent = Opponent
		Self.View = None
		Self.Embed = None
		Self.Fighters:dict = None
		Self.Fighter = None
		Self.OpponentFighter = None
		Self.Wager = Wager
		Self.OriginInteraction = Interaction
		create_task(Self.Send_Panel(Interaction))


	async def Send_Panel(Self, Interaction:DiscordInteraction, Edit=False):
		if Interaction.user.id != Self.User.id: return
		Self.Embed = Embed(title="Select the fighters")
		Self.View = View(timeout=60*5)
		
		Self.Funds = Self.ME.Bot.Get_Wallet(Interaction.user)

		ChallengerFighters = Self.ME.Get_Fighters(Interaction.user)
		Opponentfighters = Self.ME.Get_Fighters(Self.Opponent)

		if len(Opponentfighters) == 0:
			Self.Embed.title = "Challenge Error"
			Self.Embed.add_field(name="Error:", value=f"{Self.Opponent.name} has no fighters")
			if Edit:
				await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
			else:
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
			Details = "Select your fighter, and set a wager.\n"
			Details += "Then select the fighter you want to challenge,\n"
			Details += "or leave it blank to allow them to choose.\n\n"
			Details += "*⁽ᶠᵘʳᵗʰᵉʳ ʳᵉᵍᵘˡᵃᵗᶦᵒⁿˢ ᵒⁿ ᶜʰᵃˡˡᵉⁿᵍᵉˢ ᵃʳᵉ ᵗᵒ ᶜᵒᵐᵉ⁾*"
			Self.Embed.add_field(name="Welcome to the Main Event challenger!", value=Details)

			ChallengerFightersOptions = [SelectOption(label=Name) for Name in ChallengerFighters.keys()]
			OpponentFightersOptions = [SelectOption(label=Name) for Name in Opponentfighters.keys()]

			ChallengerFightersSelect = Select(placeholder="Your fighter...", options=ChallengerFightersOptions, row=0)
			if Self.Fighter: ChallengerFightersSelect.placeholder = Self.Fighter
			ChallengerFightersSelect.callback = lambda Interaction: Self.Set(Interaction, Fighter=ChallengerFightersSelect.values[0])
			Self.View.add_item(ChallengerFightersSelect)

			OpponentFightersSelect = Select(placeholder="Opponent's fighter...", options=OpponentFightersOptions, row=1)
			if Self.OpponentFighter: OpponentFightersSelect.placeholder = Self.OpponentFighter
			OpponentFightersSelect.callback = lambda Interaction: Self.Set(Interaction, OpponentFighter=OpponentFightersSelect.values[0])
			Self.View.add_item(OpponentFightersSelect)

		if Edit:
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		else:
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)


	async def Set(Self, Interaction, Fighter:str=None, OpponentFighter:str=None, Wager:int=None):
		if Fighter:Self.Fighter = Fighter
		elif OpponentFighter: Self.OpponentFighter = OpponentFighter
		elif Wager: Self.Wager = Wager
		await Self.Send_Panel(Interaction, Edit=True)


	async def Confirm_Fight(Self, Interaction:DiscordInteraction):
		Self.View = View(timeout=30)
		Self.Embed = Embed(title="Challenge Sent")
		Data = [Self.Fighter, Self.OpponentFighter, Self.Wager]
		Self.ME.Save_New_Challenge(Self.User, Self.Opponent, Data)
		Self.Embed.add_field(name="Challenge:", value=f"**{Self.Fighter}** vs. **{Self.OpponentFighter}** for **${Self.Wager:,.2f}**")
		await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		ChallengesChannel:TextChannel = Self.ME.Channels["Challenges"]
		ChallengeEmbed = Embed(title=f"{Self.User.name} has challenged {Self.Opponent.name}")
		ChallengeEmbed.add_field(name=f"**{Self.Fighter}** vs. **{Self.OpponentFighter}** for ${Self.Wager:,.2f}\n", value="")
		await ChallengesChannel.send(f"{Self.User.mention} ⚔️ {Self.Opponent.mention}\n",embed=ChallengeEmbed)
