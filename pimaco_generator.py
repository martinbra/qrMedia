from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm
from classes import generate_basic_qrcodes

LABEL = {
    "Margem Superior": 1.27*cm,
    "Margem Esquerda": 1.45*cm,
    "Espaçamento Vertical": 1.27*cm,
    "Espaçamento Horizontal": 4.75*cm,
    "Altura": 1.27*cm,
    "Largura": 4.44*cm,
    "Colunas": 4,
    "Linhas": 20,
}
QRCODE_SIZE = 3.3*cm
QR_CODES_PER_LABEL = 3
QR_CODES_PER_SHEET = LABEL["Colunas"] * LABEL["Linhas"] * QR_CODES_PER_LABEL


def _label_pos_generator(qrcodes_per_label=1):
    for linha in range(LABEL['Linhas']):
        y_pos = (LABEL['Margem Superior'] +
                 linha * LABEL['Espaçamento Vertical'])

        for coluna in range(LABEL['Colunas']):
            for div in range(qrcodes_per_label):
                x_pos = (LABEL['Margem Esquerda'] +
                         coluna * LABEL['Espaçamento Horizontal'] +
                         div * LABEL["Largura"]/qrcodes_per_label)

                yield x_pos, y_pos


def _scale(drawing, scaling_factor):
    """
    Scale a reportlab.graphics.shapes.Drawing()
    object while maintaining the aspect ratio
    """
    scaling_x = scaling_factor
    scaling_y = scaling_factor

    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing


def _add_image(image_path, page_canvas, x, y, margin=0):
    drawing = svg2rlg(image_path)
    scaling_factor = (LABEL["Altura"]-2*margin) / QRCODE_SIZE
    scaled_drawing = _scale(drawing, scaling_factor=scaling_factor)
    renderPDF.draw(scaled_drawing, page_canvas, x+margin, y+margin)


def _add_vertical_text(x, y, text, page_canvas):
    page_canvas.saveState()
    page_canvas.translate(x, y)
    page_canvas.rotate(270)
    page_canvas.drawCentredString(0, 0, text)
    page_canvas.restoreState()


def generate_labels_sheet(qrcodes, position_offset=0, page=0):
    page_canvas = canvas.Canvas(f"print-{page}.pdf", pagesize=letter, bottomup=0)

    index = 0
    font_size = 7
    page_canvas.setFont("Helvetica-Bold", font_size)

    # generator
    positions = _label_pos_generator(QR_CODES_PER_LABEL)

    # Skips the offset
    for _ in range(position_offset):
        next(positions)

    # Add each qrcode
    for qrcode in qrcodes:
        try:
            x, y = next(positions)
        except StopIteration:
            break

        # Draw grid
        # canvas.rect(x, y, LABEL['Largura']/QR_CODES_PER_LABEL, LABEL["Altura"], stroke=1, fill=0)

        # Draw indexes bellow QRCODE
        # canvas.drawString(x+LABEL["Altura"], y+LABEL["Altura"], f'{index}')

        # Draw indexes right of the QRCODE
        _add_vertical_text(x + LABEL["Altura"] + font_size/2, y + LABEL["Altura"]/2, qrcode.short_name, page_canvas)

        # Add QRCODE
        _add_image(qrcode.generate_qr_code(), page_canvas, x, y, margin=1*mm)

        index += 1
        print(f"qrcode {index} of {len(qrcodes)} done!")

    page_canvas.save()
    print(f"{index} labels printed.")

    remaining_labels = QR_CODES_PER_SHEET - (len(qrcodes) + position_offset)
    if remaining_labels >= 0:
        print(f"Sobraram {remaining_labels} QRCODES na folha")
    else:
        print(f"Restam {-remaining_labels} QRCODES a serem impressos.")
        generate_labels_sheet(qrcodes[QR_CODES_PER_SHEET:], position_offset, page+1)


if __name__ == '__main__':
    qr_codes = [qrcode for qrcode in generate_basic_qrcodes(240)]
    generate_labels_sheet(qr_codes, 30)
