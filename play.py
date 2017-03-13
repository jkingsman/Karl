import hand

playHand = hand.kaputHand()
playHand.interactivePlay = True

playHand.rerollThreshold = 5
playHand.stingyFives = True
playHand.rollAfterFull = True
playHand.rerollThresholdAfterFull = 5

while 1:
    playHand.refresh()
    print("============== NEW ROLL ==============")
    while playHand.handInPlay:
        playHand.roll()
