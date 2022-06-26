import requests
from requests.structures import CaseInsensitiveDict
import sqlite3
import time
import os

# global 
base = "https://www."

# make headers
def getHeaders(session):
    headers = CaseInsensitiveDict()
    headers["cookie"] = "JSESSIONID=" + session + ";"
    return headers

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
    #print(resp.headers["Set-Cookie"].split("JSESSIONID=")[1].split(";")[0])
    return resp.headers["Set-Cookie"].split("JSESSIONID=")[1].split(";")[0]

# logout 
def logout(host, session):
    tail = "/index.html?action=logout"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    print("[+] Logged Out")

# subscription shifter
def shifter(host, session, idVideo, idUser):
    tail = "/assignuservideo.html?idUser=" + idUser + "&idVideo=" + idVideo
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "true"):
        print("[+] Video Promotion Added")
    else:
        print("[-] Shift Failed")

# activate gold plan
def activatePlan(host, session, accountId):
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=3"
    resp = requests.get(url, headers=getHeaders(session))
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

# get account Id
def getAccountId(host, session):
    tail = "/account.html"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    accountId = resp.text.split("ID:&nbsp;<b>")[1].split("</b>")[0].strip()
    print("[+] Account ID: " + accountId)
    return accountId

# create a sqlite database accounts.db if it doesn't exist
def database():
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/accounts.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    conn.commit()
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

# add account menu
def addAccountMenu(conn):
    num = 0
    while num != -9:
        username = input("[+] Enter Username: ")
        password = input("[+] Enter Password: ")
        print ("[+] 1. submenow.com: ")
        print ("[+] 2. subscribers.video: ")
        hostId = input ("[+] Enter Host ID: ")
        if hostId == "1":
            host = "submenow.com"
        elif hostId == "2":
            host = "subscribers.video"
        else:
            print("[-] Invalid Host ID, Try Again")
            num -= 1
            continue
        # login
        session = login(host, username, password)
        # get account id
        accountId = getAccountId(host, session)
        # add account to the database
        addAccount(conn, username, password, accountId, host)
        num = int(input("[+] Enter -9 to exit: "))

# number of accounts in the database
def numAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return len(accounts)

# close the database connection
def closeDB(conn):
    conn.close()
    print("[+] Shutting Down")

# add account to the database
def addAccount(conn, username, password, accoundId, host):
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?)", (username, password, accoundId, host))
    conn.commit()
    print("[+] Account Saved")
    print("[+] Total Accounts Saved " + str(numAccounts(conn)))

# get all accounts from the database and print them
def getAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return accounts

# menu
def promote(conn, startFrom, endAt):
    # video id 
    videoUrl = input("[+] Enter Video Link: ")
    try:
        videoId = videoUrl.split("=")[1]
    except:
        videoId = videoUrl.split("shorts/")[1]
    # get user credentials from db
    accounts = getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            session = login(host, account[1], account[2])
            # account id 
            accountId = str(account[3])
            # subscription shifter
            shifter(host, session, videoId, accountId)
            # activate plan
            activatePlan(host, session, accountId)
            # logout 
            logout(host, session)
            time.sleep(2)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

# add reward points 
def addRewardPoints(host, session, accountId):
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=-200"
    resp = requests.get(url, headers=getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "false"):
        print("[+] Can't Add Reward Points")
    else:
        print("[-] Reward Points Added")
    
# reward points handler 
def rewardPoints(conn, startFrom, endAt):
    # get user credentials from db
    accounts = getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login 
            session = login(host, account[1], account[2])
            # add reward points
            accountId = str(account[3])
            addRewardPoints(host, session, accountId)
            # logout 
            logout(host, session)
            time.sleep(5)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Reward Points Added")

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

# choose the plan
def choosePlan(host, session, planId):
    tail = "/aiomarket.html?idPlan=" + str(planId)
    url = base + host + tail
    log = requests.get(url, headers=getHeaders(session))
    if (log.status_code == 200):
        print("[+] Activated")
    else:
        print("[-] Failed")

# manually activate the plan
def manualActivation(conn, startFrom, endAt) :
    # video id 
    videoUrl = input("[+] Enter Video Link: ")
    try:
        videoId = videoUrl.split("=")[1]
    except:
        videoId = videoUrl.split("shorts/")[1]
    # get user credentials from db
    accounts = getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i > startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            session = login(host, account[1], account[2])
            # account id 
            accountId = str(account[3])
            # subscription shifter
            shifter(host, session, videoId, accountId)
            # activate plan
            choosePlan(host, session, "8")
            choosePlan(host, session, "6")
            # verify
            verify(host, session)
            # logout 
            logout(host, session)
            time.sleep(2)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

# create a sign in link and open it in browser
def signInBrowser(conn):
    tail = "/signinclick.html"

    # enter account number to sign in
    accNo = int(input("[+] Enter Account Number: "))
    # get account from database
    accounts = getAccounts(conn)
    account = accounts[accNo - 1]
    # make url
    data = "?email=" + account[1] + "&idchannel=" + account[2] + "&isSignIn=true&name="
    signInUrl = base + account[4] + tail + data

    print (signInUrl)
    # open sign in link in browser
    #os.system("start " + signInUrl)
    
# menu
def main():
    # create database connection
    conn = database()
    # print total accounts in the database
    print("[+] Total Accounts Saved " + str(numAccounts(conn)))
    # menu for adding accounts and promoting videos
    print("[+] 1. Add Account")
    print("[+] 2. Promote Video")
    print("[+] 3. Add Reward Points")
    print("[+] 4. Manually Activate Plan")
    print("[+] 5. Sign In in Browser")
    option =  input("[+] Enter Option: ")
    if (option == "1"):
        addAccountMenu(conn)
    elif (option == "2"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        promote(conn, startFrom, endAt)
    elif (option == "3"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        rewardPoints(conn, startFrom, endAt)
    elif (option == "4"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        manualActivation(conn, startFrom, endAt)
    elif (option == "5"):
        signInBrowser(conn)
    else:
        print("[-] Invalid Option")
    # close database connection
    closeDB(conn)


# start point
main()

