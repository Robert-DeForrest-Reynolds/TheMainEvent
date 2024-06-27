from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Player import Player

class Activities():
    def __init__(Self, User, Interaction, MEReference) -> None:
        Self.ME = MEReference
        create_task(Self.Send_Activities_Panel(User, Interaction))

    async def Send_Activities_Panel(Self, User:Member, Interaction:Interaction):
        Self.User:Member = User
        Self.Player:Player = Self.ME.Players[Self.User.name]
        Message = f"{Self.Player.Data["Nick"]} called for a panel"
        print(Message)
        Self.ME.MainEventLogger.log(20, Message)

        MEView = View(timeout=144000)
        MEEmbed = Embed(title=f"Welcome, {Self.Player.Data["Nick"]}, to the Main Event!")
        MEDescription = ""

        if len(Self.Player.Challenges.keys()) > 0:
            MEEmbed.add_field(name="\u200b", value=f"⚔️ You have been challenged! ⚔️", inline=False)

        MEDescription += f"👑 {Self.Player.Data["Rank"]:,}\n"
        MEDescription += f"💵 {Self.Player.Data["Wallet"]:,}\n"

        ActivityChoice = Select(placeholder="Select an Activity",
                                options=[SelectOption(label=Activity) for Activity in Self.ME.ActivitiesList],
                                row=2,
                                custom_id=f"ActivityChoice")
        ActivityChoice.callback = lambda Interaction: Self.ME.Select_Activity(User, Interaction, Interaction.data["values"][0])
        MEView.add_item(ActivityChoice)

        MEEmbed.add_field(name="\u200b", value=MEDescription, inline=False)
        await Interaction.channel.send(view=MEView, embed=MEEmbed)
        await Interaction.message.delete()