class Fighter:
    def __init__(Self, Name) -> None:
        Self.Data = {
            "Name":Name,
            "Level": 1,
            "Experience": 0,
            "ExperienceRequired":0,
            "Health": 150,
            "Power": 25,
            "Defense": 20,
            "CreatureKills":0,
            "Wins": 0,
            "Losses": 0
        }
        Self.Inventory = []
        Self.Data.update({"ExperienceRequired":(Self.Data["Level"]*225)*1.5})

    async def Level_Check(Self) -> bool:
        if Self.Data["Experience"] >= Self.Data["ExperienceRequired"]:
            Self.Data["Level"] += 1
            Self.Data["Health"] += (Self.Data["Level"]*62)*1.5
            Self.Data["Power"] += (Self.Data["Level"]*40)*1.5
            Self.Data["Defense"] += (Self.Data["Level"]*40)*1.5
            Self.Data["ExperienceRequired"] = (Self.Data["Level"]*225)*1.5
            if Self.Data["Experience"] >= Self.Data["ExperienceRequired"]:
                await Self.Level_Check()
            else:
                return True
        return False