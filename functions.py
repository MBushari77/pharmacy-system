import os
import tempfile


# HERD PRINTING FUNCTION
def toPrinter(x):
	filename = tempfile.mktemp('.txt')
	open(filename, "w").write(str(x))
	os.startfile(filename, 'print')



# GET THE NUMBER OF DUPLICATED NUMBERS IN A LIST
def getRepPro(listOfElems):
	dictOfElems = dict()
	print(" ")
	print(" ")
	print(" ")
	print(listOfElems)
	for elem in listOfElems:
		if elem in dictOfElems:
			dictOfElems[elem] += 1
		else:
			dictOfElems[elem] = 1
	dictOfElems = { key:{'times':value, 'price': 0, 'name': 'none', 'id': key, 'pices': 0, 'costPBC': 0, 'ppp': 0, 'totPs': 0} for key, value in dictOfElems.items() if value > 0}

	return dictOfElems