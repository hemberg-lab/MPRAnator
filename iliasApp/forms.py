import pdb
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import validate_email
import mycustom as mc
import os
from iliasWebsite import settings
import json
import myfunctions as myf

class PositiveIntegerField(forms.IntegerField):
    def __init__(self, *args, **kwargs):

        minimum_value = kwargs.pop('min_value', 0)
        maximum_value = kwargs.pop("max_value", None)

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.NumberInput(attrs={"required": "required"})

        super(PositiveIntegerField, self).__init__(max_value=maximum_value, min_value=minimum_value, *args, **kwargs)


class OptionalPositiveIntegerField(PositiveIntegerField):
    def __init__(self, *args, **kwargs):

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.NumberInput(attrs={})

        super(OptionalPositiveIntegerField, self).__init__(required=False, *args, **kwargs)


class OptionalPercentField(OptionalPositiveIntegerField):
    def __init__(self, *args, **kwargs):
        super(OptionalPercentField, self).__init__(max_value=100, *args, **kwargs)


class GeneralField(forms.Field):

    def __init__(self, *args, **kwargs):

        self.stemClass = None
        super(GeneralField, self).__init__(*args, **kwargs)


    def validate(self, value):

        super(GeneralField, self).validate(value)
        if value != "":
            try:
                fasta = self.stemClass(value, fileName=False)
            except ValueError as e:
                raise forms.ValidationError(e)
            return fasta


class GeneralSequenceField(GeneralField):

    def __init__(self, *args, **kwargs):

        self.sequenceLengthLimit = kwargs.get("sequenceLengthLimit", 20000)
        self.sequenceLimit = kwargs.get('sequenceLimit', 9)
        super(GeneralSequenceField, self).__init__(*args, **kwargs)

class FastaField(GeneralSequenceField):

    def __init__(self, *args, **kwargs):
        super(FastaField, self).__init__(*args, **kwargs)
        self.stemClass = mc.FastaFile

class FastaSNPField(GeneralSequenceField):

    def __init__(self, *args, **kwargs):
        super(FastaSNPField, self).__init__(*args, **kwargs)
        self.stemClass = mc.FastaFileWithHeaderRange

class SnpField(GeneralField):

    def __init__(self, *args, **kwargs):
        super(SnpField, self).__init__(*args, **kwargs)
        self.stemClass = mc.SnpFile


class BedField(GeneralField):
    def __init__(self, *args, **kwargs):
        super(BedField, self).__init__(*args, **kwargs)
        self.stemClass = mc.BedFile


class TextField(forms.CharField):

     def to_python(self, data):
        # raise forms.ValidationError("ENNOT")
        return data.strip()

class FileField(forms.FileField):

    def to_python(self, value):

        super(FileField, self).to_python(value)

        data = ""
        if value:
            data = value.read().strip()
        return data


class BedTextField(forms.CharField, BedField):

    def __init__(self, *args, **kwargs):

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.Textarea
        if not kwargs.get('required'):
            kwargs['required'] = False

        super(BedTextField, self).__init__(*args, **kwargs)

    def to_python(self, data):

        return data.strip()


