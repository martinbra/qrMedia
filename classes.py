import io
import qrcode
import qrcode.image.svg
import json

def _add_trailing_slash(url):
    # check url for trailing slash:
    if url[-1] != '/':
        url += '/'
    return url


class QRCode:
    def __init__(self, qr_url, index, qr_target, short_name=""):
        self.qr_url = _add_trailing_slash(qr_url) + str(index)
        self.qr_target = qr_target
        self.index = index
        self.short_name = short_name + str(index)

    def __repr__(self):
        return ','.join((self.short_name,
                         str(self.index),
                         self.qr_url,
                         self.qr_target))

    def generate_qr_code(self):
        code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            # box_size=10,
            border=2,
        )

        code.add_data(self.qr_url)
        code.make(fit=True)
        img = code.make_image(image_factory=qrcode.image.svg.SvgPathImage)

        # Save svg qrcode to BytesIO
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)

        return buf

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def generate_basic_qrcodes(quantity, offset=0):
    for i in range(offset, quantity+offset):
        yield QRCode(f"https://martinbra.pythonanywhere.com/qr/",
                     i,
                     f"TARGET_URL_UNDEFINED",
                     f"QR")