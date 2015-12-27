import oligo
from django.test import SimpleTestCase,TestCase

from collections import Counter
import pdb


class TestOligo(SimpleTestCase):
    def setUp(self):
        self.backgroundS = "AGTAGTAGACAGGTAGACAATACGAGGTAGCAGGTTTGATATTGATCCGTAG"
        self.backgroundLengthI = len(self.backgroundS)
        self.motifsL = ["FOOOM", "BARRY", "HELLO"]
        self.distanceFromRight = 5
        self.distanceFromLeft = 2
        self.minSpacing = 2
        self.maxSpacing = 3
        self.frequencyOfInsertion = 1
        self.output = None
        self.backgroundSequenceHeaderS = "haemoglobin"

    def getOutput(self):
        if self.output == None:
            output = oligo.oligo(BackgroundS=self.backgroundS,
                                      minSpacing=self.minSpacing,
                                      maxSpacing=self.maxSpacing,
                                      motifsL=self.motifsL,
                                      distanceFromLeftEdge=self.distanceFromLeft,
                                      distanceFromRightEdge=self.distanceFromRight,
                                      frequencyOfInsertion=1,
                                      backgroundSequenceHeaderS=self.backgroundSequenceHeaderS)

            self.output = [i['sequence'] for i in output]
        return self.output

    def testLengthsEqualToBackground(self):
        """
        This tests whether the length of the output is equal to
        the background (input).

        It also tests all the lengths of the output sequences be equal.
        """
        output = self.getOutput()

        # getting the length of each output sequence
        outputSequenceLengths = [len(sequenceS) for sequenceS in output]

        # getting the distribution of the lengths
        counterDict = dict(Counter(outputSequenceLengths))

        # All the results should have the same length
        self.assertEqual(len(counterDict.keys()), 1)

        # The background length should  == length of output sequences.
        self.assertEqual(self.backgroundLengthI, counterDict.keys()[0])

    def testDistanceFromEdges(self):

        """
        This tests whether the left and right
        edges of the output sequences are
        equal to the left and right edges of
        the input sequence, as per the 'self.distanceFromLeft'
        and 'self.distanceFromRight' parameters.
        """

        output = self.getOutput()

        for sequence in output:
            outputRightEdge = sequence[-1*self.distanceFromRight:].upper()
            backgroundRightEdge = self.backgroundS[-1*self.distanceFromRight:].upper()
            outputLeftEdge = sequence[:self.distanceFromLeft].upper()
            backgroundLeftEdge = self.backgroundS[:self.distanceFromLeft]

            # testing the right edges should be equal.
            self.assertEqual(outputRightEdge, backgroundRightEdge)

            # testing the left edges should be equal.
            self.assertEqual(outputLeftEdge, backgroundLeftEdge)



