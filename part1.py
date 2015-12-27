import re
import random as rd
import itertools
import myfunctions as myf

def generatePermutations(theListOfLists):  # Used to make all permutations
    allpermutations = []
    for i in theListOfLists:
        for subset in itertools.permutations(i):
            if subset not in allpermutations:
                allpermutations.append(subset)
    return allpermutations


def generateCombinations(theList):  # Used to make all combinations
    combinationsStore = []
    upTo = len(theList) + 1
    for i in xrange(1, upTo):
        for acomb in itertools.combinations(theList, i):
            combinationsStore.append(acomb)
    return combinationsStore


def equaliseSize(theListofLists, lengthdesired):  # Adds empty strings instead of motifs, if less than 4 motifs are used
    outerList = []
    for i in theListofLists:
        innerList = []
        for j in i:
            innerList.append(j)
        while len(innerList) < lengthdesired:
            innerList.append("")
        outerList.append(innerList)
    return outerList



def gc_cont(bar_code):  # GC/AT ratio taken into account, for thermodynamics and their effects at the experiment
    bar_code = bar_code.upper()
    total_count = bar_code.count("G") + bar_code.count("C")
    return total_count/float(len(bar_code))


# function makes the barcodes
def make_barcode(length):
    barcode = []
    l1=['A','G','C','T']
    for i in range(length):
        barcode.append(rd.choice(l1))
    return ''.join(barcode)


def barcode_generator(number, mingc, maxgc,barCodeLength, diffs=2):  # generates barcodes that differ from existing barcodes by a minimum number of bases, each sequence has a unique barcode
    barcode_storage = []
    countlist = []
    l1 = ['A','G','C','T']

    for i in range(number):
        short_term = make_barcode(barCodeLength)
        if short_term not in barcode_storage and gc_cont(short_term) * 100 < maxgc and gc_cont(
                short_term) * 100 > mingc:
            for bc in barcode_storage:
                count = 0;
                for pos in range(barCodeLength):
                    if short_term[pos] == bc[pos]:
                        count += 1
                    else:
                        pass
                countlist += [count]
            if len(countlist) != 0:
                if max(countlist) < diffs:
                    barcode_storage += [short_term]
                else:
                    while short_term in barcode_storage or gc_cont(short_term) * 100 > maxgc == True or gc_cont(
                            short_term) * 100 < mingc == True:
                        position = rd.choice(range(barCodeLength))
                        short_term = short_term.replace(short_term[position], rd.choice(l1))
                    else:
                        barcode_storage += [short_term]
            else:
                barcode_storage += [short_term]
        else:
            while short_term in barcode_storage or gc_cont(short_term) * 100 > maxgc == True or gc_cont(
                    short_term) * 100 < mingc == True:
                position = rd.choice(range(barCodeLength))
                short_term = short_term.replace(short_term[position], rd.choice(l1))
            else:
                barcode_storage += [short_term]
    return barcode_storage

###########################################################################################################################################################################


