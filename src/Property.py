class Property:
    def __init__(self, name, sqf, value, growth, amountOwed, isPaidOff, happinessDelta):
        self.name = name
        self.sqf = sqf
        self.value = value
        self.growth = growth
        self.amountOwed = amountOwed
        self.isPaidOff = isPaidOff
        self.happinessDelta = happinessDelta


    def growInVlaue(self):
        self.value = self.value * (100*self.growth)