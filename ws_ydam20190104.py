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
import backoff
import requests
import os
import pandas
import json
import time
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
        #print("DEBUG(Fabio): riga (0) " + str(riga)) 
        riga=riga[0].tolist()
        #print("DEBUG(Fabio): riga (1) " + str(riga)) 
        riga = list(filter(None, riga))
        #print("DEBUG(Fabio): riga (1) " + str(riga))
        return riga
    

#def entry_add(url, payload, authentication):
#    entry_add_request = requests.post(url, data=payload, auth=authentication,headers={"Connection": "close"})
#    return entry_add_request


#def file_add(url, payload, authentication):
#    file_add_request = requests.post(url, data=payload, auth=authentication,headers={"Connection": "close"})
#    return file_add_request


#def file_upload(url, payload,myfiles, authentication):
#    file_upload_request = requests.post(url, data=payload, files=myfiles, auth=authentication,headers={"Connection": "close"})
#    return file_upload_request


#def folder_add(url, payload, authentication):
#    folder_add_request = requests.post(url, params=payload, auth=authentication,headers={"Connection": "close"})
#    return folder_add_request


#def folder_list(url, payload, authentication):
#    folder_list_request = requests.get(url, params=payload, auth=authentication)
#    return folder_list_request


    
    def createYdamFolders(self, pathList, conta, parentFolderId, ydamConfig):        
#        authentication = (ydamConfig['user'],ydamConfig['password'])
#        folder_list_url = ydamConfig['endpoint']+"/api/jsonws/media-portlet.mediaapp/list-folders"
#        folder_list_payload = {
#                'groupId':ydamConfig['groupid'],
#                'repositoryId':ydamConfig['repositoryid'], 
#                'parentFolderId':parentFolderId, 
#                'start':0, 
#                'end':10000
#                }
        try:
#            folder_list_request = folder_list(folder_list_url, folder_list_payload, authentication)
            folder_list_request = self.instance.instancelistFoldersForParentFolder(parentFolderId, start = 0, end = 1000)
        except Exception as e: 
            print("Eccezione folder_add: "+str(e))
        #folder_list_request = requests.get(folder_list_url, params=folder_list_payload, auth=authentication)
        #print folder_list_request.text
        folders_list = json.loads(folder_list_request.text)

        fTitles=[]
        fIds=[]
        for folder in folders_list:
            folderTitle = folder["titleCurrentValue"].strip()
            folderId = folder["folderId"]
            fTitles.append(folderTitle)
            fIds.append(folderId)
            # print 'Folder: ',folderId," -> ",folderTitle
            #  print str("Folders count: "+str(len(folders_list)))

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
                # print(df_selected.iloc[0]['Ids'])
                lastFolderId=df_selected.iloc[0]['Ids']
                conta += 1
                return self.createYdamFolders(pathList,conta,lastFolderId,ydamConfig)                
            else:               
                print ('\nadd subfolder for ',parentFolderId) 
#                folder_add_url = ydamConfig['endpoint']+"/api/jsonws/media-portlet.mediaapp/add-folder"
#                folder_add_payload = {
#                        'companyId':ydamConfig['companyid'],
#                        'groupId':ydamConfig['groupid'],
#                        'repositoryId':ydamConfig['repositoryid'],
#                        'parentFolderId':parentFolderId,
#                        'titleMap':'{"it_IT":"'+pathList[conta]+'"}', #note: json is already serialized as string   
#                        'descriptionMap':'{"it_IT":"'+pathList[conta]+'"}', #note: json is already serialized as string      
#                        'layoutUuid':''
#                        }
                try:
#                    folder_add_request = folder_add(folder_add_url, folder_add_payload, authentication)
                    folder_add_request = self.instance.addSubfolderForParent(parentFolderId, '{"it_IT":"' + pathList[conta] + '"}', '{"it_IT":"' + pathList[conta] + '"}', '')
                    # print folder_add_request.text
                except Exception as e: 
                    print("Eccezione folder_add: "+str(e))
                    # print folder_add_request.text
                    # folder_add_request = requests.get(folder_add_url, params=folder_add_payload, auth=authentication)
                    # print folder_add_request.text
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
#        authentication = (ydamConfig['user'],ydamConfig['password'])
#        entry_add_url = ydamConfig['endpoint']+"/api/jsonws/media-portlet.mediaapp/add-entry"
#        entry_add_payload = {
#                'companyId':ydamConfig['companyid'],
#                'groupId':ydamConfig['groupid'],
#                'repositoryId':ydamConfig['repositoryid'],  
#                'folderId':folderId,
#                'type':'',
#                'titleMap':'{"it_IT":"'+Title+'"}', #note: json is already serialized as string
#                'descriptionMap':'{"it_IT":"'+Description+'"}', #note: json is already serialized as string
#                'layoutUuid':''
#                }
        try:
#            entry_add_request = entry_add(entry_add_url, entry_add_payload, authentication) 
            entry_add_request = self.instance.addEntry('', '{"it_IT":"' + Title + '"}', '{"it_IT":"'+Description+'"}', '')
            #print entry_add_request.text
        except Exception as e:
            print("Eccezione entry_add: "+str(e))
        
        entry = json.loads(entry_add_request.text)
        entryId = entry["entryId"]

        # add file as original
#        file_add_url = ydamConfig['endpoint']+"/api/jsonws/media-portlet.mediaapp/add-file"
#        file_add_payload = {
#                'groupId':ydamConfig['groupid'],
#                'repositoryId':ydamConfig['repositoryid'], 
#                'entryId':entry["entryId"],
#                'original':'true'
#                }
        try:
#            file_add_request = file_add(file_add_url, file_add_payload, authentication) 
            file_add_request = self.instance.addFile(entryId,'true')
            #print file_add_request.text
        except Exception as e: 
            print("Eccezione file_add: "+str(e))

        entry_file = json.loads(file_add_request.text)
        fileId = entry_file["fileId"]
        # upload file - NOTE: multipart upload is limited to 10M
        print ('upload content to file ',entry_file["fileId"]) 

#        file_upload_url = ydamConfig['endpoint']+"/api/jsonws/media-portlet.mediaapp/set-file-content"
#        file_upload_payload = {
#                'fileId':entry_file["fileId"],
#                'fileName':os.path.basename(fileName)
#            }
#        time.sleep(0.01)
#        file_upload_files = {'file': ("fileName", open(fileName, 'rb'))}
        try:
#            file_upload_request = file_upload(file_upload_url,file_upload_payload,file_upload_files, authentication) 
            file_upload_request =  self.instance.uploadFile(fileId, fileName)
        #print file_upload_request.text
        except Exception as e: 
            print("Eccezione file_upload: "+str(e)+" "++str(fileName))






