from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commence import MainEventBot

from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Arena import Arena
from HorseRacing import HorseRacing
from AdminPanel import AdminPanel

class Dashboard:
    def __init__(Self, User, Interaction, MEReference:MainEventBot) -> None:
        Self.ME = MEReference
        Self.ActivitiesList = [
            "Horse Racing",
        ]
        create_task(Self.Send_Activities_Panel(User, Interaction))

    async def Send_Activities_Panel(Self, User:Member, Interaction:Interaction):
        Self.User:Member = User
        Message = f"{Self.User.name} called for a dashboard"
        
        Self.ME.Logger.log(20, Message)

        MEView = View(timeout=144000)
        MEEmbed = Embed(title=f"Welcome, {Self.User.name}, to the Main Event!")
        MEDescription = ""

        Activities = [SelectOption(label=Activity) for Activity in Self.ActivitiesList]
        
        if User.id in Self.ME.Admins:
            Activities.append(SelectOption(label="Arena"))
            Activities.append(SelectOption(label="Admin Panel"))

        ActivityChoice = Select(placeholder="Select an Activity",
                                options=Activities,
                                row=2,
                                custom_id=f"ActivityChoice")
        ActivityChoice.callback = lambda Interaction: Self.Select_Activity(User, Interaction, Interaction.data["values"][0])
        MEView.add_item(ActivityChoice)

        MEEmbed.add_field(name="\u200b", value=MEDescription, inline=False)
        await Interaction.channel.send(view=MEView, embed=MEEmbed)
        await Interaction.message.delete()

    
    async def Select_Activity(Self, User:Member, Interaction:Interaction, Selection:str) -> None:
        if Interaction.user != User: return
        
        Mapping = {
            "Arena":Arena,
            "Horse Racing":HorseRacing,
            "Admin Panel":AdminPanel,
        }

        Activity = Mapping[Selection]

        Activity(User, Interaction, Self.ME)