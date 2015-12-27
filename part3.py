import random as rd

import myfunctions as myf

def scramble_motifs(motif):
    """Args: takes as input a string, generates as output the shuffled string"""
    motif = list(motif)
    rd.shuffle(motif)
    return ''.join(motif)


# Mutate motifs
def mutateString(sequenceS, noOfPos, mapperDict=myf.mapperDict):
    """
    Args: This function mutates a string
        It uses a helper function which is mutateScrambled
        noOfPos will choose the number of mutations of helper function
        TheString is the Motif of interest
	"""

    noOfPos = int(noOfPos)
    if list(set(sequenceS)) == ["N"]:
        raise ValueError("Please do not enter a string only containing N")

    if int(noOfPos) > (len(sequenceS) - sequenceS.count("N")):
        raise ValueError("Number of positions cannot be greater than the length of the sequence")

    LengthList = range(len(sequenceS))
    positionsChosenL = []

    # this part picks index positions excluding "N";
    for i in range(noOfPos):
        posChosen = rd.choice(LengthList)
        while sequenceS[posChosen] == "N" or posChosen in positionsChosenL:
            posChosen = rd.choice(LengthList)
        positionsChosenL.append(posChosen)


    # this part mutates.
    stringL = list(sequenceS)

    for i in positionsChosenL:

        therandomchoice = rd.choice(mapperDict[stringL[i]])
        stringL[i] = therandomchoice

    mutatedmotif = "".join(stringL)
    return mutatedmotif, positionsChosenL


