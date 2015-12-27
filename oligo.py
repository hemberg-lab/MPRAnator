#!/Users/Naman/miniconda/bin/python

# importing standard modules
import re, inspect, os, sys;

# some boiler plate code.

import part1
import pdb
import itertools

def testIfWithin(startingPositionsL, motifsL, minSpacing, maxSpacing):
    starting_positions = sorted(zip(startingPositionsL, motifsL))
    startingAndLastPositionsL = [(i[0], i[0] + len(i[1]) - 1, i[1]) for i in starting_positions]

    for index, item in enumerate(startingAndLastPositionsL[:-1]):
        distanceBetweenMotifs = startingAndLastPositionsL[index + 1][0] - item[1] - 1
        if distanceBetweenMotifs < minSpacing or distanceBetweenMotifs > maxSpacing:
            return False
    return True


def testIfFarFromRightEdge(BackgroundS, startingPositionsL, motifsL, distanceFromRightEdge):
    lengthOfBackgroundSequence = len(BackgroundS)
    starting_positions = sorted(zip(startingPositionsL, motifsL))
    startingAndLastPositionsL = [( i[0], i[0] + len(i[1]) - 1, i[1]) for i in starting_positions]

    rightMostMotif = startingAndLastPositionsL[-1]

    if rightMostMotif[1] > lengthOfBackgroundSequence - 1 - distanceFromRightEdge:
        return False
    return True


def oligo(BackgroundS, minSpacing, maxSpacing, motifsL, distanceFromLeftEdge, distanceFromRightEdge, frequencyOfInsertion, backgroundSequenceHeaderS):
        allResults = []


        positionsForMotifsL = [p for p in
                               itertools.product(range(distanceFromLeftEdge, len(BackgroundS)), repeat=len(motifsL))]

        for positionsL in positionsForMotifsL:
            backgroundL = list(BackgroundS.lower())
            backgroundHTMLL = list(BackgroundS.lower())
            for index, individualPositions in enumerate(positionsL):

                currentMotif = motifsL[index].upper()
                backgroundL[individualPositions:individualPositions + len(currentMotif)] = currentMotif
                backgroundHTMLL[individualPositions:individualPositions + len(currentMotif)] = currentMotif
                #backgroundHTMLL[individualPositions:individualPositions + len(currentMotif)] = "<span style='color:red;'>"+currentMotif+"</span>"
                lastIndex = individualPositions + len(currentMotif) - 1
                backgroundLength = len(BackgroundS)
                if not ( lastIndex >= backgroundLength):

                    #print "lastIndex", lastIndex , "backgroundLength", backgroundLength, len(backgroundHTMLL), 'hola'

                    backgroundHTMLL[individualPositions] = "<span style='color:red'>"+backgroundHTMLL[individualPositions]
                    backgroundHTMLL[individualPositions + len(currentMotif)-1] = backgroundHTMLL[individualPositions + len(currentMotif)-1]+"</span>"

                # if len(positionsL) > 1:
                #     pdb.set_trace()
            #CHECK 1 : at the end of the sequence, the mutation adds more letters
            if not (len(backgroundL) > len(BackgroundS)):
                #CHECK 2 :
                if testIfWithin(positionsL, motifsL, minSpacing, maxSpacing):
                    #CHECK 3
                    if testIfFarFromRightEdge(BackgroundS, positionsL, motifsL, distanceFromRightEdge):
                        # YOU ARE DEBUGGING THIS.
                        #CHECK 4
                        if sorted(positionsL)[0] % frequencyOfInsertion == 0:
                            header = sorted(zip(motifsL, positionsL), key=lambda x: x[1])
                            # example of headerString = "BARR-22|FOOO-28"
                            headerString = "|".join(["-".join([i[0],str(i[1])]) for i in header])
                            allResults.append({"header": "> Background-%s|%s" % (backgroundSequenceHeaderS, str(headerString)),
                                               "sequence": "".join(backgroundL),
                                               "sequenceHTML": "".join(backgroundHTMLL)})

        return allResults



if __name__ == "__main__":

    startingPositionsL = (49, 47, 10)
    motifsL = "MUSK ELONS STEVE".split(" ")
    poing = inspect.getabsfile(inspect.currentframe());
    ee = execfile;
    inputMotifL = ['ELON', "TOM", "STEVE"]
    sequence = "aacaaactatcgagacattcgtagcagtaccactgaagatcctgggttatgaccc"
    minSpacing = 2
    maxSpacing = 3
    reverseComplement = "No"

    allCombinations = part1.generateCombinations(inputMotifL)
    allPermutations = part1.generatePermutations(allCombinations)

    output = oligo(sequence, minSpacing, maxSpacing, allCombinations, 1, distanceFromRightEdge=5)

