# qualtrics2ess

Convert ranked choice output from Qualtrics CSV to ES&S Excel format, 
which can be fed into the RCV Universal Tabulator.

Usage, from a terminal or command shell: qualtrics2ess.py *qualtricsfile.csv*

## Description

[Qualtrics](https://www.qualtrics.com/core-xm/survey-software/) is a cloud platform providing survey tools, including the ability to rank items, send participation links to individuals, and record their choices anonymously. It can therefore be used for ranked choice voting elections. Amherst College has written [a set of instructions for using Qualtrics for RCV elections](https://docs.google.com/document/d/1MT7JORmGbe4ALw4sfMT8w2_Wgs_8MJcbUVcXUcMc5BA/edit?usp=sharing).

At this time the [RCV Universal Tabulator](https://www.rcvresources.org/rcv-universal-tabulator) cannot read the Qualtrics format — instead the most similar format is the ES&S format, after the company whose equipment generates it. The former is in Candidate by Choice format, while the latter is Choice by Candidate. But it’s a relatively simple transformation to convert one to the other, provided by this script.

### *Qualtrics to ES&S Format* ###

This script will run on any computer that has the Python interpreter installed on it.

The Qualtrics survey / ballot document is converted to a set of ES&S-format documents, one for each election on the ballot:

![Cast Vote Record table in Choice by Candidate format](https://raw.githubusercontent.com/AmherstCollege/qualtrics2ess/main/CVR%20Vegetable%20RCV.png)

### *Excel Workbook and CSV Formats*

ES&S files are actually provided as Excel workbook (.xlsx) files, so the RCV Universal Tabulator is only designed to input that format. The qualtrics2ess.py script will generate Excel files but this requires a non-standard Python library, and if that isn’t present it will output CSV format instead. But any CSV file can be opened in Excel (usually the result if you have it installed and double-click the file) and then saved by menuing **File** > **Save As…** and select the **File Format:** **Excel Workbook (.xlsx)**.

### *Common Data Format File*

The qualtrics2ess.py script will also generate a common data format (CDF) file for each election, which provides the basic information about the ballot that can be extracted from the Qualtrics input file. This file can be loaded into the RCV Universal Tabulator as a starting point. Importantly, this includes all of the candidate names on all of the ballots, including write-ins. It does not, however, include the election rules.

## Details

* Write-in values are filled in, in the correct choice column.

* Blank or -99 values are replaced by the keyword "undervote". 
Qualtrics will by itself prevent overvotes.

* Separate elections are output into different Excel files (CSV if necessary).

* Config files are also generated with information from the Qualtrics file, including candidate names.

* Output files are URL-decoded to make them more readable by humans (this may make them less compatible on older operating systems).

* Extra header and voter identification information is dropped.

* Compatible with Python 2.5 or later, including Python 3.x.

## Installation

1. [Github Source](https://github.com/AmherstCollege/qualtrics2ess)

2. a. [Download and install Python](https://www.python.org/downloads/)<br><br>
b. To create Excel workbooks, qualtrics2ess.py depends on the library openpyxl, which can be installed by running the program **pip** in the terminal (command shell):<br><br>
pip install openpyxl<br><br>
If pip isn't available: [Download and install pip](https://pypi.org/project/pip/)<br>
Otherwise, CSV files will be generated, and Excel can be used to convert them.<br><br>
Alternative to steps 2a and 2b: [Download and install Anaconda](https://www.anaconda.com/products/individual), providing a single python installation along with a useful collection of Python libraries.

3. Install the [RCV Universal Tabulator](https://github.com/BrightSpots/rcv).

## Background

Created on Mon Apr  5 01:40:21 2021

@author: Andy Anderson, Amherst College, aanderson@amherst.edu
