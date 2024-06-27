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
        print("Loading player data")
        Self.Load_Data()
        Self.Load_Fighters()
        print("Finish loading player data")


    async def Save_Challenges(Self) -> None:
        with open(join("Data", f"{Self.Data["UUID"]}.challenges.medata"), 'w') as SaveFile:
            print(f"Saving {Self.Data['UUID']}")
            SaveData = ""
            for Challenge in Self.Challenges.values():
                SaveData += (f"{Challenge.Data['Challenger'].Data['Name']}~{Challenge.Data['ChallengerFighter'].Data['Name']}~"+
                             f"{Challenge.Data['Target'].Data['Name']}~{Challenge.Data['TargetFighter'].Data['Name']}\n")
            SaveFile.write(SaveData)


    def Load_Challenges(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.challenges.medata")):
            with open(join("Data", f"{Self.Data["UUID"]}.challenges.medata"), 'r') as SaveFile:
                print(f"Loading {Self.Data['UUID']} challenges")
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
            print(f"Saving {Self.Data['UUID']} fighters")
            SaveData = ""
            for Fighter in Self.Fighters.values():
                SaveData += (f"{Fighter.Data['Name']}~{Fighter.Data['Level']}~{Fighter.Data['Health']}~{Fighter.Data['Power']}~" +
                             f"{Fighter.Data['Defense']}~{Fighter.Data['Wins']}~{Fighter.Data['Losses']}\n")
            SaveFile.write(SaveData)


    def Load_Fighters(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.fighters.medata")):
            print("Fuck")
            with open(join("Data", f"{Self.Data["UUID"]}.fighters.medata"), 'r') as SaveFile:
                print(f"Loading {Self.Data['UUID']}'s fighters")
                Data = SaveFile.readlines()
                for Field in Data:
                    print(Self.Data["Name"])
                    Datum = Field.split("~")
                    NewFighter = Fighter(Datum[0])
                    Self.Fighters.update({NewFighter.Data["Name"]:NewFighter})
                    NewFighter.Data["Level"] = int(Datum[1])
                    NewFighter.Data["Health"] = int(Datum[2])
                    NewFighter.Data["Power"] = int(Datum[3])
                    NewFighter.Data["Defense"] = int(Datum[4])
                    NewFighter.Data["Wins"] = int(Datum[5])
                    NewFighter.Data["Losses"] = int(Datum[6])


    async def Save_Data(Self) -> None:
        with open(join("Data", f"{Self.Data["UUID"]}.medata"), 'w') as SaveFile:
            print(f"Saving {Self.Data['UUID']} data")
            SaveData = ""
            for Key, Value in Self.Data.items():
                SaveData += f"{Key}~{Value}\n"
            SaveFile.write(SaveData)


    def Load_Data(Self) -> None:
        if exists(join("Data", f"{Self.Data["UUID"]}.medata")):
            with open(join("Data", f"{Self.Data["UUID"]}.medata"), 'r') as SaveFile:
                print(f"Loading {Self.Data['UUID']}'s data")
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
