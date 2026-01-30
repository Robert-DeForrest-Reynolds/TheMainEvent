from os.path import join
from typing import Any

from discord import Member as DiscordMember
from discord.abc import GuildChannel
from discord import Game as DiscordGame
from discord import Role as DiscordRole
from discord import ForumChannel

from Library.DB import DB
from Library.EverburnBot import EverburnBot as EB
from Bots.Crucible.Pit import Pit


class Crucible(EB):
	def __init__(Self):
		Self.Forums:dict[str:ForumChannel] = {}
		Self.Channels:dict[str:GuildChannel] = {}
		Self.Roles:dict[str:DiscordRole] = {}
		Self.Weapons = []
		Self.AttackMoves = []
		Self.DefensiveMoves = []
		Self.Pit:Pit = None
		super().__init__(Self.Setup)

		with open(join("Bots", "Crucible", "Data", "Weapons.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.Weapons.append(Line.strip())

		with open(join("Bots", "Crucible", "Data", "AttackMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.AttackMoves.append(Line.strip())

		with open(join("Bots", "Crucible", "Data", "DefensiveMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.DefensiveMoves.append(Line.strip())


	async def Setup(Self) -> None:
		Self.DB = DB(join("Data", "Crucible.db"), Self) # Attach DB Task to Bot's event loop
		Self.Channels.update({"Lounge":Self.get_channel(1462614581678706739),
							  "Pit":Self.get_channel(1462614973741137953),
							  "Arena":Self.get_channel(1462615216733818943),
							  "Challenges":Self.get_channel(1464681901775392768)})
		Self.Roles.update({"Mentions":Self.TheGreatHearth.get_role(1466543997496463523)})
		Self.Roles.update({"DMs":Self.TheGreatHearth.get_role(1466544162655703255)})
		Self.Pit = Pit(Self)
		await Self.change_presence(activity=DiscordGame("Orchestrating combat."), status=f'/{"_" if Self.Testing else ""}fighters')


	async def Get_Next_Level_Requirement(Self, Level:int) -> int:
		return (Level * (19 + (Level * 2))) + Level * 3


	async def Check_Level_Up(Self, Level, Experience) -> int:
		Requirement = Self.Get_Next_Level_Requirement(Level)
		if Experience > Requirement:
			...


	async def Get_Challenges(Self, Member:DiscordMember):
		Data = await Self.DB.Request("SELECT * FROM Challenges WHERE ChallengerID=?", (Member.id,))
		Challenges = {Self.TheGreatHearth.get_member(ChallengeeID).name:
								   {"ID":ChallengeID,
							  		"Challenger":Self.TheGreatHearth.get_member(ChallengerID),
							  		"Challengee":Self.TheGreatHearth.get_member(ChallengeeID),
								    "ChallengerID":ChallengerID,
								    "ChallengeeID":ChallengeeID,
								    "ChallengerFighter":ChallengerFighter,
								    "ChallengeeFighter":ChallengeeFighter,
								    "Wager":Wager,
								    "Created At":CreatedAt}
			  		for ChallengeID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager, CreatedAt in Data}
		return Challenges


	async def Get_Opposing_Challenges(Self, Member:DiscordMember):
		Data = await Self.DB.Request("SELECT * FROM Challenges WHERE ChallengeeID=?", (Member.id,))
		Challenges = {Self.TheGreatHearth.get_member(ChallengerID).name:
								   {"ID":ChallengeID,
							  		"Challenger":Self.TheGreatHearth.get_member(ChallengerID),
							  		"Challengee":Self.TheGreatHearth.get_member(ChallengeeID),
								    "ChallengerID":ChallengerID,
								    "ChallengeeID":ChallengeeID,
								    "ChallengerFighter":ChallengerFighter,
								    "ChallengeeFighter":ChallengeeFighter,
								    "Wager":Wager,
								    "Created At":CreatedAt}
			  		for ChallengeID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager, CreatedAt in Data}
		return Challenges


	async def Get_Fighters(Self, Member:DiscordMember) -> dict:
		Data = await Self.DB.Request("SELECT ID, Name, Level, Experience, SkillPoints, Health, Power, Defense, Wins, Losses, CreatedAt FROM Fighters WHERE OwnerID=?",
				  			   (Member.id,))
		Fighters = {Name:{"ID":ID, "Name":Name, "Level":Level, "Experience":Experience, "Skill Points":SkillPoints, "Health":Health, "Power":Power, "Defense":Defense, "Wins":Wins, "Losses":Losses, "Created At":CreatedAt}
			  		for ID, Name, Level, Experience, SkillPoints, Health, Power, Defense, Wins, Losses, CreatedAt in Data}
		return Fighters


	async def Get_Fighter(Self, FighterName:str) -> list:
		Result = await Self.DB.Request("SELECT Health, Power, Defense, Level, Wins, Losses FROM Fighters WHERE Name=?", (FighterName,))
		Data = Result[0]
		return {"Name":FighterName, "Health":Data[0],"Power":Data[1],"Defense":Data[2],"Level":Data[3],"Wins":Data[4],"Losses":Data[5]}
		

	async def Increment_Fighter_Field(Self, FighterName:str, Field:str):
		Query = f"UPDATE Fighters SET {Field} = {Field} + 1 WHERE Name=?"
		await Self.DB.Request(Query, (FighterName,))
		

	async def Set_Fighter_Field(Self, FighterName:str, Field:str, Value:Any):
		Query = f"UPDATE Fighters SET {Field} = ? WHERE Name=?"
		await Self.DB.Request(Query, (Value,FighterName))
		

	async def Get_Fighter_Field(Self, FighterName:str, Field:str):
		Query = f"SELECT {Field} FROM Fighters WHERE Name=?"
		Result = await Self.DB.Request(Query, (FighterName,))
		return Result[0][0]


	async def Give_Fighter_XP(Self, FighterName:str, Amount:int) -> list:
		await Self.DB.Request("UPDATE Fighters SET Experience = Experience + ? WHERE Name=?", (Amount, FighterName))
		XP = await Self.Get_Fighter_Field(FighterName, 'Experience')
		Level = await Self.Get_Fighter_Field(FighterName, 'Level')
		Requirement = await Self.Get_Next_Level_Requirement(Level)
		if XP >= Requirement:
			Self.Send("Fighter Leveled Up")
			await Self.Set_Fighter_Field(FighterName, 'Experience', XP-Requirement)
			await Self.Set_Fighter_Field(FighterName, 'Level', Level+1)
			await Self.Increment_Fighter_Field(FighterName, 'SkillPoints')


	async def Delete_Fighter(Self, FighterName:str):
		await Self.DB.Request("DELETE FROM Fighters WHERE Name=?",
						(FighterName,))


	async def Save_New_Fighter(Self, Member:DiscordMember, FighterName):
		await Self.DB.Request("INSERT OR IGNORE INTO Fighters (OwnerID, Name, Health, Power, Defense) VALUES (?,?,?,?,?)",
						(Member.id, FighterName, 50, 50, 50))
		

	async def Get_Challenge(Self, Challenger:DiscordMember, Challengee:DiscordMember):
		Result = await Self.DB.Request("SELECT * FROM Challenges WHERE ID=?", (f"{Challenger.id}{Challengee.id}",))
		if Result:
			return Result[0]
		else:
			return None


	async def Save_New_Challenge(Self, Challenger:DiscordMember, Challengee:DiscordMember, Data:list):
		ChallengeID = f"{Challenger.id}{Challengee.id}"
		await Self.DB.Request("INSERT OR IGNORE INTO Challenges (ID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager) VALUES (?,?,?,?,?,?)",
						(ChallengeID, Challenger.id, Challengee.id, Data[0], Data[1], Data[2]))


	async def Delete_Challenge(Self, ChallengeID:str):
		await Self.DB.Request("DELETE FROM Challenges WHERE ID=?",
							  (ChallengeID,))