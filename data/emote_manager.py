import pathlib, requests, sqlite3

parentpath = pathlib.Path(__file__).parent
emotespath = parentpath / "emotes"
downloadspath = parentpath / "emote downloads"
databasepath = parentpath / "emotes.db"
    
# downloads and writes file
def downloadFromUrl(filename, url):
    filepath = str(parentpath / "emote downloads" / filename)
    print(filepath)
    download = requests.get(url)
    
    with open(filepath, 'wb') as f:
        f.write(download.content)

# renames file to emote name
def processDiscordAttachment(attachment, emote_name):
    url = attachment.url
    
    # verify name is not taken
    
    
    filetype = url.split('.')[-1]
    # verify filetype is acceptable
    if filetype in ["png", "jpg"]:
        downloadFromUrl(f'{emote_name}.{filetype}', url)
        

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

def main():
    # create emote directories if does not exist
    emotespath.mkdir(exist_ok=True)
    downloadspath.mkdir(exist_ok=True)
    # create SQL database if does not exist
    try:
        open(databasepath, "x").close()
    except FileExistsError as e:
        print(e)
    # create table in database
    database = sqlite3.connect(databasepath)
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS emotes("
            "name text UNIQUE"
            ")"
    )
    database.commit()
    database.close()
    return

if __name__ == "__main__":
    main()
    downloadFromUrl("belo.png", "https://azurlane.koumakan.jp/w/images/thumb/c/c2/Sovetskaya_Belorussiya.png/900px-Sovetskaya_Belorussiya.png")
    downloadFromUrl("2blewd.png", "https://cdn.discordapp.com/attachments/725343534437105719/845871904694730752/2Blewd.png")
    print(isNameTaken("test"))
    print(isNameTaken("no test"))