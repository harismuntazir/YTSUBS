import requests

# make the request
def request(url, cookie, data):
    return requests.post(url, data=data, cookies=cookie)

# activate the program 
def activate(host, cookie):
    base = "https://www."
    common = "/members-area/"
    url = base + host + common
    data = "activate=2"
    log = request(url, cookie, data)
    print(log.text)
    if (log.status_code == 200):
        print("[+] Activated")
    else:
        print("[-] Failed")

# start the video task loop
def task(cookie, host):
    base = "https://www."
    common = "/members-area/sub-completed-v4.php"
    url = base + host + common
    for i in range(1):
        data = "subscribers=&channel=&videoId="
        log = request(url, cookie, data)
        print(log.text)

# login to the application
def login(host, password):
    base = "https://www."
    tail = "/login/final/UCI7OjCUQzkm_X5Ma5WvbIWg/"
    url = base + host + tail
    # do a request without data
    resp = requests.get(url)

    # do login
    data = "channelid=UCI7OjCUQzkm_X5Ma5WvbIWg&password=" + str(password)
    resp = request(url, resp.cookies, data)
    print(resp.text)
    return resp.cookies

# make pairs of id : host
hosts = {"1": "subpals.com", "2": "ytpals.com", "3": "sonuker.com"}
# make pairs of id : password
passwords = {"1": "Zz!Y8_qVS2a**5p", "2": "vfDi$y5+Ww_P22r", "3": "xvK9#*k#8_A+jL9"}

# let user choose the host
for key, value in hosts.items():
    print("Enter " + str(key) + " For " + value + ".")

hostChoice = '2' # input("Host id: ")
host = hosts[hostChoice]
password = passwords[hostChoice]

# login to get the session
cookie = login(host, password)
# activate the subscription
activate(host, cookie)
# start the task
task(cookie, host)




