import pdb
import re

class GenericFile(object):

    def __init__(self, fileNameS):
            try:
                fileF = open(fileNameS)
                self.fileS = fileF.read()
                fileF.close()
            except: # fileNameS could be a file Object.
                self.fileS = fileNameS.read()



class FastaFile(GenericFile):
    """
    This class represents a FastaFile.
    """

    def __init__(self, fasta, fileName=True):
        """

        :rtype : object
        :param fasta: This can be either a file name (string) or a HTML file upload element.
        :param fileName: This is a boolean value. If False, then it is the fasta string
        :return: does not return anything.
        """
        if fileName == True:
            super(FastaFile, self).__init__(fasta)
        elif fileName == False:
            if ">" not in fasta:
                raise ValueError("It is not in Fasta Format")
            self.fileS = fasta
        else:
            raise Exception

        self.sequences = None
        self.sequences = self.getSequences()


    def __getitem__(self, item):
        if self.sequences is None:
            self.getSequences()
        return self.sequences[item]

    def __len__(self):
        return len(self.getSequences())

    def __repr__(self):
        return "< Fasta file: %s sequences >" % len(self)

    def __str__(self):
        return "< Fasta file: %s sequences >" % len(self)

    def getSequences(self):
        if self.sequences is None:
            firstSplitL = self.fileS.strip().split(">")[1:]
            eachByLineL = [i.splitlines() for i in firstSplitL]

            sequences = []
            for i in eachByLineL:
                header = i[0]
                sequence = "".join(i[1:]).upper()
                sequence = sequence.replace(" ", "")
                sequence = sequence.replace("\t", "")
                if sequence == "":
                    raise ValueError("There is no sequence !")
                sequences.append(Sequence(name=header, sequence=sequence))

            self.sequences = sequences

        return self.sequences

    def getMaxLength(self):
        """
        This returns the max length of a sequence in this object.
        """
        sequences = self.getSequences()
        maxLength = 0
        for sequence in sequences:
            seqLength = len(sequence)
            if seqLength > maxLength:
                maxLength = seqLength
        return maxLength


    def getMinLength(self):
        """
        This returns the min length of a sequence in this object.
        """
        sequences = self.getSequences()
        minLength = 1000000000000
        for sequence in sequences:
            seqLength = len(sequence)
            if seqLength < minLength:
                minLength = seqLength
        return minLength


    def areDuplicatesPresent(self):
        sequences = self.getSequences()
        sequenceL = [i.sequence for i in sequences]
        if len(sequenceL) > len(set(sequenceL)):
            return True
        return False

    def getNames(self):

        names = [sequence.name for sequence in self.sequences]
        return names

    def lengthsSame(self):
        sequences = self.getSequences()
        lengthsL = set([len(i.sequence) for i in sequences])

        if len(lengthsL) != 1:
            return False

        return True



