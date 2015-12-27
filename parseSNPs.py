import re, os, sys, itertools
import mycustom as mc
import pdb

#Inputs of users are SNPs in VCF format and FASTA file with sequences of equal size.
#The headers in the FASTA file MUST contain the following information chr:start-end 


def read_SNPs(SNP_file_path):
    # tab delimited file
    read_SNPs = open(SNP_file_path, "r")
    SNP_file = read_SNPs.readlines()
    read_SNPs.close()
    SNP_data = []
    for i in SNP_file:
        SNP_data += [i.strip().split('\t')]
    return SNP_data


def generateCombinations(theList):  # Used to make all combinations
    combinationsStore = []
    upTo = len(theList) + 1
    for i in xrange(1, upTo):
        for acomb in itertools.combinations(theList, i):
            combinationsStore.append(acomb)
    return combinationsStore	


# if the SNP contains a small deletion or insertion (smaller than 10nt) we either remove part of the sequence or we insert adenines in one edge
# the user can decide if he wants to include combinations of SNPs in the effects with variable Combinations = True or False
def make_sequence_copies(SNPs, NamesL, SequencesL, CombinationsB):
    ExtraSequences=[]
    ExtraNames=[]
    All_groups=[]
    htmlSequences = []
    if CombinationsB == True:
        for j in range(len(NamesL)):
            chromosome_number = NamesL[j][0]
            start = int(NamesL[j][1])
            end = int(NamesL[j][2])
            PerSequence=[]
            for i in SNPs:
                SNP_chromosome_number = i[0]
                Position = int(i[1])
                REF = i[3]
                ALT = i[4]
                if str(SNP_chromosome_number) == str(chromosome_number):
                    if Position >= start and Position <= end:
                        PerSequence+=[i]
            All_groups+=[PerSequence]
        for f in range(len(All_groups)):
            if All_groups[f]!=[]:
                combs=generateCombinations(All_groups[f])
                for comb in combs: #for every SNP combination
                    Sequenced = [SequencesL[f].sequence]
                    SequencedHTML= [SequencesL[f].sequence]

                    #pdb.set_trace()
                    print "This is in combs", Sequenced
                    Named=[NamesL[f]]

                    for snped in comb:
                        SNP_chromosome_number = snped[0]
                        Position = int(snped[1])
                        REF = snped[3]
                        if REF == ".":
                            REF = ""
                        ALT = snped[4]

                        chromosome_number = NamesL[f][0]
                        start = int(NamesL[f][1])
                        end = int(NamesL[f][2])
                        if (str(SNP_chromosome_number) == str(chromosome_number)) and ( start <= Position <= end):
                                position_to_change = int(Position - start)
                                changes = ALT.split(",")

                                for change in changes:
                                    if change == ".":
                                        change == ""
                                    initial_size = len(REF)
                                    SNP_size = len(change)
                                    difference = initial_size - SNP_size
                                    if abs(difference)<10:
                                        for index in range(len(Sequenced)):
                                            if type(Named[index]) == tuple:
                                                stemHeader = " ".join([str(iS) for iS in Named[index]])+"| SNP "+str(snped[2])+" | Position "+ str(Position)+" | Nucleotide change "+REF+ ":" +change
                                            else:
                                                stemHeader = Named[index]+"| SNP "+str(snped[2])+" | Position "+ str(Position)+" | Nucleotide change "+REF+ ":" +change
                                            print "This is stemHeader", stemHeader

                                            if abs(difference) < position_to_change:

                                                if difference < 0:
                                                    Sequenced+=[Sequenced[index][abs(difference):position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    SequencedHTML +=[Sequenced[index][abs(difference):position_to_change] + "<span style='color:red;'>"+str(change)+"</span>" + Sequenced[index][position_to_change + 1:]]

                                                    Named +=[ stemHeader +" removed "+str(abs(difference)) +" nucleotides from left edge"]
                                                if difference==0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    SequencedHTML += [Sequenced[index][:position_to_change] + "<span style='color:red;'>"+str(change)+"</span>"  + Sequenced[index][position_to_change + 1:]]

                                                    Named +=[ stemHeader]
                                                if difference > 0:  # deletion
                                                    Sequenced += [difference*"A"+Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1 + difference:]]
                                                    SequencedHTML += [difference*"A"+Sequenced[index][:position_to_change] +"<span style='color:red;'>"+str(change)+"</span>"  + Sequenced[index][position_to_change + 1 + difference:]]

                                                    Named += [stemHeader + " | added " +str(difference)+" Adenines bases in the left edge"]

                                            else:
                                                if difference < 0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:-abs(difference)]]
                                                    SequencedHTML +=[Sequenced[index][:position_to_change] + "<span style='color:red;'>"+str(change)+"</span>"  + Sequenced[index][position_to_change + 1:-abs(difference)]]

                                                    Named +=[ stemHeader +" removed "+str(abs(difference)) +" nucleotides from right edge"]
                                                if difference==0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    SequencedHTML +=[Sequenced[index][:position_to_change] + "<span style='color:red;'>"+str(change)+"</span>"  + Sequenced[index][position_to_change + 1:]]

                                                    Named +=[stemHeader]
                                                if difference > 0:  # deletion
                                                    Sequenced += [Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1 + difference:]+difference*"A"]
                                                    SequencedHTML += [Sequenced[index][:position_to_change] + "<span style='color:red;'>"+str(change)+"</span>"  + Sequenced[index][position_to_change + 1 + difference:]+difference*"A"]
                                                    Named += [stemHeader + " | added " +str(difference)+" Adenines bases in the right edge"]
                    Named[0]= " ".join( [str(i) for i in NamesL[f]] ) + "| REFERENCE "

                    print "Thsi is named,", Named
                print "This is sequenced", Sequenced

                ExtraSequences+= Sequenced
                htmlSequences += SequencedHTML

                ExtraNames+= Named

    else:
        ExtraSequences=[]
        ExtraNames=[]
        for i in SNPs:

            SNP_chromosome_number=i[0]
            Position=int(i[1])
            REF=i[3]
            ALT=i[4]
            for j in range(len(NamesL)):
                #pdb.set_trace()
                chromosome_number=NamesL[j][0]
                start=int(NamesL[j][1])
                end=int(NamesL[j][2])
                if str(SNP_chromosome_number)==str(chromosome_number):
                    if Position >= start and Position<=end:
                            position_to_change=int(Position-start)
                            if REF == ".":
                                REF = ""
                            size=len(REF)
                            changes=ALT.split(",")
                            number_of_changes=len(changes)
                            size_of_each_change=[len(f) for f in changes]

                            for change in changes:
                                if change == ".":
                                    change = ""
                                initial_size=len(REF)
                                SNP_size=len(change)
                                difference=initial_size-SNP_size
                                if abs(difference)<10:
                                    stemHeader = " ".join( [str(iS) for iS in NamesL[j]] )+"| SNP "+str(i[2])+" | Position "+ str(Position)+" | Nucleotide change "+REF+ ":" +change
                                    if abs(difference)<position_to_change:

                                        if difference<0:
                                            ExtraSequences+=[SequencesL[j][abs(difference):position_to_change]+str(change)+SequencesL[j][position_to_change+1:]]
                                            ExtraNames+=[ stemHeader+" | removed "+ str(abs(difference)) +" nucleotides from left edge"]
                                        if difference==0:
                                            ExtraSequences+=[SequencesL[j][:position_to_change]+str(change)+SequencesL[j][position_to_change+1:]]
                                            ExtraNames+=[stemHeader]
                                        if difference>0:  #deletion
                                            ExtraSequences+=[difference*"A"+SequencesL[j][:position_to_change]+str(change)+SequencesL[j][position_to_change+1+difference:]]
                                            ExtraNames+=[stemHeader + "| added " +str(difference)+" Adenines bases in the left edge"]
                                    if abs(difference)>=position_to_change:
                                        if difference<0:
                                            ExtraSequences+=[SequencesL[j][:position_to_change]+str(change)+SequencesL[j][position_to_change+1:-abs(difference)]]
                                            ExtraNames+=[stemHeader +" | removed "+ str(abs(difference))+ " nucleotides from right edge"]
                                        if difference==0:
                                            ExtraSequences+=[SequencesL[j][:position_to_change]+str(change)+SequencesL[j][position_to_change+1:]]
                                            ExtraNames+=[stemHeader]
                                        if difference>0:  #deletion
                                            ExtraSequences+=[SequencesL[j][:position_to_change]+str(change)+SequencesL[j][position_to_change+1+difference:]+difference*"A"]
                                            ExtraNames+=[stemHeader+"| added " +str(difference)+" Adenines bases in the right edge"]

                            ExtraSequences += [SequencesL[j].sequence]
                            ExtraNames += [" ".join( [str(iS) for iS in NamesL[j]] )+"| REFERENCE "]
        Seqs_=[]
        Nams_=[]
        for st in range(len(ExtraSequences)):
            if ExtraSequences[st] not in Seqs_:

                Seqs_+=[ExtraSequences[st]]
                Nams_+=[ExtraNames[st]]


        ExtraNames = Nams_

        ExtraSequences = Seqs_


    ExtraNamesWithArrow = [ ">"+yS for yS in ExtraNames]
    if len(ExtraNamesWithArrow) == len(ExtraSequences):
        return ExtraNamesWithArrow, ExtraSequences
    else:
        return

