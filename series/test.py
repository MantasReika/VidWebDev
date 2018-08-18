import re

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


print(cleanEpisodeName("Game of Thrones S02E02 The Night Lands (1080p x265 10bit Joy).mkv.mp4", ['Game Of Thrones', "-", "(1080p x265 10bit Joy)"]))
