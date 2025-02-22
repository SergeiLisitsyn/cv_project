from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
import yaml
from yaml.loader import SafeLoader

# Создаем холст.
c = Canvas("cv_Sergei_Lisitsyn_de.pdf", pagesize=A4)
width, height = A4
step = 18
r_height = height - 3 * cm  # Height to start
l_width, r_width = 14 * cm, 7 * cm  # Divide page on 2 parts

light = HexColor("#EDF2FD")
dark = HexColor('#071536')

base_style = ParagraphStyle('base_style',
                            fontName="Times-Bold",
                            backColor=light,
                            fontSize=12,
                            borderColor=light,
                            borderWidth=0,
                            borderPadding=(0.),
                            leading=14,
                            alignment=4,
                            leftIndent=28,
                            rightIndent=14,
                            textColor=dark
                            )

my_Style_2 = ParagraphStyle('My style 2',
                            fontName="Times-Italic",
                            backColor=dark,
                            fontSize=12,
                            borderColor=dark,
                            borderWidth=0,
                            borderPadding=0.,
                            leading=15,
                            alignment=0,
                            leftIndent=0,
                            textColor=light
                            )


class Font:
    def __init__(self, face, size):
        self.face = face
        self.size = size

    def set_font(self, string):
        return f""" <font face="{self.face}" fontSize= "{self.size}"> {string} </font>"""


bold_times_12 = Font("times-bold", 12)
times_12 = Font("times-italic", 12)

with open('meine_parameter.yaml', encoding='utf-8') as f:
    data = yaml.load(f, Loader=SafeLoader)


# print(w_height/cm, width/cm, cm, inch)
def base_page(canvas: Canvas, l_color: HexColor, r_color: HexColor):
    canvas.setFillColor(l_color)
    canvas.rect(0, 0, l_width, height, fill=1)
    canvas.setFillColor(r_color)
    canvas.rect(l_width, 0, width, height, fill=1)


def employment_data(data_dict: [str | str], can: Canvas, start_w, start_h, total_w):
    for key, value in data_dict.items():

        if isinstance(value, dict):
            can.setFont("Times-Bold", 12)
            can.setFillColor(dark)
            #can.drawString(start_w, start_h, key + ': ')
            html_text = (f'<font name="Times-Bold" size="12">{key}: '
                         f' </font><font name="Times-Italic" size="12">{data_dict[key]['Ort']} </font> ')

            p = Paragraph(html_text, base_style)
            _, res_h = p.wrapOn(can, total_w - 5, 500)
            p.drawOn(can, start_w - 23, start_h - res_h + base_style.fontSize)
            start_h -= res_h

            text = c.beginText(19, start_h)
            text.setFont('Times-Bold', 12)
            text.textOut(f' Position - {data_dict[key]["Position"]}   ')
            text.setFont('Times-BoldItalic', 10)
            text.textOut(f' {data_dict[key]["Zeitraum"]}')
            c.drawText(text)
            start_h -= 16
            add_h = employment_data(value, can, start_w - 18, start_h, total_w - 18)
            start_h = add_h

        else:  # for rows such out of Name, 'Position', 'Dates', 'Place'
            if key not in ['Position', 'Zeitraum', 'Ort']:
                html_text = (f'<font name="Times-Bold" size="12">{key}:'
                             f' </font><font name="Times-Italic" size="12">{value} </font> ')
                p = Paragraph(html_text, base_style)
                _, res_h = p.wrapOn(can, total_w + 23, 500)
                p.drawOn(can, start_w - 23, start_h - res_h + base_style.fontSize)
                start_h -= res_h + 4

    return start_h


def data_dict(name, can: Canvas, start_w, start_h, total_w):
    can.setFont("Times-BoldItalic", 14)
    can.drawString(start_w + 18, start_h, name.upper())
    start_h -= + 16
    for key, value in data[name].items():
        html_text = (f'<font name="Times-Bold" size="12">{key}: '
                     f'</font><font name="Times-Italic" size="12">{value['Ort']}</font> ')
        p = Paragraph(html_text, base_style)
        _, res_h = p.wrapOn(can, total_w, 500)
        p.drawOn(can, start_w - 23, start_h - res_h + base_style.fontSize)
        start_h -= 2

        for item, val in value.items():
            if item != 'Ort':
                html_text = (f'<font name="Times-Bold" size="12">{item}: '
                             f'</font><font name="Times-Italic" size="12">{val} </font> ')
                p = Paragraph(html_text, base_style)
                _, res_h = p.wrapOn(can, total_w, 500)
                p.drawOn(can, start_w - 23, start_h - res_h)
                start_h -= res_h
        start_h -= 14
    print(f'data are put, {start_h}, ')
    return start_h


