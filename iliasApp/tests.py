from django.test import TestCase
from selenium import webdriver



class TestPage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://localhost:8000")

        print "Starting up the browser"

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

class TestTransmutationPage(TestPage):

    def enterSequence(self, sequence):
        sequenceBox = self.driver.find_element_by_name("sequence")
        sequenceBox.clear()
        sequenceBox.send_keys(sequence)

    def setUp(self):

        print "this is setUp"
        self.driver.find_element_by_id("transmutationButton").click()
        self.assertEqual(self.driver.title, "Transmutation")

    def testIncorrectSequence(self):
        # This tests to receive an error by putting a non-FASTA sequence
        self.enterSequence("AGATA")
        print "This is testIncorrectSequence"
        self.driver.find_element_by_id("submitButton").click()
        error = self.driver.find_element_by_class_name("error").text

        self.assertEqual("Sequence is not in FASTA format!", error)
        self.assertEqual(self.driver.title, "Transmutation")

    def testCorrectSequence(self):
        sequence = "AGATAGA"
        print "this is testCorrectSequence"
        self.enterSequence(">test1\n%s" % sequence)
        self.driver.find_element_by_id("mutate").click()
        self.driver.find_element_by_name("numberToMutate").send_keys("2")
        self.driver.find_element_by_id("submitButton").click()
        mutatedSequence = self.driver.find_element_by_class_name("sequenceResult").text
        self.assertEqual(len(sequence), len(mutatedSequence))

    def testNoSequence(self):
        print "This is testNoSequence"
        self.enterSequence("")
        self.driver.find_element_by_id("submitButton").click()
        error = self.driver.find_element_by_class_name("error").text
        self.assertEqual("Please enter a sequence!", error)


class TestDocPage(TestPage):

    def setUp(self):
        self.driver.find_element_by_id("docsButton").click()

    def testPageExists(self):

        sectionTitle = self.driver.find_element_by_class_name("docSections").text
        self.assertEqual(self.driver.title, "Documentation")
        self.assertEqual(sectionTitle, "MPRAs query page")


class TestMPRAPage(TestPage):

    def setUp(self):
        self.driver.get("http://localhost:8000")
        self.driver.find_element_by_id("mprasButton").click()

    def testNoMotif(self):
        motifBox = self.driver.find_element_by_id("motifBox")
        motifBox.clear()
        self.driver.find_element_by_id("submitButton").click()
        error = self.driver.find_element_by_class_name("error").text
        self.assertEqual("Please enter motifs!", error)

