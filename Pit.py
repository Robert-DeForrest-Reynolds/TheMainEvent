from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Bots.Crucible import Crucible

from discord import Embed, ForumChannel
from discord import Message as DiscordMessage
from discord.ui import View
from asyncio import create_task, sleep
from random import randrange


class Pit:
    def __init__(Self, CReference:Crucible) -> None:
        Self.Crucible = CReference
        Self.Fights = []
        Self.Alive = True
        Self.CurrentFight = None
        create_task(Self.Start())


    async def Start(Self):
        while Self.Alive:
            if Self.CurrentFight == None and len(Self.Fights) > 0:
                Self.CurrentFight = Self.Fights.pop(0)
                Self.Crucible.Send(f"Fight starting! {Self.CurrentFight}")
                await Self.Battle()
            await sleep(5)


    async def Construct_Description(Self, BattleEmbed:Embed, FighterOne, FighterTwo):
        FighterOneDesc = ""
        FighterOneDesc += f"{FighterOne['Name']}\n"
        FighterOneDesc += f"💚 {FighterOne['Health']}\n"
        FighterOneDesc += f"💪 {FighterOne['Power']}\n"
        FighterOneDesc += f"🛡️ {FighterOne['Defense']}\n"
        
        Clash = "⚔️"

        FighterTwoDesc = ""
        FighterTwoDesc += f"{FighterTwo['Name']}\n"
        FighterTwoDesc += f"💚 {FighterTwo['Health']}\n"
        FighterTwoDesc += f"💪 {FighterTwo['Power']}\n"
        FighterTwoDesc += f"🛡️ {FighterTwo['Defense']}\n"
            
        BattleEmbed.add_field(name="\u200b", value=FighterOneDesc)
        BattleEmbed.add_field(name="\u200b", value=Clash)
        BattleEmbed.add_field(name="\u200b", value=FighterTwoDesc)
        

    async def Battle(Self):
        BattleView = View(timeout=14400)
        
        FighterOne = await Self.Crucible.Get_Fighter(Self.CurrentFight["ChallengerFighter"])
        FighterTwo = await Self.Crucible.Get_Fighter(Self.CurrentFight["ChallengeeFighter"])
        BattleEmbed = Embed(title=f"⚔️ {FighterOne['Name']} versus {FighterTwo['Name']} ⚔️")

        await Self.Construct_Description(BattleEmbed, FighterOne, FighterTwo)

        PitChannel:ForumChannel = Self.Crucible.Channels["Pit"]
        Thread = await PitChannel.create_thread(name=f"{FighterOne['Name']} vs. {FighterTwo['Name']}",
                                                content="Welcome to the pit!",
                                                view=BattleView,
                                                embed=BattleEmbed)

        Message:DiscordMessage = Thread.message

        while FighterOne['Health'] > 0 and FighterTwo['Health'] > 0:
            await sleep(5)
            # Fighter one attacks
            FighterOneRoll = randrange(FighterOne['Power']//4, FighterOne['Power']+1)
            FighterOneDamage = FighterOneRoll

            FighterTwoWeapon = Self.Crucible.Weapons[randrange(0, len(Self.Crucible.Weapons))]
            FighterOneAttackMove = Self.Crucible.AttackMoves[randrange(0, len(Self.Crucible.AttackMoves))]

            FighterTwoDefense = randrange(FighterTwo['Defense']//4, FighterTwo['Defense']+1)
            FighterTwoDefensiveMove = Self.Crucible.DefensiveMoves[randrange(0, len(Self.Crucible.DefensiveMoves))]

            if FighterOneDamage - FighterTwoDefense < FighterOne['Power']//4: FighterOneDamage = FighterOne['Power']//4
            else: FighterOneDamage -= FighterTwoDefense

            FighterTwo['Health'] -= FighterOneDamage
            if FighterTwo['Health'] <= 0: break # Stop loop if FighterTwo has zero health

            DamageDesc = ""
            DamageDesc += f"{FighterOne['Name']} rolled {FighterOneRoll}, and {FighterOneAttackMove} {FighterTwo['Name']} with {FighterTwoWeapon} dealing {FighterOneDamage}\n\n"
            DamageDesc += f"{FighterTwo['Name']} defended {FighterTwoDefensiveMove} and blocked {FighterTwoDefense} damage\n\n"

            BattleEmbed = Embed(title=f"⚔️ {FighterOne['Name']} versus {FighterTwo['Name']} ⚔️")
            BattleEmbed.add_field(name="\u200b", value=DamageDesc, inline=False)
            await Self.Construct_Description(BattleEmbed, FighterOne, FighterTwo)

            await Message.edit(embed=BattleEmbed)

            await sleep(5)

            ## Now fighter two attacks
            FighterTwoRoll = randrange(FighterTwo['Power']//4, FighterTwo['Power']+1)
            FighterTwoDamage = FighterTwoRoll

            FighterTwoWeapon = Self.Crucible.Weapons[randrange(0, len(Self.Crucible.Weapons))]
            FighterTwoAttackMove = Self.Crucible.AttackMoves[randrange(0, len(Self.Crucible.AttackMoves))]

            FighterOneDefense = randrange(FighterOne['Defense']//4, FighterOne['Defense']+1)
            FighterOneDefensiveMove = Self.Crucible.DefensiveMoves[randrange(0, len(Self.Crucible.DefensiveMoves))]

            if FighterTwoDamage - FighterOneDefense < FighterTwo['Power']//4: FighterTwoDamage = FighterTwo['Power']//4
            else: FighterTwoDamage -= FighterOneDefense

            FighterOne['Health'] -= FighterTwoDamage
            if FighterOne['Health'] <= 0: break

            DamageDesc = ""
            DamageDesc += f"{FighterTwo['Name']} rolled {FighterTwoRoll}, and {FighterTwoAttackMove} {FighterOne['Name']} with {FighterTwoWeapon} dealing {FighterTwoDamage}\n\n"
            DamageDesc += f"{FighterOne['Name']} defended {FighterOneDefensiveMove} and blocked {FighterOneDefense} damage\n"

            BattleEmbed = Embed(title=f"⚔️ {FighterOne['Name']} versus {FighterTwo['Name']} ⚔️")
            BattleEmbed.add_field(name="\u200b", value=DamageDesc, inline=False)
            await Self.Construct_Description(BattleEmbed, FighterOne, FighterTwo)

            await Message.edit(embed=BattleEmbed)

        Winner = None
        Loser = None

        if FighterTwo['Health'] <= 0:
            Winner = FighterOne
            Loser = FighterTwo
            WinningMember = Self.CurrentFight['Challenger']
            LosingMember = Self.CurrentFight["Challengee"]
        if FighterOne['Health'] <= 0:
            Winner = FighterTwo
            Loser = FighterOne
            WinningMember = Self.CurrentFight["Challengee"]
            LosingMember = Self.CurrentFight['Challenger']
        
        if Winner != None:
            WinnerXP = int((Winner['Level']*30) * Loser['Level'])
            LoserXP = int((Loser['Level']*1) * Winner['Level'])
            WinMessage = f"⚔️ {Winner['Name']} has defeated {Loser['Name']} with 💚{Winner['Health']} remaining ⚔️"
            BattleEmbed = Embed(title=WinMessage)
            BattleEmbed.add_field(name="",
                                  value=f"${Self.CurrentFight["Wager"]:,.2f} has been added to your wallet {WinningMember.name},"+
                                        f" and respectively has been removed from your wallet {LosingMember.name}.\n"+
                                        f"{Winner['Name']} gained **{WinnerXP} XP**, and {Loser['Name']} gained **{LoserXP} XP**.",
                                        inline=False)
            Details = f"(Coming soon)"
            BattleEmbed.add_field(name="**Fight Details**", value=Details)
            await Self.Crucible.Give_Fighter_XP(Winner['Name'], WinnerXP)
            await Self.Crucible.Give_Fighter_XP(Loser['Name'], LoserXP)
            await Self.Crucible.Add_To_Wallet(WinningMember, Self.CurrentFight["Wager"])
            await Self.Crucible.Subject_From_Wallet(LosingMember, Self.CurrentFight["Wager"])
            await Self.Crucible.Delete_Challenge(Self.CurrentFight["ID"])
            Self.CurrentFight = None
            await Message.edit(embed=BattleEmbed)
