import os, fnmatch
import subprocess
from progress.bar import Bar
import re
import pandas as pd
import numpy as np
import gspread
#Credentials to login to Google Sheets
from credentials import GOOGLE_LOGIN, GOOGLE_PASS, GOOGLE_SHEET

"""
Extracts sentences from text files that match a predefined glossary of terms/phrases.
Outputs them into `SENTENCEFOLDER`

To run: 
`python sentenceFinder.py` in the directory that has the folder of interest. 
(i.e. folder containing the text corpuses.)
"""

SENTENCEFOLDER = "sentences/"

#Connecting to the Google Sheet that contains the glossary
gc = gspread.login(GOOGLE_LOGIN, GOOGLE_PASS)
wb = gc.open_by_key(GOOGLE_SHEET)
ws = wb.worksheet('Benefit')
sheet = ws.get_all_values()
headers = sheet.pop(0)

#A pandas dataframe of the glossary of terms
glossary = pd.DataFrame(sheet, columns=headers)

#The folder that contains all the text files for CSR reports
FOLDERNAME = "corpus2"
if not os.path.exists(FOLDERNAME):
	os.makedirs(FOLDERNAME)

# List of all file paths
allFiles = []
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                allFiles.append(filename)
                yield filename

for filename in find_files(FOLDERNAME, '*corpus'):
	continue

def clean_up(sentence):
	"""Takes in a sentence and removes escape and unicode characters"""
	return unicode(sentence.strip().replace("\n", ""), errors='ignore').strip().replace("\x0c", "")

def check_nan(s):
	""" Checks if a string is empty or NaN"""
	if s == "":
		return True
	if type(x) is not str:
		return np.isnan(s)

#Getting all the terms from the sparse matrix glossary
terms = []
for col in list(glossary.columns):
	terms += [x for x in set(glossary[col]) if not check_nan(x)]

bar = Bar('Processing', max=len(allFiles))

saveFolderPath = r"/Users/pbio/Desktop/CSR_text/" + SENTENCEFOLDER

for i in range(len(allFiles)):

	bar.next()
	
	#Creating the paths to write to text file
	fullPath = allFiles[i].split("/")
	CSR_folder = fullPath[0]
	company_name = fullPath[1]
	corpusName = fullPath[2]
	corpusPath = CSR_folder + "/" + company_name + "/" + corpusName
	newpath = saveFolderPath + company_name
	outputPath = saveFolderPath + company_name + "/" + corpusName + "_sentences"

	#Checking if the sentence corpus already exists
	if not os.path.exists(outputPath):
		#Creating a list of all the sentences
		allSentences = []
		for j in range(len(terms)):
			path = allFiles[i]
			with open(path, 'r') as f:
				document = f.read()
				sentences = document.split(". ")
				relevant_sentences = [clean_up(x) for x in sentences if terms[j] in x.lower()]
				allSentences += relevant_sentences

		#Creating company directories if they don't already exist
		if not os.path.exists(newpath):
			print " Making a new path"
			os.makedirs(newpath)

		#Writing files
		with open(outputPath, 'w') as f:
			for line in allSentences:
				f.write("%s\n" % line)
	bar.finish()