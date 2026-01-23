from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Bots.MainEvent.__main__ import MainEvent

from discord import Interaction as DiscordInteraction
from discord import Member as DiscordMember
from discord import Embed, SelectOption, ButtonStyle
from discord import Message as DiscordMessage
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Bots.MainEvent.Entities.Fighter import Fighter
from random import randrange


class SeeFighters:
	def __init__(Self, User:DiscordMember, Interaction:DiscordInteraction, MEReference:MainEvent) -> None:
		Self.ME = MEReference
		Self.User = User
		Self.View = None
		Self.Embed = None
		create_task(Self.Send_Panel(Interaction))


	async def Send_Panel(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		Self.View = View(timeout=144000)
		Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")

		DashboardButton = Button(label="Buy Fighter", style=ButtonStyle.blurple, row=4)
		DashboardButton.callback = Self.Purchase_Fighter
		Self.View.add_item(DashboardButton)
		
		await Interaction.response.send_message(view=Self.View, embed=Self.Embed)


	async def Purchase_Fighter(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		Self.ME.Bot.Send(f"{Self.User} purchased a fighter")
		if Self.ME.Bot.Transact(Interaction.user, 300):
			Self.Embed.add_field(name="Wallet", value=f"${Self.ME.Bot.Get_Wallet(Interaction.user):,.2f}", inline=False)
			Self.Embed.add_field(name="Purchased Fighter:", value="Fighter Details", inline=False)
		else:
			Self.Embed.add_field(name="Insufficient funds.", value="Fighter Details", inline=False)
		await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)