import requests
import json
import re
import csv
## r = requests.get(apiAccInfo % (login, key))
## r = requests.get(downloadTicket % (fileId, login, key))
##  r = requests.get(downloadLink % (fileId, ticket, captchaResponse))

class metaData:
    def __init__(self, fileName):
        self.namesDict = {}
        with open(fileName, mode='r') as csvFile:
            csvReader = csv.DictReader(csvFile, delimiter='|')
            for row in csvReader:
                self.namesDict[row['NAME']] = row

    def setCurrentMovie(self, movieName):
        self.name = movieName

    def getName(self):
        try:
            return self.namesDict[self.name]['NAME']
        except KeyError:
            return ""

    def getReleaseYear(self):
        try:
            return int(self.namesDict[self.name]['RELEASED'])
        except (KeyError, ValueError) as e:
            return 0

    def getFinishYear(self):
        try:
            return int(self.namesDict[self.name]['FINISHED'])
        except (KeyError, ValueError) as e:
            return 0

    def getImdb(self):
        try:
            return float(self.namesDict[self.name]['IMDB'])
        except KeyError:
            return 0
        
    def getImage(self):
        try:
            return self.namesDict[self.name]['IMAGE']
        except KeyError:
            return ""

    def getTrailer(self):
        try:
            return self.namesDict[self.name]['TRAILER']
        except KeyError:
            return ""

    def getGenres(self):
        try:
            return self.namesDict[self.name]['GENRES']
        except KeyError:
            return ""

    def getCleanNameTextParts(self):
        try:
            return self.namesDict[self.name]['CLEAN'].split(';')
        except KeyError:
            return []
	
    def getCleanNameRegexParts(self):
        try:
            return self.namesDict[self.name]['CLEANRE'].split(';')
        except KeyError:
            return []

    def getReplaceNameParts(self):
        try:
            return self.namesDict[self.name]['REPLACE'].split(';')
        except KeyError:
            return []			

    def getDescription(self):
        try:
            return self.namesDict[self.name]['DESC']
        except KeyError:
            return ""

			
def main():
    ## This function is not active and is irrelevant for functionality, its for testing only       
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
    name = 'Game.Of.Thrones.S07E01.Dragonstone.720p.WEB-DL.Re-encode.mp4'
    aname = "Game Of Thrones S01E01 Winter Is Coming.mkv.mp4"
    textRemove = ["(1080p x265 10bit Joy)", '720p.WEB-DL.Re-encode.mp4', '.mkv.mp4', 'Game.Of.Thrones']
    regexRemove = [r'(S|Season |Season-|Season|Book )[0-9]+.(E|Episode |Episode-|Episode|Chapter )[0-9]+|(E|Episode |Episode-|Episode|Chapter )[0-9]+']
    textReplace = [['.', ' ']]
    print(cleanEpisodeName(name, textRemove, regexRemove, textReplace))
			
def getMovieMetaData(metaData, name):
    return metaData[name]    

def loadMetaData(fileName='OpenLoadUpdateDatabase.csv'):
    namesDict = {}
    with open(fileName, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter='|')
        for row in csvReader:
            namesDict[row['NAME']] = row
    return namesDict

def getEpisodeThumbnail(name):
    pass

def cleanName(name, textRemove=[], regexRemove=[], textReplace=[]):
    ##print("\nNAME: %s\nTEXT_REMOVE: %s'\nREGEX_REMOVE: %s\nTEXT_REPLACE: %s" % (name, textRemove, regexRemove, textReplace))
    print("\n'%s'" % name)
    rawName = name
    removeItems = textRemove
    for reRemove in regexRemove:
        try:
            removeItems.append(re.compile(reRemove, re.IGNORECASE).search(name).group(0))
        except AttributeError:
            pass
        
    for i in removeItems:
        rr = re.compile(re.escape(i), re.IGNORECASE)
        name = rr.sub('', name)
        name = name.replace(i, "")

    for old in textReplace:
        if old != "":
            name = name.replace(old, " ")
    name = name.strip()
    if name == '':
        episodeNr = "Episode %s" % (getEpisodeNumber(rawName))
        print("'%s'" % episodeNr)
        return episodeNr
    print("'%s'" % name)
    return name

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
    r = re.compile(r'(E|Episode +|Episode-|Episode|Chapter +)[0-9]+', re.IGNORECASE).search(episodeName)
    assert None != r, "getEpisodeNumber failed 'assert None != r', episodeName = %s" % episodeName
    return int(re.compile(r'([0-9]+)').search(r.group(0)).group(0))

def getSeasonNumber(seasonName):
    r = re.compile(r'(S|Season +|Season-|Season|Book +)[0-9]+', re.IGNORECASE).search(seasonName)
    assert None != r, "getSeasonNumber failed 'assert None != r', seasonName = %s" % seasonName
    return int(re.compile(r'([0-9]+)').search(r.group(0)).group(0))

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


