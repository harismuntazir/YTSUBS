import requests
from requests.structures import CaseInsensitiveDict
import dbconnect as db

# global 
base = "https://www."

# make headers
def getHeaders(session):
    headers = CaseInsensitiveDict()
    headers["cookie"] = "JSESSIONID=" + session + ";"
    return headers

# login into the application
def login(host, username, password):
    isDone = False
    while not isDone:
        try:
            tail = "/signinclick.html"
            data = "?email=" + username + "&idchannel=" + password + "&isSignIn=true&name="
            url = base + host + tail + data
            resp = requests.get(url)
            loggedIn = resp.text.split('ok":')[1].split(",")[0]
            if (loggedIn == "true"):
                print("[+] Logged In")
                return [loggedIn, resp.headers["Set-Cookie"].split("JSESSIONID=")[1].split(";")[0]]
            else:
                print("[-] Login Failed")
                return [loggedIn, ""]

            isDone = True
        except:
            isDone = False
            print("[-] Retrying To Login")
            continue

    

# logout 
def logout(host, session):
    tail = "/index.html?action=logout"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    print("[+] Logged Out")


# get account Id
def getAccountId(host, session):
    tail = "/account.html"
    url = base + host + tail
    resp = requests.get(url, headers=getHeaders(session))
    accountId = resp.text.split("ID:&nbsp;<b>")[1].split("</b>")[0].strip()
    print("[+] Account ID: " + accountId)
    return accountId

# create a sign in link and open it in browser
def signInBrowser(conn):
    tail = "/signinclick.html"

    # enter account number to sign in
    accNo = int(input("[+] Enter Account Number: "))
    # get account from database
    accounts = db.getAccounts(conn)
    account = accounts[accNo - 1]
    # make url
    data = "?email=" + account[1] + "&idchannel=" + account[2] + "&isSignIn=true&name="
    signInUrl = base + account[4] + tail + data

    print (signInUrl)
    # open sign in link in browser
    #os.system("start " + signInUrl)

# request user info 
def getUserInfo(session, host, accoundId):
    tail = "/updateuser.html"
    data = "?id=" + str(accoundId) + "&self=false"
    url = base + host + tail + data
    resp = requests.get(url, headers=getHeaders(session))
    return resp.text
         
    



