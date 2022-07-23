import sqlite3
import os

# create a sqlite database accounts.db if it doesn't exist
def connect():
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/accounts.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    conn.commit()
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

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