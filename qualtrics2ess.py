#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
qualtrics2ess.py

Convert ranked choice output from Qualtrics to ES&S format, 
which can be fed into the Universal RCV Tabulator.

The former is in Candidate by Choice format, while the latter is Choice by Candidate.

Extra header and voter identification information is dropped.

Compatible with both Python 2 and 3.

Usage: ./qualtrics2ess.py qualtricsfile

Created on Mon Apr  5 01:40:21 2021

@author: aanderson
"""
import sys
import os
import csv

if sys.version_info.major + sys.version_info.minor/10. <= 2.3:
    sys.exit('Version of python must be >= 2.3')
elif sys.version_info.major == 2:
    from urllib import unquote_plus
else:
    from urllib.parse import unquote_plus

if len(sys.argv) != 2 :
    sys.exit('Usage: ' + sys.argv[0] + ' qualtricsfile')
else:
    infile = sys.argv[1]
    filename = os.path.basename(infile)

voters = () # Information about all voters
elections = ()  # row indices of election information
candidates = () # list of available candidates for each election
rankings = ()   # Rankings by all voters
with open(infile, 'r') as input:
    for row in csv.reader(input):
        #print(row)
        if len(elections) == 0:   # First row, election labels
            if len(row) <= 10 or len(row[10]) < 2 or row[10][:2] != 'Q1':
                sys.exit('Error: Qualtrics file does not have election information.')
            voters = (row[:10],)
            election = 10
            elections = (election,) # index into row for election start
            qCurrent = 'Q1'
            for question in row[11:]: # ['Q1_2', ..., 'Q2_1', ...]
                election += 1
                q = question.split('_')[0]
                if q == qCurrent: continue
                qCurrent = q
                elections += (election,)
            elections += (election+1,)    # non-existent election but an end marker
            #print(row, '\n', elections)
        elif len(candidates) == 0: # Second row, election candidates
            voters = (row[:10],)
            for i in range(len(elections)-1):
                questions = ()
                for question in row[elections[i]:elections[i + 1]]:
                    questions += (question.split(' - ')[-1],)
                candidates += (questions,)
                #print(values)
        elif row[0][0] == '{': continue # Third row {"Importid": …}, skip
        else:
            voters += (row[:10],)
            rankingsByChoice = ()
            for i in range(len(elections)-1):
                #print(candidates[i])
                rankingByCandidate = row[elections[i]:elections[i + 1]]
                #print(rankingByCandidate)
                rankingByChoice = ()
                for rank in range(1,len(rankingByCandidate)):  # avoids last write-in value
                    try:
                        candidate = candidates[i][rankingByCandidate.index(str(rank))]
                    except ValueError:
                        rankingByChoice += ('undervote',)
                    else:
                        if candidate == 'Write-In':
                            writein = rankingByCandidate[-1].strip()
                            if (writein == ''): # This can mostly be avoided with a Qualtrics setting
                                rankingByChoice += ('undervote',)
                            else:
                                rankingByChoice += (writein,)
                        else:
                            rankingByChoice += (candidate,)
                rankingsByChoice += (rankingByChoice,)  # aggregates multiple elections
            rankings += (rankingsByChoice,)

input.close()

for election in range(1, len(elections)):
    with open(filename[:-4] + '_Q' + str(election) + '.csv', 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(["Cast Vote Record","Precinct","Ballot Style"] +
           ['Q' + str(election) + ' Choice ' + str(choice) for choice in range(1,elections[election] - elections[election-1])])
        for record in range(len(rankings)):
            csvwriter.writerow((str(record+1), unquote_plus(filename.split('%3F')[0]), "Qualtrics") + 
                               rankings[record][election-1])            
        output.close()