def naman_make_sequence_copies(snpO, sequenceO, combinationsB):

    subbedSequencesL = []
    sequenceHeadersL = []

    for i in sequenceO:
        subbedSequencesL.append(i.sequence)
        sequenceHeadersL.append(str(i.headerRange))
    if combinationsB:
        pass
    else:
        for snpL in snpO:
            for sequence in sequenceO:
                if snpInChromosomeRegion(snpL, sequence):

                    sequencesL, headersL = makeSequenceAndmakeHeader(snpL, sequence)
                    subbedSequencesL += sequencesL
                    sequenceHeadersL += headersL

    return subbedSequencesL, sequenceHeadersL

def getPositionToChange(snpL, sequence):
    snpPosition = int(snpL[1])
    seqStart = int(sequence.headerRange[1])
    return snpPosition - seqStart

def make_sequence_copies2(snpO, sequenceO, CombinationsB):
    """
    correcting ilias's garbage. still need to work on this.
    :param snpO:
    :param NamesL:
    :param SequencesL:
    :param CombinationsB:
    :return:
    """
    ExtraSequences=[]
    ExtraNames=[]
    All_groups=[]

    NamesL = [i.headerRange for i in sequenceO]
    SequencesL = sequenceO.getSequences()
    for j, (chromosome_number, start, end) in enumerate(NamesL):
        ExtraSequences += [SequencesL[j].sequence]
        ExtraNames += [" ".join( [str(iS) for iS in NamesL[j]] )+"| REFERENCE "]

    if CombinationsB == True:

        All_groups = getSnpGroupsinAllSeqs(snpO, NamesL)

        for f in range(len(All_groups)):

            if All_groups[f]!=[]: # well if sequence has snps

                combs = generateCombinations(All_groups[f])
                for comb in combs: #for every SNP combination

                    Sequenced = [SequencesL[f].sequence]

                    Named = [NamesL[f]]

                    for snped in comb:
                            SNP_chromosome_number = snped[0]
                            Position = int(snped[1])
                            REF = snped[3]
                            ALT = snped[4]

                            chromosome_number = NamesL[f][0]
                            start = int(NamesL[f][1])
                            end = int(NamesL[f][2])
                            position_to_change = int(Position - start)
                            changes = ALT.split(",")

                            if "." not in ALT:
                                for change in changes:
                                        initial_size = len(REF)
                                        SNP_size = len(change)
                                        difference = initial_size - SNP_size
                                        # pdb.set_trace()
                                        # preTrimSubbedSeq = substituteIntoSequence(Sequenced[0], position_to_change, change)


                                        for index in range(len(Sequenced)):

                                            if type(Named[index]) == tuple:
                                                stemHeader = " ".join([str(iS) for iS in Named[index]])+"| SNP "+str(snped[2])+" | Position "+ str(Position)+" | Nucleotide change "+REF+ ":" +change
                                            else:
                                                stemHeader = Named[index]+"| SNP "+str(snped[2])+" | Position "+ str(Position)+" | Nucleotide change "+REF+ ":" +change
                                            print "This is stemHeader", stemHeader

                                            if abs(difference) < position_to_change:

                                                if difference < 0:
                                                    Sequenced+=[Sequenced[index][abs(difference):position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    Named +=[ stemHeader +" removed "+str(abs(difference)) +" nucleotides from left edge"]
                                                if difference==0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    Named +=[ stemHeader]
                                                if difference > 0:  # deletion
                                                    Sequenced += [difference*"A"+Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1 + difference:]]
                                                    Named += [stemHeader + " | added " +str(difference)+" Adenines bases in the left edge"]

                                            else:
                                                if difference < 0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:-abs(difference)]]
                                                    Named +=[ stemHeader +" removed "+str(abs(difference)) +" nucleotides from right edge"]
                                                if difference==0:
                                                    Sequenced+=[Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1:]]
                                                    Named +=[stemHeader]
                                                if difference > 0:  # deletion
                                                    Sequenced += [Sequenced[index][:position_to_change] + str(change) + Sequenced[index][position_to_change + 1 + difference:]+difference*"A"]
                                                    Named += [stemHeader + " | added " +str(difference)+" Adenines bases in the right edge"]



                ExtraSequences += Sequenced

                ExtraNames += Named

    else:

        for i in snpO:
            SNP_chromosome_number = i[0]
            Position = int(i[1])
            snpID = i[2]
            REF = i[3]
            ALT = i[4]

            # for j, (chromosome_number, start, end) in enumerate(NamesL):
            for sequence in sequenceO:

                if snpInChromosomeRegion(i, sequence):

                        position_to_change = int(Position)-int(start)
                        changes = ALT.split(",")

                        if "." not in ALT:
                            for change in changes:

                                initial_size = len(REF)
                                SNP_size = len(change)
                                difference = initial_size-SNP_size
                                preTrimSubbedSeq = substituteIntoSequence(currentSeq, position_to_change, change)

                                trimmedSeq, header = trimSequenceAndMakeHeader(preTrimSubbedSeq, currentSeq, position_to_change,
                                                          difference, chromosome_number, start, end, snpID, Position, REF, change, defaultNucToFill="A")

                                #trimmedSeq, header = createSequenceAndMakeHeader(i, NamesL[j], currentSeq)
                                ExtraSequences += [trimmedSeq]
                                ExtraNames += [header]


    ExtraNamesWithArrow = [ ">"+yS for yS in ExtraNames]
    if len(ExtraNamesWithArrow) == len(ExtraSequences):
        return ExtraNamesWithArrow, ExtraSequences
    else:
        return

