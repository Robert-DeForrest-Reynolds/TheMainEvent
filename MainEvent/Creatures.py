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
        Self.Health = 2200
        Self.Power = 400
        Self.Defense = 800
        Self.Reward = 100


class Yujago():
    def __init__(Self):
        Self.Name = "Yujago"
        Self.Health = 1800
        Self.Power = 700
        Self.Defense = 650
        Self.Reward = 155


class Murial():
    def __init__(Self):
        Self.Name = "Murial"
        Self.Health = 3200
        Self.Power = 800
        Self.Defense = 1250
        Self.Reward = 295


Creatures = [Karragan,
             Yujago,
             Murial]


CreatureCount = len(Creatures)
