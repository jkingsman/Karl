import random


class kaputHand:
    TOTALDIE = 6
    STRAIGHTSCORE = 2000

    # DATA STORAGE
    rolled = []  # the hand that was rolled
    kept = []  # the currently retained hand
    rolls = 0  # number of rolls
    fulls = 0  # the total number of fulls
    score = 0  # total score
    kaput = False  # if the player has gone kaput
    handInPlay = True  # if the player is done
    scoreToBeat = 0  # endgame mode score to beat

    # OUTPUT
    printDebugOutput = True  # print debug output each roll
    silent = False  # print no output at all

    # GAME MODES
    endGameMode = False
    interactivePlay = False

    # TUNING
    rerollThreshold = 4  # number of dice left (or more) to reroll once 300 is reached
    stingyFives = True  # if there are multiple fives and no ones in a vanilla roll (no straight), take one and reroll
    rollAfterFull = True  # should the bot roll after recieving a flush
    rerollThresholdAfterFull = 5  # after a full, what should the rerollThreshold be

    def output(self, string):
        if not self.silent:
            print(string)

    def refresh(self):
        self.rolled = []
        self.kept = []
        self.rolls = 0
        self.fulls = 0
        self.score = 0
        self.kaput = False
        self.handInPlay = True

    def diceToRoll(self):
        return self.TOTALDIE - len(self.kept)

    def shouldRoll(self):
        if self.fulls > 0:
            if not self.rollAfterFull:
                return False
            if self.diceToRoll() >= self.rerollThresholdAfterFull:
                return True

        if self.endGameMode and self.score < self.scoreToBeat:
            return True

        if self.score < 300:
            return True

        if self.diceToRoll() >= self.rerollThreshold:
            return True

        return False

    def getRoll(self):
        if self.interactivePlay:
            inputRoll = input("Enter roll (" + str(self.diceToRoll()) +
                              " dice): ")
            return sorted([int(i) for i in list(inputRoll)])
        else:
            return sorted([random.randint(1, 6) for
                          i in range(self.diceToRoll())])

    def roll(self):
        # handle endgame input if we're in it
        if self.endGameMode and self.scoreToBeat == 0:
            self.scoreToBeat = int(input("Score to beat: "))

        if self.shouldRoll():
            self.rolled = self.getRoll()
            self.output("ROLLED: " + str(self.rolled))
            self.rolls += 1
            self.checkRoll()
        else:
            self.output("Ending turn.")
            self.handInPlay = False

        self.printStatus()

    def checkRoll(self):
        keptThisHand = 0

        # check straight
        if self.rolled == [1, 2, 3, 4, 5, 6]:
            self.score += self.STRAIGHTSCORE
            self.fulls += 1
            self.rolls = 0
            return

        # find triples
        triples = set([x for x in self.rolled if self.rolled.count(x) >= 3])
        for value in triples:
            if value == 2 and self.rolled.count(1) > 2:
                # skip 200 if we have it better in ones
                continue

            if value == 1:
                self.score += 1000
            else:
                self.score += value * 100  # take the score

            for _ in range(3):
                self.rolled.remove(value)  # pop the die
                self.kept.append(value)

            keptThisHand += 3

        # handle multiple 50s where fifties don't make the whole roll
        # and there are no 1s
        noOnes = self.rolled.count(5) > 1 and self.rolled.count(1) == 0
        onlyFives = (len(self.rolled) - self.rolled.count(5)) == 0
        if noOnes and not onlyFives and self.stingyFives:
            self.score += 50
            self.kept.append(5)
            self.rolled.remove(5)
            return

        iterableRolled = self.rolled[:]
        # do basic score count
        for value in iterableRolled:
            if value == 1:
                self.score += 100
            elif value == 5:
                self.score += 50
            else:
                continue

            self.kept.append(value)
            self.rolled.remove(value)
            keptThisHand += 1

        if keptThisHand == 0:
            self.handInPlay = False
            self.score = 0
            self.kaput = True

        # handle full
        if len(self.kept) == 6:
            self.fulls += 1
            self.kept = []
        else:
            if self.rolls == 3 and not self.endGameMode:
                self.handInPlay = False
                if self.score < 300:
                    self.score = 0
                    self.kaput = True

    def debugStatus(self):
        print("Roll Debug")
        print("\tRoll count: " + str(self.rolls))
        print("\tFulls: " + str(self.fulls))
        print("\tCurrent kept: " + str(self.kept))
        print("\tCurrent score: " + str(self.score))
        print("\tHand in play? " + str(self.handInPlay))
        print("\tKaput? " + str(self.kaput))
        print("")

    def endTurnStatus(self):
        print("Turn status:")
        print("\tKept: " + str(self.kept))
        print("\tScore: " + str(self.score))
        print("\tKaput? " + str(self.kaput))
        print("")

    def printStatus(self):
        if not self.silent:
            if self.handInPlay and self.printDebugOutput:
                self.debugStatus()
            else:
                self.endTurnStatus()
