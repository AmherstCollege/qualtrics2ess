# qualtrics2ess

Convert ranked choice output from Qualtrics to ES&S format, 
which can be fed into the Universal RCV Tabulator.

The former is in Candidate by Choice format, while the latter is Choice by Candidate.

Separate elections are output into different files.

Extra header and voter identification information is dropped.

Compatible with both Python 2 and 3.

Usage: ./qualtrics2ess.py qualtricsfile

Created on Mon Apr  5 01:40:21 2021

@author: aanderson@amherst.edu
