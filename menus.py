import server
import dbconnect as db
import promote
import time
import videos

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
        session = server.login(host, username, password)
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
            session = server.login(host, account[1], account[2])
            # account id 
            accountId = str(account[3])
            # subscription shifter
            promote.shifter(host, session, videoId, accountId)
            # activate plan
            promote.activatePlan(host, session, accountId)
            # logout 
            server.logout(host, session)
            time.sleep(2)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoId + " Started")

    
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
            session = server.login(host, account[1], account[2])
            # add reward points
            accountId = str(account[3])
            promote.addRewardPoints(host, session, accountId)
            # logout 
            server.logout(host, session)
            time.sleep(5)
        else:
            print("Skipping Account " + str(account[0]))
        
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
        if i > startFrom and i <= endAt: 
            print("Tempering Account " + str(account[0]))
            # get host
            host = str(account[4])
            # login
            session = server.login(host, account[1], account[2])
            # account id 
            accountId = str(account[3])
            # subscription shifter
            promote.shifter(host, session, videoId, accountId)
            # activate plan
            promote.choosePlan(host, session, "8")
            promote.choosePlan(host, session, "6")
            # verify
            promote.verify(host, session)
            # logout 
            server.logout(host, session)
            time.sleep(2)
        else:
            print("Skipping Account " + str(account[0]))
        
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
            session = server.login(host, account[1], account[2])
            # account id 
            accountId = str(account[3])
            # subscription shifter
            promote.shifter(host, session, videoIds[i][1], accountId)
            # activate plan
            promote.activatePlan(host, session, accountId)
            # logout 
            server.logout(host, session)
            time.sleep(2)
        else:
            print("Skipping Account " + str(account[0]))
        
        # increment the counter
        i += 1
    
    # print status
    print("[+] Promotion For Video " + videoIds[0] + " Started")