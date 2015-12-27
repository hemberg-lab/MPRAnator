import math
from math import log10, floor
from collections import Counter
import numpy as np
import re

mapperDict = {"A": 'TGC', "G": 'ACT', "C": 'TGA', "T": 'GCA', "M": 'GT', "K": 'AC', "W": 'GC', "S": 'AT', "Y": 'AG',
                  "R": 'TC', 'H': 'G', "V": 'T', "D": 'C', "B": 'A'}

def complement(backgroundS):

    complementD = {"A": "T", "T": "A", "G": "C", "C": "G", "R": "Y", "Y": "R", "S": "W", "W": "S", "M": "K", "K": "M",
                  "B": "V", "V": "B", "D": "H", "H": "D", "N": "N"}

    return "".join([complementD[i] for i in backgroundS])

def revcompl(backgroundS):

    """

    :param backgroundS (string) - The sequence to be reverse complemented.
    :return: string.
    """

    return complement(backgroundS[::1])


def regex_mapper(s):
    """

    :param s (string) - This converts non-nucleotide letters to possible nucleotides.
    :return: string.
    """

    D = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'R': '[A|G]', 'Y': '[C|T]', 'N': '[A|T|G|C]', 'S': '[G|C]',
         'W': '[A|T]', 'K': '[G|T]', 'M': '[A|C]', 'B': '[CGT]', 'D': '[A|G|T]', 'H': '[A|C|T]', 'V': '[A|C|G]'}
    upperS = s.upper()
    outputString = ""
    for nucleotide in upperS:
        outputString += D[nucleotide]
    return outputString



def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)


def findMatch(sequenceS, motifS, getRevCompMatch=True):
    """
    This function find the positions of the motif matches in a sequence.

    :param sequenceS (string) - The sequence.
    :param motifS (string) - The motif.
    :param getRevCompMatch (boolean) - Dictates if matches need to be
    found in the reverse complemented sequence.
    :return list.
    """

    output = []

    thePattern = regex_mapper(motifS)

    theMatches = re.finditer(thePattern, sequenceS)

    for i in theMatches:
        output.append(i.start())

    if getRevCompMatch == True:
        revCompSequenceS = revcompl(sequenceS)
        theMatches = re.finditer(thePattern, revCompSequenceS)

        for i in theMatches:
            output.append(len(revCompSequenceS) - i.start() - 1)

    return output


def highlightString(stringToHighlight, positionsL, color="red"):
    stringToHighlightL = list(stringToHighlight)

    for index in positionsL:
        stringToHighlightL[index] = "<span style='color:%s;'>%s</span>" % (color, stringToHighlightL[index])

    return "".join(stringToHighlightL)


if __name__ == "__main__":
    matches =  [6, 286, 460, 532, 572, 1043, 1063, 1115, 1137, 1141, 1147]
    length = 1231