class BedFileField(BedField, forms.FileField):

    def __init__(self, *args, **kwargs):

        if not kwargs.get("required"):
            kwargs['required'] = False
        super(BedFileField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        super(BedFileField, self).to_python(value)

        data = ""
        if value:
            data = value.read().strip()
        return data

class BedForm(forms.Form):
    bedS = BedTextField(label="Enter in bed units ")
    bedF = BedFileField(label="upload in the bed file ")

    def __init__(self, *args, **kwargs):

        self.sequenceLimit = kwargs.get('sequenceLimit', 50000)
        super(BedForm, self).__init__(*args, **kwargs)

    def clean(self):

        super(BedForm, self).clean()
        fastaFile = self.cleaned_data.get("bedF")
        fastaSequence = self.cleaned_data.get("bedS")


        if fastaFile == None:

            pass
        elif fastaSequence == None:

            pass
        elif fastaFile == "" and fastaSequence == "":
            raise forms.ValidationError("Enter a sequence ! Either upload or enter in directly!")
        elif fastaFile and fastaSequence:
            raise forms.ValidationError("Either upload or enter in directly ! Don't do both!")

        if fastaFile:
            sequence = mc.BedFile(fastaFile, fileName=False)
        elif fastaSequence:
            sequence = mc.BedFile(fastaSequence, fileName=False)
        else:
            sequence = None
        if sequence:
            if len(sequence) > self.sequenceLimit:
                raise forms.ValidationError("Currently only a maximum of %s sequences are allowed" % self.sequenceLimit)


class SnpTextField(forms.CharField, SnpField):

     def __init__(self, *args, **kwargs):

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.Textarea
        if not kwargs.get('required'):
            kwargs['required'] = False

        super(SnpTextField, self).__init__(*args, **kwargs)

     def to_python(self, data):
        return data.strip()


class FastaTextField(forms.CharField, FastaField):
    def __init__(self, *args, **kwargs):

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.Textarea
        if not kwargs.get('required'):
            kwargs['required'] = False

        super(FastaTextField, self).__init__(*args, **kwargs)

    def to_python(self, data):

        return data.strip()


class FastaFileField(FastaField, forms.FileField):
    def __init__(self, *args, **kwargs):

        if not kwargs.get("required"):
            kwargs['required'] = False
        super(FastaFileField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        super(FastaFileField, self).to_python(value)

        data = ""
        if value:
            data = value.read().strip()
        return data


class FastaSNPTextField(forms.CharField, FastaSNPField):
    def __init__(self, *args, **kwargs):

        if not kwargs.get('widget'):
            kwargs['widget'] = forms.Textarea
        if not kwargs.get('required'):
            kwargs['required'] = False

        super(FastaSNPTextField, self).__init__(*args, **kwargs)

    def to_python(self, data):

        return data.strip()


class FastaSNPFileField(FastaSNPField, forms.FileField):
    def __init__(self, *args, **kwargs):

        if not kwargs.get("required"):
            kwargs['required'] = False
        super(FastaSNPFileField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        super(FastaSNPFileField, self).to_python(value)

        data = ""
        if value:
            data = value.read().strip()
        return data

class FastaSNPForm(forms.Form):
    error_css_class = "error"
    sequenceS = FastaSNPTextField(label="Enter FASTA sequences")
    sequenceF = FastaSNPFileField(label="Upload FASTA sequences")

    def __init__(self, *args, **kwargs):

        self.sequenceLengthLimit = kwargs.get("sequenceLengthLimit", 20000)
        self.sequenceLimit = kwargs.get('sequenceLimit', 50000)
        super(FastaSNPForm, self).__init__(*args, **kwargs)

    def clean(self):

        super(FastaSNPForm, self).clean()
        fastaFile = self.cleaned_data.get("sequenceF")
        fastaSequence = self.cleaned_data.get("sequenceS")


        if fastaFile == None:

            pass
        elif fastaSequence == None:

            pass
        elif fastaFile == "" and fastaSequence == "":
            raise forms.ValidationError("Enter a sequence ! Either upload or enter in directly!")
        elif fastaFile and fastaSequence:
            raise forms.ValidationError("Either upload or enter in directly ! Don't do both!")

        if fastaFile:
            sequence = mc.FastaFileWithHeaderRange(fastaFile, fileName=False)
        elif fastaSequence:
            sequence = mc.FastaFileWithHeaderRange(fastaSequence, fileName=False)
        else:
            sequence = None
        if sequence:
            if len(sequence) > self.sequenceLimit:
                raise forms.ValidationError("Currently only a maximum of %s sequences are allowed" % self.sequenceLimit)
            if sequence.getMaxLength() > self.sequenceLengthLimit:
                raise forms.ValidationError("Currently a sequence can only be %s long." % self.sequenceLengthLimit)



class FastaForm(forms.Form):
    error_css_class = "error"
    sequenceS = FastaTextField(label="Enter FASTA sequences")
    sequenceF = FastaFileField(label="Upload FASTA sequences")

    def __init__(self, *args, **kwargs):

        self.sequenceLengthLimit = kwargs.get("sequenceLengthLimit", 20000)
        self.sequenceLimit = kwargs.get('sequenceLimit', 1000)
        super(FastaForm, self).__init__(*args, **kwargs)

    def clean(self):

        super(FastaForm, self).clean()
        fastaFile = self.cleaned_data.get("sequenceF")
        fastaSequence = self.cleaned_data.get("sequenceS")


        if fastaFile == None:
            pass
        elif fastaSequence == None:
            pass
        elif fastaFile == "" and fastaSequence == "":
            raise forms.ValidationError("Enter a sequence ! Either upload or enter in directly!")
        elif fastaFile and fastaSequence:
            raise forms.ValidationError("Either upload or enter in directly ! Don't do both!")

        if fastaFile:
            sequence = mc.FastaFile(fastaFile, fileName=False)
        elif fastaSequence:
            sequence = mc.FastaFile(fastaSequence, fileName=False)
        else:
            sequence = None
        if sequence:
            if len(sequence) > self.sequenceLimit:
                raise forms.ValidationError("Currently only a maximum of %s sequences are allowed" % self.sequenceLimit)
            if sequence.getMaxLength() > self.sequenceLengthLimit:
                raise forms.ValidationError("Currently a sequence can only be %s long." % self.sequenceLengthLimit)



class Part3Form(FastaForm):
    numToMutate = PositiveIntegerField(label="Number of nucleotides to mutate", initial=0)
    scramble = forms.BooleanField(label="Scramble motif?", required=False, initial=False,
                                  widget=forms.CheckboxInput(attrs={}))

    reverse = forms.BooleanField(label="Reverse motif?", required=False, initial=False,
                                  widget=forms.CheckboxInput(attrs={}))

    complement = forms.BooleanField(label="Complement motif?", required=False, initial=False,
                                 widget=forms.CheckboxInput(attrs={}))

    def clean(self):
        super(Part3Form, self).clean()

        numToMutate = self.cleaned_data.get("numToMutate")

        sequenceF = self.cleaned_data.get("sequenceF")
        sequenceS = self.cleaned_data.get("sequenceS")
        if sequenceF:
            sequence = mc.FastaFile(sequenceF, fileName=False)
        elif sequenceS:
            sequence = mc.FastaFile(sequenceS, fileName=False)
        else:
            sequence = None

        if sequence:

                allowedLetters = set(myf.mapperDict.keys()+["N"])

                for i in sequence:
                    if len(set(i.sequence) - set(allowedLetters)) > 0:
                        raise forms.ValidationError("Invalid letters!")

                    if list(set(i.sequence)) == ["N"]:
                        raise forms.ValidationError("Please do not enter a string only containing N!")

                if numToMutate > sequence.getMinLength():
                    raise forms.ValidationError("The number of mutations is greater than the length of the smallest sequence")

def getFastaFileNamesS():
    base_dir = settings.BASE_DIR
    fastaFiles = [ i.split(".")[0] for i in os.listdir(os.path.join(base_dir,"fasta_files")) if i.endswith("fa")]
    return [(i,i) for i in fastaFiles]

def getPopUp():
    popupL = {
        'minSpacing': 'The minimum spacing between the motifs.',
        'maxSpacing': 'This is the maximum spacing between the motifs.',
        'rightDistance': 'This is the distance of the motif from the right edge of the sequence',
        'leftDistance': 'This is the distance of the motif from the left edge of the sequence.',
        'frequencyOfInsertion': 'This specifies the interval length to insert the motifs',
        'barCodeLength': 'The size of the bar code specified',
        'minimumGCContent': 'The minimum amount (in percent) of GC content in each of the barcodes',
        'maximumGCContent': 'The maximum amount (in percent) of GC content in each of the barcodes',
        'numOfBarCodesPerSequence': 'The number of barcodes a user would like per sequence. A value of 2 would mean\
                                     that there would be 2 copies of the motif inserted sequence, but only differing in the barcode',
        'barCodeDistance': 'The Levenshtein distance between each barcode. The default is 2.',
        'numOfBarCodes': 'This specifies the number of barcodes inserted per sequence.',
    }
    return popupL


class Part1Form(FastaForm):

    motifS = FastaTextField(label="Enter your motifs")
    error_css_class = "error"

    reverseComplement = forms.BooleanField(label="Reverse complement sequence before motif substitution?",
                                           required=False)

    minSpacing = PositiveIntegerField(label="Minimum Spacing", required=True,
                                      widget=forms.NumberInput(attrs={
                                          "title":
                                          'The minimum spacing between the motifs.'}))

    maxSpacing = PositiveIntegerField(label="Maximum Spacing",
                                      widget=forms.NumberInput(attrs={
                                          "title": getPopUp()['maxSpacing']}))

    leftDistance = PositiveIntegerField(label="Distance from left edge",
                                    widget=forms.NumberInput(attrs={
                                        "title":
                                            getPopUp()['leftDistance']}))
    rightDistance = PositiveIntegerField(label="Distance from right edge",
                                         widget=forms.NumberInput(attrs={
                                            "title":
                                                 getPopUp()['rightDistance']}))

    frequencyOfInsertion = PositiveIntegerField(label="Interval of substitution of motifs",
                                                widget=forms.NumberInput(attrs={
                                                    "title":
                                                        getPopUp()['frequencyOfInsertion']}))

    barCodeLength = OptionalPositiveIntegerField(label="Barcode length",
                                                 min_value=10,
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['barCodeLength']}))

    minimumGCContent = OptionalPercentField(label="Minimum barcode GC content (%)",
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['minimumGCContent']}))

    maximumGCContent = OptionalPercentField(label="Maximum barcode GC content (%)",
    widget=forms.NumberInput(attrs={
    "title":
    getPopUp()['maximumGCContent']}))

    barCodeDistance = OptionalPositiveIntegerField(label="Barcode edit distance ",
    widget=forms.NumberInput(attrs={ "title":
            getPopUp()['barCodeDistance']
                                     }))

    numOfBarCodesPerSequence = OptionalPositiveIntegerField(label="Number of barcodes per sequence", min_value=1,
                                                            max_value=5,
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['numOfBarCodes']}))

    def clean(self):
        super(Part1Form, self).clean()

        minSpacing = self.cleaned_data['minSpacing']
        maxSpacing = self.cleaned_data['maxSpacing']
        leftDistance = self.cleaned_data['minSpacing']
        rightDistance = self.cleaned_data['maxSpacing']
        minimumGCContent = self.cleaned_data['minimumGCContent']
        maximumGCContent = self.cleaned_data['maximumGCContent']
        motifS = self.cleaned_data.get('motifS')
        sequenceF = self.cleaned_data.get('sequenceF')
        sequenceS = self.cleaned_data.get('sequenceS')

        if motifS == "":
            raise forms.ValidationError("Enter motifs!")
        if motifS:
            motifO = mc.FastaFile(motifS, fileName=False)
            if motifO.areDuplicatesPresent():
                raise forms.ValidationError("There are duplicate motifs!")


        maximumNumberOfMotifsTimesSequences = 100

        if sequenceF or sequenceS:
            if sequenceF:
                sequenceO = mc.FastaFile(sequenceF, fileName=False)
            elif sequenceS:
                sequenceO = mc.FastaFile(sequenceS, fileName=False)

            if not sequenceO.lengthsSame():
                raise forms.ValidationError("Sizes of the sequences should be the same")

        if (len(motifO)**4)*len(sequenceO) > maximumNumberOfMotifsTimesSequences:
            raise forms.ValidationError("Only a maximum of %s motifs^4*sequences allowed" % maximumNumberOfMotifsTimesSequences)

        if minSpacing > maxSpacing:
            raise forms.ValidationError("Maximum spacing should be greater than min spacing")
        elif minimumGCContent > maximumGCContent:
            raise forms.ValidationError("Minimum GC content is larger than maximum GC content")


