import requests
from requests.structures import CaseInsensitiveDict

# global 
base = "https://www."

# make headers
def getHeaders(session):
    headers = CaseInsensitiveDict()
    headers["cookie"] = "JSESSIONID=" + session + ";"
    return headers

# fake verify view
def verify(host, session):
    while (True):
        tail = "/aioverify.html?idVideo=maKl5kVcUbo"
        url = base + host + tail
        resp = requests.get(url, headers=getHeaders(session))

        views = resp.text.split('views":')[1].split(",")[0]
        finished = resp.text.split('finished":')[1].split(",")[0]
        retry = resp.text.split('retry":')[1].split(",")[0]
        if (finished == "true" or finished == "false" and retry == "true"):
            print("[+] Subscription Activated")
            break
        else:
            print("[-] Views: " + views)
        

# activate the subscription
def finish(host, session):
    tail = "/account.html?sub=true"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    subs = resp.text.split("id='will-get-subs'>")[2].split("</b>")[0].strip()
    print("You Will Get " + subs + " Subscribers")

# login into the application
def login(host, username, password):
    tail = "/signinclick.html"
    data = "?email=" + username + "&idchannel=" + password + "&isSignIn=true&name="
    url = base + host + tail + data
    resp = requests.get(url)
    loggedIn = resp.text.split('ok":')[1].split(",")[0]
    if (loggedIn == "true"):
        print("[+] Logged In")
    else:
        print("[-] Login Failed")
    # return the JSESSIONID cookie
    return resp.headers["Set-Cookie"].split("JSESSIONID=")[1].split(";")[0]

# choose the plan
def choosePlan(host, session, planId):
    tail = "/aiomarket.html?idPlan=" + str(planId)
    url = base + host + tail
    log = requests.get(url, headers=getHeaders(session))
    if (log.status_code == 200):
        print("[+] Activated")
    else:
        print("[-] Failed")

# get account Id
def getAccountId(host, session):
    tail = "/account.html"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    accountId = resp.text.split("ID:&nbsp;<b>")[1].split("</b>")[0].strip()
    return accountId


# main
def main():
    # make pairs of hosts, usernames, passwords and channels
    hosts = {"1": "subscribers.video", "2": "submenow.com"}
    usernames = {"1": "haris.0813.m@gmail.com", "2": "fakemail@gmail.com", "3": "ghrasool2028@gmail.com", "4": "anothermail@gmail.com"}
    passwords = {"1": "UCI7OjCUQzkm_X5Ma5WvbIWg", "2": "UCdWmRO6ndhMcG6EgFa9vLTg", "3": "UCzMBl5JQx7f_eVilDeTzuwQ", "4": "UCLnl1lkA0FyPtC58JRelunw"}
    channels = {"1": "SolutionTips", "2": "HarisMuntazir", "3": "ShanoSharik", "4": "hm.813.m"}
    
    # menu options to choose a host and a channel
    for id, host in hosts.items():
        print("Press " + str(id) + " For ", host)
    hostId = input("Host Id: ")
    host = hosts[hostId]
    for id, channel in channels.items():
        print("Press " + str(id) + " For ", channel)
    channelId = input("Channel Id: ")

    # #get username and password from user
    # username = input("Username: ")
    # password = input("Password: ")
    # # do login
    session = login(host, usernames[channelId], passwords[channelId])
    # session = login(host, username, password)

    # choose the plan
    if (hostId == "1"):
        choosePlan(host, session, "6")
        verify(host, session)
    if (hostId == "2"):
        choosePlan(host, session, "8")
        verify(host, session)


    # # finish the subscription
    finish(host, session)

# now run the main function
main() 

# https://www.submenow.com/account.html?accountId=1581144&plan=4&day=1000
# https://www.submenow.com/account.html?accountId=1581144&videoUrl=wKuGhLo66oA&views=2
# https://www.submenow.com/assignuservideo.html?idUser=1640494&idVideo=xZPyhSw9BwE