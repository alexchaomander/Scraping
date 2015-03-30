import os, fnmatch
import subprocess
from progress.bar import Bar

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

#print allFiles
bar = Bar('Processing', max=len(allFiles))
corpus_name = "corpus"

for i in range(len(allFiles)):
	fullPath = allFiles[i].split("/")
	CSR_folder = fullPath[0]
	company_name = fullPath[1]
	pdfName = fullPath[2]
	pdfPath = CSR_folder + "/" + company_name + "/" + pdfName
	newpath = r"/Users/pbio/Desktop/CSR_text/corpus2/" + company_name
	outputPath = r'/Users/pbio/Desktop/CSR_text/corpus2/' + company_name + "/" + pdfName[:-4] + "_corpus"
	if not os.path.exists(newpath):
		print " Making a new path"
		os.makedirs(newpath)
	process = subprocess.Popen('pdf2txt.py "{}" > "{}"'.format(pdfPath, outputPath), shell=True)
	process.wait()
	bar.next()
bar.finish()

# print "Writing to files"
# corpus_name = "corpus"
# for i in range(len(documents)):
# 	f = open("~/Desktop/CSR_text/corpus/" + corpus_name, "w")
# 	f.write(documents[i])
# 	f.close()

