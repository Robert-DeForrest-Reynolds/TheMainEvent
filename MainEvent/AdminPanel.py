from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commence import MainEvent

from asyncio import create_task
from discord import Embed, SelectOption, Interaction, Member
from discord.ui import View, Button

class AdminPanel:
    def __init__(Self, User, Interaction, MEReference:MainEvent) -> None:
        Self.ME = MEReference
        create_task(Self.Send_Admin_Panel(User, Interaction))
        
	
    async def Send_Admin_Panel(Self, User:Member, Interaction:Interaction):
        Self.User:Member = User
        Message = f"{Self.User.name} called for an admin panel"
        
        Self.ME.MainEventLogger.log(20, Message)

        AdminView = View(timeout=144000)
        AdminEmbed = Embed(title=f"Welcome, {Self.User.name}, to the Admin Panel")
        
        await Interaction.response.edit_message(view=AdminView, embed=AdminEmbed)
