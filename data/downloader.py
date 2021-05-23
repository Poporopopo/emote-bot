

import pathlib, requests
parentpath = pathlib.Path(__file__).parent
emotespath = parentpath / "emotes"

# downloads and writes file
def downloadFromUrl(filename, url):
    filepath = str(emotespath / filename)
    print(filepath)
    download = requests.get(url)
    
    with open(filepath, 'wb') as f:
        f.write(download.content)

# reads the url and determines filetype
# renames file to emote name
def processDiscordAttachment(attachment, emote_name):
    url = attachment.url
    filetype = url.split('.')[-1]
    # verify filetype is acceptable
    if filetype in ["png", "jpg"]:
        downloadFromUrl(f'{emote_name}.{filetype}', url)

if __name__ == "__main__":
    print(str(emotespath))
    downloadFromUrl("belo.png", "https://azurlane.koumakan.jp/w/images/thumb/c/c2/Sovetskaya_Belorussiya.png/900px-Sovetskaya_Belorussiya.png")
    downloadFromUrl("2blewd.png", "https://cdn.discordapp.com/attachments/725343534437105719/845871904694730752/2Blewd.png")