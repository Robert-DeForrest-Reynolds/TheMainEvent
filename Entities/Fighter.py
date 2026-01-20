class Fighter:
    def __init__(Self, Name, Health, Power, Defense) -> None:
        Self.Data = {
            "Name":Name,
            "Health": int(Health),
            "Power": int(Power),
            "Defense": int(Defense),
        }
    
    @property
    def Name(Self): return Self.Data["Name"]

    @Name.setter
    def Name(Self, Value): Self.Data["Name"] = Value
    
    @property
    def Health(Self): return Self.Data["Health"]

    @Health.setter
    def Health(Self, Value): Self.Data["Health"] = Value
    
    @property
    def Power(Self): return Self.Data["Power"]

    @Power.setter
    def Power(Self, Value): Self.Data["Power"] = Value
    
    @property
    def Defense(Self): return Self.Data["Defense"]

    @Name.setter
    def Defense(Self, Value): Self.Data["Defense"] = Value
