# qualtrics2ess

Convert ranked choice output from Qualtrics CSV to ES&S format, 
which can be fed into the RCV Universal Tabulator.

Usage: ./qualtrics2ess.py qualtricsfile.csv

• The former is in Candidate by Choice format, while the latter is Choice by Candidate.

• Write-in values are filled in in the correct choice column.

• Blank or -99 values are replaced by the keyword "undervote". 
Qualtrics will by itself prevent overvotes.

• Separate elections are output into different CSV files.

• Extra header and voter identification information is dropped.

• Compatible with both Python 2 and 3.

Created on Mon Apr  5 01:40:21 2021

@author: aanderson@amherst.edu
