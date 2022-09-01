import dbconnect as db

# init
def init(conn):
    createAccountsTable(conn)
    initAllAccounts(conn)
    createTableVidoes(conn)

# create the table if it doesn't exist
def initAllAccounts(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS allAccounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    # create table to store the last parsed account id with host id
    c.execute("CREATE TABLE IF NOT EXISTS lastParsedAccount (id INTEGER PRIMARY KEY, accountId TEXT, host TEXT)")
    conn.commit()
    print("[+] Initilized allAccounts Data Table")

# if accounts table does not exist create it
def createAccountsTable(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, accountId TEXT, host TEXT)")
    conn.commit()

# create table videos
def createTableVidoes(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, videoId TEXT)")
    conn.commit()