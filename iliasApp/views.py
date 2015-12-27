from django.core import urlresolvers
from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect

import pdb
from django.views.decorators.csrf import csrf_exempt
import itertools
import part1
import myfunctions as myf
import mycustom as mc
import numpy as np
import part3
import oligo
import json

from iliasApp.forms import FastaForm, Part1Form, Part3Form, MpraSnpsForm
import os
from iliasWebsite import settings
import math
import forms
import parseSNPs
import viewsCore

def indexView(request):
    context = {}
    part1Form = Part1Form()

    context['part1form'] = part1Form
    context['boxes'] = ['restriction','adapter']
    return render(request, 'iliasApp/part1.html', context)


@csrf_exempt
def resultsView(request):
    context = {}
    if request.method == "POST":

        part1Form = Part1Form(request.POST, request.FILES)
        if not part1Form.is_valid():
            context['part1form'] = part1Form
            context['boxes'] = ['restriction', 'adapter']

            return render(request, "iliasApp/part1.html", context)

        ordering = request.POST.get('ordering').strip().split(",")[:-1]

        postDict = request.POST
        sequenceS = part1Form.cleaned_data['sequenceS']
        sequenceF = part1Form.cleaned_data['sequenceF']
        motifS = part1Form.cleaned_data['motifS']

        reverseComplement = part1Form.cleaned_data['reverseComplement']
        leftDistance = int(part1Form.cleaned_data['leftDistance'])
        rightDistance = int(part1Form.cleaned_data['rightDistance'])
        frequencyOfInsertion = int(part1Form.cleaned_data['frequencyOfInsertion'])
        minSpacing = int(part1Form.cleaned_data['minSpacing'])
        maxSpacing = int(part1Form.cleaned_data['maxSpacing'])

        barCodeDistance = int(part1Form.cleaned_data.get('barCodeDistance')) if postDict.get('barCodeDistance') else None
        barCodeLength = int(part1Form.cleaned_data.get('barCodeLength')) if postDict.get('barCodeLength') else None
        minimumGCContent = postDict.get('minimumGCContent')
        maximumGCContent = postDict.get('maximumGCContent')
        numOfBarCodesPerSequence = int(postDict['numOfBarCodesPerSequence']) if postDict.get("numOfBarCodesPerSequence") else None

        restriction1 = postDict.get('restriction1')
        restriction2 = postDict.get('restriction2')

        adapter1 = postDict.get('adapter1')
        adapter2 = postDict.get('adapter2')

        motifO = mc.FastaFile(motifS, fileName=False)

        if sequenceF:
            sequenceO = mc.FastaFile(sequenceF, fileName=False)
        elif sequenceS:
            sequenceO = mc.FastaFile(sequenceS, fileName=False)


        motifsL = [motif.sequence for motif in motifO]
        allCombinations = part1.generateCombinations(motifsL)

        # This is only working for 20 sequence for now. CHANGE THIS
        numOfSequencesToUse = 20
        backgroundSequencesL = [i.sequence[:800] for i in sequenceO[:numOfSequencesToUse]]
        backgroundSequenceHeadersL = [i.name for i in sequenceO[:numOfSequencesToUse]]

        # doing the reverse complement
        if reverseComplement:
            copyBackgroundSequencesL = backgroundSequencesL[:]
            backgroundSequencesL = [myf.revcompl(backgroundSequence).lower() for backgroundSequence in copyBackgroundSequencesL]

        # getting the combinations
        finalOutput = []
        for index, backgroundSequence in enumerate(backgroundSequencesL):
            for combination in allCombinations:
                finalOutput += oligo.oligo(backgroundSequence,
                                               minSpacing, maxSpacing,
                                               combination, leftDistance,
                                               rightDistance, frequencyOfInsertion,
                                                backgroundSequenceHeadersL[index])


        # creating the barcodes. It can be a none value
        barCodes, numOfBarCodesPerSequence = part1.getBarCodes(barCodeLength, minimumGCContent, maximumGCContent,
                                                         numOfBarCodesPerSequence, barCodeDistance, finalOutput)

        mpraOutput, sequenceHTMLL = part1.createMPRAResultOutput(finalOutput, numOfBarCodesPerSequence, barCodes,
                                                                 restriction1, restriction2, adapter1, adapter2, ordering)

        usingDownload = request.POST.get('usingDownload', False)

        if usingDownload:
            response = HttpResponse(content_type="text/plain")
            response.write(mpraOutput)
            # context = {"backgroundSequence": sequenceS, "motif": motif, "allCombinations": allCombinations, "finalOutput": finalOutput, "barCodes" : barCodes}
            return response

        else:
            response = HttpResponse(content_type="text/plain")
            response.write(mpraOutput)
            context['sequenceHTML'] = sequenceHTMLL
            context['forDownload'] = mpraOutput
            context['fileName'] = 'MPRA_Motif_results.txt'
            return render(request, "iliasApp/results.html", context)

    return HttpResponseRedirect(urlresolvers.reverse(("iliasApp:ViewIndex")))



