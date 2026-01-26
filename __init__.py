from sqlite3 import connect
from os.path import join

from discord import Member as DiscordMember
from discord.abc import GuildChannel
from discord import ForumChannel

from Library.EverburnBot import EverburnBot
from Bots.MainEvent.Pit import Pit

class MainEvent:
	def __init__(Self, Bot:EverburnBot):
		Self.Forums:dict[str:ForumChannel] = {}
		Self.Channels:dict[str:GuildChannel] = {}
		Self.Weapons = []
		Self.AttackMoves = []
		Self.DefensiveMoves = []
		Self.Bot:EverburnBot = Bot
		Self.Pit:Pit = None

		with open(join("Bots", "MainEvent", "Data", "Weapons.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.Weapons.append(Line.strip())

		with open(join("Bots", "MainEvent", "Data", "AttackMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.AttackMoves.append(Line.strip())

		with open(join("Bots", "MainEvent", "Data", "DefensiveMoves.txt"), 'r') as File:
			Lines = File.readlines()
			for Line in Lines:
				Self.DefensiveMoves.append(Line.strip())


		Self.DB = connect(join("Data", "MainEvent.db"))

		Self.DBCursor = Self.DB.cursor()
		
		Self.DBCursor.execute('PRAGMA journal_mode=WAL;')
		Self.DB.commit()

		Self.DBCursor.execute("""
		CREATE TABLE IF NOT EXISTS Fighters (
			ID   INTEGER PRIMARY KEY AUTOINCREMENT,
			OwnerID     TEXT NOT NULL,
			Name        TEXT NOT NULL UNIQUE,
			Level       INTEGER DEFAULT 1,
			Experience  INTEGER DEFAULT 0,
			Health		INTEGER NOT NULL,
			Power		INTEGER NOT NULL,
			Defense		INTEGER NOT NULL,
			CreatedAt   TEXT NOT NULL DEFAULT (datetime('now'))
		);
		""")

		Self.DBCursor.execute("""
		CREATE TABLE IF NOT EXISTS Challenges (
			ID   				TEXT PRIMARY KEY,
			ChallengerID    	INTEGER NOT NULL,
			ChallengeeID  		INTEGER NOT NULL,
			ChallengerFighter	TEXT NOT NULL,
			ChallengeeFighter	TEXT NOT NULL,
			Wager				REAL NOT NULL,
			CreatedAt   		TEXT NOT NULL DEFAULT (datetime('now'))
		);
		""")
		Self.DB.commit()


	def Get_Challenges(Self, Member:DiscordMember):
		Self.DBCursor.execute(
			"SELECT * FROM Challenges WHERE ChallengerID=?",
			(Member.id,),
		)
		Data = Self.DBCursor.fetchall()
		Challenges = {Self.Bot.TheGreatHearth.get_member(ChallengeeID).name:
								   {"ID":ChallengeID,
							  		"Challenger":Self.Bot.TheGreatHearth.get_member(ChallengerID),
							  		"Challengee":Self.Bot.TheGreatHearth.get_member(ChallengeeID),
								    "ChallengerID":ChallengerID,
								    "ChallengeeID":ChallengeeID,
								    "ChallengerFighter":ChallengerFighter,
								    "ChallengeeFighter":ChallengeeFighter,
								    "Wager":Wager,
								    "Created At":CreatedAt}
			  		for ChallengeID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager, CreatedAt in Data}
		return Challenges


	def Get_Opposing_Challenges(Self, Member:DiscordMember):
		Self.DBCursor.execute(
			"SELECT * FROM Challenges WHERE ChallengeeID=?",
			(Member.id,),
		)
		Data = Self.DBCursor.fetchall()
		Challenges = {Self.Bot.TheGreatHearth.get_member(ChallengerID).name:
								   {"ID":ChallengeID,
							  		"Challenger":Self.Bot.TheGreatHearth.get_member(ChallengerID),
							  		"Challengee":Self.Bot.TheGreatHearth.get_member(ChallengeeID),
								    "ChallengerID":ChallengerID,
								    "ChallengeeID":ChallengeeID,
								    "ChallengerFighter":ChallengerFighter,
								    "ChallengeeFighter":ChallengeeFighter,
								    "Wager":Wager,
								    "Created At":CreatedAt}
			  		for ChallengeID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager, CreatedAt in Data}
		return Challenges


	def Get_Fighters(Self, Member:DiscordMember):
		Self.DBCursor.execute("SELECT ID, Name, Level, Experience, Health, Power, Defense, CreatedAt FROM Fighters WHERE OwnerID=?", (Member.id,))
		Data = Self.DBCursor.fetchall()
		Fighters = {Name:{"ID":ID, "Name":Name, "Level":Level, "Experience":Experience, "Health":Health, "Power":Power, "Defense":Defense, "Created At":CreatedAt}
			  		for ID, Name, Level, Experience, Health, Power, Defense, CreatedAt in Data}
		return Fighters


	def Get_Fighter(Self, FighterName:str) -> list:
		Self.DBCursor.execute("SELECT Health, Power, Defense FROM Fighters WHERE Name=?", (FighterName,))
		FighterData = Self.DBCursor.fetchone()
		return {"Name":FighterName, "Health":FighterData[0],"Power":FighterData[1],"Defense":FighterData[2]}
	

	def Delete_Fighter(Self, FighterName:str):
		Self.DBCursor.execute(
			"DELETE FROM Fighters WHERE Name=?",
			(FighterName,)
		)
		Self.DB.commit()


	def Save_New_Fighter(Self, Member:DiscordMember, FighterName):
		Self.DBCursor.execute("INSERT OR IGNORE INTO Fighters (OwnerID, Name, Health, Power, Defense) VALUES (?,?,?,?,?)",
							  (Member.id, FighterName, 50, 50, 50))
		Self.DB.commit()


	def Save_New_Challenge(Self, Challenger:DiscordMember, Challengee:DiscordMember, Data:list):
		ChallengeID = f"{Challenger.id}{Challengee.id}"
		Self.DBCursor.execute("INSERT OR IGNORE INTO Challenges (ID, ChallengerID, ChallengeeID, ChallengerFighter, ChallengeeFighter, Wager) VALUES (?,?,?,?,?,?)",
							  (ChallengeID, Challenger.id, Challengee.id, Data[0], Data[1], Data[2]))
		Self.DB.commit()


	def Delete_Challenge(Self, ChallengeID:str):
		Self.DBCursor.execute(
			"DELETE FROM Challenges WHERE ID=?",
			(ChallengeID,)
		)
		Self.DB.commit()