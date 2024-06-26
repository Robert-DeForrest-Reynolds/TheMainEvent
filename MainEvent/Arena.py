from discord import Embed, SelectOption, Interaction, Member
from discord.ui import Button, Modal, Select, TextInput, View
from asyncio import create_task, sleep
from Player import Player
from Fighter import Fighter
from Challenge import Challenge
from random import randrange
from Activites import Activities

class Arena:
    def __init__(Self, User, Interaction, MEReference) -> None:
        Self.ME = MEReference
        Self.SelectedFighter = None
        Self.SelectedOpponentFighter = None
        Self.Target = None
        Self.InsufficientFunds = False
        Self.MaximumFighters = False
        Self.SelectedChallenge = None
        create_task(Self.Send_Arena_Panel(User, Interaction))

    
    async def Battle(Self, Challenge, Exhibition=False):
        if Exhibition == True:
            BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['ChallengerFighter'].Data['Name']} versus {Challenge.Data['TargetFighter'].Data['Name']} ⚔️")
        else:
            BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['Target'].Data['Name']} versus {Challenge.Data['Challenger'].Data['Name']} ⚔️")
        TargetDescription = ""
        
        FighterOne = Fighter(Challenge.Data['TargetFighter'].Data['Name'])
        for Key, Value in Challenge.Data['TargetFighter'].Data.items():
            FighterOne.Data[Key] = Value
        FighterTwo = Fighter(Challenge.Data['ChallengerFighter'].Data['Name'])
        for Key, Value in Challenge.Data['ChallengerFighter'].Data.items():
            FighterTwo.Data[Key] = Value

        TargetDescription += f"{FighterOne.Data['Name']}\n"
        if Exhibition == False:
            TargetDescription += f"💠{FighterOne.Data['Level']}\n"
        TargetDescription += f"💚{FighterOne.Data['Health']}\n"
        TargetDescription += f"💪{FighterTwo.Data['Power']}\n"
        TargetDescription += f"🛡️{FighterOne.Data['Defense']}\n"
        if Exhibition == False:
            TargetDescription += f"🏆{FighterOne.Data['Wins']}\n"
            TargetDescription += f"💀{FighterOne.Data['Losses']}\n"
        
        Clash = "⚔️"

        ChallengerDescription = ""
        ChallengerDescription += f"{FighterTwo.Data['Name']}\n"
        if Exhibition == False:
            ChallengerDescription += f"💠{FighterTwo.Data['Level']}\n"
        ChallengerDescription += f"💚{FighterTwo.Data['Health']}\n"
        ChallengerDescription += f"💪{FighterTwo.Data['Power']}\n"
        ChallengerDescription += f"🛡️{FighterTwo.Data['Defense']}\n"
        if Exhibition == False:
            ChallengerDescription += f"🏆{FighterTwo.Data['Wins']}\n"
            ChallengerDescription += f"💀{FighterTwo.Data['Losses']}\n"

        BattleEmbed.add_field(name="\u200b", value=TargetDescription)
        BattleEmbed.add_field(name="\u200b", value=Clash)
        BattleEmbed.add_field(name="\u200b", value=ChallengerDescription)

        Message = await Self.ME.Channels["Arena"].send(embed=BattleEmbed)

        while FighterOne.Data['Health'] > 0 or FighterTwo.Data['Health'] > 0:
            TargetDescription = ""
            ChallengerDescription = ""
            DamageDescription = ""
            await sleep(7)
            FighterOneDefense = randrange(1, FighterOne.Data["Defense"]+1) 
            FighterTwoDefense = randrange(1, FighterTwo.Data["Defense"]+1) 

            FighterOneDamage = randrange(1, FighterOne.Data["Power"]+1)
            FighterTwoDamage = randrange(1, FighterTwo.Data["Power"]+1)

            FighterOneAttackMove = Self.ME.AttackMoves[randrange(0, len(Self.ME.AttackMoves))]
            FighterTwoAttackMove = Self.ME.AttackMoves[randrange(0, len(Self.ME.AttackMoves))]

            FighterOneDefensiveMove = Self.ME.DefensiveMoves[randrange(0, len(Self.ME.DefensiveMoves))]
            FighterTwoDefensiveMove = Self.ME.DefensiveMoves[randrange(0, len(Self.ME.DefensiveMoves))]

            if FighterOneDamage - FighterTwoDefense < 0: FighterOneDamage = 0
            else: FighterOneDamage -= FighterTwoDefense

            if FighterTwoDamage - FighterOneDefense < 0: FighterTwoDamage = 0
            else: FighterTwoDamage -= FighterOneDefense

            FighterTwo.Data["Health"] -= FighterOneDamage
            if FighterTwo.Data["Health"] <= 0: break
            
            FighterOne.Data["Health"] -= FighterTwoDamage
            if FighterOne.Data["Health"] <= 0: break

            if Exhibition == True:
                BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['ChallengerFighter'].Data['Name']} versus {Challenge.Data['TargetFighter'].Data['Name']} ⚔️")
            else:
                BattleEmbed = Embed(title=f"⚔️ {Challenge.Data['Target'].Data['Name']} versus {Challenge.Data['Challenger'].Data['Name']} ⚔️")
                
            DamageDescription += f"{FighterOne.Data['Name']} {FighterOneAttackMove} and dealt {FighterOneDamage}\n"
            DamageDescription += f"{FighterTwo.Data['Name']} defended {FighterTwoDefensiveMove} and blocked {FighterTwoDefense} damage\n\n"

            DamageDescription += f"{FighterTwo.Data['Name']} {FighterTwoAttackMove} and dealt {FighterTwoDamage}\n"
            DamageDescription += f"{FighterOne.Data['Name']} defended {FighterOneDefensiveMove} and blocked {FighterOneDefense} damage\n"

            TargetDescription += f"{FighterOne.Data['Name']}\n"
            if Exhibition == False:
                TargetDescription += f"💠{FighterOne.Data['Level']}\n"
            TargetDescription += f"💚{FighterOne.Data['Health']}\n"
            TargetDescription += f"💪{FighterTwo.Data['Power']}\n"
            TargetDescription += f"🛡️{FighterOne.Data['Defense']}\n"
            if Exhibition == False:
                TargetDescription += f"🏆{FighterOne.Data['Wins']}\n"
                TargetDescription += f"💀{FighterOne.Data['Losses']}\n"
            
            Clash = "⚔️"

            ChallengerDescription = ""
            ChallengerDescription += f"{FighterTwo.Data['Name']}\n"
            if Exhibition == False:
                ChallengerDescription += f"💠{FighterTwo.Data['Level']}\n"
            ChallengerDescription += f"💚{FighterTwo.Data['Health']}\n"
            ChallengerDescription += f"💪{FighterTwo.Data['Power']}\n"
            ChallengerDescription += f"🛡️{FighterTwo.Data['Defense']}\n"
            if Exhibition == False:
                ChallengerDescription += f"🏆{FighterTwo.Data['Wins']}\n"
                ChallengerDescription += f"💀{FighterTwo.Data['Losses']}\n"
            BattleEmbed.add_field(name="\u200b", value=DamageDescription, inline=False)
            BattleEmbed.add_field(name="\u200b", value=TargetDescription)
            BattleEmbed.add_field(name="\u200b", value=Clash)
            BattleEmbed.add_field(name="\u200b", value=ChallengerDescription)

            await Message.edit(embed=BattleEmbed)
        Winner = None

        if FighterTwo.Data["Health"] <= 0:
            Winner = FighterOne
            Loser = FighterTwo
        if FighterOne.Data["Health"] <= 0:
            Winner = FighterTwo
            Loser = FighterOne
        
        BattleEmbed = Embed(title=f"⚔️ {Winner.Data['Name']} has defeated {Loser.Data['Name']} ⚔️")
        await Message.edit(embed=BattleEmbed)


    async def Buy_Fighter(Self, Interaction):
        if Self.Player.Data["Wallet"] >= 1200:
            DefaultName = f"Fighter{len(Self.Player.Fighters)+1}"
            NewFighter = Fighter(DefaultName)
            Self.Player.Fighters.update({DefaultName:NewFighter})
            Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - 1200, 2)
            await Self.Player.Save_Data()
            await Self.Player.Save_Fighters()
        elif len(Self.Player.Fighters.values()) + 1 > 25:
            Self.MaximumFighters = True
        else:
            Self.InsufficientFunds = True
        await Self.Send_Arena_Panel(Self.User, Interaction)


    async def Select_Fighter(Self, Interaction):
        Self.SelectedFighter = Self.Player.Fighters[Interaction.data["values"][0]]
        await Self.Send_Arena_Panel(Self.User, Interaction)


    async def Send_Change_Name_Modal(Self, Interaction:Interaction):
        Self.ChangeNameModal = Modal(title="Change Facility Name", custom_id="Modal")
        Self.ChangeNameModal.on_submit = lambda Interaction: Self.Change_Fighter_Name(Interaction, Self.FighterNaSelf.ME.value)

        Self.FighterName = TextInput(label="Enter new fighter name:")
        Self.ChangeNameModal.add_item(Self.FighterName)

        await Interaction.response.send_modal(Self.ChangeNameModal)


    async def Change_Fighter_Name(Self, Interaction, NewFighterName):
        if NewFighterName in Self.Player.Fighters.keys(): return
        Self.SelectedFighter.Data["Name"] = NewFighterName
        await Self.Player.Save_Fighters()
        await Self.Send_Arena_Panel(Self.User, Interaction)


    async def Send_Select_Challenge_Target_Modal(Self, Interaction:Interaction):
        SelectTargetModal = Modal(title="Who are you challenging?", custom_id="Modal")
        SelectTargetModal.on_submit = lambda Interaction: Self.Send_Challenge_Panel(Interaction, TargetName=TargetName)

        TargetName = TextInput(label="Enter a user's name")
        SelectTargetModal.add_item(TargetName)

        await Interaction.response.send_modal(SelectTargetModal)


    async def Select_Challenge_Fighter(Self, Interaction):
        Self.SelectedFighter = Self.Player.Fighters[Interaction.data["values"][0]]
        await Self.Send_Challenge_Panel(Interaction)


    async def Select_Challenge_Opponent_Fighter(Self, Interaction):
        Self.SelectedOpponentFighter = Self.ME.Players[Self.TargetName].Fighters[Interaction.data["values"][0]]
        await Self.Send_Challenge_Panel(Interaction)


    async def Send_Challenge_Panel(Self, Interaction:Interaction, TargetName=None):
        if TargetName != None: Self.TargetName = TargetName
        Message = f"{Interaction.message.author} called for a Challenge Panel"
        print(Message)
        Self.Target:Player = Self.ME.Players[Self.TargetName]
        Self.ME.MainEventLogger.log(20, Message)

        ChallengeView = View(timeout=144000)
        ChallengeEmbed = Embed(title=f"⚔️ Welcome, {Self.Player.Data["Name"]}! Challenge, Fight, Win! ⚔️")
        ChallengeDescription = ""

        FighterChoice = Select(placeholder="Select a Fighter",
                               options=[SelectOption(label=Fighter) for Fighter in Self.Player.Fighters],
                               row=0,
                               custom_id=f"FighterChoice")
        FighterChoice.callback = lambda Interaction: Self.Select_Challenge_Fighter(Interaction)
        ChallengeView.add_item(FighterChoice)

        OpponentFighterChoice = Select(placeholder="Select an Opponents Fighter",
                               options=[SelectOption(label=Fighter) for Fighter in Self.ME.Players[Self.TargetName].Fighters],
                               row=1,
                               custom_id=f"OpponentFighterChoice")
        OpponentFighterChoice.callback = lambda Interaction: Self.Select_Challenge_Opponent_Fighter(Interaction)
        ChallengeView.add_item(OpponentFighterChoice)

        if Self.SelectedFighter != None: FighterChoice.placeholder = Self.SelectedFighter.Data["Name"]
        if Self.SelectedOpponentFighter != None: OpponentFighterChoice.placeholder = Self.SelectedOpponentFighter.Data["Name"]

        SubmitChallengeButton = Button(label="Submit Challenge", row=2)
        SubmitChallengeButton.callback = lambda Interaction: Self.Challenge(Interaction)
        ChallengeView.add_item(SubmitChallengeButton)

        await Interaction.response.edit_message(view=ChallengeView, embed=ChallengeEmbed)


    async def Challenge(Self, Interaction):
        NewChallenge = Challenge(Self.Player, Self.SelectedFighter, Self.Target, Self.SelectedOpponentFighter)
        Self.Target.Challenges.update({Self.Player.Data["Name"]:NewChallenge})
        Self.SelectedFighter = None
        Self.SelectedOpponentFighter = None
        await Self.Target.Save_Challenges()
        await Self.Send_Arena_Panel(Self.User, Interaction)


    async def Select_Challenge(Self, Interaction):
        Self.SelectedChallenge = Self.Player.Challenges[Interaction.data["values"][0]]
        await Self.Send_Arena_Panel(Self.User, Interaction)


    async def Accept_Challenge(Self, Interaction:Interaction, Challenge):
        await Self.ME.Channels["Arena"].send(content=f"{Challenge.Data['Target'].Data['MemberReference'].mention} accepted {Challenge.Data['Challenger'].Data['MemberReference'].mention}'s challenge!")
        await Self.Send_Arena_Panel(Self.User, Interaction)
        await Self.Battle(Challenge)


    async def Get_First_Fighter_Modal(Self, Interaction:Interaction):
        FirstFighterModal = Modal(title="Who is the fighter one?", custom_id="FirstFighterModal")
        FirstFighterModal.on_submit = lambda Interaction: Self.Send_Exhibition_Panel(Interaction, [FighterOneName, FighterOneHealth.value, FighterOnePower.value, FighterOneDefense.value])

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
        SecondFighterModal.on_submit = lambda Interaction: Self.Send_Exhibition_Panel(Interaction, FighterOneData, [FighterTwoName, FighterTwoHealth.value, FighterTwoPower.value, FighterTwoDefense.value])

        FighterTwoName = TextInput(label="Enter Second Fighter's Name")
        FighterTwoHealth = TextInput(label="Enter Second Fighter's Health")
        FighterTwoPower = TextInput(label="Enter Second Fighter's Power")
        FighterTwoDefense = TextInput(label="Enter Second Fighter's Defense")

        SecondFighterModal.add_item(FighterTwoName)
        SecondFighterModal.add_item(FighterTwoHealth)
        SecondFighterModal.add_item(FighterTwoPower)
        SecondFighterModal.add_item(FighterTwoDefense)

        await Interaction.response.send_modal(SecondFighterModal)


    async def Create_Exhibition_Match(Self, FighterOneData, FighterTwoData):
        FighterOne = Fighter(FighterOneData[0])
        FighterTwo = Fighter(FighterTwoData[0])

        FighterOne.Data["Health"] = int(FighterOneData[1])
        FighterOne.Data["Power"] = int(FighterOneData[2])
        FighterOne.Data["Defense"] = int(FighterOneData[3])

        FighterTwo.Data["Health"] = int(FighterTwoData[1])
        FighterTwo.Data["Power"] = int(FighterTwoData[2])
        FighterTwo.Data["Defense"] = int(FighterTwoData[3])

        ExhibitionChallenge = Challenge(None, FighterOne, None, FighterTwo, Exhibition=True)
        await Self.Battle(ExhibitionChallenge, Exhibition=True)


    async def Send_Exhibition_Panel(Self, Interaction, FighterOneData=None, FighterTwoData=None):
        ExhibitionView = View(timeout=144000)
        ExhibitionEmbed = Embed(title=f"Name your fighters!")

        if FighterOneData != None:
            FighterOneDescription = ""
            FighterOneDescription += f"{FighterOneData[0]}\n"
            FighterOneDescription += f"💚 {FighterOneData[1]}\n"
            FighterOneDescription += f"💪 {FighterOneData[2]}\n"
            FighterOneDescription += f"🛡️ {FighterOneData[3]}\n"
            ExhibitionEmbed.add_field(name="\u200b", value=FighterOneDescription)
        
        if FighterTwoData != None:
            Clash = "⚔️"

            FighterTwoDescription = ""
            FighterTwoDescription += f"{FighterTwoData[0]}\n"
            FighterTwoDescription += f"💚{FighterTwoData[1]}\n"
            FighterTwoDescription += f"💪{FighterTwoData[2]}\n"
            FighterTwoDescription += f"🛡️{FighterTwoData[3]}\n"

            ExhibitionEmbed.add_field(name="\u200b", value=Clash)
            ExhibitionEmbed.add_field(name="\u200b", value=FighterTwoDescription)

        AddFighterOneButton = Button(label="Add Fighter One", row=0)
        AddFighterOneButton.callback = lambda Interaction: Self.Get_First_Fighter_Modal(Interaction)
        ExhibitionView.add_item(AddFighterOneButton)

        AddFighterTwoButton = Button(label="Add Fighter Two", row=0)
        AddFighterTwoButton.callback = lambda Interaction: Self.Get_Second_Fighter_Modal(Interaction, FighterOneData)
        ExhibitionView.add_item(AddFighterTwoButton)

        if FighterOneData != None and FighterTwoData != None:
            AddFighterTwoButton = Button(label="Battle!", row=1)
            AddFighterTwoButton.callback = lambda Interaction: Self.Create_Exhibition_Match(FighterOneData, FighterTwoData)
            ExhibitionView.add_item(AddFighterTwoButton)
        
        await Interaction.response.edit_message(view=ExhibitionView, embed=ExhibitionEmbed)


    async def Send_Arena_Panel(Self, User:Member=None, Interaction:Interaction=None, ExhibitionProcess=False) -> None:
        Self.User:Member = User
        Self.Player:Player = Self.ME.Players[Self.User.name]

        Message = f"{Self.Player.Data["Name"]} called for an Arena Panel"
        print(Message)
        Self.ME.MainEventLogger.log(20, Message)

        ArenaView = View(timeout=144000)
        ArenaEmbed = Embed(title=f"Welcome, {Self.Player.Data["Name"]}, to the Arena!")
        ArenaDescription = ""
        ChallengeDescription = ""
        ChallengerDescription = ""
        TargetDescription = ""
        FighterDescription = ""

        if Self.InsufficientFunds == True:
            ArenaEmbed.add_field(name="\u200b", value=f"💸 You don't have enough money to buy a fighter! 💸", inline=False)
            Self.InsufficientFunds = False

        if Self.MaximumFighters == True:
            ArenaEmbed.add_field(name="\u200b", value=f"You have the maximum amount of fighters!", inline=False)
            Self.MaximumFighters = False

        if len(Self.Player.Challenges.keys()) > 0:
            ChallengesChoice = Select(placeholder="You have challenges!",
                                options=[SelectOption(label=Challenge.Data["Challenger"].Data["Name"]) for Challenge in Self.Player.Challenges.values()],
                                row=0,
                                custom_id=f"ChallengesChoice")
            ChallengesChoice.callback = lambda Interaction: Self.Select_Challenge(Interaction)
            ArenaView.add_item(ChallengesChoice)

        ArenaDescription += f"👑 {Self.Player.Data["Rank"]:,}\n"
        ArenaDescription += f"💵 {Self.Player.Data["Wallet"]:,}\n"

        BuyFighterButton = Button(label="Buy Fighter", row=3)
        BuyFighterButton.callback = lambda Interaction: Self.Buy_Fighter(Interaction)
        ArenaView.add_item(BuyFighterButton)

        if Self.User.id in [713798389908897822, 897410636819083304]:
            ExhibitionMatchButton = Button(label="Exhibition Battle", row=3)
            ExhibitionMatchButton.callback = lambda Interaction: Self.Send_Exhibition_Panel(Interaction)
            ArenaView.add_item(ExhibitionMatchButton)

        if len(Self.Player.Fighters) > 0:
            ChallengeButton = Button(label="Challenge", row=3)
            ChallengeButton.callback = lambda Interaction: Self.Send_Select_Challenge_Target_Modal(Interaction)
            ArenaView.add_item(ChallengeButton)

            FighterChoice = Select(placeholder="Select a Fighter",
                                   options=[SelectOption(label=Fighter) for Fighter in Self.Player.Fighters],
                                   row=1,
                                   custom_id=f"FighterChoice")
            FighterChoice.callback = lambda Interaction: Self.Select_Fighter(Interaction)
            ArenaView.add_item(FighterChoice)

        if Self.Target != None:
            ArenaEmbed.add_field(name="\u200b", value="\u200b", inline=False)
            ArenaEmbed.add_field(name="⚔️ Challenged ⚔️", value=f"You challenged {Self.Target.Data['Name']}!", inline=False)
            Self.Target = None

        if Self.SelectedFighter != None:
            ArenaEmbed.add_field(name="\u200b", value="\u200b", inline=False)
            ArenaEmbed.add_field(name=Self.SelectedFighter.Data["Name"], value="\u200b", inline=False)
            FighterDescription += f"💠 {Self.SelectedFighter.Data["Level"]}\n"
            FighterDescription += f"💚 {Self.SelectedFighter.Data["Health"]}\n"
            FighterDescription += f"💪 {Self.SelectedFighter.Data["Power"]}\n"
            FighterDescription += f"🛡️ {Self.SelectedFighter.Data["Defense"]}\n"
            FighterDescription += f"🏆 {Self.SelectedFighter.Data["Wins"]}\n"
            FighterDescription += f"💀 {Self.SelectedFighter.Data["Losses"]}\n"
            FighterChoice.placeholder = Self.SelectedFighter.Data["Name"]

            ChangeFighterNameButton = Button(label="Change Fighter Name", row=3)
            ChangeFighterNameButton.callback = lambda Interaction: Self.Send_Change_Name_Modal(Interaction)
            ArenaView.add_item(ChangeFighterNameButton)

        ArenaEmbed.add_field(name="\u200b", value=ArenaDescription + "\n" + FighterDescription, inline=False)

        if Self.SelectedChallenge != None:
            Challenge = Self.SelectedChallenge
            ChallengeDescription += f"{Self.SelectedChallenge.Data["Challenger"].Data['Name']} challenges you!\n"
            ChallengeDescription += f"They proposed {Self.SelectedChallenge.Data["TargetFighter"].Data['Name']} versus {Self.SelectedChallenge.Data["ChallengerFighter"].Data['Name']}\n"

            TargetDescription += f"{Self.SelectedChallenge.Data['TargetFighter'].Data['Name']}\n"
            TargetDescription += f"💠{Self.SelectedChallenge.Data['TargetFighter'].Data['Level']}\n"
            TargetDescription += f"💚{Self.SelectedChallenge.Data['TargetFighter'].Data['Health']}\n"
            TargetDescription += f"💪{Self.SelectedChallenge.Data['TargetFighter'].Data['Power']}\n"
            TargetDescription += f"🛡️{Self.SelectedChallenge.Data['TargetFighter'].Data['Defense']}\n"
            TargetDescription += f"🏆{Self.SelectedChallenge.Data['TargetFighter'].Data['Wins']}\n"
            TargetDescription += f"💀{Self.SelectedChallenge.Data['TargetFighter'].Data['Losses']}\n"
            
            Clash = "⚔️"

            ChallengerDescription += f"{Self.SelectedChallenge.Data["ChallengerFighter"].Data['Name']}\n"
            ChallengerDescription += f"💠{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Level']}\n"
            ChallengerDescription += f"💚{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Health']}\n"
            ChallengerDescription += f"💪{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Power']}\n"
            ChallengerDescription += f"🛡️{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Defense']}\n"
            ChallengerDescription += f"🏆{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Wins']}\n"
            ChallengerDescription += f"💀{Self.SelectedChallenge.Data['ChallengerFighter'].Data['Losses']}\n"

            ArenaEmbed.add_field(name="\u200b", value=ChallengeDescription, inline=False)
            ArenaEmbed.add_field(name="\u200b", value=TargetDescription)
            ArenaEmbed.add_field(name="\u200b", value=Clash)
            ArenaEmbed.add_field(name="\u200b", value=ChallengerDescription)

            AcceptChallengeButton = Button(label="Accept Challenge", row=2)
            AcceptChallengeButton.callback = lambda Interaction: Self.Accept_Challenge(Interaction, Challenge)
            ArenaView.add_item(AcceptChallengeButton)
            ChallengesChoice.placeholder = Self.SelectedChallenge.Data["Challenger"].Data["Name"]
            Self.SelectedChallenge = None


        BackToActivities = Button(label="Back to Activities", row=4)
        BackToActivities.callback = lambda Interaction: Self.Send_Activities(User, Interaction)
        ArenaView.add_item(BackToActivities)

        if Interaction.data["custom_id"] == "Modal":
            await Interaction.response.edit_message(view=ArenaView, embed=ArenaEmbed)
        else:
            await Interaction.channel.send(view=ArenaView, embed=ArenaEmbed)
            await Interaction.message.delete()


    async def Send_Activities(Self, User, Interaction): Activities(User, Interaction)