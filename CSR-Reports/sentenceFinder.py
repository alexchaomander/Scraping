import os, fnmatch
import subprocess
from progress.bar import Bar
import re
import pandas as pd
import numpy as np
import gspread
#Credentials to login to Google Sheets
from credentials import GOOGLE_LOGIN, GOOGLE_PASS, GOOGLE_SHEET

gc = gspread.login(GOOGLE_LOGIN, GOOGLE_PASS)
wb = gc.open_by_key(GOOGLE_SHEET)
ws = wb.worksheet('Sheet1')
sheet = ws.get_all_values()
headers = sheet.pop(0)

#A pandas dataframe of the glossary of terms
glossary = pd.DataFrame(sheet, columns=headers)

#The folder that contains all the text files for CSR reports
folderName = "corpus2"

# List of all file paths
allFiles = []
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                allFiles.append(filename)
                yield filename

for filename in find_files(folderName, '*corpus'):
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

synonyms = [x for x in glossary['Synonyms'] if not check_nan(x)]
keyWords = [x for x in glossary['Key Words'] if not check_nan(x)]
terms = synonyms + keyWords
#print terms

for i in range(1):
	allSentences = []
	for j in range(len(terms)):
		path = allFiles[i]
		with open(path, 'r') as f:
			document = f.read()
			sentences = document.split(". ")
			relevant_sentences = [clean_up(x) for x in sentences if terms[j] in x.lower()]
			allSentences += relevant_sentences
	print allSentences