def snpInChromosomeRegion(snpL, sequence):
    """
    checking if snp is within the chromosome region
    :return: boolean
    """
    snpChromosome =  snpL[0]
    snpPosition = snpL[1]
    seqChromosome = sequence.headerRange[0]
    seqStart = sequence.headerRange[1]
    seqEnd = sequence.headerRange[2]

    if str(snpChromosome) == str(seqChromosome) and ( ( int(snpPosition) >= int(seqStart)) and (int(snpPosition) <= int(seqEnd)) ):
        return True
    return False

def substituteIntoSequence(sequenceS, position, nucToSubstituteS):
    """

    :param sequenceS (string) -
    :param position (int) -
    :param nucToSubstituteS (string) - the nucleotide(s) that will substitute at the position
    :return: string. The substituted sequenceS
    """
    outputSequenceL = list(sequenceS)
    outputSequenceL[int(position)] = nucToSubstituteS
    return "".join(outputSequenceL)


def trimSequenceAndMakeHeader(preTrimSubbedSeq, currentSeq, position_to_change, difference, snpL, change,
                               defaultNucToFill="A"):

    chromosome_number = snpL[0]
    start = currentSeq.headerRange[1]
    end = currentSeq.headerRange[2]
    snpID = snpL[2]
    Position = snpL[1]
    REF = snpL[3]

    header = "%s %s %s | SNP %s | Nucleotide change %s%s%s " % (chromosome_number, start, end, snpID,  REF, Position, change)
    pdb.set_trace()
    adeninesToAdd = abs(difference)*defaultNucToFill
    trimmedSeq = preTrimSubbedSeq

    if position_to_change > len(currentSeq)/2:

        if difference < 0:
            trimmedSeq = trimmedSeq[abs(difference):]
            header += "| removed %s nucleotides from the left edge" % abs(difference)

        elif difference > 0:
            trimmedSeq = trimmedSeq + adeninesToAdd
            header += "| added %s nucleotides from the right edge" % abs(difference)
    else:
        if difference < 0:
            trimmedSeq = trimmedSeq[:difference]
            header += "| removed %s nucleotides from the right edge" % abs(difference)

        elif difference > 0:
            header += "| added %s nucleotides from the left" % abs(difference)
            trimmedSeq = adeninesToAdd + trimmedSeq

    return trimmedSeq, header