def oligosynthesizer(BackgroundS, minSpacing, maxSpacing, permutationsL, ReverseOrNot, windowSize=70):

    middle_background = len(BackgroundS)/2
    Identifier = []
    Sequences = []

    if BackgroundS != '' and not BackgroundS.startswith('>'):

        maxSpacingForRange = int(maxSpacing)+1

        for permutationL in permutationsL:
            for distanceBetween1_2 in range(maxSpacingForRange):
                for distanceBetween2_3 in range(maxSpacingForRange):
                    for distanceBetween3_4 in range(maxSpacingForRange):

                        motiflen = distanceBetween1_2 + distanceBetween2_3 + distanceBetween3_4
                        windowSize = min(windowSize, middle_background)


                        first_position = windowSize - motiflen/2
                        first_position_last = first_position + len(permutationL[0]) - 1

                        second_position = first_position_last + 1 + distanceBetween1_2
                        second_position_last = second_position + len(permutationL[1]) - 1

                        third_position = second_position_last + 1 + distanceBetween2_3
                        third_position_last = third_position + len(permutationL[2]) - 1

                        fourth_position = third_position_last + 1 + distanceBetween3_4
                        fourth_position_last = fourth_position + len(permutationL[3]) - 1


                        startingAndLastPositionsL = [(first_position, first_position_last), (second_position, second_position_last),
                            (third_position, third_position_last), (fourth_position, fourth_position_last)]



                        #for i in startingAndLastPositionsL: print "%s - %s" %(i[0], i[1])

                        # This code block is checking whether the motif distances are within the parameters
                        # minSpacing and maxSpacing. The next code takes care of this.
                        make_sequence_or_no = True
                        for index, item in enumerate(startingAndLastPositionsL[:-1]):
                            distanceBetweenMotifs = startingAndLastPositionsL[index+1][0] - item[1] - 1
                            if distanceBetweenMotifs < minSpacing or distanceBetweenMotifs > maxSpacing:
                                make_sequence_or_no = False
                                break

                        if make_sequence_or_no:
                            # Sequence = ''.join([BackgroundS[:startingPositionsL[0]], permutationL[0],
                            #                     BackgroundS[(startingPositionsL[0] + len(permutationL[0])):startingPositionsL[1]], permutationL[1],
                            #                     BackgroundS[(startingPositionsL[1] + len(permutationL[1])):startingPositionsL[2]], permutationL[2],
                            #                     BackgroundS[(startingPositionsL[2] + len(permutationL[2])):startingPositionsL[3]], permutationL[3],
                            #                     BackgroundS[startingPositionsL[3]:]])

                            BackgroundCopy = list(BackgroundS)
                            for index, (startingPosition, lastPosition) in enumerate(startingAndLastPositionsL):

                                if lastPosition < startingPosition:
                                    pass

                                else:
                                    BackgroundCopy[startingPosition: lastPosition] = permutationL[index]
                            Sequence = "".join(BackgroundCopy)


                            #pdb.set_trace()
                            if Sequence not in Sequences:
                                Sequences += [Sequence]
                                Identifier += [permutationL, distanceBetween1_2, distanceBetween2_3, distanceBetween3_4, ]

                            if ReverseOrNot == 'Yes':  #ReverseComplement if YES to generate these sequences too
                                print "YESSSS THIS IS REERSE OR NOT YES"
                                ReverseComplementBackground = myf.revcompl(BackgroundS)

                                # the insertion begins.. WE EED TO FIX THIS BULSHIT
                                Sequence_ = ''.join([ReverseComplementBackground[:startingAndLastPositionsL[0][0]], permutationL[0],
                                                     ReverseComplementBackground[
                                                     (startingPositionsL[0][0] + len(permutationL[0])):startingPositionsL[1][0]], permutationL[1],
                                                     ReverseComplementBackground[
                                                     (startingPositionsL[1] + len(permutationL[1])):startingPositionsL[2]], permutationL[2],
                                                     ReverseComplementBackground[
                                                     (startingPositionsL[2] + len(permutationL[2])):startingPositionsL[3]], permutationL[3],
                                                     ReverseComplementBackground[startingPositionsL[3]:]])
                                Sequences += [Sequence_]
                                Identifier += [[permutationL, distanceBetween1_2, distanceBetween2_3, distanceBetween3_4, ]]
                        else:
                            print "The if statement is false that means the motif distances are not within the constraints."

    storeID = []
    Step = len(Identifier) / len(Sequences)
    for distanceBetween1_2 in range(0, len(Identifier), Step):
        storeID += [[Identifier[distanceBetween1_2 + distanceBetween3_4] for distanceBetween3_4 in range(Step)]]

    return {"storeID": storeID, "Sequences": Sequences}


##############################################################################################################################################
#

def TotalSeq(Adaptors1, Restriction1, Restriction2, Sequences, barcode_storage, Adaptors2):

    Synthetics = [Adaptors1 + Restriction1 + Sequences[i] + barcode_storage[i]+Restriction2 + Adaptors2]
    return Synthetics


def Invalid_data(Sequences, Restriction):

    for i in Sequences:
        for j in Restriction:
            match = myf.findMatch(i, j)
            if match != {}:

                print "for sequence", i, " and for Restriction Seq", Restriction[j], "and Position", match



