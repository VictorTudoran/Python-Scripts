#!/usr/bin/python
import os,sys
import shutil
from collections import Counter
import json

try:
    inFolder = sys.argv[1]
    outputFolder = sys.argv[2]
except:
    usage = "analyzeAnnotation.py inFolder outputFolder\n"
    sys.stderr.write(usage)
    sys.exit(0)


stopwords = ['',' ', 'And','The','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has','had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after','above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]



#get the range of offset surrounding an annotation
#get the text fragment in .txt that corresponds to the offset from .ann
def getOffset(enType, start, end, path):
    n = 500
    start = int(start)
    end = int(end)
    start -= 250
    end += 250
        
    path = path[:-3]
    path = path + "txt"
    txtfile = open(path,'r')
    cnt = txtfile.read()
    
    if start < 0:
        start = 0
        end = 500

    if end > len(cnt):
        start = len(cnt) - 500
        end = len(cnt)
        
    #print(start, end)
    
    fragment = cnt[start:end]
    writer = open(outputFolder + '/' + enType + '.txt', 'a+')

    writer.write(("\n%s\n")%("**************"*5))
    writer.write(fragment)
    writer.close()
 
    pass


#traverse through analysis/*.count files and count frequency of words    
def wordFrequency():

    for path,dirs,files in os.walk(outputFolder):
        for filename in files:
            fullpath = os.path.join(path,filename)
            if fullpath.find(".txt") != -1:
                counterfile = open(fullpath,'r')
                cnt = counterfile.read()
                counterfile.close()
                wordList = [word.strip("=* -:;,<>_.") for word in cnt.split()]
                wordList = [word.lower() for word in wordList]
                
                cleanList =(difference(wordList,stopwords))
                #print cleanList
                #print wordList
                
                newPath = fullpath[:-3] + 'count'
                #print newPath

                countfile = open(newPath,'w+')
                counts = Counter(cleanList).most_common(50)
                countfile.write(json.dumps(counts))
                
                countfile.close()



#check if file is empty
def isNotEmpty(path):
    return os.stat(path).st_size != 0


#find difference between items of 2 lists
def difference(firstList, secondList):
    listDiff = [i for i in firstList if i not in secondList]
    return listDiff


#start by clearing the output folder
filelist = [ f for f in os.listdir(outputFolder)]
for f in filelist:
    os.remove(os.path.join(outputFolder, f))


# #iterate through entitities and search for them in *.ann files recursively
for path,dirs,files in os.walk(inFolder):
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
                enStart = lineSplited[2]
                enEnd = lineSplited[3]
                if enStart.find(';') == -1 and enEnd.find(';') == -1:      
                    #print (enStart, enEnd)
                    getOffset(enType, enStart, enEnd, fullpath)
            
            searchfile.close()

              
wordFrequency()