def part3View(request):
    context = {}
    form = Part3Form()
    context['form'] = form
    return render(request, "iliasApp/part3.html", context)


def homeView(request):
    context = {}

    itemsToShowL = [
        ["MPRA (Motifs) construction", urlresolvers.reverse("iliasApp:ViewIndex"), "Allows the substitution of motifs in a background sequence at all possible positions within the constraints of the parameters"],
        ["MPRA (SNPs) construction", urlresolvers.reverse("iliasApp:ViewMpraSnp"), "Allows the substitution of reference positions with SNPs"],
        ["Transmutation", urlresolvers.reverse("iliasApp:ViewPart3"), "Creates a specified number of random mutations on a sequence"],

    ]

    context['itemsToShowL'] = itemsToShowL
    return render(request, "iliasApp/homepage.html", context)


def part3RresultsView(request):
    context = {}
    if request.method == "POST":
        form = Part3Form(request.POST, request.FILES)

        if form.is_valid():
            pass
        else:
            context['form'] = form
            return render(request, "iliasApp/part3.html", context)

        sequenceS = form.cleaned_data.get('sequenceS')
        sequenceF = form.cleaned_data.get('sequenceF')

        scrambleOption = request.POST.get('scramble')
        reverseOption = request.POST.get('reverse')
        compOption = request.POST.get('complement')



        numToMutate = int(form.cleaned_data.get('numToMutate'))

        if sequenceF:
            sequenceO = mc.FastaFile(sequenceF, fileName=False)
        elif sequenceS:
            sequenceO = mc.FastaFile(sequenceS, fileName=False)


        outputSequenceL = [i.sequence for i in sequenceO]

        scrambleHeader = "No"
        reverseHeader = "No"
        complementHeader = "No"

        if scrambleOption == "on":
            scrambleHeader = "Yes"
            outputSequenceL = [part3.scramble_motifs(seq) for seq in outputSequenceL]

        if reverseOption == "on":
            reverseHeader = "Yes"
            outputSequenceL = [ seq[::-1] for seq in outputSequenceL ]

        if compOption == "on":
            complementHeader = "Yes"
            outputSequenceL = [ myf.complement(seq) for seq in outputSequenceL ]

        finalOutputSequenceL = outputSequenceL
        outputSequenceHTMLL = outputSequenceL

        if numToMutate:
            finalOutputSequenceL = []
            outputSequenceHTMLL = []

            for seq in outputSequenceL:
                mutatedString, positionMutated = part3.mutateString(seq, numToMutate)
                finalOutputSequenceL.append(mutatedString)

                outputSequenceHTMLL.append(myf.highlightString(mutatedString, positionMutated))


        headers = [">"+seq.name+"| Mutated_nucleotides - %s | Scrambled - %s | Reversed - %s | Complemented - %s" % (numToMutate, scrambleHeader, reverseHeader, complementHeader )
                   for seq in sequenceO]


        context['headers'] = headers
        context['zipped'] = zip(headers, outputSequenceHTMLL)


        forDownload = ""
        for header, scramble in zip(headers, finalOutputSequenceL):
            forDownload += header+'\n'
            forDownload += scramble+'\n'
        # YOU NEED TO add new lines as the sequence will be displayed
        context['forDownload'] = forDownload
        context['fileName'] = "Transmutation_results.txt"

        return render(request, "iliasApp/part3Results.html", context)

    else:
        return HttpResponseRedirect(urlresolvers.reverse(("iliasApp:ViewPart3")))


