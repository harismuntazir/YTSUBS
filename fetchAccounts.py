import dbconnect as db

# create a table inside db to store all accounts with id, username, password, accountId, host
def saveAccount(conn, username, password, accountId, host):
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?)", (username, password, accountId, host))
    conn.commit()
    print("[+] Account Saved: " + accountId)

# get all accounts
def getAccounts(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    return c.fetchall()

# get the last parsed account id where host = host
def getLastParsedAccount(conn, host):
    try:
        c = conn.cursor()
        c.execute("SELECT accountId FROM lastParsedAccount WHERE host = ?", (host,))
        return c.fetchone()[0]
    except:  
        # insert the last parsed account id with host id
        c.execute("INSERT INTO lastParsedAccount VALUES (NULL, ?, ?)", ('0', "subscribers.video"))
        c.execute("INSERT INTO lastParsedAccount VALUES (NULL, ?, ?)", ('0', "submenow.com"))
        return '0'

# update the last parsed account id where host = host
def updateLastParsedAccount(conn, accountId, host):
    c = conn.cursor()
    c.execute("UPDATE lastParsedAccount SET accountId = ? WHERE host = ?", (accountId, host))
    conn.commit()

# see if password exist in the database table where host = host
def checkPassword(conn, password, host):
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE password = ? AND host = ?", (password, host))
    if c.fetchone() is None:
        return False
    else:
        return True