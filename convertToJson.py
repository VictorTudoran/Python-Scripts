#!/usr/bin/python
import os,sys
import shutil
from collections import Counter
import json

try:
    inFolder1 = sys.argv[1]
    inFolder2 = sys.argv[2]
    outputDocument = sys.argv[3]

except:
    usage = "convertToJson.py InputFolder1 InputFolder2 outputDocument\n"
    sys.stderr.write(usage)
    sys.exit(0)

writer = open(outputDocument,'w')
writer.write("[\n")


for path,dirs,files in os.walk(inFolder1):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".txt") != -1:
            textfile = open(fullpath,'r')
            textcnt = textfile.read()
            newstr = textcnt.replace("\n", "\\n")
            newnew = newstr.replace("\t", " ")
            newnew = newnew.replace('"', '')
            newnew = newnew.replace("\r", "\\r")
            newnew = newnew.replace("\\", "\\\\")
            

            writer.write("{\n")
            writer.write('\t"id" : "%s",\n' %(filename[:-4]))
            writer.write('\t"text" : "%s",\n' %(newnew))
            writer.write('\t"label" : "PHI"\n')
            writer.write("},")
'''            
        if fullpath.find(".ann") != -1 and isNotEmpty(fullpath):
            searchfile = open(fullpath,'r')
            cnt = searchfile.readlines()
            for line in cnt:
                if line == "" or line == "\n" or line[0] != 'T':
                    continue
                lineSplited = line.split()
                entityGroup = lineSplited[1].split()
                enType = lineSplited[1]
'''
        
for path,dirs,files in os.walk(inFolder2):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".txt") != -1:
            textfile = open(fullpath,'r')
            textcnt = textfile.read()
            newstr = textcnt.replace("\n", "\\n")
            newnew = newstr.replace("\t", " ")
            newnew = newnew.replace('"', '')
            newnew = newnew.replace("\r", "\\n")
            newnew = newnew.replace("\\", "\\\\")
            writer.write("{\n")
            writer.write('\t"id" : "%s",\n' %(filename[:-4]))
            writer.write('\t"text" : "%s",\n' %(newnew))
            writer.write('\t"label" : "NON_PHI"\n')
            writer.write("},")



writer.write('\b')
writer.write("]")

writer.close()
