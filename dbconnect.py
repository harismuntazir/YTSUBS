import sqlite3
import os

# create a sqlite database accounts.db if it doesn't exist
def connect():
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/accounts.db")
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

# close the database connection
def closeDB(conn):
    conn.close()
    print("[+] Shutting Down")

# add account to the database
def addAccount(conn, username, password, accoundId, host):
    c = conn.cursor()
    
    # if accounts table does not exist create it
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    conn.commit()

    # now insert the account and save it
    c.execute("INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?)", (username, password, accoundId, host))
    conn.commit()
    print("[+] Account Saved")
    print("[+] Total Accounts Saved " + str(numAccounts(conn)))

# get all accounts from the database
def getAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    return accounts

# number of accounts in the database
def numAccounts(conn):
    return (len(getAccounts(conn)))
