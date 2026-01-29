from sqlite3 import connect
from os.path import join

from discord import Member as DiscordMember
from discord.abc import GuildChannel
from discord import Game as DiscordGame
from discord import ForumChannel

from Library.DB import DB
from Library.EverburnBot import EverburnBot as EB
from Bots.Crucible.Pit import Pit


class Crucible(EB):
	def __init__(Self):
		super().__init__(Self.Setup)
		Self.DB:DB = None
		Self.Forums:dict[str:ForumChannel] = {}
		Self.Channels:dict[str:GuildChannel] = {}
		Self.Weapons = []
		Self.AttackMoves = []
		Self.DefensiveMoves = []
		Self.Pit:Pit = None

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
		Self.Pit = Pit(Self)
		await Self.change_presence(activity=DiscordGame("Orchestrating combat."), status=f'/{"_" if Self.Testing else ""}fighters')


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
		Data = await Self.DB.Request("SELECT ID, Name, Level, Experience, Health, Power, Defense, CreatedAt FROM Fighters WHERE OwnerID=?",
				  			   (Member.id,))
		Fighters = {Name:{"ID":ID, "Name":Name, "Level":Level, "Experience":Experience, "Health":Health, "Power":Power, "Defense":Defense, "Created At":CreatedAt}
			  		for ID, Name, Level, Experience, Health, Power, Defense, CreatedAt in Data}
		return Fighters


	async def Get_Fighter(Self, FighterName:str) -> list:
		Result = await Self.DB.Request("SELECT Health, Power, Defense FROM Fighters WHERE Name=?", (FighterName,))
		Data = Result[0]
		return {"Name":FighterName, "Health":Data[0],"Power":Data[1],"Defense":Data[2]}
	

	async def Delete_Fighter(Self, FighterName:str):
		await Self.DB.Request("DELETE FROM Fighters WHERE Name=?",
						(FighterName,))


	async def Save_New_Fighter(Self, Member:DiscordMember, FighterName):
		await Self.DB.Request("INSERT OR IGNORE INTO Fighters (OwnerID, Name, Health, Power, Defense) VALUES (?,?,?,?,?)",
						(Member.id, FighterName, 50, 50, 50))


	async def Save_New_Challenge(Self, Challenger:DiscordMember, Challengee:DiscordMember, Data:list):
		ChallengeID = f"{Challenger.id}{Challengee.id}"
		await Self.DB.Request("INSERT OR IGNORE INTO Challenges (ID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager) VALUES (?,?,?,?,?,?)",
						(ChallengeID, Challenger.id, Challengee.id, Data[0], Data[1], Data[2]))


	async def Delete_Challenge(Self, ChallengeID:str):
		await Self.DB.Request("DELETE FROM Challenges WHERE ID=?",
						(ChallengeID,))