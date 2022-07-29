import dbconnect as db

# create the table if it doesn't exist
def initAllAccounts(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS allAccounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    conn.commit()
    print("[+] allAccounts Table Created")

# create a table inside db to store all accounts with id, username, password, accountId, host
def saveAccount(conn, username, password, accountId, host):
    c = conn.cursor()
    c.execute("INSERT INTO allAccounts VALUES (NULL, ?, ?, ?, ?)", (username, password, accountId, host))
    conn.commit()
    print("[+] Account Saved: " + accountId)

    # update the last parsed account id
    updateLastParsedAccount(conn, accountId)

# get the last parsed account id
def getLastParsedAccount(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS lastParsedAccount (accountId TEXT)")
    c.execute("SELECT accountId FROM lastParsedAccount")
    accountId = c.fetchone()
    if accountId is None:
        return "0"
    else:
        return accountId[0]

# update the last parsed account id
def updateLastParsedAccount(conn, accountId):
    c = conn.cursor()
    c.execute("UPDATE lastParsedAccount SET accountId = ?", (accountId,))
    conn.commit()
    print("[+] Last Parsed Account Updated")

# see if password exist in the database table
def checkPassword(conn, password):
    c = conn.cursor()
    c.execute("SELECT password FROM allAccounts WHERE password = ?", (password,))
    password = c.fetchone()
    if password is None:
        return False
    else:
        return True