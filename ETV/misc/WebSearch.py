import requests

class searchResults:
    header = ""
    content = ""

    def __init__(self, header,content):
        self.header = header
        self.content = content

def request(searchText):
    url = f"http://api.duckduckgo.com/?q={searchText}&format=json"
    r = requests.get(url)
    jsn = r.json()
    return searchResults(jsn["Heading"],jsn["Abstract"])
