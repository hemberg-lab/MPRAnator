import mycustom as mc

def getMotifAndSequenceObjects(motifF, motifS, sequenceF, sequenceS):

    if motifF:
        motifO = mc.FastaFile(motifF, fileName=False)
    elif motifS:
        motifO = mc.FastaFile(motifS, fileName=False)

    if sequenceF:
            sequenceO = mc.FastaFile(sequenceF, fileName=False)
    elif sequenceS:
            sequenceO = mc.FastaFile(sequenceS, fileName=False)


    return sequenceO, motifO
