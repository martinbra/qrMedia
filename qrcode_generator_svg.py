import qrcode
import qrcode.image.svg


def generate_img(url, index, folder='qrcodes'):

    # check url for trailing slash:
    if url[-1] != '/':
        url += '/'
    data = f"{url}{index}"

    code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=10,
        border=2,
    )

    code.add_data(data)
    code.make(fit=True)
    img = code.make_image(image_factory=qrcode.image.svg.SvgPathImage)

    # Save svg file somewhere
    try:
        img.save(f"{folder}/{index}.svg")
    except FileNotFoundError:
        print(f"Please create folder {folder}")

def generate_range(start, end):
    # TODO: Documentation
    for i in range(start, end+1):
        generate_img("https://martinbra.pythonanywhere.com/qrcode/", i)


# TODO: Documentation
generate_range(1, 80*3)