def makeSequenceAndmakeHeader(snpL, sequence):


    subbedSequencesL = []
    sequenceHeadersL = []

    positionToChange = getPositionToChange(snpL, sequence)
    targetsL = snpL[4].split(",")

    for targetS in targetsL:
        difference = len(snpL[3])-len(targetS)

        preTrimSubbedSeq = substituteIntoSequence(sequence.sequence, positionToChange, targetS)
        pdb.set_trace()
        trimmedSeq, header = trimSequenceAndMakeHeader(preTrimSubbedSeq=preTrimSubbedSeq,
                                                       currentSeq=sequence,
                                                       position_to_change=positionToChange,
                                                       snpL=snpL,
                                                       difference=difference,
                                                       change=targetS,
                                                        defaultNucToFill="A")

        subbedSequencesL.append(trimmedSeq)
        sequenceHeadersL.append(header)

    return subbedSequencesL, sequenceHeadersL

def getSnpGroupsinAllSeqs(SNPs, NamesL):

    allGroups = []

    for j in range(len(NamesL)):

        chromosome_number = NamesL[j][0]
        start = int(NamesL[j][1])
        end = int(NamesL[j][2])
        PerSequence=[]

        for i in SNPs:
            SNP_chromosome_number = i[0]
            snpPosition = int(i[1])
            REF = i[3]
            ALT = i[4]

            if snpInChromosomeRegion(SNP_chromosome_number, snpPosition,
                                     chromosome_number, start, end):
                    PerSequence.append(i)

        allGroups.append(PerSequence)

    return allGroups
