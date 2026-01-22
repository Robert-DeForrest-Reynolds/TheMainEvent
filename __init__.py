from os.path import join

from discord.abc import GuildChannel
from discord import ForumChannel

from Library.EverburnBot import EverburnBot


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