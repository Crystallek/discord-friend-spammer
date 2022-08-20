import deep_translator
import requests
import colorama
import json
import time
import os

start = time.time()
channelSave = 0
os.chdir(os.path.dirname(__file__))
colorama.init(convert=True)

print(f"""{colorama.Fore.BLUE}  _____ _____  _____  _____ ____  _____  _____     ______ _____  _____ ______ _   _ _____      _____ _____        __  __ __  __ ______ _____  
 |  __ \_   _|/ ____|/ ____/ __ \|  __ \|  __ \   |  ____|  __ \|_   _|  ____| \ | |  __ \    / ____|  __ \ /\   |  \/  |  \/  |  ____|  __ \ 
 | |  | || | | (___ | |   | |  | | |__) | |  | |  | |__  | |__) | | | | |__  |  \| | |  | |  | (___ | |__) /  \  | \  / | \  / | |__  | |__) |
 | |  | || |  \___ \| |   | |  | |  _  /| |  | |  |  __| |  _  /  | | |  __| | . ` | |  | |   \___ \|  ___/ /\ \ | |\/| | |\/| |  __| |  _  / 
 | |__| || |_ ____) | |___| |__| | | \ \| |__| |  | |    | | \ \ _| |_| |____| |\  | |__| |   ____) | |  / ____ \| |  | | |  | | |____| | \ \ 
 |_____/_____|_____/ \_____\____/|_|  \_\_____/   |_|    |_|  \_\_____|______|_| \_|_____/   |_____/|_| /_/    \_\_|  |_|_|  |_|______|_|  \_\ {colorama.Fore.RESET}\n\nBy Crystallek#3348""")

try:
    with open("data/data.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        tokenDiscord = lines[0].removeprefix("token=").replace("\n", "")
        groupDmName = lines[1].removeprefix("groupname=").replace("\n", "")
        targetLang = lines[2].removeprefix("targetlang=").replace("\n", "") 
        friendsToSpam = lines[3].removeprefix("friendstospam=").replace("\n", "").replace(" ", "").replace("\"", "").split(",")
        repeats = lines[4].removeprefix("repeats=").replace("\n", "")
        leaveWhenRepeatsAreDone = lines[5].removeprefix("leavewhenrepeatsdone=").replace("\n", "")
        f.close()
    print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Settings successfully loaded.\n" + "="*50 + f"\nToken: {tokenDiscord}\nGroup Name: {groupDmName}\nLanguage: {targetLang}\nFriends to spam: {friendsToSpam}\nRepeats: {repeats}\nLeave when repeats are done: {leaveWhenRepeatsAreDone.capitalize()}\n" + "="*50)
except:
    input(f"\n{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} File cannot be read. Press any key to exit the program... ")
    exit()

tokenTrivia = "824c28fc3cmshfa0dfba9bd5ff5bp1bdfbfjsnb90fc16d0447"
headersDiscordData = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36',
    'Authorization': tokenDiscord,
    'Content-Type': 'application/json'
}

headersFactsData = {
    "X-RapidAPI-Key": tokenTrivia,
    "X-RapidAPI-Host": "trivia-by-api-ninjas.p.rapidapi.com"
}

def createGroupDM():
    global friendsToSpam
    global channelSave
    
    if len(friendsToSpam) > 9:
        input("{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} You can spam only 9 friends at the time (for now).")
        exit()
    else:
        jsonDiscordData = {"recipients": friendsToSpam}
        rDis = requests.post(f"https://discord.com/api/v9/users/@me/channels", headers=headersDiscordData, json=jsonDiscordData)
        if rDis.status_code == 401:
            input(f"\n{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Unauthorized access, check your token. Press any key to exit the program... ") 
            exit()
        elif rDis.status_code == 400:
            input(f"\n{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Invalid recipients. Press any key to exit the program... ") 
            exit()
        else:
            jDis = json.loads(rDis.text)
            if "id" in jDis:
                print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Group successfully created.")

            try:
                return jDis["id"]
            except:
                return channelSave

def changeGroupDMName(channel):
    if channel == 0:
        input("{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Rate limited. Wait a few minutes and try again.")
        exit()

    jsonDiscordData = {"name": groupDmName}
    r = requests.patch(f"https://discord.com/api/v9/channels/{channel}", headers=headersDiscordData, json=jsonDiscordData)
    if r.status_code != 200:
        print(f"{colorama.Fore.YELLOW}[WARN]{colorama.Fore.RESET} Group could not be renamed.", r.status_code)
    else:
        print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Group has been renamed to {groupDmName}!")
        
def spam(channel, repeats):
    global channelSave
    channelSave = channel
    for x in range(repeats):
        rTrivia = requests.get("https://trivia-by-api-ninjas.p.rapidapi.com/v1/trivia", headers=headersFactsData)
        jTrivia = json.loads(rTrivia.text)

        if targetLang.lower() != "none":
            try:
                translate = jTrivia[0]['question'] + "|||" + jTrivia[0]['answer']
                translation = deep_translator.GoogleTranslator(source='auto', target=targetLang.lower()).translate(translate)
                question, answer = translation.split('|||')
            except Exception as e:
                print(f"{colorama.Fore.YELLOW}[WARN]{colorama.Fore.RESET} Could not translate. {e}")
                question = jTrivia[0]['question']
                answer = jTrivia[0]['answer']
        else:
            question = jTrivia[0]['question']
            answer = jTrivia[0]['answer']
        jsonDiscordData = {"content": f"{question}? {answer}! @everyone"}

        rDis = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=headersDiscordData, json=jsonDiscordData)
        jDis = json.loads(rDis.text)

        print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Message sent: {question}? {answer}!")

        if rDis.status_code == 429:
            timeToStop = float(jDis["retry_after"])
            print(f"{colorama.Fore.YELLOW}[WARN]{colorama.Fore.RESET} Rate limited for {timeToStop} seconds.")
            time.sleep(timeToStop)

while True:
    if channelSave != 0 and leaveWhenRepeatsAreDone.lower() == "true":
        requests.delete(f"https://discord.com/api/v9/channels/{channelSave}?silent=true", headers=headersDiscordData, json={"silent": "true"})
        print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Successfully left the group.")
    channel = createGroupDM()
    changeGroupDMName(channel)
    spam(channel, int(repeats))