class Sequence(object):
    """
    This class represents a DNA/RNA sequence.
    Each object needs to have a name.
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

    def __repr__(self):
        return "%s : %s" %(self.name, self.sequence)

    def __getitem__(self, item):
        return self.sequence[item]

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return "%s : %s " % (self.name, self.sequence)

class FastaFileWithHeaderRange(FastaFile):

     def getSequences(self):
        if self.sequences is None:
            firstSplitL = self.fileS.strip().split(">")[1:]
            eachByLineL = [i.splitlines() for i in firstSplitL]

            sequences = []
            for i in eachByLineL:
                header = i[0]
                headerRange = self.getHeaderRange(header)
                sequence = "".join(i[1:]).upper()
                sequence = sequence.replace(" ", "")
                sequence = sequence.replace("\t", "")
                if sequence == "":
                    raise ValueError("There is no sequence !")
                sequences.append(SequenceWithRange(name=header, sequence=sequence, headerRange=headerRange))

            self.sequences = sequences

        return self.sequences

     def getHeaderRange(self, headerS):

         """
            eg: chr15:12900-12950
         :param headerS:
         :return:
         """

         positionL = re.findall(r"chr(\w+):(\d+)-(\d+)", headerS)
         if len(positionL) == 0:
             raise ValueError("Header does not contain chromosome and positions in the proper format. eg. 'chr1:start-end'")

         positionL = positionL[0]
         chrNumber = positionL[0].upper()
         if chrNumber.isdigit():
             if int(chrNumber) < 1 or int(chrNumber) > 23 :
                 raise ValueError("Chromosome numbers are between 1 and 22")

         if not chrNumber.isdigit() and chrNumber not in ["X","Y"]:
             raise ValueError("Only 'X' and 'Y' are accepted for chromosome letters")

         return positionL

class SequenceWithRange(Sequence):

    def __init__(self, name, sequence, headerRange):
        self.name = name
        self.sequence = sequence
        self.headerRange = headerRange

class BedFile(GenericFile):
     def __init__(self, bed, fileName=True):
        """
        :rtype : object
        :param fasta: This can be either a file name (string) or a HTML file upload element.
        :param fileName: This is a boolean value. If False, then it is the fasta string
        :return: does not return anything.
        """
        if fileName == True:
            super(BedFile, self).__init__(bed)
        elif fileName == False:
            self.fileS = bed
        else:
            raise Exception

        self.sequences = None
        self.sequences = self.getPositions()


     def getPositions(self):
        if self.sequences is None:
            firstSplitL = self.fileS.strip().split("\n")
            eachByLineL = [re.split(r"\s+", i.strip()) for i in firstSplitL]

            sequences = []
            for i in eachByLineL:
                if len(i) < 3:
                    raise ValueError("less than 3 columns, probably not a bed file")
                if i[0][:3] != "chr" or len(i[0]) < 4:
                    raise ValueError("doesn't start with 'chr', probably not a bed file")

                sequences.append(i)

            self.sequences = sequences

        return self.sequences

     def __repr__(self):
        return "< Bed file: %s sequences >" % len(self)

     def __len__(self):
        return len(self.getPositions())


class SnpFile(GenericFile):
     def __init__(self, snp, fileName=True):
        if fileName == True:
            super(SnpFile, self).__init__(snp)
        elif fileName == False:
            self.fileS = snp
        else:
            raise ValueError("fileName should be a boolean")

        self.chromosomes = [str(i) for i in range(1, 23)] + ["X", "Y"]
        self.snps = None
        self.snps = self.getSnps()

        self.maximumTargetSize = 10

     def getSnps(self):
        if self.snps == None:

            firstSplitL = self.fileS.strip().split("\n")

            eachByLineL = [re.split(r"\s+", i.strip()) for i in firstSplitL]

            # Error checking
            for i in eachByLineL:

                if len(i) < 5:
                    raise ValueError("less than 5 columns, probably not a VCF file")

                if not i[0].upper() in self.chromosomes:
                    raise ValueError("Chromosome position should be between 1-22 or X or Y")

                lettersL = set(list("ATGCU."))
                firstNucPosL = set(list(i[3].upper()))
                secondNucPosL = set(list("".join(i[4].split(",")).upper()))

                if len(firstNucPosL - lettersL) > 0 or len(secondNucPosL - lettersL) > 0:
                     raise ValueError("There should be %s for the nucleotide positions, so probably not a VCF file." % "".join(lettersL))

            self.snps = eachByLineL
        return self.snps

     def getMaximumTargetSize(self):
         snps = self.snps
         targetSizesL = []
         for snpL in snps:
             targetsL = snpL[4].split(",")
             for targetS in targetsL:
                 targetSizesL.append(len(targetS))

         return max(targetSizesL)

     def __repr__(self):
         return "< Snp file: %s locations>" % len(self)

     def __len__(self):
         return len(self.getSnps())

     def __getitem__(self, item):
        if self.snps is None:
            self.getSnps()
        return self.snps[item]