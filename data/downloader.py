

import pathlib, requests
parentpath = pathlib.Path(__file__).parent
emotespath = parentpath / "emotes"

def downloadFromUrl(filename, url):
    filepath = str(emotespath / filename)
    print(filepath)
    download = requests.get(url)
    
    with open(filepath, 'wb') as f:
        f.write(download.content)

if __name__ == "__main__":
    print(str(emotespath))
    downloadFromUrl("belo.png", "https://azurlane.koumakan.jp/w/images/thumb/c/c2/Sovetskaya_Belorussiya.png/900px-Sovetskaya_Belorussiya.png")
    downloadFromUrl("2blewd.png", "https://cdn.discordapp.com/attachments/725343534437105719/845871904694730752/2Blewd.png")