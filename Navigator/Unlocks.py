import Settings as settings

# UNLOCKS
class Unlocks:
    def __init__(self,records):
        self.ships = records
        self.messages = [] # [[Unlock Message,Variant Name], Ship Name  ]
        settings.debug("Loaded unlocks") # Debug


    # UPDATE UNLOCKS IN MENU
    def update(self,game):
        preUpdate = self.ships[:] # copy previous list to check for update

        # Default ship - L1
        if not self.ships[0][1] and game.records["longestRun"] >= 15: self.ships[0][1] = True
        if not self.ships[0][2] and game.records["longestRun"] >= 30: self.ships[0][2] = True
        if not self.ships[0][3] and game.records["longestRun"] >= 45: self.ships[0][3] = True
        if not self.ships[0][4] and game.records["longestRun"] >= 60: self.ships[0][4] = True
        if not self.ships[0][5] and game.records["longestRun"] >= 75: self.ships[0][5] = True
        if not self.ships[0][6] and game.records["longestRun"] >= 90: self.ships[0][6] = True
        if not self.ships[0][7] and game.records["longestRun"] >= 105:self.ships[0][7] = True
        if not self.ships[0][8] and game.records["longestRun"] >= 120:self.ships[0][8] = True
        if not self.ships[0][9] and game.records["longestRun"] >= 135:self.ships[0][9] = True
        if not self.ships[0][10] and game.records["longestRun"] >= 150:self.ships[0][10] = True
        if not self.ships[0][11] and game.records["longestRun"] >= 165:self.ships[0][11] = True
        levelMessages = [
                            [None,None],
                            ["Survive for 15 seconds",None],
                            ["Survive for 30 seconds",None],
                            ["Survive for 45 seconds",None],
                            ["Survive for 60 seconds",None],
                            ["Survive for 75 seconds",None],
                            ["Survive for 90 seconds",None],
                            ["Survive for 105 seconds","Taxigator"],
                            ["Survive for 120 seconds","WhatColorsYourSpaceship"],
                            ["Survive for 135 seconds",None],
                            ["Survive for 150 seconds",None],
                            ["Survive for 165 seconds",None] ]

        # Record holder unlocks
        if game.assets.leaderboard is not None and game.assets.leaderboard[0]['id'] == game.records['id']:
            settings.debug("User is record holder") # Debug
            if not self.ships[0][12]: self.ships[0][12] = True
        else:
        # Re locks
            if self.ships[0][12]: self.ships[0][12] = False

        levelMessages.append(["Be #1 on Leaderboard","Champion"])
        self.messages.append([levelMessages, "Classic Ship"])

        # Rocket buggy - L2
        if not self.ships[1][0] and game.records["highScore"] >= 25: self.ships[1][0] = True
        self.messages.append([[["Score 25 in a run", None]], "Rocket Buggy"])

        # Laser ship - L3
        if not self.ships[2][0] and game.records["highScore"] >= 50: self.ships[2][0] = True
        self.messages.append([[["Score 50 in a run", None]], "Lasership"])

        # Hyper yacht - L4
        if not self.ships[3][0] and game.records["points"] >= 200: self.ships[3][0] = True
        self.messages.append([[["Score 200 points total", None]], "Hyper Yacht"])

        # Ol reliable - L5
        if not self.ships[4][0] and game.records["timePlayed"] >= 1200: self.ships[4][0] = True
        self.messages.append([[["Play for 1200 seconds", None]], "Ol' Reliable"])

        # Icon ship - L6
        if not self.ships[5][0] and game.records["points"] >= 500: self.ships[5][0] = True
        if not self.ships[5][1] and game.records["points"] >= 600: self.ships[5][1] = True
        if not self.ships[5][2] and game.records["points"] >= 700: self.ships[5][2] = True
        if not self.ships[5][3] and game.records["points"] >= 800: self.ships[5][3] = True
        if not self.ships[5][4] and game.records["points"] >= 900:  self.ships[5][4] = True
        levelMessages = [
            ["Score 500 points total",None],
            ["Score 600 points total",None],
            ["Score 700 points total",None],
            ["Score 800 points total",None],
            ["Score 900 points total",None] ]
        self.messages.append([levelMessages, "Classic 2.0"])

        if preUpdate != self.ships: # Save unlocks if list was updated
            game.records["unlocks"] = self.ships
            game.assets.storeRecords(game.records)


    # Skin other than default for a specific ship is unlocked
    def hasSkinUnlock(self, shipIndex):
        if len(self.ships[shipIndex]) <= 1: return False
        else:
            for skin in self.ships[shipIndex][1:]:
                if skin: return True
            return False


    # Ship other than default is unlocked
    def hasShipUnlock(self):
        for ship in self.ships[1:]:
            if ship[0]: return True
        return False


    # Index of highest ship unlock
    def highestShip(self):
        highest = 0
        for shipIndex in range(len(self.ships)):
            if self.ships[shipIndex][0]: highest = shipIndex
        return highest


    # Index of highest skin unlock
    def highestSkin(self,shipNum):
        highest = 0
        for skinIndex in range(len(self.ships[shipNum])):
            if self.ships[shipNum][skinIndex]: highest = skinIndex
        return highest


    # Index of next unlocked skin
    def nextUnlockedSkin(self,shipNum,skinNum):
        if self.hasSkinUnlock(shipNum):
            for skinIndex in range(len(self.ships[shipNum])):
                if skinIndex > skinNum and self.ships[shipNum][skinIndex]: return skinIndex
        return None


    # Index of last unlocked skin
    def lastUnlockedSkin(self,shipNum,skinNum):
        if self.hasSkinUnlock(shipNum):
            for skinIndex in reversed(range(len(self.ships[shipNum]))):
                if skinIndex < skinNum and self.ships[shipNum][skinIndex]: return skinIndex
        return None


    # Index of next unlocked ship
    def nextUnlockedShip(self,shipNum):
        if self.hasShipUnlock():
            for shipIndex in range(len(self.ships)):
                if shipIndex > shipNum and self.ships[shipIndex][0]: return shipIndex
        return None


    # Index of last unlocked ship
    def lastUnlockedShip(self,shipNum):
        if self.hasShipUnlock():
            for shipIndex in reversed(range(len(self.ships))):
                if shipIndex < shipNum and self.ships[shipIndex][0]: return shipIndex
        return None