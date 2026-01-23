from sqlite3 import connect
from os.path import join

from discord import Member as DiscordMember
from discord.abc import GuildChannel
from discord import ForumChannel

from Library.EverburnBot import EverburnBot
from Bots.MainEvent.Entities.Fighter import Fighter


class MainEvent:
	def __init__(Self, Bot:EverburnBot):
		Self.Forums:dict[str:ForumChannel] = {}
		Self.Channels:dict[str:GuildChannel] = {}
		Self.Weapons = []
		Self.AttackMoves = []
		Self.DefensiveMoves = []
		Self.Bot:EverburnBot = Bot

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
			FighterId   INTEGER PRIMARY KEY AUTOINCREMENT,
			OwnerId     TEXT NOT NULL,
			Name        TEXT NOT NULL,
			Level       INTEGER DEFAULT 1,
			Health		INTEGER NOT NULL,
			Power		INTEGER NOT NULL,
			Defense		INTEGER NOT NULL,
			CreatedAt   TEXT NOT NULL DEFAULT (datetime('now'))
		);
		""")
		Self.DB.commit()


	def Get_Fighters(Self, Member:DiscordMember):
		Self.DBCursor.execute("SELECT * FROM Fighters WHERE OwnerID=?", (Member.id,))
		Data = Self.DBCursor.fetchall()
		return Data


	def Save_New_Fighter(Self, Member:DiscordMember, F:Fighter):
		Data = Self.Bot.Get_Player_Data(Member)

		Connection = connect(join("Data", "Desmond.db"))
		Connection.cursor().execute("UPDATE Players SET FighterCount=? WHERE ID=?", (Data["Fighter Count"]+1, Member.id))
		Connection.commit()

		Self.DBCursor.execute("INSERT OR IGNORE INTO Fighters (OwnerID, Name, Health, Power, Defense) VALUES (?,?,?,?,?)",
							  (Member.id, F.Name, F.Health, F.Power, F.Defense))
		Self.DB.commit()