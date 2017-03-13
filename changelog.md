# Changelog & Scores

## VERSION 0.0.1

**Won: 0**
**Lost: 1**

Beat Evan!

Optimal play:
```
player.rerollThreshold = 5
player.stingyFives = True
player.rollAfterFull = True
player.rerollThresholdAfterFull = 5
```

## Version 0.2.0

* Added option to ignore triple 2's
* Added option to abandon 5 collection at a certain threshold
* Added endgame mode management
* Process 1's and 5's separately

**Won: 0**
**Lost: 1**


Optimal play:
```
player.stingyFives = True
player.rollAfterFull = True
player.ignoreTriple2 = True
player.rerollThreshold = 6
player.rerollThresholdAfterFull = 6
player.abandon5Threshold = 450
```
