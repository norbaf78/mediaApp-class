"""
/***************************************************************************
Name                    : Ydam
Description          : 
Date                 : 2/Nov/2017/
copyright            : (C) 2011 by Ruggero Valentinotti
email                : valruggero@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import pandas
#import backoff
#import requests
import os
import json
#import time
import mediaApp

# =============================================================================
# endpoint = "http://multimedia.trentinonetwork.it"
# emailAddress = 'ruggero.valentinotti@provincia.tn.it'
# password = ''
# authentication = (emailAddress,password)
# companyId = 20154
# groupId = 2564504
# repositoryId = 0
# =============================================================================

class ws_ydam:
    def __init__(self, endpoint, emailAddress, password, companyId, groupId, repositoryId, folderId):
        self.instance = mediaApp.mediaApp(endpoint, emailAddress, password)
        self.instance.setCompanyId(companyId)
        self.instance.setGroupId(groupId)
        self.instance.setRepositoryId(repositoryId)
        self.instance.setFolderId(folderId) 

    def strip_accents(self, s):
        return s.encode()

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)

    def getNomeAsta(self, nameCsv,asta,data):
        fullpath=self.resolve(nameCsv)
        df_nomeasta=pandas.read_csv(fullpath,sep=";",dtype={'asta':str, 'nomeb0':str, 'nomeb1':str,'nomeb2':str,'nomecorso':str} )
        df_nomeasta = df_nomeasta.where((pandas.notnull(df_nomeasta)), '') # sostituisce NaN con ''
        nRighe=df_nomeasta.index[df_nomeasta["asta"]==str(asta)].tolist()
        riga=df_nomeasta.iloc[nRighe[0]]
        if riga['nomecorso'] == '': 
            riga['nomecorso']=riga['asta'] # metto il codice asta al posto del nome se il nome non esiste
        else:
            riga['nomecorso'] = riga['asta']+': ('+riga['nomecorso']+')'
        if riga['nomeb1'] != '':
            riga['nomeb1'] = 'BAC I: '+riga['nomeb1']
        if riga['nomeb2'] != '':
            riga['nomeb2'] = 'BAC II: '+riga['nomeb2']
        df_tmp=pandas.DataFrame(data=[[data]],index=["data"],dtype=str)
        riga=riga.append(df_tmp)
        riga=riga[0].tolist()
        riga = list(filter(None, riga))
        return riga
    
   
    def createYdamFolders(self, pathList, conta, parentFolderId, ydamConfig):        
        try:
            folder_list_request = self.instance.instancelistFoldersForParentFolder(parentFolderId, start = 0, end = 1000)
        except Exception as e: 
            print("Eccezione folder_add: " + str(e))
        folders_list = json.loads(folder_list_request.text)

        fTitles=[]
        fIds=[]
        for folder in folders_list:
            folderTitle = folder["titleCurrentValue"].strip()
            folderId = folder["folderId"]
            fTitles.append(folderTitle)
            fIds.append(folderId)

        df=pandas.DataFrame({'Ids': fIds, 'Titles': fTitles})
    
        print("conta:",conta)
        print(df)
        esiste=False
        if not df.empty:
            df_selected=df.loc[df['Titles'] == pathList[conta]]
            if len(df_selected.index)>0:
                esiste=True

        if conta<len(pathList):
            print("pathList[conta]=",pathList[conta])
            if esiste:            
                lastFolderId=df_selected.iloc[0]['Ids']
                conta += 1
                return self.createYdamFolders(pathList,conta,lastFolderId,ydamConfig)                
            else:               
                print ('\nadd subfolder for ',parentFolderId) 
                try:
                    folder_add_request = self.instance.addSubfolderForParent(parentFolderId, '{"it_IT":"' + pathList[conta] + '"}', '{"it_IT":"' + pathList[conta] + '"}', '')
                except Exception as e: 
                    print("Eccezione folder_add: " + str(e))
                folder = json.loads(folder_add_request.text)
                folderId = folder["folderId"]         
                print ('New folderId: ',folderId) 
                lastFolderId=folderId
                conta += 1
                return self.createYdamFolders(pathList,conta,lastFolderId,ydamConfig)
        else:
            print("fuori",conta,len(pathList))
            return parentFolderId


    def sendFileToYdam(self, folderId,fileName,Title,Description,ydamConfig):
        self.instance.setFolderId(folderId)
        try:
            entry_add_request = self.instance.addEntry('', '{"it_IT":"' + Title + '"}', '{"it_IT":"'+Description+'"}', '')
        except Exception as e:
            print("Eccezione entry_add: " + str(e))
        
        entry = json.loads(entry_add_request.text)
        entryId = entry["entryId"]
        try:
            file_add_request = self.instance.addFile(entryId,'true')
        except Exception as e: 
            print("Eccezione file_add: " + str(e))

        entry_file = json.loads(file_add_request.text)
        fileId = entry_file["fileId"]
        print ('upload content to file ',entry_file["fileId"]) 

        try:
            file_upload_request =  self.instance.uploadFile(fileId, fileName)
        except Exception as e: 
            print("Eccezione file_upload: "+str(e) + " " + str(fileName))






