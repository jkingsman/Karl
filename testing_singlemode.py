import hand
import numpy as np
import matplotlib.pyplot as plt

handCount = 1100
turnsTo5K = []

player = hand.kaputHand()
player.silent = True

player.stingyFives = True
player.rollAfterFull = True
player.ignoreTriple2 = False
player.rerollThreshold = 4
player.rerollThresholdAfterFull = 4
player.abandon5Threshold = 50

for _ in range(handCount):
    player.refresh()
    score = 0
    turnCount = 0

    while score < 5000:
        turnCount += 1
        player.refresh()
        while player.handInPlay:
            player.roll()
        score += player.score

    turnsTo5K.append(turnCount)

results = np.array(turnsTo5K)
mean = np.mean(results)

print("====== SINGLE STRATEGY DRILLDOWN: " + str(mean) + " MHTW ======")
print("stingyFives: " + str(player.stingyFives))
print("rollAfterFull: " + str(player.rollAfterFull))
print("ignoreTriple2: " + str(player.ignoreTriple2))
print("rerollThreshold: " + str(player.rerollThreshold))
print("rerollThresholdAfterFull: " + str(player.rerollThresholdAfterFull))
print("abandon5Threshold: " + str(player.abandon5Threshold))
print("")

print("Percentiles & Mean:")
print("\tMean: " + str(mean))
print("\tp10: " + str(np.percentile(results, 10)))
print("\tp50: " + str(np.percentile(results, 50)))
print("\tp90: " + str(np.percentile(results, 90)))
print("\tp95: " + str(np.percentile(results, 95)))
print("\tp99: " + str(np.percentile(results, 99)))

plt.hist(results, bins=range(1, 20))
plt.title("MHTW " + str(mean) + " -- " + str(handCount) + " iterations")
plt.xlabel("Mean Hands to Win")
plt.ylabel("Occurrences")
# plt.show()
