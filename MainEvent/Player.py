from asyncio import create_task, wait_for
from os.path import join, exists
from Fighter import Fighter
from Challenge import Challenge
from discord import Member

class Player:
    def __init__(Self, MemberReference:Member, MEReference) -> None:
        Self.ME = MEReference
        Self.Data = {
            "UUID":MemberReference.id,
            "MemberReference": MemberReference,
            "Name":MemberReference.name,
            "Nick":MemberReference.display_name,
            "Rank":0,
            "Wallet":5000.0,
        }
        Self.Fighters = {}
        Self.FightersTraining = []
        Self.Horses = {}
        Self.Challenges = {}
        Self.Load_Data()
        Self.Load_Fighters()


    async def Save_Challenges(Self) -> None:
        with open(join("Data", f"{Self.Data["UUID"]}.challenges.medata"), 'w') as SaveFile:
            SaveData = ""
            for Challenge in Self.Challenges.values():
                SaveData += (f"{Challenge.Data['Challenger'].Data['Name']}~{Challenge.Data['ChallengerFighter'].Data['Name']}~"+
                             f"{Challenge.Data['Target'].Data['Name']}~{Challenge.Data['TargetFighter'].Data['Name']}\n")
            SaveFile.write(SaveData)


    def Load_Challenges(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.challenges.medata")):
            with open(join("Data", f"{Self.Data["UUID"]}.challenges.medata"), 'r') as SaveFile:
                Data = SaveFile.readlines()
                for Field in Data:
                    Datum = Field.split("~")
                    Challenger = Self.ME.Players[Datum[0]]
                    ChallengerFighter = Self.ME.Players[Datum[0]].Fighters[Datum[1]]
                    Target = Self.ME.Players[Datum[2]]
                    TargetFighter = Self.ME.Players[Datum[2]].Fighters[Datum[3].strip()]
                    NewChallenge = Challenge(Challenger, ChallengerFighter, Target, TargetFighter)
                    Self.Challenges.update({Challenger.Data["Name"]:NewChallenge})
                    Self.ME.AllChallenges.update({Challenger.Data["Name"]:NewChallenge})


    async def Save_Fighters(Self) -> None:
        with open(join("Data", f"{Self.Data["UUID"]}.fighters.medata"), 'w') as SaveFile:
            SaveData = ""
            for Fighter in Self.Fighters.values():
                SaveData += (f"{Fighter.Data['Name']}~{Fighter.Data['Level']}~{Fighter.Data['Experience']}~{Fighter.Data['Health']}~{Fighter.Data['Power']}~" +
                             f"{Fighter.Data['Defense']}~{Fighter.Data['Wins']}~{Fighter.Data['Losses']}~{Fighter.Data['CreatureKills']}\n")
            SaveFile.write(SaveData)


    def Load_Fighters(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.fighters.medata")):
            with open(join("Data", f"{Self.Data["UUID"]}.fighters.medata"), 'r') as SaveFile:
                Data = SaveFile.readlines()
                for Field in Data:
                    print(Self.Data["Name"])
                    Datum = Field.split("~")
                    NewFighter = Fighter(Datum[0])
                    Self.Fighters.update({NewFighter.Data["Name"]:NewFighter})
                    NewFighter.Data["Level"] = int(Datum[1])
                    NewFighter.Data["Experience"] = int(Datum[2])
                    NewFighter.Data["Health"] = int(Datum[3])
                    NewFighter.Data["Power"] = int(Datum[4])
                    NewFighter.Data["Defense"] = int(Datum[5])
                    NewFighter.Data["Wins"] = int(Datum[6])
                    NewFighter.Data["Losses"] = int(Datum[7])
                    NewFighter.Data["CreatureKills"] = int(Datum[8])


    async def Save_Data(Self) -> None:
        with open(join("Data", f"{Self.Data["UUID"]}.medata"), 'w') as SaveFile:
            SaveData = ""
            for Key, Value in Self.Data.items():
                SaveData += f"{Key}~{Value}\n"
            SaveFile.write(SaveData)


    def Load_Data(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.medata")):
            with open(join("Data", f"{Self.Data["UUID"]}.medata"), 'r') as SaveFile:
                Data = SaveFile.readlines()
                for Field in Data:
                    Exclusions = ["UUID", "MemberReference"]
                    Datum = Field.split("~")
                    Key:str = Datum[0]
                    Value:str = Datum[1].strip()
                    if Key not in Exclusions:
                        if Value.isdigit():
                            Value = int(Value)
                        elif "." in Value and Value.replace(".", "").isdigit():
                            Value = float(Value)
                        Self.Data[Key] = Value
