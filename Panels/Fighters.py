from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Bots.Crucible import Crucible as C

from discord import Interaction as DiscordInteraction
from discord import Embed, SelectOption, ButtonStyle
from discord.ui import Button, Modal, Select, TextInput
from asyncio import create_task, sleep
from Library.Panel import Panel

# This needs to be moved later
FighterValue = 300

class Fighters(Panel):
	def __init__(Self, Interaction:DiscordInteraction, CrucibleReference:C) -> None:
		super().__init__(Interaction.user, CrucibleReference.EverburnBot)
		Self.Crucible = CrucibleReference
		Self.Fighters:dict = None
		Self.Challenges:dict = None
		Self.OpposingChallenges:dict = None
		Self.SelectedFighter = None
		Self.SelectedChallenge:str = None
		Self.SelectedOpposingChallenge:str = None
		Self.OriginInteraction = Interaction
		Self.ViewTimeout = 60 * 3
		Self.InvalidName = None
		Self.Task = create_task(Self.Send_Panel(Interaction))


	async def Send_Panel(Self, Interaction:DiscordInteraction, FollowUp=False):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title=f"{Interaction.user}'s Fighter's")
		Self.Funds = Self.EverburnBot.Get_Wallet(Self.User)
		Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
		if Self.InvalidName:
			Self.Embed.add_field(name="Error:", value=f"`{Self.InvalidName}` already exists", inline=False)

		BuyButton = Button(label="Buy Fighter", style=ButtonStyle.green, row=3)
		BuyButton.callback = Self.Check_Funds
		Self.View.add_item(BuyButton)

		if Self.SelectedFighter:
			Self.SelectedFighter = Self.SelectedFighter
			Self.Stats = Self.Fighters[Self.SelectedFighter]
			Details = f"Level: {Self.Stats["Level"]}\n"
			Details += f"Health: {Self.Stats["Health"]}\n"
			Details += f"Power: {Self.Stats["Power"]}\n"
			Details += f"Defense: {Self.Stats["Defense"]}\n"
			Self.Embed.add_field(name=Self.SelectedFighter, value=Details, inline=False)

			SellButton = Button(label="Sell Fighter", style=ButtonStyle.green, row=3)
			SellButton.callback = Self.Sell_Fighter
			Self.View.add_item(SellButton)

		if Self.SelectedChallenge:
			Self.Embed.add_field(name=f"**Challenge Details:**", value="", inline=False)
			Self.SelectedOpposingChallenge = None

			CancelButton = Button(label="Cancel Challenge", style=ButtonStyle.red, row=4)
			CancelButton.callback = Self.Cancel_Challenge
			Self.View.add_item(CancelButton)
		elif Self.SelectedOpposingChallenge:
			Self.Embed.add_field(name=f"**Challenge Details:**", value="", inline=False)
			Self.SelectedChallenge = None

			AcceptButton = Button(label="Accept Challenge", style=ButtonStyle.green, row=4)
			AcceptButton.callback = Self.Accept_Challenge
			Self.View.add_item(AcceptButton)

			RejectButton = Button(label="Reject Challenge", style=ButtonStyle.red, row=4)
			RejectButton.callback = Self.Reject_Challenge
			Self.View.add_item(RejectButton)
			
		await Self.Build_Fighter_Select()
		await Self.Build_Challenge_Select()
		await Self.Build_Opposing_Challenge_Select()
		if FollowUp:
			await Interaction.followup.edit_message(message_id=Interaction.message.id, view=Self.View, embed=Self.Embed)
		else:
			await Interaction.response.send_message(view=Self.View, embed=Self.Embed, ephemeral=True)
		

	async def Check_Funds(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		if not await Self.Check_Fighters_Count():
			Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
			Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
			Self.Embed.add_field(name="You already possess maximum fighters (25)", value="", inline=False)
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
			return
		Self.Funds = Self.EverburnBot.Get_Wallet(Self.User)
		if FighterValue > Self.Funds:
			Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
			Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
			Self.Embed.add_field(name="Insufficient funds.", value="", inline=False)
			await Interaction.response.edit_message(view=Self.View, embed=Self.Embed)
		else:
			await Self.Get_Name_Modal(Interaction)


	async def Select_Fighter(Self, Interaction:DiscordInteraction):
		Self.SelectedFighter = Self.FightersSelect.values[0]
		await Self.Send_Panel(Interaction)


	async def Select_Challenge(Self, Interaction:DiscordInteraction):
		Self.SelectedChallenge = Self.ChallengesSelect.values[0]
		await Self.Send_Panel(Interaction)


	async def Select_Opposing_Challenge(Self, Interaction:DiscordInteraction):
		Self.SelectedOpposingChallenge = Self.OpposingChallengesSelect.values[0]
		await Self.Send_Panel(Interaction)


	async def Build_Fighter_Select(Self):
		Self.Fighters = await Self.Crucible.Get_Fighters(Self.User)
		if len(Self.Fighters) > 0:
			Options = [SelectOption(label=F["Name"]) for F in Self.Fighters.values()]

			Self.FightersSelect = Select(placeholder="Select Fighter...", options=Options, row=0)
			Self.FightersSelect.callback = Self.Select_Fighter
			Self.View.add_item(Self.FightersSelect)


	async def Build_Challenge_Select(Self):
		Self.Challenges = await Self.Crucible.Get_Challenges(Self.User)
		if len(Self.Challenges) > 0:
			Options = [SelectOption(label=f'{C["Challengee"].name}') for C in Self.Challenges.values()]

			Self.ChallengesSelect = Select(options=Options, row=1)
			if Self.SelectedChallenge:
				Self.ChallengesSelect.placeholder = Self.Challenges[Self.SelectedChallenge]['Challengee'].name
			else:
				Self.ChallengesSelect.placeholder = "Your pending challenges..."
			Self.ChallengesSelect.callback = Self.Select_Challenge
			Self.View.add_item(Self.ChallengesSelect)


	async def Build_Opposing_Challenge_Select(Self):
		Self.OpposingChallenges = await Self.Crucible.Get_Opposing_Challenges(Self.User)
		if len(Self.OpposingChallenges) > 0:
			Options = [SelectOption(label=f'{C["Challenger"].name}') for C in Self.OpposingChallenges.values()]

			Self.OpposingChallengesSelect = Select(options=Options, row=2)
			if Self.SelectedOpposingChallenge:
				Self.OpposingChallengesSelect.placeholder = Self.OpposingChallenges[Self.SelectedOpposingChallenge]['Challenger'].name
			else:
				Self.OpposingChallengesSelect.placeholder = "You have opposing challenges..."
			Self.OpposingChallengesSelect.callback = Self.Select_Opposing_Challenge
			Self.View.add_item(Self.OpposingChallengesSelect)

	
	async def Check_Fighters_Count(Self) -> bool:
		Result = await Self.Crucible.DB.Request("SELECT COUNT(*) FROM Fighters WHERE OwnerID = ?",
								 (Self.User.id,))
		FighterCount = Result[0][0]
		if FighterCount >= 25:
			return False
		else:
			return True


	async def Validate_Name(Self, Interaction:DiscordInteraction):
		Result = await Self.Crucible.DB.Request("SELECT 1 FROM Fighters WHERE Name = ? LIMIT 1",
										  (Self.FighterNameSubmission.value,))
		if not Result:
			await Self.Purchase_Fighter(Interaction, Self.FighterNameSubmission.value)
		else:
			Self.InvalidName = Self.FighterNameSubmission.value
			await Self.Send_Panel(Interaction)


	async def Get_Name_Modal(Self, Interaction:DiscordInteraction):
		NameModal = Modal(title="What is your fighter's name?", timeout=Self.ViewTimeout)

		Self.FighterNameSubmission = TextInput(label="Name")
		NameModal.add_item(Self.FighterNameSubmission)

		NameModal.on_submit = Self.Validate_Name

		await Interaction.response.send_modal(NameModal)


	async def Purchase_Fighter(Self, Interaction:DiscordInteraction, Name:str):
		Self.Funds -= FighterValue
		Self.EverburnBot.Transact(Self.User, Self.Funds)
		Self.Funds = Self.EverburnBot.Get_Wallet(Self.User)
		
		Self.EverburnBot.Send(f"{Self.User} purchased a fighter")
		
		Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
		Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
		Self.Embed.add_field(name="Purchased Fighter:", value=Name, inline=False)
		
		await Self.Crucible.Save_New_Fighter(Self.User, Name)
		
		await Interaction.response.defer()
		await Interaction.followup.edit_message(message_id=Interaction.message.id ,view=Self.View, embed=Self.Embed)

		await sleep(5)

		await Self.Send_Panel(Interaction, FollowUp=True)


	async def Sell_Fighter(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return

		Self.Crucible.Delete_Fighter(Self.SelectedFighter)

		Self.EverburnBot.Apply_Wallet(Self.User, Self.Funds + FighterValue)

		Self.EverburnBot.Send(f"{Self.User} sold {Self.SelectedFighter}")
		
		Self.Funds = Self.EverburnBot.Get_Wallet(Self.User)
		Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
		Self.Embed.add_field(name="Wallet", value=f"${Self.Funds:,.2f}", inline=False)
		Self.Embed.add_field(name=f"Sold {Self.SelectedFighter} for {FighterValue}", value="", inline=False)

		Self.SelectedFighter = None
		await Self.Build_Fighter_Select()
		await Interaction.response.defer()
		await Interaction.followup.edit_message(message_id=Interaction.message.id ,view=Self.View, embed=Self.Embed)

		await sleep(5)

		await Self.Send_Panel(Interaction, FollowUp=True)


	async def Accept_Challenge(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
		Self.Embed.add_field(name=f"Accepted Challenge", value=f"Fight will start in the <#{Self.Crucible.Channels["Pit"].id}> soon!", inline=False)

		Challenge = Self.OpposingChallenges.pop(Self.SelectedOpposingChallenge)
		Self.Crucible.Pit.Fights.append(Challenge)
		Self.SelectedOpposingChallenge = None

		await Interaction.response.defer()
		await Interaction.followup.edit_message(message_id=Interaction.message.id ,view=Self.View, embed=Self.Embed)

		await sleep(5)

		await Self.Send_Panel(Interaction, FollowUp=True)


	async def Reject_Challenge(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
		Self.Embed.add_field(name=f"Rejected Challenge", value="", inline=False)

		await Self.Crucible.Delete_Challenge(Self.SelectedOpposingChallenge["ID"])
		Self.SelectedOpposingChallenge = None

		await Interaction.response.defer()
		await Interaction.followup.edit_message(message_id=Interaction.message.id ,view=Self.View, embed=Self.Embed)

		await sleep(5)

		await Self.Send_Panel(Interaction, FollowUp=True)



	async def Cancel_Challenge(Self, Interaction:DiscordInteraction):
		if Interaction.user.id != Self.User.id: return
		await Self.Referesh_Panel()
		Self.Embed = Embed(title=f"{Self.User.name}'s Fighter's")
		Self.Embed.add_field(name=f"Canceled Challenge", value="", inline=False)

		await Self.Crucible.Delete_Challenge(Self.Challenges[Self.SelectedChallenge]["ID"])
		Self.SelectedChallenge = None

		await Interaction.response.defer()
		await Interaction.followup.edit_message(message_id=Interaction.message.id ,view=Self.View, embed=Self.Embed)

		await sleep(5)

		await Self.Send_Panel(Interaction, FollowUp=True)