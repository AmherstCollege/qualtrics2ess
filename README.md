# qualtrics2ess

Convert ranked choice output from Qualtrics CSV to ES&S format, 
which can be fed into the RCV Universal Tabulator.

Usage: ./qualtrics2ess.py qualtricsfile.csv

## Description

At this time the RCV Universal Tabulator cannot read the Qualtrics format — instead the most similar format is the ES&S format, after the company whose equipment generates it. The former is in Candidate by Choice format, while the latter is Choice by Candidate. But it’s a relatively simple transformation to convert one to the other.

This script will run on any computer that has the Python interpreter installed on it.

The Qualtrics survey / ballot document is converted to a set of ES&S-format documents, one for each election on the ballot:

![Cast Vote Record table in Choice by Candidate format](CVR Vegetable RCV.png)

### Excel Workbook and CSV Formats

ES&S files are actually provided as Excel workbook (.xlsx) files, so the RCV Universal Tabulator is only designed to input that format. The qualtrics2ess.py script will generate Excel files but this requires a non-standard Python library, and if that isn’t present it will output CSV format instead. But any CSV file can be opened in Excel (usually the result if you have it installed and double-click the file) and then saved by menuing File > Save As… and select the File Format: Excel Workbook (.xlsx).

### Common Data Format File

The qualtrics2ess.py script will also generate a common data format (CDF) file for each election, which provides the basic information about the ballot that can be extracted from the Qualtrics input file. This file can be loaded into the RCV Universal Tabulator as a starting point. Importantly, this includes all of the candidate names on all of the ballots, including write-ins. It does not, however, include the election rules.

## Details

• Write-in values are filled in, in the correct choice column.

• Blank or -99 values are replaced by the keyword "undervote". 
Qualtrics will by itself prevent overvotes.

• Separate elections are output into different Excel files (CSV if necessary).

• Extra header and voter identification information is dropped.

• Compatible with both Python 2.5 or later, including Python 3.x.

## Installation

[Github Source](https://github.com/AmherstCollege/qualtrics2ess)

[Download and install Python](https://www.python.org/downloads/)

qualtrics2ess.py depends on the library openpyxl, which can be installed with pip:

[Download and install pip](https://pypi.org/project/pip/)

then in the terminal run the command line statement:

pip install openpyxl


## Background

Created on Mon Apr  5 01:40:21 2021

@author: aanderson@amherst.edu
