import hand

playHand = hand.kaputHand()
playHand.interactivePlay = True
playHand.endGameMode = True

playHand.rerollThreshold = 5
playHand.stingyFives = True
playHand.rollAfterFull = True
playHand.rerollThresholdAfterFull = 5

while playHand.handInPlay:
    playHand.roll()
