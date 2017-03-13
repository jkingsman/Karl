import hand

player = hand.kaputHand()
player.interactivePlay = False

player.stingyFives = True
player.rollAfterFull = True
player.ignoreTriple2 = True
player.rerollThreshold = 6
player.rerollThresholdAfterFull = 6
player.abandon5Threshold = 450

while 1:
    player.refresh()
    print("============== NEW ROLL ==============")
    direction = input("Enter to roll, e for endgame roll, or x for exit: ")

    if "e" in direction:
        print("Endgame Mode Entered")
        player.endGameMode = True

    if "x" in direction:
        print("Bye!")
        break

    while player.handInPlay:
        player.roll()
