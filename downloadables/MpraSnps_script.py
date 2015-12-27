import sys
try:
	import requests
except:
	print "You need to install the 'requests' module. Use 'pip install requests'"
	sys.exit()

url = "https://genomegeek.com/MPRAResults/SNPs/"
fileToWriteResults = "MPRASNPresultFile.fa"


# MPRA Sample Data change as appropriate.
sequenceS = ">sequence1chr1:42990-43041,testest\nACAGATTAGTCAGTACGGCTAGCTAGCTACGTCTATATTATAGCGATACGGG"
snpS = "1	 42991	rs43434	 T	 G\n 1	43030	rs121212	A	G"


# ordering of output
barcodeOrder = "Barcode,"
backgroundOrder = "Background,"
restriction1Order = "restriction site 1,"
restriction2Order = "restriction site 2,"
adapter1Order = "adapter site 1,"
adapter2Order = "adapter site 2,"

# Change the ordering below as appropriate. Just move the variables in your 
# desired order.
ordering = barcodeOrder + backgroundOrder + restriction1Order + restriction2Order + adapter1Order + adapter2Order

# Data below is optional. Add the appropriate parameters. Default numbers are given below.
barCodeDistance = "2"
barCodeLength = "12"
minimumGCContent = "20"
maximumGCContent = "80"
numOfBarCodesPerSequence = "4"
restriction1 = ""
restriction2 = ""
adapter1 = ""
adapter2 = ""


# put data in a dictionary
data = {"sequenceS":sequenceS,
"SnpS":snpS,
"ordering":ordering,
"barCodeDistance":barCodeDistance,
"barCodeLength":barCodeLength,
"minimumGCContent":minimumGCContent,
"maximumGCContent":maximumGCContent,
"numOfBarCodesPerSequence":numOfBarCodesPerSequence,
"restriction1":restriction1,
"restriction2":restriction2,
"adapter1":adapter1,
"adapter2":adapter2,
"usingDownload":True,
}


# Posting the data.
result = requests.post(url = url, data = data)

# writing the results 
openfile = open(fileToWriteResults, "w")
openfile.write(result.content)
openfile.close()

