from requests_threads import AsyncSession
import json
import requests


BASE_LINK1 = "http://novocantico.com.br/hino/{n:03}/{n:03}.xml"
BASE_LINK2 = "https://archive.org/download/impessoal_elleralmeida_{n:03}/{n:03}.mp3"


existing_numbers = {}

for i in range(0, 400 + 1):
    url = BASE_LINK2.format(n=i)

    r = requests.head(url)

    if r.status_code == 404:
        print(i)
        # skip number if not found
        continue
    elif r.status_code in [200, 302]:
        existing_numbers[i] = url
        print(f"{i} added")
    else:
        print(f"{i} mp3 request {url} got {r.status_code}. Why?")


with open('novo-cantico.json', 'w') as fp:
    json.dump(existing_numbers, fp)
