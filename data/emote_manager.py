

import pathlib, requests
parentpath = pathlib.Path(__file__).parent

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
    return

if __name__ == "__main__":
    downloadFromUrl("belo.png", "https://azurlane.koumakan.jp/w/images/thumb/c/c2/Sovetskaya_Belorussiya.png/900px-Sovetskaya_Belorussiya.png")
    downloadFromUrl("2blewd.png", "https://cdn.discordapp.com/attachments/725343534437105719/845871904694730752/2Blewd.png")