import requests
import utils

class searchResults:
    header = ""
    content = ""

    def __init__(self, header ="",content=""):
        self.header = header
        self.content = content

def request(searchText):
    url = f"http://api.duckduckgo.com/?q={searchText}&format=json"
    r = requests.get(url)
    jsn = r.json()
    try:
        ret = searchResults(jsn["Heading"],jsn["Abstract"])
    except Exception as e:
        utils.cprint(f"Error in WebSearch: {str(e)}")
        ret = searchResults()
    return ret
