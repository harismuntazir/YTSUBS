import sqlite3
import webbrowser
import requests
import time

#webbrowser.open(link)

# create a sqlite database accounts.db if it doesn't exist
def database():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

# close the database connection
def closeDB(conn):
    conn.close()
    print("[+] Shutting Down")

# get all accounts from the database and print them
def getAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return accounts

# create account
def createAccount(username, password):
    base = "https://www.subscribers.video"
    data = "?email=" + username + "&idchannel=" + password + "&isSignIn=false&name=" + password
    url = base + "/signinclick.html" + data
    resp = requests.get(url)
    loggedIn = resp.text.split('ok":')[1].split(",")[0]
    if (loggedIn == "true"):
        link = base + "/terms.html?idchannel=" + password
        print("[+] Creating New Account: " + password)
        webbrowser.open(link)
        time.sleep(15) # wait for user to accept captcha
    else:
        print("[-] Accound Already , Skipping..")


# handler
def main():
    db = database()
    accounts = getAccounts(db)
    for account in accounts:
        if (account[0] > 80):
            print("[+] Creating Account: " + str(account[0]))
            createAccount(account[1], account[2])   
    closeDB(db)

# start Up
main()
