import dbconnect as db
import menus
import videos
import server
import prepare_db

#globals
startFrom = 0
endAt = 0

# menu handler
def main():
    # create database connection
    conn = db.connect()
    prepare_db.init(conn)
    # print total accounts in the database
    print("[+] Total Accounts Saved " + str(db.numAccounts(conn)))
    # menu for adding accounts and promoting videos
    print("[+] 1. Add Account")
    print("[+] 2. Promote Video")
    print("[+] 3. Add Video Id")
    print("[+] 4. Fetch Accounts")
    print("[+] 5. Promote One By One")
    print("[+] 6. Add Reward Points to All Accounts")
    print("[+] 7. Browser Sign In")
    print("[+] 8. Manual Activation")
    print("[+] 9. Only Shifter")
    print("[+] 10. Find Channel")
    option =  input("[+] Enter Option: ")

    if (option == "1"):
        menus.addAccountMenu(conn)
    elif (option == "2"):
        accLimits()
        menus.promoteMenu(conn, startFrom, endAt)
    elif (option == "3"):
        menus.addVideosMenu(conn)
    elif (option == "4"):
        menus.fetchAccountsMenu(conn)
    elif (option == "5"):
        print("Total Videos = " + str(videos.numVideos(conn)))
        accLimits()
        menus.promoteOneByOneMenu(conn, startFrom, endAt)
    elif (option == "6"):
        accLimits()
        menus.addRewardPointsOnlyMenu(conn, startFrom, endAt)
    elif (option == "7"):
        server.signInBrowser(conn)
    elif (option == "8"):
        accLimits()
        menus.manualActivationMenu(conn, startFrom, endAt)
    elif (option == "9"):
        accLimits()
        menus.shiftVideosMenu(conn, startFrom, endAt)
    elif (option == "10"):
        menus.findChannelMenu(conn)
    else:
        print("[-] Invalid Option")
    # close database connection
    db.closeDB(conn)


# get accounts start from and end at
def accLimits():
    global startFrom 
    startFrom = int(input("[+] Accounts From: "))
    global endAt 
    endAt = int(input("[+] Accounts To: "))

# start here
main()