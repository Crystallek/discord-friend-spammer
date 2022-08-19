import requests, json, time, deep_translator

with open("data/data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    tokenDiscord = lines[2].removeprefix("token=").replace("\n", "")
    groupDmName = lines[3].removeprefix("groupname=").replace("\n", "")
    targetLang = lines[4].removeprefix("targetlang=").replace("\n", "") # insert ur token here (bot tokens wont work)
    friendsToSpam = lines[5].removeprefix("friendstospam=").replace("\n", "").replace(" ", "").replace("\"", "").split(",")
    f.close()

print(targetLang, type(targetLang))
print(groupDmName)
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
    if len(friendsToSpam) > 9:
        print("You can spam only 9 friends at the time (for now).")
        exit()
    else:
        jsonDiscordData = {"recipients": friendsToSpam}
        print(friendsToSpam)
        rDis = requests.post(f"https://discord.com/api/v9/users/@me/channels", headers=headersDiscordData, json=jsonDiscordData)
        jDis = json.loads(rDis.text)
        print(jDis)
        return jDis["id"]

def changeGroupDMName(channel):
    jsonDiscordData = {"name": groupDmName}
    requests.patch(f"https://discord.com/api/v9/channels/{channel}", headers=headersDiscordData, json=jsonDiscordData)

run = True
def spam(channel):
    global run
    while run:
        rTrivia = requests.get("https://trivia-by-api-ninjas.p.rapidapi.com/v1/trivia", headers=headersFactsData)
        jTrivia = json.loads(rTrivia.text)

        if targetLang.lower() != "none":
            try:
                question = deep_translator.GoogleTranslator(source='auto', target="de").translate(jTrivia[0]['question'])
                answer = deep_translator.GoogleTranslator(source='auto', target="de").translate(jTrivia[0]['answer'])
            except Exception as e:
                print(f"Could not translate. {e}")
                question = jTrivia[0]['question']
                answer = jTrivia[0]['answer']
        else:
            question = jTrivia[0]['question']
            answer = jTrivia[0]['answer']
        jsonDiscordData = {"content": f"{question}? {answer}! @everyone"}

        rDis = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=headersDiscordData, json=jsonDiscordData)
        jDis = json.loads(rDis.text)

        if rDis.status_code == 429:
            timeToStop = float(jDis["retry_after"])
            print(f"Rate limited for {timeToStop} seconds.")
            time.sleep(timeToStop)
            

channel = createGroupDM()
changeGroupDMName(channel)
spam(channel)
