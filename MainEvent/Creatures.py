class Creature:
    def __init__(Self) -> None:
        Self.Name = None
        Self.Health = None
        Self.Power = None
        Self.Defense = None
        Self.Reward = None

class Karragan():
    def __init__(Self):
        Self.Name = "Karragan"
        Self.Health = 80
        Self.Power = 30
        Self.Defense = 30
        Self.Reward = 60


class Goblin():
    def __init__(Self):
        Self.Name = "Goblin"
        Self.Health = 80
        Self.Power = 30
        Self.Defense = 30
        Self.Reward = 100


class Wendigo():
    def __init__(Self):
        Self.Name = "Goblin"
        Self.Health = 80
        Self.Power = 35
        Self.Defense = 35
        Self.Reward = 70


class Deathclaw():
    def __init__(Self):
        Self.Name = "Goblin"
        Self.Health = 90
        Self.Power = 50
        Self.Defense = 80
        Self.Reward = 130


class JuniperJumper():
    def __init__(Self):
        Self.Name = "Juniper Jumper"
        Self.Health = 70
        Self.Power = 30
        Self.Defense = 30
        Self.Reward = 60


class Yujago():
    def __init__(Self):
        Self.Name = "Yujago"
        Self.Health = 125
        Self.Power = 65
        Self.Defense = 45
        Self.Reward = 110


class Murial():
    def __init__(Self):
        Self.Name = "Murial"
        Self.Health = 200
        Self.Power = 100
        Self.Defense = 100
        Self.Reward = 200


Creatures = [Karragan,
             Yujago,
             Murial,
             Goblin,
             Wendigo,
             JuniperJumper,
             Deathclaw]


CreatureCount = len(Creatures)
