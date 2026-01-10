from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commence import MainEvent

from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Fighter import Fighter
from Challenge import Challenge
from random import randrange

class Arena:
    def __init__(Self, User, Interaction:Interaction, MEReference:MainEvent) -> None:
        Self.ME = MEReference
        Self.SelectedFighter = None
        Self.SelectedOpponentFighter = None
        Self.Target = None
        Self.InsufficientFunds = False
        Self.MaximumFighters = False
        Self.SelectedChallenge = None
        Self.EarlyStop = False
        create_task(Self.Send_Arena_Panel(Interaction))


    async def Stop_Battle(Self, Interaction:Interaction):
        if Interaction.user.id in [713798389908897822, 897410636819083304]:
            BattleView = View(timeout=14400)
            BattleEmbed = Embed(title=f"⚔️ Battle Stopped Early ⚔️")
            Self.EarlyStop = True
            NotificationMessage = await Interaction.channel.send(view=BattleView, embed=BattleEmbed)
            await sleep(4)
            await NotificationMessage.delete()
            await Interaction.message.edit(view=BattleView, embed=BattleEmbed)


    async def Battle(Self, Challenge):
        BattleView = View(timeout=14400)
        BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['ChallengerFighter'].Data['Name']} versus {Challenge.Data['TargetFighter'].Data['Name']} ⚔️")
        TargetDescription = ""
        
        FighterOne = Fighter(Challenge.Data['TargetFighter'].Data['Name'])
        for Key, Value in Challenge.Data['TargetFighter'].Data.items():
            FighterOne.Data[Key] = Value
        FighterTwo = Fighter(Challenge.Data['ChallengerFighter'].Data['Name'])
        for Key, Value in Challenge.Data['ChallengerFighter'].Data.items():
            FighterTwo.Data[Key] = Value

        TargetDescription += f"{FighterOne.Data['Name']}\n"
        TargetDescription += f"💚{FighterOne.Data['Health']}\n"
        TargetDescription += f"💪{FighterOne.Data['Power']}\n"
        TargetDescription += f"🛡️{FighterOne.Data['Defense']}\n"
        
        Clash = "⚔️"

        ChallengerDescription = ""
        ChallengerDescription += f"{FighterTwo.Data['Name']}\n"
        ChallengerDescription += f"💚{FighterTwo.Data['Health']}\n"
        ChallengerDescription += f"💪{FighterTwo.Data['Power']}\n"
        ChallengerDescription += f"🛡️{FighterTwo.Data['Defense']}\n"

        BattleEmbed.add_field(name="\u200b", value=TargetDescription)
        BattleEmbed.add_field(name="\u200b", value=Clash)
        BattleEmbed.add_field(name="\u200b", value=ChallengerDescription)

        Message = await Self.ME.Channels["Arena"].send(view=BattleView, embed=BattleEmbed)

        while FighterOne.Data['Health'] > 0 or FighterTwo.Data['Health'] > 0:
            if Self.EarlyStop == True:
                print("Battle Stopped")
                return
            # Initial 4 second wait
            await sleep(4)

            # Fighter one attacks
            TargetDescription = ""
            ChallengerDescription = ""
            DamageDescription = ""

            FighterOneRoll = randrange(FighterOne.Data["Power"]//4, FighterOne.Data["Power"]+1)
            FighterOneDamage = FighterOneRoll

            FighterTwoWeapon = Self.ME.Weapons[randrange(0, len(Self.ME.Weapons))]
            FighterOneAttackMove = Self.ME.AttackMoves[randrange(0, len(Self.ME.AttackMoves))]

            FighterTwoDefense = randrange(FighterTwo.Data["Defense"]//4, FighterTwo.Data["Defense"]+1)
            FighterTwoDefensiveMove = Self.ME.DefensiveMoves[randrange(0, len(Self.ME.DefensiveMoves))]

            if FighterOneDamage - FighterTwoDefense < FighterOne.Data["Power"]//4: FighterOneDamage = FighterOne.Data["Power"]//4
            else: FighterOneDamage -= FighterTwoDefense

            FighterTwo.Data["Health"] -= FighterOneDamage
            if FighterTwo.Data["Health"] <= 0: break
            
            BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['ChallengerFighter'].Data['Name']} versus {Challenge.Data['TargetFighter'].Data['Name']} ⚔️")
                
            DamageDescription += f"{FighterOne.Data['Name']} rolled {FighterOneRoll}, and {FighterOneAttackMove} with {FighterTwoWeapon} dealing {FighterOneDamage}\n\n"
            DamageDescription += f"{FighterTwo.Data['Name']} defended {FighterTwoDefensiveMove} and blocked {FighterTwoDefense} damage\n\n"

            TargetDescription += f"{FighterOne.Data['Name']}\n"
            TargetDescription += f"💚{FighterOne.Data['Health']}\n"
            TargetDescription += f"💪{FighterOne.Data['Power']}\n"
            TargetDescription += f"🛡️{FighterOne.Data['Defense']}\n"
            
            Clash = "⚔️"

            ChallengerDescription = ""
            ChallengerDescription += f"{FighterTwo.Data['Name']}\n"
            ChallengerDescription += f"💚{FighterTwo.Data['Health']}\n"
            ChallengerDescription += f"💪{FighterTwo.Data['Power']}\n"
            ChallengerDescription += f"🛡️{FighterTwo.Data['Defense']}\n"
            
            BattleEmbed.add_field(name="\u200b", value=DamageDescription, inline=False)
            BattleEmbed.add_field(name="\u200b", value=TargetDescription)
            BattleEmbed.add_field(name="\u200b", value=Clash)
            BattleEmbed.add_field(name="\u200b", value=ChallengerDescription)

            if Self.EarlyStop != True:
                await Message.edit(embed=BattleEmbed)

            # Wait 4 seconds
            await sleep(4)

            ## Now fighter two attacks
            TargetDescription = ""
            ChallengerDescription = ""
            DamageDescription = ""

            BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['ChallengerFighter'].Data['Name']} versus {Challenge.Data['TargetFighter'].Data['Name']} ⚔️")

            FighterTwoRoll = randrange(FighterTwo.Data["Power"]//4, FighterTwo.Data["Power"]+1)
            FighterTwoDamage = FighterTwoRoll

            FighterTwoWeapon = Self.ME.Weapons[randrange(0, len(Self.ME.Weapons))]
            FighterTwoAttackMove = Self.ME.AttackMoves[randrange(0, len(Self.ME.AttackMoves))]

            FighterOneDefense = randrange(FighterOne.Data["Defense"]//4, FighterOne.Data["Defense"]+1)

            FighterOneDefensiveMove = Self.ME.DefensiveMoves[randrange(0, len(Self.ME.DefensiveMoves))]

            if FighterTwoDamage - FighterOneDefense < FighterTwo.Data["Power"]//4: FighterTwoDamage = FighterTwo.Data["Power"]//4
            else: FighterTwoDamage -= FighterOneDefense

            FighterOne.Data["Health"] -= FighterTwoDamage
            if FighterOne.Data["Health"] <= 0: break

            DamageDescription += f"{FighterTwo.Data['Name']} rolled {FighterTwoRoll}, and {FighterTwoAttackMove} with {FighterTwoWeapon} dealing {FighterTwoDamage}\n\n"
            DamageDescription += f"{FighterOne.Data['Name']} defended {FighterOneDefensiveMove} and blocked {FighterOneDefense} damage\n"

            TargetDescription += f"{FighterOne.Data['Name']}\n"
            TargetDescription += f"💚{FighterOne.Data['Health']}\n"
            TargetDescription += f"💪{FighterOne.Data['Power']}\n"
            TargetDescription += f"🛡️{FighterOne.Data['Defense']}\n"
            
            Clash = "⚔️"

            ChallengerDescription += f"{FighterTwo.Data['Name']}\n"
            ChallengerDescription += f"💚{FighterTwo.Data['Health']}\n"
            ChallengerDescription += f"💪{FighterTwo.Data['Power']}\n"
            ChallengerDescription += f"🛡️{FighterTwo.Data['Defense']}\n"


            BattleEmbed.add_field(name="\u200b", value=DamageDescription, inline=False)
            BattleEmbed.add_field(name="\u200b", value=TargetDescription)
            BattleEmbed.add_field(name="\u200b", value=Clash)
            BattleEmbed.add_field(name="\u200b", value=ChallengerDescription)

            if Self.EarlyStop != True:
                await Message.edit(embed=BattleEmbed)

        Winner = None

        if FighterTwo.Data["Health"] <= 0:
            Winner = FighterOne
            Loser = FighterTwo
        if FighterOne.Data["Health"] <= 0:
            Winner = FighterTwo
            Loser = FighterOne
        
        if Winner != None:
            BattleEmbed = Embed(title=f"⚔️ {Winner.Data['Name']} has defeated {Loser.Data['Name']} with 💚{Winner.Data["Health"]} remaining ⚔️")

        if Self.EarlyStop != True:
            StopButton = Button(label="Stop", row=0)
            StopButton.callback = lambda Interaction: Self.Stop_Battle(Interaction)
            BattleView.add_item(StopButton)
            await Message.edit(embed=BattleEmbed)


    async def Get_First_Fighter_Modal(Self, Interaction:Interaction):
        FirstFighterModal = Modal(title="Who is the fighter one?", custom_id="FirstFighterModal")
        FirstFighterModal.on_submit = lambda Interaction: Self.Send_Arena_Panel(Interaction,
                                                                                [FighterOneName,
                                                                                FighterOneHealth.value,
                                                                                FighterOnePower.value,
                                                                                FighterOneDefense.value])

        FighterOneName = TextInput(label="Enter First Fighter's Name")
        FighterOneHealth = TextInput(label="Enter First Fighter's Health")
        FighterOnePower = TextInput(label="Enter First Fighter's Power")
        FighterOneDefense = TextInput(label="Enter First Fighter's Defense")
        
        FirstFighterModal.add_item(FighterOneName)
        FirstFighterModal.add_item(FighterOneHealth)
        FirstFighterModal.add_item(FighterOnePower)
        FirstFighterModal.add_item(FighterOneDefense)

        await Interaction.response.send_modal(FirstFighterModal)


    async def Get_Second_Fighter_Modal(Self, Interaction:Interaction, FighterOneData):
        SecondFighterModal = Modal(title="Who is fighter two?", custom_id="SecondFighterModal")
        SecondFighterModal.on_submit = lambda Interaction: Self.Send_Arena_Panel(Interaction,
                                                                                 FighterOneData,
                                                                                 [FighterTwoName,
                                                                                 FighterTwoHealth.value,
                                                                                 FighterTwoPower.value,
                                                                                 FighterTwoDefense.value])

        FighterTwoName = TextInput(label="Enter Second Fighter's Name")
        FighterTwoHealth = TextInput(label="Enter Second Fighter's Health")
        FighterTwoPower = TextInput(label="Enter Second Fighter's Power")
        FighterTwoDefense = TextInput(label="Enter Second Fighter's Defense")

        SecondFighterModal.add_item(FighterTwoName)
        SecondFighterModal.add_item(FighterTwoHealth)
        SecondFighterModal.add_item(FighterTwoPower)
        SecondFighterModal.add_item(FighterTwoDefense)

        await Interaction.response.send_modal(SecondFighterModal)


    async def Create_Arena_Match(Self, Interaction:Interaction, FighterOneData, FighterTwoData):
        ArenaView = View(timeout=144000)
        ArenaEmbed = Embed(title=f"Fight has begun in the Main-Event-Arena!")
        FighterOne = Fighter(FighterOneData[0])
        FighterTwo = Fighter(FighterTwoData[0])

        FighterOne.Data["Health"] = int(FighterOneData[1])
        FighterOne.Data["Power"] = int(FighterOneData[2])
        FighterOne.Data["Defense"] = int(FighterOneData[3])

        FighterTwo.Data["Health"] = int(FighterTwoData[1])
        FighterTwo.Data["Power"] = int(FighterTwoData[2])
        FighterTwo.Data["Defense"] = int(FighterTwoData[3])

        ArenaChallenge = Challenge(FighterOne, FighterTwo)
        await Interaction.response.edit_message(view=ArenaView, embed=ArenaEmbed)
        await Self.Battle(ArenaChallenge)


    async def Send_Arena_Panel(Self, Interaction:Interaction, FighterOneData=None, FighterTwoData=None):
        ArenaView = View(timeout=144000)
        ArenaEmbed = Embed(title=f"Name your fighters!")

        if FighterOneData != None:
            FighterOneDescription = ""
            FighterOneDescription += f"{FighterOneData[0]}\n"
            FighterOneDescription += f"💚 {FighterOneData[1]}\n"
            FighterOneDescription += f"💪 {FighterOneData[2]}\n"
            FighterOneDescription += f"🛡️ {FighterOneData[3]}\n"
            ArenaEmbed.add_field(name="\u200b", value=FighterOneDescription)
        
        if FighterTwoData != None:
            Clash = "⚔️"

            FighterTwoDescription = ""
            FighterTwoDescription += f"{FighterTwoData[0]}\n"
            FighterTwoDescription += f"💚{FighterTwoData[1]}\n"
            FighterTwoDescription += f"💪{FighterTwoData[2]}\n"
            FighterTwoDescription += f"🛡️{FighterTwoData[3]}\n"

            ArenaEmbed.add_field(name="\u200b", value=Clash)
            ArenaEmbed.add_field(name="\u200b", value=FighterTwoDescription)

        AddFighterOneButton = Button(label="Add Fighter One", row=0)
        AddFighterOneButton.callback = lambda Interaction: Self.Get_First_Fighter_Modal(Interaction)
        ArenaView.add_item(AddFighterOneButton)

        AddFighterTwoButton = Button(label="Add Fighter Two", row=0)
        AddFighterTwoButton.callback = lambda Interaction: Self.Get_Second_Fighter_Modal(Interaction, FighterOneData)
        ArenaView.add_item(AddFighterTwoButton)

        if FighterOneData != None and FighterTwoData != None:
            BattleButton = Button(label="Battle!", row=1)
            BattleButton.callback = lambda Interaction: Self.Create_Arena_Match(Interaction, FighterOneData, FighterTwoData)
            ArenaView.add_item(BattleButton)
        
        await Interaction.response.edit_message(view=ArenaView, embed=ArenaEmbed)