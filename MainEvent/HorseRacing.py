from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep

class HorseRacing:
    def __init__(Self, User, Interaction, MEReference) -> None:
        Self.ME = MEReference
        create_task(Self.Send_Horse_Racing_Panel(User, Interaction))
    
    async def Send_Horse_Racing_Panel(Self, User:Member=None, Interaction:Interaction=None) -> None:
        Self.User:Member = User

        Message = f"{Self.User.name} called for an Horse Racing Panel"
        print(Message)
        Self.ME.MainEventLogger.log(20, Message)

        HorseRacingView = View(timeout=144000)
        HorseRacingEmbed = Embed(title=f"Welcome, {Self.User.name}, to Valor Heights Horse Arena!")

        HorseChoice = Select(placeholder="Select a Horse",
                            options=[SelectOption(label=Horse) for Horse in ["Lewis (Dev)", "Clark (Dev)"]],
                            row=0,
                            custom_id=f"HorseChoice")
        HorseChoice.callback = lambda Interaction: Self.Send_Horse_Racing_Panel(Interaction)
        HorseRacingView.add_item(HorseChoice)

        BuyHorseButton = Button(label="Buy Horse", row=1)
        HorseRacingView.add_item(BuyHorseButton)

        await Interaction.channel.send(view=HorseRacingView, embed=HorseRacingEmbed)
        await Interaction.message.delete()