#!/usr/bin/python

import os,sys
import shutil
from sklearn.metrics import cohen_kappa_score
from pathlib import Path

try:
    inFolder1 = sys.argv[1]
    inFolder2 = sys.argv[2]
    outFolder = sys.argv[3]

except:
    usage = "kappaScore.py inFolder1 inFolder2 outFolder \n"
    sys.stderr.write(usage)
    sys.exit(0)


list1 = []
list2 = []
entitySet = set()

#check if file is empty
def isNotEmpty(path):
    return os.stat(path).st_size != 0


#get kappa score for lists of all annotations
def listAnalysis(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    
  
    intersectionSet = set.intersection(set1,set2)
    
    differenceSet1 = set1.difference(set2) # set1 - set2 (IDs included in set 1 only)
    differenceSet2 = set2.difference(set1) # set2 - set1 (IDs included in set 2 only)
    
    zero1 = [0] * len(differenceSet1)
    zero2 = [0] * len(differenceSet2)

    
    intersectionSet = list(intersectionSet)

    differenceSet1 = list(differenceSet1)
    zero1 = list(zero1)
    final1 = intersectionSet + differenceSet1 + zero2
    
    differenceSet2 = list(differenceSet2)
    zero2 = list(zero2)
    final2 = intersectionSet + zero1 + differenceSet2
    
    
    print ('The average kappa score is: ')
    print cohen_kappa_score(final1,final2)



#get kappa score from 2 filenames with specific annotation type
def fileAnalysis(file1,file2):
    list1 = open(file1).readlines()
    list2 = open(file2).readlines()

    set1 = set(list1)
    set2 = set(list2)

    intersectionSet = set.intersection(set1,set2)
    
    differenceSet1 = set1.difference(set2) # set1 - set2 (IDs included in set 1 only)
    differenceSet2 = set2.difference(set1) # set2 - set1 (IDs included in set 2 only)
    
    zero1 = [0] * len(differenceSet1)
    zero2 = [0] * len(differenceSet2)

    intersectionSet = list(intersectionSet)
    differenceSet1 = list(differenceSet1)
    zero1 = list(zero1)
    
    final1 = intersectionSet + differenceSet1 + zero2
    
    differenceSet2 = list(differenceSet2)
    zero2 = list(zero2)
    
    final2 = intersectionSet + zero1 + differenceSet2

    
    print cohen_kappa_score(final1,final2)



#start by clearing the output folder
filelist = [ f for f in os.listdir(outFolder)]
for f in filelist:
    os.remove(os.path.join(outFolder, f))


#iterate through entitities and search for them in *.ann files recursively
for path,dirs,files in os.walk(inFolder1):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".ann") != -1 and isNotEmpty(fullpath):
            searchfile = open(fullpath,'r')
            cnt = searchfile.readlines()
            for line in cnt:
                if line == "" or line == "\n" or line[0] != 'T':
                    continue
                lineSplited = line.split()
                entityGroup = lineSplited[1].split()
                enType = lineSplited[1]
                entitySet.add(enType)
                startOffset = lineSplited[2]
                uniqueIdentifier = filename[:-4] + "_" + enType + "_" + startOffset
                list1.append(uniqueIdentifier) 
                entityFile = open(outFolder + '/' + enType + '.vic','a+')
                entityFile.write(("%s\n")%(uniqueIdentifier))

                entityFile.close()

            searchfile.close()


#iterate through entitities and search for them in *.ann files recursively
for path,dirs,files in os.walk(inFolder2):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".ann") != -1 and isNotEmpty(fullpath):
            searchfile = open(fullpath,'r')
            cnt = searchfile.readlines()
            for line in cnt:
                if line == "" or line == "\n" or line[0] != 'T':
                    continue
                lineSplited = line.split()
                entityGroup = lineSplited[1].split()
                enType = lineSplited[1]
                startOffset = lineSplited[2]
                uniqueIdentifier = filename[:-4] + "_" + enType + "_" + startOffset
                list2.append(uniqueIdentifier)
                entityFile = open(outFolder + '/' + enType + '.yan','a+')
                entityFile.write(("%s\n")%(uniqueIdentifier))

                entityFile.close()

            searchfile.close()


listAnalysis(list1,list2)

for entityName in entitySet:
    filenameVic = outFolder + entityName + '.vic'
    filenameYan = outFolder + entityName + '.yan'
    print('The Kappa score for ' + entityName + ' is:')
    #if filenameVic.exists() and filenameYan.exists(): 
    #    fileAnalysis(filenameVic,filenameYan)
    if os.path.exists(filenameVic) and os.path.exists(filenameYan):
        fileAnalysis(filenameVic,filenameYan)
