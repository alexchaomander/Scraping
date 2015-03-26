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

print allFiles
bar = Bar('Processing', max=len(allFiles))
documents = []
corpus_name = "corpus"
for i in range(len(allFiles)):
	process = subprocess.Popen('pdf2txt.py "' + allFiles[i] + '" > ~/Desktop/CSR_text/corpus/' + corpus_name + str(i) , shell=True)
	bar.next()
bar.finish()

# print "Writing to files"
# corpus_name = "corpus"
# for i in range(len(documents)):
# 	f = open("~/Desktop/CSR_text/corpus/" + corpus_name, "w")
# 	f.write(documents[i])
# 	f.close()

