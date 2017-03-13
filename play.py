import hand

player = hand.kaputHand()
player.interactivePlay = True

player.stingyFives = True
player.rollAfterFull = True
player.ignoreTriple2 = True
player.rerollThreshold = 6
player.rerollThresholdAfterFull = 6
player.abandon5Threshold = 450

while 1:
    player.refresh()
    print("============== NEW ROLL ==============")
    while player.handInPlay:
        player.roll()
