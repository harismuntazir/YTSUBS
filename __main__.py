import dbconnect as db
import menus
import videos

# menu handler
def main():
    # create database connection
    conn = db.connect()
    # print total accounts in the database
    print("[+] Total Accounts Saved " + str(db.numAccounts(conn)))
    # menu for adding accounts and promoting videos
    print("[+] 1. Add Account")
    print("[+] 2. Promote Video")
    print("[+] 3. Add Video Id")
    print("[+] 4. Fetch Accounts")
    print("[+] 5. Promote One By One")
    print("[+] 6. Sign In in Browser")
    option =  input("[+] Enter Option: ")
    if (option == "1"):
        menus.addAccountMenu(conn)
    elif (option == "2"):
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        menus.promoteMenu(conn, startFrom, endAt)
    elif (option == "3"):
        menus.addVideosMenu(conn)
    elif (option == "4"):
        menus.fetchAccountsMenu(conn)
    elif (option == "5"):
        print("Total Videos = " + str(videos.numVideos(conn)))
        startFrom = int(input("[+] Accounts From: "))
        endAt = int(input("[+] Accounts To: "))
        menus.promoteOneByOneMenu(conn, startFrom, endAt)
    elif (option == "6"):
        menus.server.signInBrowser(conn)
    else:
        print("[-] Invalid Option")
    # close database connection
    db.closeDB(conn)


# start here
main()