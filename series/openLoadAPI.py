import requests
import json
import re

## r = requests.get(apiAccInfo % (login, key))
## r = requests.get(downloadTicket % (fileId, login, key))
##  r = requests.get(downloadLink % (fileId, ticket, captchaResponse))

def main():
    login   = "08af2f7ed0f90e4c"
    key     = "Vt9iQlnS"
    fileId  = "1"
    folderId = "5991313" # Season 1getFolderFoldersById
    folder2 = "5991327"
    ticket  = "1~08af2f7ed0f90e4c~1533973649~n~~1~a1p0kqVLOJNfl3Qb"
    captchaResponse = "1"
    apiAccInfo = "https://api.openload.co/1/account/info?login=%s&key=%s"
    downloadTicket = "https://api.openload.co/1/file/dlticket?file=%s&login=%s&key=%s"
    downloadLink = "https://api.openload.co/1/file/dl?file=%s&ticket=%s&captcha_response=%s"

    """
        rootFolderList = "https://api.openload.co/1/file/listfolder?login=%s&key=%s"
        folderList = "https://api.openload.co/1/file/listfolder?login=%s&key=%s&folder=%s"

        r = requests.get(folderList % (login, key, folderId))
        jsonObj =  json.loads(r.text)
        print(r)
        print(json.dumps(jsonObj, indent=4))
    """
    #foldersJsonObj = getFolderFilesById(login, key, folder2)
    #print(json.dumps(foldersJsonObj, indent=4))
    seasonNr = getSeasonNumber('S01')
    print("%s" % seasonNr)
    #episodes = getFolderFilesById(login, key, folderId)

##    for episode in episodes:
##        try:
##            episodeNumber = int(getEpisodeNumber(episode['name'])[1:])
##        except:
##            continue

def getEpisodeThumbnail(name):
    pass

def cleanEpisodeName(name, customRemove=[]):
    try:
        episodeNrPart = re.compile(r'S[0-9]+E[0-9]+', re.IGNORECASE).search(name).group(0)
    except AttributeError:
        pass
    removeItems = [".mkv", ".mp4"] + customRemove + [episodeNrPart]
    for i in removeItems:
        rr = re.compile(re.escape(i), re.IGNORECASE)
        name = rr.sub('', name)
        name = name.replace(i, "")
    return name.strip()

def getFolderIdByName(login, key, folderName, folderId=""):        
    if folderId == "":
        folders = getRootFolders(login, key)
    else:
        folders = getFolderFoldersById(loging, key, folderId)

    for folder in folders:
        if folder['name'] == folderName:
            return folder['id']

def getEmbededLinkFromRawLink(link):
    return link.replace('f', 'embed', 1)
            
def getEpisodeNumber(episodeName):
    r = re.compile(r'E[0-9]+', re.IGNORECASE).search(episodeName)
    assert None != r, "getEpisodeNumber failed 'assert None != r', episodeName = %s" % episodeName
    return int(r.group(0)[1:])

def getSeasonNumber(seasonName):
    r = re.compile(r'S[0-9]+', re.IGNORECASE).search(seasonName)
    assert None != r, "getSeasonNumber failed 'assert None != r', seasonName = %s" % seasonName
    return int(r.group(0)[1:])

def getRootFolders(login, key):
    folderList = "https://api.openload.co/1/file/listfolder?login=%s&key=%s"
    r = requests.get(folderList % (login, key))
    jsonObj =  json.loads(r.text)   
    assert  jsonObj['status'] == 200, "getRootFolders failed 'assert jsonObj['status'] == 200'; \nrequest status = %s, jsonObj = %s " % (r, jsonObj)
    return jsonObj['result']['folders']
    
def getFolderFoldersById(login, key, folderId):
    folderList = "https://api.openload.co/1/file/listfolder?login=%s&key=%s&folder=%s"
    r = requests.get(folderList % (login, key, folderId))
    jsonObj =  json.loads(r.text)   
    assert  jsonObj['status'] == 200, "getFolderFoldersById failed 'assert jsonObj['status'] == 200'; \nrequest status = %s, jsonObj = %s " % (r, jsonObj)
    return jsonObj['result']['folders']

def getFolderFilesById(login, key, folderId):
    folderList = "https://api.openload.co/1/file/listfolder?login=%s&key=%s&folder=%s"
    r = requests.get(folderList % (login, key, folderId))
    jsonObj =  json.loads(r.text)   
    assert  jsonObj['status'] == 200, "getFolderFilesById failed 'assert jsonObj['status'] == 200'; \nrequest status = %s, jsonObj = %s " % (r, jsonObj)
    return jsonObj['result']['files']

if __name__ == "__main__":
    main()


