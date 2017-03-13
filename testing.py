import hand
import numpy as np
import matplotlib.pyplot as plt
import pprint
import copy

# handCounts = [10, 100, 1000, 10000, 100000]
handCounts = [10000]

for handCount in handCounts:
    bestMHTW = 99999.99
    bestMHTWObj = hand.kaputHand()

    print("Simulating " + str(handCount) + " hands per tuning option; sit tight")
    print("==============================")

    testHands = []
    gameModes = 0
    gameModesPlayed = 0

    for rollAfterFullIter in range(2):
        options = {}
        if rollAfterFullIter == 0:
            options['rollAfterFull'] = False
        else:
            options['rollAfterFull'] = True

        for stingyFivesIter in range(2):
            if stingyFivesIter == 0:
                options['stingyFives'] = False
            else:
                options['stingyFives'] = True

            for rerollThresholdAfterFullSet in range(7):
                options['rerollThresholdAfterFull'] = rerollThresholdAfterFullSet

                for rerollThresholdSet in range(7):
                    options['rerollThreshold'] = rerollThresholdSet

                    testHands.append(options.copy())
                    gameModes += 1

    for testHand in testHands:
        testHandObj = hand.kaputHand()
        testHandObj.silent = True

        testHandObj.stingyFives = testHand['stingyFives']
        testHandObj.rollAfterFull = testHand['rollAfterFull']
        testHandObj.rerollThreshold = testHand['rerollThreshold']
        testHandObj.rerollThresholdAfterFull = testHand['rerollThresholdAfterFull']

        print("stingyFives: " + str(testHandObj.stingyFives))
        print("rollAfterFull: " + str(testHandObj.rollAfterFull))
        print("rerollThreshold: " + str(testHandObj.rerollThreshold))
        print("rerollThresholdAfterFull: " + str(testHandObj.rerollThresholdAfterFull))

        turnsTo5K = []

        for _ in range(handCount):
            testHandObj.refresh()
            score = 0
            turnCount = 0

            while score < 5000:
                turnCount += 1
                testHandObj.refresh()
                while testHandObj.handInPlay:
                    testHandObj.roll()
                score += testHandObj.score

            turnsTo5K.append(turnCount)

        results = np.array(turnsTo5K)
        mhtw = np.mean(results)
        gameModesPlayed += 1
        print("Mean hands to win: " +
              str(mhtw))
        print("Played " + str(gameModesPlayed) + " modes out of " + str(gameModes) + "(" + str(round((gameModesPlayed / gameModes) * 100)) + "% done)")
        print("")

        # handle best scoring
        if mhtw.item() < bestMHTW:
            bestMHTW = mhtw
            bestMHTWObj = copy.deepcopy(testHandObj)

    print("====== OPTIMUM TUNING: " + str(bestMHTW) + " MHTW ======")
    print("stingyFives: " + str(bestMHTWObj.stingyFives))
    print("rollAfterFull: " + str(bestMHTWObj.rollAfterFull))
    print("rerollThreshold: " + str(bestMHTWObj.rerollThreshold))
    print("rerollThresholdAfterFull: " + str(bestMHTWObj.rerollThresholdAfterFull))
    print("Played " + str(handCount * gameModes) + " games in " + str(gameModes) + " modes")

    timeTo5K = []
    for _ in range(handCount):
        bestMHTWObj.refresh()
        score = 0
        turnCount = 0

        while score < 5000:
            turnCount += 1
            bestMHTWObj.refresh()
            while bestMHTWObj.handInPlay:
                bestMHTWObj.roll()
            score += bestMHTWObj.score

        timeTo5K.append(turnCount)

    timeTo5KNP = np.array(timeTo5K)

    print("Percentiles:")
    print("\t10%: " + str(np.percentile(timeTo5KNP, 10)))
    print("\t50%: " + str(np.percentile(timeTo5KNP, 50)))
    print("\t90%: " + str(np.percentile(timeTo5KNP, 90)))
    print("\t95%: " + str(np.percentile(timeTo5KNP, 95)))
    print("\t99%: " + str(np.percentile(timeTo5KNP, 99)))

    plt.hist(timeTo5KNP, bins=range(1, 20))
    plt.suptitle("MHTW: " + str(bestMHTW) + " -- " + str(handCount) + " iterations")
    plt.title("(stingy: " + str(bestMHTWObj.stingyFives) + ", rollAFterFull: " + str(bestMHTWObj.rollAfterFull) + ", rerollThresh: " + str(bestMHTWObj.rerollThreshold) + ", rerollThreshPostFull: " + str(bestMHTWObj.rerollThresholdAfterFull) + ")")
    plt.savefig("optimum-" + str(handCount) + ".png")
    print("Histogram saved!")
