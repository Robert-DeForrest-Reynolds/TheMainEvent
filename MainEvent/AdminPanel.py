from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Commence import MainEvent

from asyncio import create_task
from discord import Embed, SelectOption, Interaction, Member, ButtonStyle
from discord.ui import View, Button, Modal, Select, TextInput

class AdminPanel:
	def __init__(Self, User, Interaction, MEReference:MainEvent) -> None:
		Self.ME = MEReference
		create_task(Self.Send_Admin_Panel(User, Interaction))
		
	
	async def Send_Admin_Panel(Self, User:Member, Interaction:Interaction, InfoType=None, Message=None):
		Self.User:Member = User
		LogMessage = f"{Self.User.name} called for an admin panel"
		
		Self.ME.MainEventLogger.log(20, LogMessage)

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
		
		if InfoType == "Weapons":
			AdminDescription += "Displaying weapons:\n\n"
			for Weapon in Self.ME.Weapons:
				AdminDescription += f"{Weapon}\n"
		elif InfoType == "Attack Moves":
			AdminDescription += "Displaying attack moves:\n\n"
			for Move in Self.ME.AttackMoves:
				AdminDescription += f"{Move}\n"
		elif InfoType == "Defensive Moves":
			AdminDescription += "Displaying defensive moves:\n\n"
			for Move in Self.ME.DefensiveMoves:
				AdminDescription += f"{Move}\n"

		AdminEmbed.add_field(name="", value=AdminDescription)
		
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

		if Query not in Mapping[EntryType]:
			Mapping[EntryType].append(Query)
		else:
			Failed = True

		if Failed:
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Failed to add {Query} in {NameMapping[EntryType]}, I dunno why, is it already in it?")
		else:
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

		if Query in Mapping[EntryType]:
			Mapping[EntryType].remove(Query)
		else:
			Failed = True

		if Failed:
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Failed to delete {Query} in {NameMapping[EntryType]}, couldn't find it.")
		else:
			await Self.Send_Admin_Panel(User, Interaction, Message=f"Deleted {Query}")