def education_dict(edu_dict, can: Canvas, start_w, start_h):
    can.setFont("Times-BoldItalic", 14)
    can.drawString(start_w, start_h, 'Ausbildung'.upper())
    start_h -= 16  # edu_dict['Name']
    input_string = can.beginText(start_w - 18, start_h)
    input_string.setFont('Times-Bold', 12)
    input_string.textOut(f' {edu_dict["Name"]}   ')
    input_string.setFont('Times-Italic', 12)
    input_string.textOut(f' {edu_dict["Zeitraum"]}')
    can.drawText(input_string)
    start_h -= 16
    for key, value in edu_dict.items():

        if key not in ['Name', 'Zeitraum']:
            input_string = can.beginText(start_w - 12, start_h)
            input_string.setFont('Times-Bold', 12)
            input_string.textOut(f'{key}:  ')
            input_string.setFont('Times-BoldItalic', 12)
            input_string.textOut(f'{value}')
            can.drawText(input_string)
            start_w += can.stringWidth(key + ':      ' + value, "Times-BoldItalic", 12)
    start_h -= 16

    return start_h


def set_details(name, canvas, w_width, w_height):
    canvas.setFont("Times-Bold", 14)
    canvas.drawString(w_width + 18, w_height, name.upper())
    canvas.setFont("Times-Italic", 12)
    input_text = data[name]
    for key, value in input_text.items():
        w_height -= step
        line = f'{key}: {value}'
        if canvas.stringWidth(line, "Times-Italic", 12) < .33 * width + 6:
            canvas.drawString(w_width, w_height, line)
        else:
            list_line = line.split(',')
            # print(list_line)
            canvas.drawString(w_width, w_height, list_line[0])
            w_height -= step
            for line in list_line[1:]:
                canvas.drawString(w_width + cm, w_height, f"  {line}")
                if line != list_line[-1]:
                    w_height -= step
    print("Details is putted")
    return w_height


def set_details_new(name, canvas, w_width, w_height):
    canvas.setFont("Times-Bold", 14)
    canvas.drawString(w_width + 18, w_height, name.upper())
    canvas.setFont("Times-Italic", 12)
    input_text = data[name]
    for key, value in input_text.items():
        w_height -= step
        html_text = (f'<font name="Times-Bold" size="12">{key}: '
                     f'</font><font name="Times-Italic" size="12">{value} </font> ')
        p = Paragraph(html_text, base_style)
        _, res_h = p.wrapOn(canvas, r_width + 18, 500)
        p.drawOn(canvas, w_width - 20, w_height)
        w_height -= res_h

    print("Details is putted")
    return w_height


def put_contacts(can, dates, w_height):
    table_data = []
    for key, value in data[dates].items():
        img = Image(f"{key}.png", 25, 25)
        text_line = value
        input_text = Paragraph(text_line, my_Style_2)
        table_data.append([img, input_text])
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), dark),
                               ("FONT", (1, 0), (-1, -1), "Times-Italic", 12),
                               ("LEFTPADDING", (0, 0), (-1, -1), 1),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                               ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (1, 1), (-1, -1), 1),
                               ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
                               ('TEXTCOLOR', (1, 0), (-1, -1), light)]))
    table_width = width * 0.34
    w, h = table.wrapOn(can, 160, table_width)
    wR = width * 0.66 + 20
    hR = w_height - h
    table.drawOn(can, wR, hR)
    print("contacts is putted")
    return hR


base_page(c, l_color=light, r_color=dark)
text = data['Motto']['Voltaire']
c.setFont("Times-BoldItalic", 14)
c.drawString(36, height - 52, 'Berufserfahrung'.upper())
c.setFont("Times-Italic", 12)
c.drawString(width * 0.66 - c.stringWidth(text.split('.')[0], "Times-Italic", 12) - step, height - cm,
             text.split('.')[0] + ".")
c.drawString(width * 0.66 - c.stringWidth(text.split('.')[1], "Times-Italic", 12) - 14,
             height - cm - step, text.split('.')[1])
t_height = employment_data(data['Berufserfahrung'], c, 36, height - 72, l_width)
t_height = education_dict(data['Ausbildung'], c, 36, t_height - 4)
t_height = data_dict('Trainingskurse', c, 18, t_height - 4, l_width - 18)
d = r_width - 2 * step
x = width * 0.83 - d / 2
y = height - d - step
c.drawImage('my_photo.png', x, y, width=d, height=d, mask='auto')
c.setFillColor(light)
l_height = set_details('Details', c, l_width + 3, height - d - 2 * step)
l_height = put_contacts(c, 'Öffentliches Profil & URL', l_height - 4)
l_height = set_details('Sprachen', c, l_width + 3, l_height - 24)
l_height = set_details('Soft Skills', c, l_width + 3, l_height - 24)
base_style.backColor = dark
base_style.textColor = light
l_height = set_details_new('Hard Skills', c, l_width, l_height - 24)
c.save()
