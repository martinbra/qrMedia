import json
import requests

if __name__ == '__main__':
    FILE = 'hnc-periel.json'
else:
    FILE = 'media_links/novo_cantico/hnc-periel.json'

def parse_novo_cantico_mp3(update=False):

    if not update:
        return None

    existing_numbers = {}

    with open(FILE.replace('.json','.csv')) as f:
        for line in f.readlines():
            nc, link = line.strip().replace('"', '').split(',')
            nc = nc.replace('NC', '')
            existing_numbers[nc] = link

    with open(FILE, 'w') as fp:
        json.dump(existing_numbers, fp)


def get_qrcodes_dict():
    with open(FILE, 'r') as fp:
        nc = json.load(fp)

    # reparse entries to their int value
    nc = {i: url for i, url in nc.items()}
    return nc

if __name__ == '__main__':
    parse_novo_cantico_mp3(True)
    dict = get_qrcodes_dict()
    print(dict)