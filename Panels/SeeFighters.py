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
	def __init__(Self, Interaction:DiscordInteraction, MEReference:MainEvent) -> None:
		Self.ME = MEReference
		Self.User = Interaction.user
		Self.View = None
		Self.Embed = None
		Self.Fighters:dict = None
		Self.SelectedFighter = None
		Self.OriginInteraction = Interaction
		create_task(Self.Send_Panel(Interaction))


	async def Send_Panel(Self, Interaction:DiscordInteraction, SelectedFighter:str=None, InvalidName:str|None=None):
		if Interaction.user.id != Self.User.id: return
		Self.Fighters = Self.ME.Get_Fighters(Self.User)
		Self.View = View(timeout=60*5)
		Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")
		Self.Funds = Self.ME.Bot.Get_Wallet(Interaction.user)
		Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
		if InvalidName:
			Self.Embed.add_field(name="Error:", value=f"`{InvalidName}` already exists", inline=False)

		if SelectedFighter:
			Self.SelectedFighter = SelectedFighter
			Self.Stats = Self.Fighters[Self.SelectedFighter]
			Details = f"Level: {Self.Stats["Level"]}\n"
			Details += f"Health: {Self.Stats["Health"]}\n"
			Details += f"Power: {Self.Stats["Power"]}\n"
			Details += f"Defense: {Self.Stats["Defense"]}\n"
			Self.Embed.add_field(name=SelectedFighter, value=Details, inline=False)

		Options = [SelectOption(label=F["Name"]) for F in Self.Fighters.values()]

		Fighters = Select(placeholder="Select Fighter...", options=Options)
		Fighters.callback = lambda Interaction: Self.Send_Panel(Interaction, SelectedFighter=Fighters.values[0])
		Self.View.add_item(Fighters)

		DashboardButton = Button(label="Buy Fighter", style=ButtonStyle.green, row=4)
		DashboardButton.callback = Self.Check_Funds
		Self.View.add_item(DashboardButton)
		
		await Interaction.response.send_message(view=Self.View, embed=Self.Embed)

	
	def Check_Fighters(Self) -> bool:
		Cursor = Self.ME.DB.cursor()
		Cursor.execute(
			"SELECT COUNT(*) FROM Fighters WHERE OwnerID = ?",
			(Self.User.id,)
		)
		FighterCount = Cursor.fetchone()[0]

		if FighterCount >= 25:
			return False
		else:
			return True
		

	async def Check_Funds(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		if not Self.Check_Fighters():
			Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")
			Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
			Self.Embed.add_field(name="You already possess maximum fighters (25)", value="", inline=False)
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
			return
		Self.Funds = Self.ME.Bot.Get_Wallet(Interaction.user)
		if 300 > Self.Funds:
			Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")
			Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
			Self.Embed.add_field(name="Insufficient funds.", value="", inline=False)
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		else:
			await Self.Get_Name_Modal(Interaction)


	async def Validate_Name(Self, Interaction:DiscordInteraction, Name:str):
		Cursor = Self.ME.DB.cursor()
		Cursor.execute(
			"SELECT 1 FROM Fighters WHERE Name = ? LIMIT 1",
			(Name,)
		)
		Exists = Cursor.fetchone() is not None
		if not Exists:
			await Self.Purchase_Fighter(Interaction, Name)
		else:
			await Self.Send_Panel(Interaction, InvalidName=Name)


	async def Get_Name_Modal(Self, Interaction:DiscordInteraction):
		NameModal = Modal(title="What is your fighter's name?", timeout=60*5)

		Name = TextInput(label="Name")
		NameModal.add_item(Name)

		NameModal.on_submit = lambda Interaction: Self.Validate_Name(Interaction, Name.value)

		await Interaction.response.send_modal(NameModal)


	async def Purchase_Fighter(Self, Interaction:DiscordInteraction, Name:str):
		Self.Funds -= 300
		Self.ME.Bot.Transact(Self.User, Self.Funds)
		Self.Funds = Self.ME.Bot.Get_Wallet(Interaction.user)
		
		Self.ME.Bot.Send(f"{Self.User} purchased a fighter")
		
		Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")
		Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
		Self.Embed.add_field(name="Purchased Fighter:", value=Name, inline=False)
		
		F = Fighter(Name)
		Self.ME.Save_New_Fighter(Interaction.user, F)
		
		await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)