def docsView(request):
    rawHeaderLabels = ["<Motif>:A particular motif inserted by the user.",
                       "BARCODE:",
                       "restriction: This is the restriction site put by the user",
                       "adapter:",
                        "DUPLICATE_RESTRICTION_SITES: The restriction site which has multiple copies present."]

    rawMpraSNPHeaderLabels = ["<SNP> : Name of SNP", "<Nucleotide> :REF / ALT",
                              "BARCODE: This is the unique identifier for the variants",
                              "RESTRICTION : This is the restriction site(s) put by the user",
                              "ADAPTER:  This is the adapter site(s) put by the user",
                              "DUPLICATE_RESTRICTION_SITES: Report the restriction site which has multiple copies present in the oligo"]


    mpraSNPheaderLabels = [ i.split(":") for i in rawMpraSNPHeaderLabels]
    headerLabels = [ i.split(":") for i in rawHeaderLabels]
    headerFormat = "<LABEL> - <INFO> |"
    context = {}
    context['headerLabels'] = headerLabels
    context['headerFormat'] = headerFormat
    context['mpraSNPheaderLabels'] = mpraSNPheaderLabels

    return render(request, "iliasApp/docs.html", context)



def tableDownloadView(request):
    if request.method == "POST":
        content = request.POST.get('content')
        fileName = request.POST.get("fileName")
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename = %s' % fileName
        response.write(content)
        return response
    return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewPart2"))


def mutationDownloadView(request):
    if request.method == "POST":
        content = request.POST['content']
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename = MutationResults.txt'
        response.write(content)
        return response
    return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewPart3"))


def getSequenceView(request):
    fastaFile = request.GET.get('fastaFile')
    sampleFastaB = request.GET.get('sampleFastaFile')

    response = HttpResponse(content_type="text/plain")
    base_dir = settings.BASE_DIR
    if not sampleFastaB:
        response = HttpResponse(content_type="text/plain")
        openfile = open(os.path.join(base_dir,"fasta_files/%s.fa" % fastaFile))
        readfile = openfile.read()
        openfile.close()
        fastaO = mc.FastaFile(readfile, fileName=False)
        html = ""
        for i in fastaO:
            html +="<input type='checkbox' value='>%s\n%s'>&gt;%s<br>%s<br><br>"% (i.name, i.sequence, i.name, i.sequence)

        response.write(html)
    else:
        openfile = open(os.path.join(base_dir, "sample_fasta.fa"))
        readfile = openfile.read()
        openfile.close()
        response.write(readfile)

    return response



def mpraSnp(request):

    context = {}
    mpraSnpsForm = MpraSnpsForm()

    context['part1form'] = mpraSnpsForm

    context['boxes'] = ['restriction','adapter']

    return render(request, 'iliasApp/mpraSnp.html', context)


