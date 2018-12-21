#!/usr/bin/python
import os,sys
import shutil
import json

try:
    inFolder1 = sys.argv[1]
    inFolder2 = sys.argv[2]
    outputDocument = sys.argv[3]

except:
    usage = "convertToJson.py InputFolder1 InputFolder2 outputDocument\n"
    sys.stderr.write(usage)
    sys.exit(0)


dataSet ={}

for path,dirs,files in os.walk(inFolder1):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".txt") != -1:
            textFile = open(fullpath,'r')
            textcnt = textFile.read()
            newstr = textcnt.replace("\n", " ")
            newnew = newstr.replace("\t", " ")
            newnew = newnew.replace('"', '')
            newnew = newnew.replace("\r", "")
            newnew = newnew.replace("\\", " ")
               
            dataSet["id"] = filename[:-4]
            dataSet["text"] = newnew

            #writer.write("{\n")
            #writer.write('\t"id" : "%s",\n' %(filename[:-4]))
            #writer.write('\t"text" : "%s",\n' %(newnew))
            #writer.write('\t"tags" : [\n')

            tags = {}

            annFile = open(fullpath[:-3]+"ann",'r')
            cnt = annFile.readlines()
            for line in cnt:
                if line == "" or line  == "\n" or line[0] != 'T':
                    continue
                lineSplited = line.split('\t')
                enID = lineSplited[0]
                enInfo = lineSplited[1].split()
                enType = enInfo[0]
                if enType == "DOC_REVIEWED" or enType == "DOC_PII" or enType == "DOC_PHI" or enType == "DOC_PCI" or enType == "DOC_AUTOGEN":
                    continue
                enStart = enInfo[1]
                enEnd = enInfo[2]
                enText = lineSplited[2]
                enText = enText.strip('\n')
                enText = enText.strip('"')
                if enStart.find(';') == -1 and enEnd.find(';') == -1:
                    #writer.write('\t\t{\n')
                    #writer.write('\t\t\t"category" : "%s",\n' %(enType))
                    #writer.write('\t\t\t"end" : "%s",\n' %(enEnd))
                    #writer.write('\t\t\t"id" : "%s",\n' %(enID))
                    #writer.write('\t\t\t"start" : "%s",\n' %(enStart))
                    #writer.write('\t\t\t"text" : "%s",\n' %(enText))
                    #writer.write('\t\t\t"type" : "%s"\n' %(enType))
                    #writer.write('\t\t},\n')
                    tags["category"] = enType
                    tags["end"] = enEnd
                    tags["id"] = enID
                    tags["start"] = enStart
                    tags["text"] = enText
                    tags["type"] = enType
                    
            dataSet["tags"] = tags
            #print (json.dumps(dataSet, indent = 4))

            #writer.write('\b')
            #writer.write('\t\t]')

            #writer.write("},")

            annFile.close()


for path,dirs,files in os.walk(inFolder2):
    for filename in files:
        fullpath = os.path.join(path,filename)
        if fullpath.find(".txt") != -1:
            textFile = open(fullpath,'r')
            textcnt = textFile.read()
            newstr = textcnt.replace("\n", " ")
            newnew = newstr.replace("\t", " ")
            newnew = newnew.replace('"', '')
            newnew = newnew.replace("\r", " ")
            newnew = newnew.replace("\\", " ")

            dataSet["id"] = filename[:-4]
            dataSet["text"] = newnew

            #writer.write("{\n")
            #writer.write('\t"id" : "%s",\n' %(filename[:-4]))
            #writer.write('\t"text" : "%s",\n' %(newnew))
            #writer.write('\t"tags" : [\n')

            tags = {}

            annFile = open(fullpath[:-3]+"ann",'r')
            cnt = annFile.readlines()
            for line in cnt:
                if line == "" or line  == "\n" or line[0] != 'T':
                    continue
                lineSplited = line.split('\t')
                enID = lineSplited[0]
                enInfo = lineSplited[1].split()
                enType = enInfo[0]
                if enType == "DOC_REVIEWED" or enType == "DOC_PII" or enType == "DOC_PHI" or enType == "DOC_PCI" or enType == "DOC_AUTOGEN":
                    continue
                enStart = enInfo[1]
                enEnd = enInfo[2]
                enText = lineSplited[2]
                enText = enText.strip('\n')
                enText = enText.strip('"')
                if enStart.find(';') == -1 and enEnd.find(';') == -1:
                    #writer.write('\t\t{\n')
                    #writer.write('\t\t\t"category" : "%s",\n' %(enType))
                    #writer.write('\t\t\t"end" : "%s",\n' %(enEnd))
                    #writer.write('\t\t\t"id" : "%s",\n' %(enID))
                    #writer.write('\t\t\t"start" : "%s",\n' %(enStart))
                    #writer.write('\t\t\t"text" : "%s",\n' %(enText))
                    #writer.write('\t\t\t"type" : "%s"\n' %(enType))
                    #writer.write('\t\t},\n')
                    tags["category"] = enType
                    tags["end"] = enEnd
                    tags["id"] = enID
                    tags["start"] = enStart
                    tags["text"] = enText
                    tags["type"] = enType

            dataSet["tags"] = tags

            #writer.write('\b')
            #writer.write('\t\t]')

            #writer.write("},")

            annFile.close()


print (json.dumps(dataSet, indent = 4))




'''
with open(outputDocument,'w') as outFile:
    json.dump(dataSet, outFile)
'''



#writer.write('\b')
#writer.write("]")

#writer.close()

