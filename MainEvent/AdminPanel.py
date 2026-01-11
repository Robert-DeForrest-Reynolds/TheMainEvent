from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Commence import MainEventBot

from asyncio import create_task
from discord import Embed, SelectOption, Interaction, Member, ButtonStyle, File
from discord.ui import View, Button, Modal, Select, TextInput
from os.path import join

class AdminPanel:
	def __init__(Self, User, Interaction, MEReference:MainEventBot) -> None:
		Self.ME = MEReference
		create_task(Self.Send_Admin_Panel(User, Interaction))
		
	
	async def Send_Admin_Panel(Self, User:Member, Interaction:Interaction, InfoType=None, Message=None):
		Self.User:Member = User
		LogMessage = f"{Self.User.name} called for an admin panel"
		
		Self.ME.Logger.log(20, LogMessage)

		AdminView = View(timeout=144000)
		AdminEmbed = Embed(title=f"Welcome, {Self.User.name}, to the Admin Panel")
		AdminDescription = ""
		if Message != None:
			AdminDescription += Message + "\n"
		
		DisplayWeapons = Button(label="Display Weapons", row=0)
		DisplayWeapons.callback = lambda Interaction: create_task(Self.Send_Admin_Panel(User, Interaction, "Weapons"))
		AdminView.add_item(DisplayWeapons)
		
		DisplayAttackMoves = Button(label="Display Attack Moves", row=0)
		DisplayAttackMoves.callback = lambda Interaction: create_task(Self.Send_Admin_Panel(User, Interaction, "Attack Moves"))
		AdminView.add_item(DisplayAttackMoves)
		
		DisplayDefensiveMoves = Button(label="Display Defensive Moves", row=0)
		DisplayDefensiveMoves.callback = lambda Interaction: create_task(Self.Send_Admin_Panel(User, Interaction, "Defensive Moves"))
		AdminView.add_item(DisplayDefensiveMoves)
		
		DisplayDefensiveMoves = Button(label="Add Entry", row=1, style=ButtonStyle.green)
		DisplayDefensiveMoves.callback = lambda Interaction: create_task(Self.Send_Add_Entry_Modal(User, Interaction))
		AdminView.add_item(DisplayDefensiveMoves)
		
		DisplayDefensiveMoves = Button(label="Delete Entry", row=1, style=ButtonStyle.red)
		DisplayDefensiveMoves.callback = lambda Interaction: create_task(Self.Send_Delete_Entry_Modal(User, Interaction))
		AdminView.add_item(DisplayDefensiveMoves)
		
		DiscordFile = None
		if InfoType == "Weapons":
			with open(join("MainEvent", "Data", "Weapons.txt"), "rb") as WeaponsFile:
				DiscordFile = File(WeaponsFile, "Weapons.txt")
		elif InfoType == "Attack Moves":
			with open(join("MainEvent", "Data", "AttackMoves.txt"), "rb") as AttackMovesFile:
				DiscordFile = File(AttackMovesFile, "AttackMoves.txt")
		elif InfoType == "Defensive Moves":
			with open(join("MainEvent", "Data", "AttackMoves.txt"), "rb") as DefensiveMovesFile:
				DiscordFile = File(DefensiveMovesFile, "AttackMoves.txt")

		AdminEmbed.add_field(name="", value=AdminDescription)
		if DiscordFile:
			await Interaction.response.edit_message(view=AdminView, embed=AdminEmbed, attachments=[DiscordFile])
		else:
			await Interaction.response.edit_message(view=AdminView, embed=AdminEmbed)


	async def Send_Add_Entry_Modal(Self, User, Interaction):
		AddEntry = Modal(title="What're we adding?")
		AddEntry.on_submit = lambda Interaction: create_task(Self.Add_Entry(User, Interaction, EntryType.value, Query.value))

		
		EntryType = TextInput(label="w=Weapon | a=Attack Moves | d=Defensive Moves")

		Query = TextInput(label="Entry", row=1)
		
		AddEntry.add_item(EntryType)
		AddEntry.add_item(Query)

		await Interaction.response.send_modal(AddEntry)


	async def Send_Delete_Entry_Modal(Self, User, Interaction):
		DeleteEntry = Modal(title="What're we deleting?")
		DeleteEntry.on_submit = lambda Interaction: create_task(Self.Delete_Entry(User, Interaction, EntryType.value, Query.value))

		
		EntryType = TextInput(label="w=Weapon | a=Attack Moves | d=Defensive Moves")

		Query = TextInput(label="Entry", row=1)
		
		DeleteEntry.add_item(EntryType)
		DeleteEntry.add_item(Query)

		await Interaction.response.send_modal(DeleteEntry)


	async def Add_Entry(Self, User, Interaction, EntryType, Query):
		Failed = False
		Mapping = {
			"w":Self.ME.Weapons,
			"a":Self.ME.AttackMoves,
			"d":Self.ME.DefensiveMoves,
		}
		NameMapping = {
			"w":"weapons",
			"a":"attack moves",
			"d":"defensive moves",
		}
		FileMapping = {
			"w":"Weapons",
			"a":"AttackMoves",
			"d":"DefensiveMoves",
		}

		if Query not in Mapping[EntryType]:
			Mapping[EntryType].append(Query)
		else:
			Failed = True

		if Failed:
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Failed to add {Query} in {NameMapping[EntryType]}, I dunno why, is it already in it?")
		else:
			with open(join("MainEvent", "Data", f"{FileMapping[EntryType]}.txt"), 'w+') as File:
				File.write(f"\n".join(Mapping[EntryType]))
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Added {Query}")


	async def Delete_Entry(Self, User, Interaction, EntryType, Query):
		Failed = False
		Mapping = {
			"w":Self.ME.Weapons,
			"a":Self.ME.AttackMoves,
			"d":Self.ME.DefensiveMoves,
		}
		NameMapping = {
			"w":"weapons",
			"a":"attack moves",
			"d":"defensive moves",
		}
		FileMapping = {
			"w":"Weapons",
			"a":"AttackMoves",
			"d":"DefensiveMoves",
		}

		if Query in Mapping[EntryType]:
			Mapping[EntryType].remove(Query)
		else:
			Failed = True

		if Failed:
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Failed to delete {Query} in {NameMapping[EntryType]}, couldn't find it.")
		else:
			with open(join("MainEvent", "Data", f"{FileMapping[EntryType]}.txt"), 'w+') as File:
				File.write(f"\n".join(Mapping[EntryType]))
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Deleted {Query}")