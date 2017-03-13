import hand
import numpy as np
import matplotlib.pyplot as plt
import pprint
import copy

# handCounts = [10, 100, 1000, 10000, 100000]
handCounts = [100, 1000, 10000]
debugOutput = False
lastPercentage = -1

for handCount in handCounts:
    bestMHTW = 99999.99
    bestMHTWObj = hand.kaputHand()

    print("Simulating " + str(handCount) + " hands per tuning option; sit tight")
    print("==============================")

    testHands = []
    gameModes = 0
    gameModesPlayed = 0

    # mode assembly
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

            for ignoreTriple2Iter in range(2):
                if ignoreTriple2Iter == 0:
                    options['ignoreTriple2'] = False
                else:
                    options['ignoreTriple2'] = True

                for rerollThresholdAfterFullSet in range(6):
                    options['rerollThresholdAfterFull'] = rerollThresholdAfterFullSet + 1

                    for rerollThresholdSet in range(6):
                        options['rerollThreshold'] = rerollThresholdSet + 1

                        for abandon5ThresholdSet in range(50, 500, 50):
                            options['abandon5Threshold'] = abandon5ThresholdSet

                            testHands.append(options.copy())
                            gameModes += 1

    # mode testing
    for testHand in testHands:
        testHandObj = hand.kaputHand()
        testHandObj.silent = True

        testHandObj.stingyFives = testHand['stingyFives']
        testHandObj.rollAfterFull = testHand['rollAfterFull']
        testHandObj.rerollThreshold = testHand['rerollThreshold']
        testHandObj.rerollThresholdAfterFull = testHand['rerollThresholdAfterFull']
        testHandObj.ignoreTriple2 = testHand['ignoreTriple2']
        testHandObj.abandon5Threshold = testHand['abandon5Threshold']

        if debugOutput:
            print("stingyFives: " + str(testHandObj.stingyFives))
            print("rollAfterFull: " + str(testHandObj.rollAfterFull))
            print("ignoreTriple2: " + str(testHandObj.ignoreTriple2))
            print("rerollThreshold: " + str(testHandObj.rerollThreshold))
            print("rerollThresholdAfterFull: " + str(testHandObj.rerollThresholdAfterFull))
            print("abandon5Threshold: " + str(testHandObj.abandon5Threshold))

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
        # print("Mean hands to win: " +
        #       str(mhtw))
        if round((gameModesPlayed / gameModes) * 100) % 5 == 0 and round((gameModesPlayed / gameModes) * 100) > lastPercentage:
            print("Played " + str(gameModesPlayed) + " modes out of " + str(gameModes) + "(" + str(round((gameModesPlayed / gameModes) * 100)) + "% done)")
            lastPercentage = round((gameModesPlayed / gameModes) * 100)

        # handle best scoring
        if mhtw.item() < bestMHTW:
            bestMHTW = mhtw
            bestMHTWObj = copy.deepcopy(testHandObj)

    print("====== OPTIMUM TUNING: " + str(bestMHTW) + " MHTW ======")
    print("stingyFives: " + str(testHandObj.stingyFives))
    print("rollAfterFull: " + str(testHandObj.rollAfterFull))
    print("ignoreTriple2: " + str(testHandObj.ignoreTriple2))
    print("rerollThreshold: " + str(testHandObj.rerollThreshold))
    print("rerollThresholdAfterFull: " + str(testHandObj.rerollThresholdAfterFull))
    print("abandon5Threshold: " + str(testHandObj.abandon5Threshold))
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

    print("Percentiles & Mean:")
    print("\tMean: " + str(bestMHTW)))
    print("\tp10: " + str(np.percentile(timeTo5KNP, 10)))
    print("\tp50: " + str(np.percentile(timeTo5KNP, 50)))
    print("\tp90: " + str(np.percentile(timeTo5KNP, 90)))
    print("\tp95: " + str(np.percentile(timeTo5KNP, 95)))
    print("\tp99: " + str(np.percentile(timeTo5KNP, 99)))

    plt.hist(timeTo5KNP, bins=range(1, 20))
    plt.title("MHTW: " + str(bestMHTW) + " -- " + str(handCount) + " iterations")
    plt.xlabel("Mean Hands to Win")
    plt.ylabel("Occurrences")
    plt.savefig("optimum-test-" + str(handCount) + ".png")
    print("Histogram saved!")
