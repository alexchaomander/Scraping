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
# for i in range(len(allFiles)):
# 	print allFiles[i].split("/")[2]

for i in range(len(allFiles)):
	company_name = allFiles[i].split("/")[1]
	newpath = r"~/Desktop/CSR_text/corpus/" + company_name
	pdfName = allFiles[i].split("/")[2]
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	process = subprocess.Popen('pdf2txt.py "' + allFiles[i] + '" > ~/Desktop/CSR_text/corpus/' + company_name + "/" + pdfName, shell=True)
	bar.next()
bar.finish()

# print "Writing to files"
# corpus_name = "corpus"
# for i in range(len(documents)):
# 	f = open("~/Desktop/CSR_text/corpus/" + corpus_name, "w")
# 	f.write(documents[i])
# 	f.close()

