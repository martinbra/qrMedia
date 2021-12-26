import reportlab

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import letter

def cm_to_points(cm):
    # inches = cm / 2.54
    # points = inches * DPI
    points = (DPI * cm) / 2.54
    return points


LABEL_CM = {
    "Margem Superior": 1.27,
    "Margem Esquerda": 1.45,
    "Espaçamento Vertical": 1.27,
    "Espaçamento Horizontal": 4.75,
    "Altura": 1.27,
    "Largura": 4.44,
    "Colunas": 4,
    "Linhas": 20,
}
DPI = 72
QRCODE_SIZE_CM = 3.3  # mm/10

LABEL = {key: cm_to_points(val) for key, val in LABEL_CM.items()}
LABEL["Colunas"] = LABEL_CM["Colunas"]
LABEL["Linhas"] = LABEL_CM["Linhas"]


def label_pos_generator(qrcodes_per_label=1):
    for linha in range(LABEL['Linhas']):
        y_pos = (LABEL['Margem Superior'] +
                 linha * LABEL['Espaçamento Vertical'])

        for coluna in range(LABEL['Colunas']):
            for div in range(qrcodes_per_label):
                x_pos = (LABEL['Margem Esquerda'] +
                         coluna * LABEL['Espaçamento Horizontal'] +
                         div * LABEL["Largura"]/qrcodes_per_label)

                yield x_pos, y_pos


def scale(drawing, scaling_factor):
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


def add_image(image_path, canvas, x, y):
    drawing = svg2rlg(image_path)
    scaling_factor = LABEL_CM["Altura"] / QRCODE_SIZE_CM
    scaled_drawing = scale(drawing, scaling_factor=scaling_factor)
    renderPDF.draw(scaled_drawing, canvas, x, y)


def add_vertical_text(x, y, text, canvas):
    canvas.saveState()
    canvas.translate(x, y)
    canvas.rotate(270)
    canvas.drawCentredString(0, 0, text)
    canvas.restoreState()


if __name__ == '__main__':
    canvas = canvas.Canvas('print.pdf', pagesize=letter, bottomup=0)
    width, height = letter

    index = 1
    qrcodes_per_label = 3
    font_size = 8
    canvas.setFont("Helvetica-Bold", font_size)

    for x, y in label_pos_generator(qrcodes_per_label):
        # Draw grid
        # canvas.rect(x, y, LABEL['Largura']/qrcodes_per_label, LABEL["Altura"], stroke=1, fill=0)

        # Draw indexes
        # canvas.drawString(x+LABEL["Altura"], y+LABEL["Altura"], f'{index}')
        add_vertical_text(x+LABEL["Altura"]+font_size/2, y+LABEL["Altura"]/2, f'{index}', canvas)

        # Add QRCODE
        add_image(f"qrcodes/{index}.svg", canvas, x, y)

        print(f"qrcode {index} done!")
        index += 1

    canvas.save()
    print(LABEL['Largura']/qrcodes_per_label-LABEL["Altura"])