class MpraSnpsForm(FastaSNPForm):
    SnpS = SnpTextField(label="Enter your SNPs (VCF Format)")
    error_css_class = "error"
    makeSnpCombinations = forms.BooleanField(label="Make Snp Combinations?",
                                           required=False)

    barCodeLength = OptionalPositiveIntegerField(label="Barcode length",
                                                 min_value=10,
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['barCodeLength']}))

    minimumGCContent = OptionalPercentField(label="Minimum barcode GC content (%)",
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['minimumGCContent']}))

    maximumGCContent = OptionalPercentField(label="Maximum barcode GC content (%)",
    widget=forms.NumberInput(attrs={
    "title":
    getPopUp()['maximumGCContent']}))

    barCodeDistance = OptionalPositiveIntegerField(label="Barcode edit distance ",
    widget=forms.NumberInput(attrs={ "title":
            getPopUp()['barCodeDistance']
                                     }))

    numOfBarCodesPerSequence = OptionalPositiveIntegerField(label="Number of barcodes per sequence", min_value=1,
                                                            max_value=5,
    widget=forms.NumberInput(attrs={
        "title":
            getPopUp()['numOfBarCodes']}))

    def clean(self):
        super(MpraSnpsForm, self).clean()

        SnpS= self.cleaned_data.get('SnpS')

        if SnpS == "":
            raise forms.ValidationError("Enter SNPs!")

        snpO = mc.SnpFile(SnpS, fileName=False)

        if snpO.getMaximumTargetSize() > 10:
            raise forms.ValidationError("SNP sizes cannot be greater than 10!")



