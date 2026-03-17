import http.client
import json
import os
import dotenv

dotenv.load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")

class Serper:
    def __init__(self,query):
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
          "q": query
        })
        print(serper_api_key)
        headers = {
          'X-API-KEY': serper_api_key,
          'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        self.info = json.loads(data)
        # results = []
        self.source = [item["link"] for item in self.info["organic"]]
        self.results = [item["snippet"] for item in self.info["organic"]]
    def serper_result(self):
        return self.results, self.source
