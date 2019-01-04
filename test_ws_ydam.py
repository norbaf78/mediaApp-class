# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:59:37 2019

@author: fabio.roncato
"""
#import csv
import ws_ydam

ws_ydamTest = ws_ydam.ws_ydam("http://multimedia.trentinonetwork.it", "fabio.roncato@trilogis.it", "Norbaf78_", 20154, 2564504, 0, 72728)
a = ws_ydamTest.strip_accents("Dddddddddddddddddddddd")
print (a)
























'''
Mytest = mediaApp.mediaApp("http://multimedia.trentinonetwork.it", "fabio.roncato@trilogis.it", "Norbaf78_")
Mytest.setCompanyId(20154)
Mytest.setGroupId(2564504)
Mytest.setRepositoryId(0)
Mytest.setFolderId(72728) 
print ("Endpoint: " + Mytest.getEndpoint())
print ("EmailAddress: " + Mytest.getEmailAddress())
print ("Password: " + Mytest.getPassword())
print ("CompanyId: " + str(Mytest.getCompanyId()))
print ("tGroupId: " + str(Mytest.getGroupId()))
print ("RepositoryId: " + str(Mytest.getRepositoryId()))
print ("FolderId: " + str(Mytest.getFolderId()))
print ("countEntryInFolder(): \n\r" + str(Mytest.countEntryInFolder()))
print ("listEntriesForFolder(start = 0, end = 4): \n\r" + str(Mytest.listEntriesForFolder(start = 0, end = 4)))
typ_e = ''
titleMap = '{"it_IT":"test entry python API"}'
descriptionMap = '{"it_IT":"test entry python API"}'
layoutUuid = ''
entryId = Mytest.addEntry(typ_e, titleMap, descriptionMap, layoutUuid)
print ("addEntry(typ_e, titleMap, descriptionMap, layoutUuid): \n\r" + str(entryId))
print ("getEntry(entryId): \n\r" + str(Mytest.getEntry(entryId))) 
print ("getEntry(entryId): \n\r" + str(Mytest.getEntry(entryId)))
print ("countEntriesForVocabulary(40030052): \n\r" + str(Mytest.countEntriesForVocabulary(40030052)))
print ("listCategoriesForVocabulary(40030052, start = 0, end = 4): \n\r" + str(Mytest.listCategoriesForVocabulary(40030052, start = 0, end = 4)))
# addCategory do not run !!
#categoryId = Mytest.addCategory(40030052, 0, '{"it_IT":"test category python API"}', '{"it_IT":"test category python API"}','')
#print ("addCategory(40030052, 0, '{'it_IT':'test category python API'}', '{'it_IT':'test category python API'}', '')" + str(categoryId))
categoryId = 44746593
print ("getCategory(categoryId): \n\r" + str(Mytest.getCategory(categoryId)))
# entryId is available from before
fileId = Mytest.addFile(entryId, 'true')
print ("addFile(entryId, 'true'): \n\r" + str(fileId))
print ("uploadFile( fileId, 'logo-ydam-small.png'): \n\r" + str(Mytest.uploadFile( fileId, 'logo-ydam-small.png')))
# entryId is available from before
files = Mytest.listFilesForEntry(entryId)
print ("listFilesForEntry(entryId): \n\r" + str(files))
print ("downloadOriginalIfFound(files, fileId): \n\r" + str(Mytest.downloadOriginalIfFound(files, fileId)))
parentFolderId = 72728
print ("countFoldersForParentFolder(parentFolderId): \n\r" + str(Mytest.countFoldersForParentFolder(parentFolderId)))
print ("listFoldersForParentFolder(parentFolderId, start = 0, end = 6): \n\r" + str(Mytest.listFoldersForParentFolder(parentFolderId, start = 0, end = 6)))
print ("addSubfolderForParent(parentFolderId, '{'it_IT':'test folder python API'}', '{'it_IT':'test folder python API'}', ''): \n\r" + str(Mytest.addSubfolderForParent(parentFolderId, '{"it_IT":"test folder python API"}', '{"it_IT":"test folder python API"}', '')))
print ("getFolder(): \n\r" + str(Mytest.getFolder()))



# get data from CSV with key,value into single string
csvFile = 'sbm_sibam.csv'
csvData = csv.reader(open(csvFile))
xmlData = []
xmlData.append('<?xml version="1.0"?>' + "\n\n")
# root top-level tag
xmlData.append('<root>' + "\n")
rowNum = 0
for row in csvData:
    xmlData.append('\t<dynamic-element default-language-id="it_IT" name="' + row[0] + '">' + '\n')
    xmlData.append('\t\t<dynamic-content language-id="it_IT"><![CDATA['+ row[1]+']]></dynamic-content>' + '\n')
    xmlData.append('\t</dynamic-element>' + '\n')            
    rowNum +=1
xmlData.append('</root>')
xmlContent = ''.join(xmlData)


entryId = Mytest.addEntry_('', '{"it_IT":"SBM sibam python API"}', '{"it_IT":"SBM sibam python API"}', 43591227, 0, xmlContent, '')
print ("addEntry_('', '{'it_IT':'SBM sibam python API'}', '{'it_IT':'SBM sibam python API'}', 43591227, 0, xmlContent, ''): \n\r" + str(entryId))
'''

