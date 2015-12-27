from django.test import TestCase
import mycustom as mc
import part3


class TestCustomClasses(TestCase):
    def setUp(self):
        self.sampleFasta = ">hello\nAGAGATACATAGACAATGTG  "
        self.sampleFastas = ">hello\nAGAGATACATAGACAATGTG\nTTGCGTAG\nAGATAG  \n >hello2 \nTTTTGGAA"


    def test_One(self):
        """
        Testing whether the Fasta class parses Fasta files properly.
        There are 2 tests here.

        :return:
        """
        a = mc.FastaFile(self.sampleFastas, fileName=False)
        self.assertEqual(a[0].sequence, "AGAGATACATAGACAATGTGTTGCGTAGAGATAG")
        self.assertEqual(a[1].sequence, "TTTTGGAA")
        self.assertEqual(len(a), 2)


class TestFunctions(TestCase):
    def setUp(self):
        self.motifsL = ["AATT", "GGCG"]
        self.seqL = ["AGAGATACATAGACAATGTG", "TTACGATACCAGATTCC"]

    def testMutateString(self):

        noOfPos = 3

        # mutating only the first self.seqL sequence.
        mutatedS = part3.mutateString(self.seqL[0], noOfPos)[0]

        mutatedNumber = 0

        # testing if the length of the mutated string is equal
        # to the length of the original string.
        self.assertEqual(len(self.seqL[0]), len(mutatedS))

        for index, item in enumerate(mutatedS):

            if mutatedS[index] != self.seqL[0][index]:
                mutatedNumber += 1
        self.assertEqual(mutatedNumber, noOfPos)