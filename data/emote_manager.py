import pathlib, requests, sqlite3, numpy
from PIL import Image
import imagehash

parentpath = pathlib.Path(__file__).parent
emotespath = parentpath / "emotes"
downloadspath = parentpath / "emote downloads"
databasepath = parentpath / "emotes.db"

# returns values depending on success or errors
# 0: success
# 1: name is taken
# 2: file is not supported
def processDiscordAttachment(attachment, emote_name):
    # verify name is not taken
    if isNameTaken(emote_name):
        return 1
    url = attachment.url
    filetype = url.split('.')[-1]
    # verify filetype is acceptable
    if filetype in ["png", "jpg"]:
        # download to local downloads folder
        downloadFromUrl(f'{emote_name}.{filetype}', url)
    else:
        return 2
    # add to database and emote folder
    storeEmote(emote_name,filetype)
    return 0
        
# downloads and writes file
def downloadFromUrl(filename, url):
    filepath = parentpath / "emote downloads" / filename
    download = requests.get(url)
    
    with filepath.open('wb') as f:
        f.write(download.content)

def isNameTaken(emote_name):
    database = sqlite3.connect(databasepath)
    cursor = database.cursor()
    cursor.execute(
        "SELECT name FROM emotes WHERE name == (?)", (emote_name, )
    )
    rows = cursor.fetchall()
    database.commit()
    database.close()
    return len(rows) > 0

# moves emote from downloads to emotes folder
# adds entry in database with name and filetype
def storeEmote(emote_name, filetype):
    currentlocation = downloadspath / f'{emote_name}.{filetype}'
    if filetype in ["png", "jpg"]:
        hashstring = averagehashImage(currentlocation)
        if checkForSimilar(hashstring):
            return 3
        addToDatabase(emote_name, filetype, hashstring)
    # move to emote folder
    targetlocation = emotespath / f'{emote_name}.{filetype}'
    currentlocation.rename(targetlocation)
    return

def addToDatabase(emote_name, filetype, hashstring):
    database = sqlite3.connect(databasepath)
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO emotes VALUES (?, ?, ?)", (emote_name, filetype, hashstring, )
    )
    database.commit()
    database.close()

def averagehashImage(filepath):
    hash = imagehash.average_hash(Image.open(str(filepath)))
    return str(hash)

def checkForSimilar(hashstring):
    database = sqlite3.connect(databasepath)
    cursor = database.cursor()
    cursor.execute(
        "SELECT hashstring FROM emotes"
    )
    rows = cursor.fetchall()
    database.commit()
    database.close()

    for row in rows:
        print(row[0], type(row[0]))
        if compareFromImageHashString(hashstring, row[0]) < 0:
            return True
    
    return False

def compareFromImageHashString(hashString1, hashString2):
    binarray1 = createNumpyArrayFromString(hashString1)
    binarray2 = createNumpyArrayFromString(hashString2)
    return numpy.count_nonzero(binarray1 != binarray2)

# creates numpy array for hash comparision from hash string
def createNumpyArrayFromString(hashString, expectedlength=64):
    print(hashString)
    binstring = f'{int(hashString,16):b}'
    # accounting for binary conversion losing zeros
    if len(binstring) < expectedlength:
        zerostring = "0" * abs(expectedlength - len(binstring))
        binstring = zerostring + binstring
    return numpy.array([int(char) for char in binstring])

def main():
    # create emote directories if does not exist
    emotespath.mkdir(exist_ok=True)
    downloadspath.mkdir(exist_ok=True)
    # create SQL database if does not exist
    try:
        databasepath.open("x").close()
    except FileExistsError as e:
        print(e)
    # create table in database
    database = sqlite3.connect(databasepath)
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS emotes("
            "name text UNIQUE,"
            "filetype text,"
            "hashstring text"
            ")"
    )
    database.commit()
    database.close()
    return

if __name__ == "__main__":
    print("Setting Up Directories and Database")
    main()
    
    print("Downloading Example Images")
    downloadFromUrl("belo.png", "https://azurlane.koumakan.jp/w/images/thumb/c/c2/Sovetskaya_Belorussiya.png/900px-Sovetskaya_Belorussiya.png")
    downloadFromUrl("2blewd.png", "https://cdn.discordapp.com/attachments/725343534437105719/845871904694730752/2Blewd.png")
    
    print("Testing Name Verifier")
    print(isNameTaken("belo"))
    print(isNameTaken("2blewd"))
    
    print("Testing Hash Comparision")
    hash1 = imagehash.average_hash(Image.open(str(downloadspath / "2blewd.png")))
    print(hash1)
    hash2 = imagehash.average_hash(Image.open(str(downloadspath / "belo.png")))
    print(hash2)
    print(compareFromImageHashString(str(hash1),str(hash2)))

    print("Testing Emote Relocation and Database Insertion")
    storeEmote("belo", "png")