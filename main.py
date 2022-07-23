import server
import dbconnect as db
import promote
import time

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
    try:
        videoId = videoUrl.split("=")[1]
    except:
        videoId = videoUrl.split("shorts/")[1]
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
    try:
        videoId = videoUrl.split("=")[1]
    except:
        videoId = videoUrl.split("shorts/")[1]
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

# menu handler
def main():
    # create database connection
    conn = db.connect()
    # print total accounts in the database
    print("[+] Total Accounts Saved " + str(db.numAccounts(conn)))
    # menu for adding accounts and promoting videos
    print("[+] 1. Add Account")
    print("[+] 2. Promote Video")
    print("[+] 3. Add Reward Points")
    print("[+] 4. Manually Activate Plan (Basic)")
    print("[+] 5. Sign In in Browser")
    option =  input("[+] Enter Option: ")
    if (option == "1"):
        addAccountMenu(conn)
    elif (option == "2"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        promoteMenu(conn, startFrom, endAt)
    elif (option == "3"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        rewardPointsMenu(conn, startFrom, endAt)
    elif (option == "4"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        manualActivationMenu(conn, startFrom, endAt)
    elif (option == "5"):
        server.signInBrowser(conn)
    else:
        print("[-] Invalid Option")
    # close database connection
    db.closeDB(conn)


# start here
main()