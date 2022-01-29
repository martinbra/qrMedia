import media_links.novo_cantico
from classes import QRCode, generate_basic_qrcodes
from pimaco_generator import generate_labels_sheet, QR_CODES_PER_SHEET
import json

# Not going to update links
UPDATE = False
GENERATE_PDF = True

# Offset to start position of first QRCODE in the label's sheet.
PAGE_QRCODE_START_OFFSET = 0

# ------------------------------------------------------------
# NOVO CANTICO
# look for content.
media_links.novo_cantico.parse_novo_cantico_mp3(update=UPDATE)

# get dictionary of links.
nc = media_links.novo_cantico.get_qrcodes_dict()

# generate in RAM SVGs for qrcodes lists:
URL = "https://martinbra.pythonanywhere.com/nc/"
qr_codes = []
for index, target_url in nc.items():
    qr_url = URL.format(index)
    new_qrcode = QRCode(URL, index, target_url, "NC")
    qr_codes.append(new_qrcode)

# Generate more qrcodes to fill the page.
pages, used_slots = divmod(len(qr_codes), QR_CODES_PER_SHEET)
remaining_slots = QR_CODES_PER_SHEET - used_slots
qr_codes.extend(generate_basic_qrcodes(remaining_slots))

# populate a PDF page with these qr_codes
if GENERATE_PDF:
    generate_labels_sheet(qr_codes)

    # log the generated pdf file.
    with open('generate.log', 'a') as f:
        for qrcode in qr_codes:
            f.write(f"{qrcode}\n")


# create json file for server.
qrcodes_json = {}
for qrcode in qr_codes:
    endpoint, index, qr_target = qrcode.get_data()
    print(qrcode.get_data())
    if endpoint not in qrcodes_json.keys():
        qrcodes_json[endpoint] = {}
    qrcodes_json[endpoint][index] = qr_target

with open('qrcodes.json', 'w') as f:
    # f.write(qrcodes_json)
    json.dump(qrcodes_json, f, indent=4)
