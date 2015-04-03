import os, fnmatch
import subprocess
from progress.bar import Bar

""" 
PDF text extractor.

Assumes that the directory is structured like:

CSRs
	CompanyA
		csr_report.pdf
		csr_report2.pdf
	CompanyB
		csr_report3.pdf
	...

To run: 
`python textGetter.py` in the directory that has the folder of interest. 
(i.e. folder containing the folder CSRs)

Will create a folder in the current directory called `FOLDERNAME` that contains
directories of companies with the text of the PDFs saved in text files for each company.
"""

FOLDERNAME = "corpus2/"

if not os.path.exists(FOLDERNAME):
	os.makedirs(FOLDERNAME)

print "Finding Files"
allFiles = []

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                allFiles.append(filename)
                yield filename

for filename in find_files('CSRs', '*.pdf'):
	continue

bar = Bar('Processing', max=len(allFiles))

for i in range(len(allFiles)):
	fullPath = allFiles[i].split("/")
	CSR_folder = fullPath[0]
	company_name = fullPath[1]
	pdfName = fullPath[2]
	pdfPath = CSR_folder + "/" + company_name + "/" + pdfName
	newpath = r"/Users/pbio/Desktop/CSR_text/" + FOLDERNAME + company_name
	outputPath = r'/Users/pbio/Desktop/CSR_text/' + FOLDERNAME + company_name + "/" + pdfName[:-4] + "_corpus"
	if not os.path.exists(newpath):
		print " Making a new path"
		os.makedirs(newpath)
	if not os.path.exists(outputPath):
		print " Creating the corpus"
		process = subprocess.Popen('pdf2txt.py "{}" > "{}"'.format(pdfPath, outputPath), shell=True)
		process.wait()
	bar.next()
bar.finish()