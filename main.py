import requests, json, time

tokenDiscord = "" # insert ur token here (bot tokens wont work)
tokenTrivia = "824c28fc3cmshfa0dfba9bd5ff5bp1bdfbfjsnb90fc16d0447"
groupDmName = "groupname"

friendsToSpam = [] #max 9 friends for now (paste friends ids as strings here pls, one friend, one string in a list)
#btw insert only the ids of your friends, you cant insert a random person here

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
        rDis = requests.post(f"https://discord.com/api/v9/users/@me/channels", headers=headersDiscordData, json=jsonDiscordData)
        jDis = json.loads(rDis.text)
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
        jsonDiscordData = {"content": f"{jTrivia[0]['question']}? {jTrivia[0]['answer']}! @everyone"}

        rDis = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=headersDiscordData, json=jsonDiscordData)
        jDis = json.loads(rDis.text)

        if rDis.status_code == 429:
            timeToStop = float(jDis["retry_after"])
	    print(f"Rate limited for {timeToStop} seconds.")
            time.sleep(timeToStop)
            

channel = createGroupDM()
changeGroupDMName(channel)
spam(channel)
