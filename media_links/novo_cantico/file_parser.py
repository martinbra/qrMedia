import json
import requests

if __name__ == '__main__':
    FILE = 'novo-cantico.json'
else:
    FILE = 'media_links/novo_cantico/novo-cantico.json'

def parse_novo_cantico_mp3(update=True):

    if not update:
        return None

    # base_link1 = "http://novocantico.com.br/hino/{n:03}/{n:03}.xml"
    base_link2 = "https://archive.org/download/impessoal_elleralmeida_{n:03}/{n:03}.mp3"

    existing_numbers = {}

    for i in range(0, 400 + 1):
        url = base_link2.format(n=i)

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

    with open(FILE, 'w') as fp:
        json.dump(existing_numbers, fp)


def get_qrcodes_dict():
    with open(FILE, 'r') as fp:
        nc = json.load(fp)

    # reparse entries to their int value
    nc = {int(i): url for i, url in nc.items()}
    return nc
