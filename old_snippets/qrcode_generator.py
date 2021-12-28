import qrcode
from PIL import ImageDraw, ImageFont

_APP_PROTOCOL = "qrmp://"


def generate_img(name, content, folder='qrcodes'):
    # TODO: Documentation
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4)
    qr.add_data(f"{_APP_PROTOCOL}{content}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # put label on image
    # TODO:
    #  CENTER the code
    #  use better font
    #  respect spacing around qrcode
    draw = ImageDraw.Draw(img)
    draw.text((165, 310), name, anchor='ms')
    # font = ImageFont.truetype("media/FiraCode-Regular.ttf", 16)
    # draw.text((165, 310), name, anchor='ms', font=font)

    try:
        img.save(f"{folder}/{name}.png")
    except FileNotFoundError:
        print(f"Please create folder {folder}")


def generate_range(number_range):
    # TODO: Documentation
    for i in number_range:
        filename = f"{i:04}"
        content = str(i)
        generate_img(filename, content)


# TODO: Documentation
file_range = range(1)
generate_range(file_range)
