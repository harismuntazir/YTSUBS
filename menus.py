import server
import dbconnect as db
import promote
import time
import videos
import fetchAccounts

# add account menu handler
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
        inst = server.login(host, username, password)
        if (inst[0] == "true"):
            session = inst[1]
        else:
            return
        # get account id
        accountId = server.getAccountId(host, session)
        # add account to the database
        db.addAccount(conn, username, password, accountId, host)
        num = int(input("[+] Enter -9 to exit: "))



# promte menu handler
def promoteMenu(conn, startFrom, endAt):
    # video id 
    videoUrl = input("[+] Enter Video Link: ")
    videoId = videos.videoId(videoUrl)
    # get user credentials from db
    accounts = db.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            inst = server.login(host, account[1], account[2])
            if (inst[0] == "true"):
                session = inst[1]
            else:
                continue  
            # account id 
            accountId = str(account[3])
            # subscription shifter
            isDone = False
            while not isDone:
                try:
                    promote.shifter(host, session, videoId, accountId)
                    isDone = True
                except:
                    print("[-] URL Shifting Failed, Retrying")
                    isDone = False
                    continue
            # activate plan
            isDone = False
            while not isDone:
                try:
                    promote.activatePlan(host, session, accountId)
                    isDone = True
                except:
                    print("[-] Plan Activation Failed, Retrying")
                    isDone = False
                    continue
            # logout 
            try:
                server.logout(host, session)
            except:
                print("[-] Could Not Logout")

            # how wait for 30 minutes
            # wait = 30 * 60
            # time.sleep(wait)
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

# only shift videos menu handler
def shiftVideosMenu(conn, startFrom, endAt):
    # video id 
    videoUrl = input("[+] Enter Video Link: ")
    videoId = videos.videoId(videoUrl)
    # get user credentials from db
    accounts = db.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            inst = server.login(host, account[1], account[2])
            if (inst[0] == "true"):
                session = inst[1]
            else:
                continue  
            # account id 
            accountId = str(account[3])
            # subscription shifter
            isDone = False
            while not isDone:
                try:
                    promote.shifter(host, session, videoId, accountId)
                    isDone = True
                except:
                    print("[-] URL Shifting Failed, Retrying")
                    isDone = False
                    continue
    print("[+] URL Shifting Started")

# reward points menu handler 
def rewardPointsMenu(conn, startFrom, endAt):
    # get user credentials from db
    accounts = db.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login 
            try:
                inst = server.login(host, account[1], account[2])
                if (inst[0] == "true"):
                    session = inst[1]
                else:
                    continue  
            except:
                print("[-] Could Not Login, Skipping Account")
                continue
            # add reward points
            accountId = str(account[3])
            promote.addRewardPoints(host, session, accountId)
            #time.sleep(5)
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Reward Points Added")


# manually activate the plan menu handler
def manualActivationMenu(conn, startFrom, endAt) :
    # video id 
    videoUrl = input("[+] Enter Video Link: ")
    videoId = videos.videoId(videoUrl)
    # get user credentials from db
    accounts = db.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            try:
                inst = server.login(host, account[1], account[2])
                if (inst[0] == "true"):
                    session = inst[1]
                else:
                    continue  
            except:
                print("[-] Could Not Login, Skipping Account")
                continue
            # account id 
            accountId = str(account[3])
            # subscription shifter
            promote.shifter(host, session, videoId, accountId)
            # activate plan
            promote.choosePlan(host, session, "8")
            promote.choosePlan(host, session, "6")
            # verify
            promote.verify(host, session)
            # # logout 
            # server.logout(host, session)
            # time.sleep(2)
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

# add videos menu handler
def addVideosMenu(conn):
    num = 0
    while num != -9:
        videoUrl = input("[+] Enter Video Link: ")
        videoId = videos.videoId(videoUrl)
        # save the video id to the database
        videos.addVideoId(conn, videoId)
        
        num = int(input("[+] Enter -9 to exit: "))

# get video id from videos table and accounts from accounts table
# then promote video 1 by account 1 and video 2 by account 2 and so on
def promoteOneByOneMenu(conn, startFrom, endAt):
    # get video id from videos table
    videoIds = videos.getVideoIds(conn)
    # get user credentials from db
    accounts = db.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            try:
                inst = server.login(host, account[1], account[2])
                if (inst[0] == "true"):
                    session = inst[1]
                else:
                    continue  
            except:
                print("[-] Could Not Login, Skipping Account")
                continue
            # account id 
            accountId = str(account[3])
            # subscription shifter
            promote.shifter(host, session, videoIds[i-1][1], accountId)
            # activate plan
            promote.activatePlan(host, session, accountId)
            # # logout 
            # server.logout(host, session)
            # time.sleep(2)
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Multiple Videos Started")

# request to https://www.subscribers.video/updateuser.html?id=348073&self=false
def fetchAccountsMenu(conn):
    # choose host
    print("1. submenow.com\n2. subscribers.video")
    hostId = input("[+] Enter Host ID: ")
    if hostId == "1":
        host = "submenow.com"
    elif hostId == "2":
       host = "subscribers.video"
    else:
        print("[-] Invalid Host ID")
        return

    tempUser = "natangel.ua@gmail.com"
    tempPass = "UCrz2JKBVaDnjoDYVszSeGVQ"
    inst = server.login(host, tempUser, tempPass)
    if (inst[0] == "true"):
        session = inst[1]
    else:
        return

    # init allAcounts table
    fetchAccounts.initAllAccounts(conn)
    # get last parsed account id
    accountId = int(fetchAccounts.getLastParsedAccount(conn, host)) + 1
    
    count = 0
    keepGoing = "1"
    while (keepGoing == "1"):
        resp = server.getUserInfo(session, host, accountId)
        # spliting 
        try:
            mess = resp.split("id='email"+ str(accountId) +"' value='")[1]
            username = mess.split("'")[0].strip()
            password = mess.split(",")[2].split("&lt;")[0].strip()

            # save the details if they are not already there
            if (fetchAccounts.checkPassword(conn, password, host) == False):
                fetchAccounts.saveAccount(conn, username, password, str(accountId), host)
        except:
            print("[-] User Not Found")

        # update the last parsed account id
        fetchAccounts.updateLastParsedAccount(conn, str(accountId), host)

        # increment the counter
        accountId += 1
        count += 1
        if (count == 100000):
            keepGoing = input("Press 1 to continue or any other key to exit")
            if (keepGoing == "1"):
                count = 0
            else:
                print("Job Done\nTotal Accounts Saved: " + str(accountId))
                break

# get account details from allAccounts table loop and login, add reward points, logout
def addRewardPointsOnlyMenu(conn, startFrom, endAt):
    # get user credentials from db
    accounts = fetchAccounts.getAccounts(conn)
    # counter
    i = 1
    # loop through accounts and login
    for account in accounts:
        if i >= startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            inst = server.login(host, account[1], account[2])
            if (inst[0] == "true"):
                session = inst[1]
            else:
                continue 
            # account id 
            accountId = str(account[3])
            # add reward points
            isDone = False
            while not isDone:
                try:
                    promote.addRewardPoints(host, session, accountId)
                    isDone = True
                except:
                    print("[-] Retrying...")
                    isDone = False
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Reward Points Added")

# find channel id
def findChannelMenu(conn):
    channelId = input("[+] Channel Id: ")
    acc = db.findChannel(conn, channelId)
    if (acc == None):
        print("[-] Channel Not Found")
    else:
        print("[+] Channel Found")
        print("[+] Username: " + acc[1])
        print("[+] Password: " + acc[2])
        print("[+] Host: " + acc[4])
