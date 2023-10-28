

import requests

url = "http://localhost:1450/summarize"

files = {"file": ("example.txt", open("/home/samuel/Downloads/poopoer.pdf", "rb"))}
data = {
  "context_words": "capsules, squashing, non-linear",
  "runtype": "file"
}


response = requests.post(url, files=files, data=data)

print(response.status_code)
print(response.json())
