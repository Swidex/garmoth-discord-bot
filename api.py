import os, requests, asyncio, json

API_URL = "https://garmoth.com/api"
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
        'Accept': 'application/json',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

class ApiRequest():
    response = ""
    call = ""

    def __init__(self, call):
        self.call = call
        #do nothing

    async def execute(self):
        r = requests.get(API_URL + self.call, headers=HEADERS)
        r.raise_for_status()
        if r.status_code != 204:
            self.response = r.json()

    def dump(self):
        fname = str(hash(self)) + "_dump.json"
        with open(fname, "w") as outfile:
            outfile.write(json.dumps(self.response, indent=4))