def createMPRAResultOutput(finalOutput, numOfBarCodesPerSequence, barCodes, restriction1,
                     restriction2, adapter1, adapter2, ordering):
     response = ""
     sequenceHTMLL = []
     for index, item in enumerate(finalOutput):
                for numTimes in range(numOfBarCodesPerSequence):

                    outputHeader = item['header']

                    if barCodes:
                        outputHeader += "|BARCODE - " + str(numTimes+1)


                    if restriction1:
                        outputHeader += "|RESTRICTION - 1"


                    if restriction2:
                        outputHeader += "|RESTRICTION - 2"


                    if adapter1:
                        outputHeader += "|ADAPTER - 1"


                    if adapter2:
                        outputHeader += "|ADAPTER - 2"


                    outputSequence = ""
                    outputSequenceHTML = ""
                    for orderItem in ordering:

                        if adapter1 and orderItem == "adapter site 1":
                            outputSequence += adapter1
                            outputSequenceHTML += adapter1


                        if restriction1 and orderItem == "restriction site 1":
                            outputSequence += restriction1
                            outputSequenceHTML += restriction1


                        elif orderItem == "Background":

                            outputSequence += item['sequence']
                            if not item.get('sequenceHTML'):
                                outputSequenceHTML += item.get('sequence')
                            else:
                                outputSequenceHTML += item.get('sequenceHTML')


                        elif restriction2 and orderItem == "restriction site 2":
                            outputSequence += restriction2
                            outputSequenceHTML += restriction2


                        elif adapter2 and orderItem == "adapter site 2":
                            outputSequence += adapter2
                            outputSequenceHTML += adapter2


                        elif barCodes and orderItem == "Barcode":
                            outputSequence += barCodes[index * numOfBarCodesPerSequence + numTimes]
                            outputSequenceHTML += barCodes[index * numOfBarCodesPerSequence + numTimes]


                    outputSequence += "\n"
                    if restriction1:
                        #if outputSequence.lower().count(restriction1.lower()) > 1:
                        if len(myf.findMatch(sequenceS=outputSequence.lower(), motifS=restriction1.lower()) ) > 1:
                            outputHeader += "|DUPLICATE_RESTRICTION_SITES - RESTRICTION1"

                    if restriction2:
                        # if outputSequence.lower().count(restriction2.lower()) > 1:
                        if len(myf.findMatch(sequenceS=outputSequence.lower(), motifS=restriction2.lower()) ) > 1:
                            outputHeader += "|DUPLICATE_RESTRICTION_SITES - RESTRICTION2"

                    outputHeader += "\n"
                    response += outputHeader
                    response += outputSequence
                    sequenceHTMLL.append([outputHeader, outputSequenceHTML])
     return response, sequenceHTMLL


def getBarCodes(barCodeLength, minimumGCContent, maximumGCContent, numOfBarCodesPerSequence, barCodeDistance, finalOutput):

            """
            This returns the barcodes ( as a list of strings or just 'None').

            :param barCodeLength:
            :param minimumGCContent:
            :param maximumGCContent:
            :param numOfBarCodesPerSequence:
            :param barCodeDistance:
            :param finalOutput:
            :return: a tuple of 2 elements. First element - barCodes. Second element - number of barcodes per sequence
            """

            barCodes = None
            # checking if the user wants to input barcodes.
            if barCodeLength and minimumGCContent and maximumGCContent and numOfBarCodesPerSequence:
                editdistance = 2
                if barCodeDistance: editdistance = barCodeDistance
                barCodes = barcode_generator(len(finalOutput) * numOfBarCodesPerSequence, minimumGCContent,
                                               maximumGCContent, barCodeLength=barCodeLength, diffs=editdistance)
            else:
                numOfBarCodesPerSequence = 1 # NOTE THIS DOES NOT ACTUALLY MEAN 1 barcode per sequence. this
                # else statement means 0 numOfBarCodesPerSequence.
            return barCodes, numOfBarCodesPerSequence