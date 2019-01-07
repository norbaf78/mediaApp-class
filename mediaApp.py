# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:22:42 2019

@author: fabio.roncato
"""

# use requests to provide HTTP communication
import requests
import json

class mediaApp:
    # set login data as basic authentication
    #endpoint = "http://multimedia.trentinonetwork.it"
    #emailAddress = "fabio.roncato@trilogis.it"#'demo@ymir.eu'
    #password = "Norbaf78_" # 'demo2.16'
    #authentication = (emailAddress,password)
    #companyId = 20154
    #groupId = 2564504 #20889
    #repositoryId = 0
    #folderId = 72728 #44384 #6323
    
    def __init__(self, endpoint, emailAddress, password):
        self.endpoint = endpoint
        self.emailAddress = emailAddress
        self.password = password
        self.authentication = (emailAddress,password)
        
#    def setEndpoint(self, endpoint):
#        self.endpoint = endpoint
#    def setEmailAddress(self, emailAddress):
#        self.emailAddress = emailAddress
#        self.authentication = (self.emailAddress,self.password)
#    def setPassword(self, password):
#        self.password = password
#        self.authentication = (self.emailAddress,self.password)
    def setCompanyId(self, companyId):
        self.companyId = companyId
    def setGroupId(self, groupId):
        self.groupId = groupId
    def setRepositoryId(self, repositoryId):
        self.repositoryId = repositoryId
    def setFolderId(self, folderId):
        self.folderId = folderId      
        
    def getEndpoint(self):
        return self.endpoint
    def getEmailAddress(self):
        return self.emailAddress
    def getPassword(self):
        return self.password
    def getCompanyId(self):
        return self.companyId
    def getGroupId(self):
        return self.groupId
    def getRepositoryId(self):
        return self.repositoryId
    def getFolderId(self):
        return self.folderId     

########################################################################################################  
#mediaApp entries 
########################################################################################################  
   
    # count entries for folder ("folderId" parameters is the ID of the folder and the returned value is the number of file present in it)
    def countEntryInFolder(self):
        #print ('\ncount entries for folder ',self.folderId)
        entry_count_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/count-entries"
        entry_count_payload = {
                'groupId':self.groupId,
                'repositoryId':self.repositoryId,
                'folderId':self.folderId
                }
        entry_count_request = requests.get(entry_count_url, params=entry_count_payload, auth=self.authentication)
        return (entry_count_request.text)    
    
    
    # list entries for folder page start(default 0)-end (default is 20) # 
    def listEntriesForFolder(self, start = 0, end = 20):
        #print ('\nlist entries for folder page 0-20')
        entry_list_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/list-entries"
        entry_list_payload = {
                'groupId':self.groupId,
                'repositoryId':self.repositoryId, 
                'folderId':self.folderId, 
                'start':start, 
                'end':end
                }
        entry_list_request = requests.get(entry_list_url, params=entry_list_payload, auth=self.authentication)
        return (entry_list_request.text)
    
    
    # add entry 
    def addEntry(self, typ_e, titleMap, descriptionMap, layoutUuid):
        #print ('\nadd entry')
        entry_add_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/add-entry"
        entry_add_payload = {
                'companyId':self.companyId,
                'groupId':self.groupId, 
                'repositoryId':self.repositoryId, 
                'folderId':self.folderId,
                'type':typ_e,
                'titleMap':titleMap,
                'descriptionMap':descriptionMap,  
                'layoutUuid':layoutUuid
                }
        entry_add_request = requests.post(entry_add_url, data=entry_add_payload, auth=self.authentication)
        #print (entry_add_request.text)
        entry = json.loads(entry_add_request.text)
        entryId = entry["entryId"]
        return (entryId)
    
    # get entry 
    def getEntry(self, entryId):
        #print ('\nget entry ',self.entryId)
        entry_get_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/get-entry"
        entry_get_payload = {
                'entryId': entryId
                }
        entry_get_request = requests.get(entry_get_url, params=entry_get_payload, auth=self.authentication)
        return (entry_get_request.text)
     
    
########################################################################################################  
#mediaApp vocabularies 
########################################################################################################        
    # count entries for folder
    def countEntriesForVocabulary(self, vocabularyId):
        #print ('\ncount entries for vocabulary ',vocabularyId)
        category_count_url = self.endpoint+"/api/jsonws/assetcategory/get-vocabulary-categories-count"
        category_count_payload = {
                'groupId':self.groupId,
                'vocabularyId':vocabularyId
                }
        category_count_request = requests.get(category_count_url, params=category_count_payload, auth=self.authentication)
        return (category_count_request.text)
    
    # list categories for vocabulary page start(default 0)-end (default is 20)
    def listCategoriesForVocabulary(self, vocabularyId, start = 0, end = 20):    
        #print ('\nlist categories for vocabulary page 0-20')
        category_list_url = self.endpoint+"/api/jsonws/assetcategory/get-vocabulary-categories"
        category_list_payload = {
                'groupId':self.groupId,
                'vocabularyId':vocabularyId,
                '-obc':'',  #empty orderByComparator
                'start':start, 
                'end':end
                }
        category_list_request = requests.get(category_list_url, params=category_list_payload, auth=self.authentication)
        return (category_list_request.text)  

    # add category
    def addCategory(self, vocabularyId, parentCategoryId, titleMap, descriptionMap, categoryProperties): 
        #print ('\nadd category')
        category_add_url = self.endpoint+"/api/jsonws/assetcategory/add-category"
        category_add_payload = {
                'vocabularyId':vocabularyId,
                'parentCategoryId':parentCategoryId, # id for parent in tree, 0 is root 
                'titleMap':titleMap, 
                'descriptionMap':descriptionMap,
                '-categoryProperties':categoryProperties
                }
        category_add_request = requests.post(category_add_url, data=category_add_payload, auth=self.authentication)
        #print (category_add_request.text)
        category = json.loads(category_add_request.text)
        categoryId = category["categoryId"]
        return (categoryId)    
    
    # get category 
    def getCategory(self, categoryId):
        #print ('\nget category ',categoryId)
        category_get_url = self.endpoint+"/api/jsonws/assetcategory/get-category"
        category_get_payload = {
                'categoryId': categoryId
                }
        category_get_request = requests.get(category_get_url, params=category_get_payload, auth=self.authentication)
        return (category_get_request.text)
    
    
########################################################################################################  
#mediaApp upload 
########################################################################################################      
#    # add entry 
#    def addEntry(self, typ_e, titleMap, descriptionMap, layoutUuid):
#        #print ('\nadd entry')
#        entry_add_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/add-entry"
#        entry_add_payload = {
#                'companyId':self.companyId,
#                'groupId':self.groupId, 
#                'repositoryId':self.repositoryId, 
#                'folderId':self.folderId,
#                'type':typ_e,
#                'titleMap':titleMap, 
#                'descriptionMap':descriptionMap, 
#                'layoutUuid':layoutUuid
#                }
#        entry_add_request = requests.post(entry_add_url, data=entry_add_payload, auth=self.authentication)
#        #print (entry_add_request.text)
#        entry = json.loads(entry_add_request.text)
#        entryId = entry["entryId"]
#        return (entryId)
    
    # add file as original
    def addFile(self,entryId, original):
        #print ('\nadd file as original to entry ',entry["entryId"])
        file_add_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/add-file"
        file_add_payload = {
                'groupId':self.groupId, 
                'repositoryId':self.repositoryId, 
                'entryId':entryId,
                'original':original # original = "true" or "false"
                }
        file_add_request = requests.post(file_add_url, data=file_add_payload, auth=self.authentication)
        #print (file_add_request.text)
        entry_file = json.loads(file_add_request.text)
        fileId = entry_file["fileId"]
        return (fileId)

    # upload file - NOTE: multipart upload is limited to 10M
    def uploadFile(self, fileId, fileNameString):
        #print ('\nupload content to file ',entry_file["fileId"])
        fileName = fileNameString
        file_upload_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/set-file-content"
        file_upload_payload = {
                'fileId':fileId,
                'fileName':fileName
                }
        file_upload_files = {'file': (fileName, open(fileName, 'rb'))}
        file_upload_request = requests.post(file_upload_url, data=file_upload_payload, files=file_upload_files, auth=self.authentication)
        return (file_upload_request.text)

########################################################################################################  
#mediaApp download 
########################################################################################################   
    # list files for entry
    def listFilesForEntry(self, entryId):
        #print ('\nlist files for ',entryId)
        file_list_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/list-files"
        file_list_payload = {
                'entryId':entryId
                }
        file_list_request = requests.get(file_list_url, params=file_list_payload, auth=self.authentication)
        #print (file_list_request.text)
        files = json.loads(file_list_request.text)
        return (files)  # return (file_list_request.text)
             
    # download original if found
    def downloadOriginalIfFound(self, files, fileId):
        original = None
        for f in files:
            if f["original"] == True:
                original = f    

        if original is not None:
            fileId = original["fileId"]
            #print ('\noriginal file id',fileId)
            file_get_url = self.endpoint+"/api/jsonws/media-portlet.fileapp/get-download-url"
            file_get_payload = {
                    'fileId':fileId
                    }
            file_get_request = requests.get(file_get_url, params=file_get_payload, auth=self.authentication)
            #print (file_get_request.text)
            downloadUrl = self.endpoint+file_get_request.text.strip('"')
            return (downloadUrl)
        else:
            return None
   

########################################################################################################  
#mediaApp folders 
########################################################################################################       
    # count folders for parentFolder
    def countFoldersForParentFolder(self, parentFolderId):
        #print ('\ncount folders for folder ',parentFolderId)
        folder_count_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/count-folders"
        folder_count_payload = {
                'groupId':self.groupId,
                'repositoryId':self.repositoryId,
                'parentFolderId':parentFolderId
                }
        folder_count_request = requests.get(folder_count_url, params=folder_count_payload, auth=self.authentication)
        return (folder_count_request.text)


    # list folders for parentFolder page 0-20
    def listFoldersForParentFolder(self, parentFolderId, start = 0, end = 20):    
        #print ('\nlist folders for parentFolder page 0-20')
        folder_list_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/list-folders"
        folder_list_payload = {
                'groupId':self.groupId,
                'repositoryId':self.repositoryId, 
                'parentFolderId':parentFolderId, 
                'start':start, 
                'end':end
                }
        folder_list_request = requests.get(folder_list_url, params=folder_list_payload, auth=self.authentication)
        return (folder_list_request)


    # add subfolder for parent
    def addSubfolderForParent(self, parentFolderId, titleMap, descriptionMap, layoutUuid):
        #print ('\nadd subfolder for ',parentFolderId)
        folder_add_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/add-folder"
        folder_add_payload = {
                'companyId':self.companyId,
                'groupId':self.groupId, 
                'repositoryId':self.repositoryId, 
                'parentFolderId':parentFolderId,
                'titleMap':titleMap,
                'descriptionMap':descriptionMap, 
                'layoutUuid':layoutUuid
                }
        folder_add_request = requests.get(folder_add_url, params=folder_add_payload, auth=self.authentication)
        #print (folder_add_request.text)
        folder = json.loads(folder_add_request.text)
        folderId = folder["folderId"]
        return (folderId)

    # get folder
    def getFolder(self):
        #print ('\nget folder ',self.folderId)
        folder_get_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/get-folder"
        folder_get_payload = {
                'folderId': self.folderId
                }
        folder_get_request = requests.get(folder_get_url, params=folder_get_payload, auth=self.authentication)
        return (folder_get_request.text) 
    
    
########################################################################################################  
#mediaApp entries_content 
########################################################################################################     
    # add entry
    def addEntry_(self, typ_e, titleMap, descriptionMap, structureId, templateId, xmlContent, layoutUuid):
        #print ('\nadd entry')
        entry_add_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/add-entry"
        entry_add_payload = {
                'companyId':self.companyId,
                'groupId':self.groupId, 
                'repositoryId':self.repositoryId, 
                'folderId':self.folderId,
                'type':typ_e,
                'titleMap':titleMap, #note: json is already serialized as string
                'descriptionMap':descriptionMap, #note: json is already serialized as string   
                'structureId': structureId,
                'templateId' : templateId,
                'content' : xmlContent,
                'layoutUuid':layoutUuid
                }
        entry_add_request = requests.post(entry_add_url, data=entry_add_payload, auth=self.authentication)
        #print (entry_add_request.text)
        entry = json.loads(entry_add_request.text)
        entryId = entry["entryId"]
        return (entryId)

#    # get entry 
#    def getEntry(self, entryId):
#        #print ('\nget entry ',entryId)
#        entry_get_url = self.endpoint+"/api/jsonws/media-portlet.mediaapp/get-entry"
#        entry_get_payload = {
#                'entryId': entryId
#                }
#        entry_get_request = requests.get(entry_get_url, params=entry_get_payload, auth=self.authentication)
#        return (entry_get_request.text)