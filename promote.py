import requests
from requests.structures import CaseInsensitiveDict
import server

# global 
base = "https://www."

# subscription shifter
def shifter(host, session, idVideo, idUser):
    tail = "/assignuservideo.html?idUser=" + idUser + "&idVideo=" + idVideo
    url = base + host + tail
    resp = requests.get(url, headers=server.getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "true"):
        print("[+] Video Promotion Added")
    else:
        print("[-] Shift Failed")

# activate gold plan
def activatePlan(host, session, accountId):
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=3"
    resp = requests.get(url, headers=server.getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "false"):
        print("[+] Plan Activation Failed")
        err = resp.text.split('error":"')[1].split(".")[0]
        if (err == "You need 24 but you only have 24 reward points"):
            print("[-] Adding Reward Points To Account: " + str(accountId))
            addRewardPoints(host, session, accountId)
        else:
            print("[-] Error: " + err)
    else:
        print("[+] Plan Activated For 3 Days")

# add reward points 
def addRewardPoints(host, session, accountId):
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=-6"
    resp = requests.get(url, headers=server.getHeaders(session))
    print(resp.text)
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "false"):
        print("[+] Can't Add Reward Points")
    else:
        print("[-] Reward Points Added")

# choose the plan
def choosePlan(host, session, planId):
    tail = "/aiomarket.html?idPlan=" + str(planId)
    url = base + host + tail
    log = requests.get(url, headers=server.getHeaders(session))
    if (log.status_code == 200):
        print("[+] Activated")
    else:
        print("[-] Failed")
    
# fake verify view
def verify(host, session):
    while (True):
        tail = "/aioverify.html?idVideo=maKl5kVcUbo"
        url = base + host + tail
        resp = requests.get(url, headers=server.getHeaders(session))

        views = resp.text.split('views":')[1].split(",")[0]
        finished = resp.text.split('finished":')[1].split(",")[0]
        retry = resp.text.split('retry":')[1].split(",")[0]
        if (finished == "true" or finished == "false" and retry == "true"):
            print("[+] Subscription Activated")
            break
        else:
            print("[-] Views: " + views)