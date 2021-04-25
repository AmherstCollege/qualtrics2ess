#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
qualtrics2ess.py

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

@author: aanderson
"""
import sys
import os
import csv
import re
from json import dumps as jsonPrint
from random import SystemRandom as sr
from datetime import datetime

if sys.version_info.major + sys.version_info.minor/10. < 2.5:
    sys.exit('Version of python must be >= 2.5')
elif sys.version_info.major == 2:
    from urllib import unquote_plus
else:
    from urllib.parse import unquote_plus

# The openpyxl library must be installed with conda or pip
try:
    import openpyxl
except:
    excel = False
else:
    excel = True

if len(sys.argv) != 2 :
    sys.exit('Usage: ' + sys.argv[0] + ' qualtricsfile')
else:
    infile = sys.argv[1]
outputDirectory = os.path.dirname(infile)
if outputDirectory == '':
    outputDirectory = os.getcwd()
filename = unquote_plus(os.path.splitext(os.path.basename(infile))[0])    # Root filename
if re.search("win", sys.platform):
    filename = re.sub(r'[\\/\:*"<>\|\.%\$\?\^&£]', '', filename)
elif re.search("darwin", sys.platform):
    filename = re.sub(r'[/\:]', '', filename)
else:
    filename = re.sub(r'/', '', filename)


(contestName, electionDate, time) = filename.split('_')
date = datetime.strptime(electionDate, '%B %d, %Y')

config = {
  "tabulatorVersion" : "1.2.0",
  "outputSettings" : {
    "contestName" : contestName,
    "outputDirectory" : outputDirectory,
    "contestDate" : date.isoformat()[:10],
    "contestJurisdiction" : "",
    "contestOffice" : "",
    "tabulateByPrecinct" : False,
    "generateCdfJson" : False
  },
  "cvrFileSources" : [ {
    "filePath" : "",
    "contestId" : "",
    "firstVoteColumnIndex" : "4",
    "firstVoteRowIndex" : "2",
    "idColumnIndex" : "1",
    "precinctColumnIndex" : "2",
    "overvoteDelimiter" : "",
    "provider" : "ess",
    "overvoteLabel" : "overvote",
    "undervoteLabel" : "undervote",
    "undeclaredWriteInLabel" : "",
    "treatBlankAsUndeclaredWriteIn" : False
  } ],
  "candidates" : [ ],  # e.g. { "name" : "Lettuce", "code" : "", "excluded" : False }
  "rules" : {
    "tiebreakMode" : "previousRoundCountsThenRandom",
    "overvoteRule" : "exhaustImmediately",
    "winnerElectionMode" : "",
    "randomSeed" : str(round(sr().random()*10000)),
    "numberOfWinners" : "",
    "multiSeatBottomsUpPercentageThreshold" : "",
    "decimalPlacesForVoteArithmetic" : "4",
    "minimumVoteThreshold" : "",
    "maxSkippedRanksAllowed" : "1",
    "maxRankingsAllowed" : "max",
    "nonIntegerWinningThreshold" : False,
    "hareQuota" : False,
    "batchElimination" : False,
    "continueUntilTwoCandidatesRemain" : False,
    "exhaustOnDuplicateCandidate" : False,
    "rulesDescription" : "",
    "treatBlankAsUndeclaredWriteIn" : False
  }
}

#voters = () # Information about all voters, if one wishes to include in output.
elections = ()  # row indices of election information
eLabels = ()    # labels assigned to each election, e.g. 'Q1'
candidates = () # lists of declared candidates for each election
allCandidates = []  # unique sets of all candidates for each election
rankings = ()   # Rankings by all voters
with open(infile, 'r') as input:
    for row in csv.reader(input):
        if len(elections) == 0:   # First row, election labels
            if len(row) <= 10:
                sys.exit('Error: Qualtrics file does not have election information.')
            #voters = (row[:10],)
            election = 10
            elections = (election,) # index into row for election start
            eCurrent = row[10].split('_')[0]    # current label, e.g. 'Q1_1' => ['Q1','1']
            eLabels = (eCurrent,)
            for candidate in row[11:]: # e.g. ['Q1_2', ..., 'Q2_1', ...]
                election += 1
                e = candidate.split('_')[0]
                if e == eCurrent: continue    # otherwise define a new election
                elections += (election,)
                eCurrent = e
                eLabels += (eCurrent,)
            elections += (election+1,)    # non-existent election but an end marker
        elif len(candidates) == 0: # Second row, election candidates
            #voters = (row[:10],)
            for election in range(len(elections)-1):
                names = ()
                for name in row[elections[election]:elections[election+1]]:
                    names += (name.split(' - ')[-1],)
                candidates += (names,)
                allCandidates += [set(names)-set(('Write-In', 'Text'))]    # a unique set
        elif row[0][0] == '{': continue # Third row {"Importid": …}, skip
        else:
            #voters += (row[:10],)
            rankingsByChoice = ()
            for election in range(len(elections)-1):
                rankingByCandidate = row[elections[election]:elections[election + 1]]
                rankingByChoice = ()
                for rank in range(1,len(rankingByCandidate)):  # avoids last write-in value
                    try:
                        candidate = candidates[election][rankingByCandidate.index(str(rank))]
                    except ValueError:
                        rankingByChoice += ('undervote',)
                    else:
                        if candidate == 'Write-In':
                            writein = rankingByCandidate[-1].strip()
                            if (writein == ''): # This can generally be avoided with a Qualtrics setting
                                rankingByChoice += ('undervote',)
                            else:
                                rankingByChoice += (writein,)
                                allCandidates[election] |= set((writein,))
                        else:
                            rankingByChoice += (candidate,)
                rankingsByChoice += (rankingByChoice,)  # aggregates multiple elections
            rankings += (rankingsByChoice,) # aggregates multiple voter records
    input.close()

# Output individual election files and corresponding configuration files
for election in range(len(elections)-1):
    eLabel = eLabels[election]
    config['outputSettings']['contestOffice'] = eLabel
    config['candidates'] = []
    for candidate in allCandidates[election]:
        config['candidates'] += [{ "name" : candidate, "code" : "", "excluded" : False }]
    filenameElection = filename + '_' + eLabel
    config['cvrFileSources'][0]['filePath'] = filenameElection + '.xlsx'
    with open(filenameElection + '_cdf.json', 'w') as output:
        output.write(jsonPrint(config, indent=4, separators=(',', ': ')))
        print("Saved: " + filenameElection + '_cdf.json')

    header = ["Cast Vote Record","Precinct","Ballot Style"] + \
               [eLabel + ' Choice ' + str(choice) 
                for choice in range(1, elections[election+1] - elections[election])]
    if excel:
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Marked Sheet"
        ws1.append(header)
        for record in range(len(rankings)):
            ws1.append((record+1, filename, "Qualtrics") + 
                       rankings[record][election])            
        wb.save(filename = config['cvrFileSources'][0]['filePath'])
        wb.close()
        print("Saved: " + config['cvrFileSources'][0]['filePath'])
    else:   # CSV
        with open(filenameElection + '.csv', 'w') as output:
            csvwriter = csv.writer(output)
            csvwriter.writerow(header)
            for record in range(len(rankings)):
                csvwriter.writerow((str(record+1), filename, "Qualtrics") + 
                                   rankings[record][election])            
            print("Saved: " + filenameElection + '.csv')

if not excel:
    print("Warning: Output CSV files must be opened by Excel and resaved as Excel Workbook (.xlsx) files.")

print("Notice: Election rules are not determined! Open the cdf.json files in the RCV Tabulator, and set the Rules Description and Winning Rules.")
