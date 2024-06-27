from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Player import Player
from Activites import Activities

class HorseRacing:
    def __init__(Self, User, Interaction, MEReference) -> None:
        Self.ME = MEReference
        create_task(Self.Send_Horse_Racing_Panel(User, Interaction))
    
    async def Send_Horse_Racing_Panel(Self, User:Member=None, Interaction:Interaction=None) -> None:
        Self.User:Member = User
        Self.Player:Player = Self.ME.Players[Self.User.name]

        Message = f"{Self.Player.Data["Nick"]} called for an Horse Racing Panel"
        print(Message)
        Self.ME.MainEventLogger.log(20, Message)

        HorseRacingView = View(timeout=144000)
        HorseRacingEmbed = Embed(title=f"Welcome, {Self.Player.Data["Nick"]}, to Valor Heights Horse Arena!")

        HorseRacingEmbed.add_field(name="\u200b", value=f"👑 {Self.Player.Data["Rank"]:,}", inline=False)
        HorseRacingEmbed.add_field(name="\u200b", value=f"💵 {Self.Player.Data["Wallet"]:,}", inline=False)

        HorseChoice = Select(placeholder="Select a Horse",
                            options=[SelectOption(label=Activity) for Activity in Self.ME.ActivitiesList],
                            row=0,
                            custom_id=f"HorseChoice")
        HorseChoice.callback = lambda Interaction: Self.Send_Horse_Racing_Panel(Interaction)
        HorseRacingView.add_item(HorseChoice)

        BuyHorseButton = Button(label="Buy Horse", row=1)
        HorseRacingView.add_item(BuyHorseButton)

        BackToActivities = Button(label="Back to Activities", row=4)
        BackToActivities.callback = lambda Interaction: Self.Send_Activities(User, Interaction)
        HorseRacingView.add_item(BackToActivities)

        await Interaction.channel.send(view=HorseRacingView, embed=HorseRacingEmbed)
        await Interaction.message.delete()


    async def Send_Activities(Self, User, Interaction): Activities(User, Interaction)