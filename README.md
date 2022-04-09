# qualtrics2ess

Convert ranked choice output from Qualtrics CSV to ES&S Excel format, 
which can be fed into the RCV Universal Tabulator.

Usage, from a terminal or command shell: qualtrics2ess.py *qualtricsfile.csv*

## Description

[Qualtrics](https://www.qualtrics.com/core-xm/survey-software/) is a popular cloud platform providing survey tools, including the ability to rank items, e-mail participation links to individuals, and record their choices anonymously. It can therefore be used for ranked choice voting elections. Amherst College has written [a set of instructions for using Qualtrics for RCV elections](https://docs.google.com/document/d/1MT7JORmGbe4ALw4sfMT8w2_Wgs_8MJcbUVcXUcMc5BA/edit?usp=sharing).

At this time the [RCV Universal Tabulator](https://www.rcvresources.org/rcv-universal-tabulator) cannot read the Qualtrics format — instead the most similar format is the ES&S format, after the company whose equipment generates it. The former is in Candidate by Choice format, while the latter is Choice by Candidate. But it’s a relatively simple transformation to convert one to the other, provided by this script.

### *Qualtrics to ES&S Format* ###

This script will run on any computer that has the Python interpreter installed on it.

A Qualtrics survey / ballot document is provided here for testing: [What+Are+Your+Favorite+Fruits+and+Vegetables%3F_April+13%2C+2021_23.28.csv](https://github.com/AmherstCollege/qualtrics2ess/blob/main/What%2BAre%2BYour%2BFavorite%2BFruits%2Band%2BVegetables%253F_April%2B13%252C%2B2021_23.28.csv):

![Cast Vote Record table in Candidate by Choice format](https://raw.githubusercontent.com/AmherstCollege/qualtrics2ess/main/CVR%20Vegetable%20Qualtrics.png)

The script will convert such files to a set of ES&S-format Cast Vote Record (CVR) documents, one for each election on the ballot:

![Cast Vote Record table in Choice by Candidate format](https://raw.githubusercontent.com/AmherstCollege/qualtrics2ess/main/CVR%20Vegetable%20RCV.png)

### *Excel Workbook and CSV Formats*

ES&S CVR files are actually provided as Excel workbook (.xlsx) files, so the RCV Universal Tabulator is only designed to input that format. The qualtrics2ess.py script will generate Excel files, ending in _cvr.xlsx. This does require a non-standard Python library, but if it isn’t present it will output files in CSV format instead, ending in _cvr.csv. Any CSV file can be opened in Excel (usually the result if it’s installed and you double-click the file) and then saved as **File Format:** **Excel Workbook (.xlsx)**.

### *Common Data Format File*

The qualtrics2ess.py script will also generate a common data format (CDF) file for each election, which provides the basic information about the ballot contained in the Qualtrics input file. They will be in JSON format, a standard format for distributing datasets, and will have a file name ending in _cdf.json. This file can be loaded into the RCV Universal Tabulator as a starting point. Importantly, this includes all of the candidate names on all of the ballots, including write-ins. It does not, however, include the election rules, which must be specified in the Tabulator.

## Details

* Write-in values are filled in, in the correct choice column.

* Blank or -99 values are replaced by the keyword "undervote". 
Qualtrics will by itself prevent overvotes.

* Separate elections are output into different Excel files (CSV if necessary).

* Config files are also generated with information from the Qualtrics file, including candidate names.

* The base name of these files will be the same as the Qualtrics file. To make the file names easier to read the ‘+’ and “%XX” characters are either replaced with allowed filename characters or removed.

* Extra header and voter identification information is dropped.

* Compatible with Python 2.5 or later, including Python 3.x.

## Installation

1. [Github Source](https://github.com/AmherstCollege/qualtrics2ess)

2. a. [Download and install Python](https://www.python.org/downloads/)<br><br>
b. To create Excel workbooks, qualtrics2ess.py depends on the library openpyxl, which can be installed by running the program **pip** in the terminal (command shell):<br><br>
pip install openpyxl<br><br>
If pip isn't available: [Download and install pip](https://pypi.org/project/pip/)<br><br>
Otherwise, CSV files will be generated, and Excel can be used to convert them.<br><br>
c. Alternative to steps 2a and 2b: [Download and install Anaconda](https://www.anaconda.com/products/individual), providing a single python installation along with a useful collection of Python libraries.

3. Install the [RCV Universal Tabulator](https://github.com/BrightSpots/rcv).

## Running qualtrics2ess

1. qualtrics2ess.py is a python-language script. You must use python to run it in a command-line environment: the terminal on Macintosh, the CMD or PowerShell on Windows, or a shell on Unix. The command is:<br><br>
`python qualtrics2ess.py qualtricsfile.cvr`<br><br>
where `qualtricsfile.cvr` is your Qualtrics cast-vote-records file.

2. On Mac or Unix, you can also make the program executable<br><br>
`chmod +x qualtrics2ess.py`
<br><br>
and then you don't need to precede it with `python`.

3. Be aware that in a command-line environment, quotes, spaces, and other special characters in a file name can be interpreted as something different, so if you have any characters other than letters or numbers in the file name, enclose it between single quotes, or if it contains a single quote enclose it between double quotes.

## Background

Created on Mon Apr  5 01:40:21 2021

@author: [Andy Anderson](https://www.amherst.edu/people/facstaff/aanderson), [Amherst College](https://www.amherst.edu), aanderson@amherst.edu
