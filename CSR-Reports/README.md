# Archive
Tools and scripts to process CSR reports. 

## textGetter.py
PDF text extractor.

Assumes that the directory is structured like:

>CSRs
>>CompanyA
>>>csr_report.pdf

>>>csr_report2.pdf

>>CompanyB
>>>csr_report3.pdf

>>...

To run: 
`python textGetter.py` in the directory that has the folder of interest. 
(i.e. folder containing the folder CSRs)

Will create a folder in the current directory called `FOLDERNAME` that contains
directories of companies with the text of the PDFs saved in text files for each company.

## sentenceFinder.py
Extracts sentences from text files that match a predefined glossary of terms/phrases.
Outputs them into `SENTENCEFOLDER`

To run: 
`python sentenceFinder.py` in the directory that has the folder of interest. 
(i.e. folder containing the text corpuses.)