@csrf_exempt
def mpraSnpResults(request):

    context = {}
    if request.method == "POST":


        mpraSnpsForm = MpraSnpsForm(request.POST, request.FILES)
        if not mpraSnpsForm.is_valid():
            context['part1form'] = mpraSnpsForm
            context['boxes'] = ['restriction', 'adapter']

            return render(request, "iliasApp/mpraSnp.html", context)

        sequenceF = mpraSnpsForm.cleaned_data['sequenceF']
        sequenceS = mpraSnpsForm.cleaned_data['sequenceS']

        postDict = request.POST
        barCodeDistance = int(mpraSnpsForm.cleaned_data.get('barCodeDistance')) if postDict.get('barCodeDistance') else None
        barCodeLength = int(mpraSnpsForm.cleaned_data.get('barCodeLength')) if postDict.get('barCodeLength') else None
        minimumGCContent = postDict.get('minimumGCContent')
        maximumGCContent = postDict.get('maximumGCContent')
        numOfBarCodesPerSequence = int(postDict['numOfBarCodesPerSequence']) if postDict.get("numOfBarCodesPerSequence") else None
        ordering = postDict.get('ordering').strip().split(",")[:-1]
        makeSnpCombinations = mpraSnpsForm.cleaned_data['makeSnpCombinations']
        restriction1 = postDict.get('restriction1')
        restriction2 = postDict.get('restriction2')


        adapter1 = postDict.get('adapter1')
        adapter2 = postDict.get('adapter2')


        snpS = mpraSnpsForm.cleaned_data['SnpS']
        snpO = mc.SnpFile(snpS, fileName=False)

        if sequenceF:
            sequenceO = mc.FastaFileWithHeaderRange(sequenceF, fileName=False)
        elif sequenceS:
            sequenceO = mc.FastaFileWithHeaderRange(sequenceS, fileName=False)


        headersL = [i.headerRange for i in sequenceO]

        subbedSequenceHeadersL, subbedSequencesL = parseSNPs.make_sequence_copies(SNPs=snpO, NamesL=headersL, SequencesL=sequenceO.getSequences(), CombinationsB=makeSnpCombinations)
        #subbedSequencesL, subbedSequenceHeadersL = parseSNPs.naman_make_sequence_copies(snpO=snpO, sequenceO=sequenceO, combinationsB=makeSnpCombinations)

        finalOutput = []
        for headerS, seqS in (zip(subbedSequenceHeadersL, subbedSequencesL)):
                finalOutput.append({"header": headerS, "sequence": seqS})

        barCodes, numOfBarCodesPerSequence = part1.getBarCodes(barCodeLength, minimumGCContent, maximumGCContent,
                                                               numOfBarCodesPerSequence, barCodeDistance, finalOutput=finalOutput)

        mpraOutput, mpraOutputHTML = part1.createMPRAResultOutput(finalOutput, numOfBarCodesPerSequence, barCodes,
                                                  restriction1, restriction2, adapter1, adapter2, ordering)

        # responding as a plain response
        usingDownload = request.POST.get("usingDownload", False)

        if usingDownload:
            response = HttpResponse(content_type="text/plain")
            response.write(mpraOutput)
            return response

        else:
            context['forDownload'] = mpraOutput
            context['sequenceHTML'] = mpraOutputHTML
            context['fileName'] = 'MPRA_SNP_result.txt'
            return render(request, "iliasApp/results.html", context)
        #return response

    else: return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewMpraSnp"))


@csrf_exempt
def downloadScriptView(request, fileToDownload):

    acceptableFilesD = { "MpraMotifs": "MpraMotifs_script.py",
                         "MpraSnps": "MpraSnps_script.py",
                         }

    if request.method == "POST":
        if fileToDownload not in acceptableFilesD:
            return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewHome"))

        response = HttpResponse(content_type="text/plain")
        fileNameS = acceptableFilesD[fileToDownload]
        filePathS = os.path.join(settings.BASE_DIR, "downloadables", fileNameS)
        openfile = open(filePathS)
        content = openfile.read()
        openfile.close()
        response["Content-Disposition"] = 'attachment; filename = %s' % fileNameS
        response.write(content)
        return response

    else: return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewMpraSnp"))




@csrf_exempt
def MpraSnpApiView(request):
    if request.method == "POST":

        return HttpResponse("testing")
    else: return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewMpraSnp"))


def restView(request):
    return HttpResponseRedirect(urlresolvers.reverse("iliasApp:ViewHome"))

