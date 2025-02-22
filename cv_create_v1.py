from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
import yaml
from yaml.loader import SafeLoader

left_padding = 0
bottom_padding = 0
width, height = A4
step = 0.5 * cm

light, dark, medium, txt = (219, 228, 250), (10, 16, 69), (11, 147, 235), (7, 21, 54)

canvas = Canvas("example_1.pdf")
# Constants for right column
r_height = height - 5 * cm        # Height to start
r_width = width * 0.66 + step / 2 # Divide page on 2 parts
text_length = width * 0.34 - step
# Style for left sie of the page
my_Style = ParagraphStyle('My style',
                          fontName="Times-Italic",
                          backColor='#EDF2FD',
                          fontSize=11,
                          borderColor='#EDF2FD',
                          borderWidth=0,
                          borderPadding=(5, 5, 5),
                          leading=16,
                          alignment=4,
                          leftIndent=10,
                          textColor='#071536'
                          )
# Style for right side
my_Style_2 = ParagraphStyle('My style 2',
                            fontName="Times-Italic",
                            backColor='#0A1045',
                            fontSize=12,
                            borderColor='#0A1045',
                            borderWidth=0,
                            borderPadding=(0, 0, 0),
                            leading=15,
                            alignment=0,
                            leftIndent=0,
                            textColor='#EDF2FD'
                            )

# load of parameters to put into CV
class Font:
    def __init__(self, face, size):
        self.face = face
        self.size = size

    def set_font(self, string):
        return f""" <font face="{self.face}" fontSize= "{self.size}"> {string} </font>"""

bold_times_12 = Font("times-bold", 12)
times_12 = Font("times", 12)

with open('my_parameters.yaml', encoding='utf-8') as f:
    data = yaml.load(f, Loader=SafeLoader)

def set_color(color):
    return canvas.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)


def set_employment_history(job_data, main_canvas):
    """ set job_data from Employment history part """
    height_to_draw = height - 2.2 * cm
    for company, category in job_data.items():
        company_name =  bold_times_12.set_font(company)
        place =  bold_times_12.set_font(category["Place"])
        position = bold_times_12.set_font(f' Position - {category["Position"]}')
        dates =  times_12.set_font(category["Dates"])
        for text_line in [company_name + place , '**' + position + '**' +  dates]:
            sample = Paragraph(text_line, my_Style)
            wR, hR = sample.wrapOn(main_canvas, r_width - step, height)
            height_to_draw -= (hR + .2 * step)
            sample.drawOn(main_canvas, 0, height_to_draw)

        for key, value in category.items():
            if key not in ["Place", "Position", "Dates"]:
                #print(f"{key} - {value}")
                line = f'{key}: {value}  <BR/>'

                p = Paragraph(line, my_Style)
                wR, hR = p.wrapOn(main_canvas, r_width - step, height)
                height_to_draw -= (hR + .2 * step)
                p.drawOn(main_canvas, 0, height_to_draw)

    print("Employment History is putted")
    return wR, hR

class Counter:
    COUNT = 0

    def count(self):
        Counter.COUNT += 1
        return Counter.COUNT

    def count_reset(self):
        Counter.COUNT = 0
        return Counter.COUNT


counter = Counter()


def set_color(color):
    return canvas.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)


def set_details_par(name: dict[str | str], main_canvas, height_to_put, width_to_put):
    input_text = Font("times-bold", 16).set_font(name.__name__)
    add_h, add_w = canvas.drawString(width_to_put,  height_to_put, input_text)
    for key, value in data[name].items():
        line = f'{key}: {value}  <BR/>'
        input_text += line
        p = Paragraph(input_text, my_Style_2)
        rW, rH = p.wrapOn(main_canvas, text_length - 1, 500)
        p.drawOn(main_canvas, r_width, r_height - rH)
    print("Details is putted")
    return r_height - rH

def set_details_dict(name: dict[str | str], main_canvas):
    main_canvas.setFillColor('#EDF2FD')
    height = r_height
    input_text = f""" <font face="times-bold" fontSize= "16"> {name} </font>  <BR/>"""
    for key, value in data[name].items():
        line = f'{key}: {value}  <BR/>'
        input_text += line
        p = Paragraph(input_text, my_Style_2)
        rW, rH = p.wrapOn(main_canvas, text_length - 1, 500)
        p.drawOn(main_canvas, r_width, r_height - rH)
    print("Details is putted")
    return r_height - rH


def set_details(name):
    #    main_canvas.setFillColor('#EDF2FD')
    canvas.setFont("Times-Bold", 16)
    height = r_height
    canvas.drawString(r_width, height, name)
    counter.count()
    height -= .5 * step
    canvas.setFont("Times-Italic", 12)
    input_text = data[name]
    for key, value in input_text.items():
        height -= step
        line = f'{key}: {value}'
        #print(line)
        #print(canvas.stringWidth(line, "Times-Italic", 10), .33 * width + step / 2)
        if canvas.stringWidth(line, "Times-Italic", 12) < .33 * width + step / 2:
            canvas.drawString(r_width, height, line)
            counter.count()
        else:
            list_line = line.split(',')
            #print(list_line)
            canvas.drawString(r_width, height, list_line[0])
            counter.count()
            height -= step
            for line in list_line[1:]:
                canvas.drawString(r_width + cm, height, f" - {line};")
                if line != list_line[-1]:
                    counter.count()
                    height -= step
    print("Details is putted")

def set_links(name, work_canvas):
    input_text = data[name]
    set_color(light)
    work_canvas.setFont("Times-Bold", 16)
    h = r_height - step
    #main_canvas.drawString(w_width, h, "Public profile & URL")
    #counter.count()
    work_canvas.setFont("Times-Italic", 10)
    h -= step
    for key, line in input_text.items():
        file_name = key + '.png'
        work_canvas.drawImage(file_name, r_width, h - step / 3, width=step, height=step, mask='auto')
        if work_canvas.stringWidth(line, "Times-Italic", 10) < text_length:
            work_canvas.drawString(r_width + step + 6, h, line)
            counter.count()
            h -= step
        else:
            list_line = line.split('-')
            new_line = "-".join(list_line[:-1])
            work_canvas.drawString(r_width + step + 6, h, new_line)
            counter.count()
            h -= step
            n_width = width - step - work_canvas.stringWidth("-".join(list_line[-1:]), "Helvetica-Oblique", 12)
            work_canvas.drawString(n_width, h, '-' + "-".join(list_line[-1:]))
            counter.count()
            h -= step
    print("Public profile & URL is putted")
    print(Counter.COUNT)


def put_contacts(c, dates):
    table_data = []
    text_len = width * 0.34 - 30
    print(f'text_len: {text_len}')
    hD = r_height
    for key, value in data[dates].items():
        img = Image(f"{key}.png", 25, 25)
        text_line = value


        input_text = Paragraph(text_line, my_Style_2)

        table_data.append([img, input_text])

    #print(table_data)
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), '#0A1045'),
                               ("FONT", (1, 0), (-1, -1), "Times-Italic", 12),
                               ("LEFTPADDING", (0, 0), (-1, -1), 1),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                               ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (1, 1), (-1, -1), 1),
                               ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
                               ('TEXTCOLOR', (1, 0), (-1, -1), '#EDF2FD')]))
    table_width = width * 0.34
    print(f'table_width: {table_width}')
    w, h = table.wrapOn(c, 160, table_width)
    print(h, w)
    wR = width * 0.66 + 15
    hR = hD - h
    table.drawOn(c, wR, hR)
    print("contacts is putted")
    return hR


set_color(dark)
canvas.rect(left_padding, bottom_padding, width, height, fill=1)

canvas.setFillColor('#EDF2FD')
canvas.rect(left_padding, bottom_padding, width * 0.66, height, fill=1)
text = data['Moto']['Voltaire']
set_color(txt)
canvas.setFont("Times-Italic", 12)
canvas.drawString(width * 0.66 - canvas.stringWidth(text.split('.')[0], "Times-Italic", 12) - step, height - cm,
                  text.split('.')[0] + ".")
canvas.drawString(width * 0.66 - canvas.stringWidth(text.split('.')[1], "Times-Italic", 12) - 14,
                  height - cm - step, text.split('.')[1])
canvas.setFont("Times-Roman", 16)
set_color(txt)
set_details('Details')
r_height = set_details_par('Details', canvas) - .5 * step
d = 5 * cm - 2 * step
x = width * 0.83 - d / 2
y = height - 5 * cm + step
canvas.drawImage('my_photo.png', x, y, width=d, height=d, mask='auto')

r_height = put_contacts(canvas, 'Public profile & URL') - 2 * step

set_details('Languages')
r_height = r_height - step - 5.5 * step
set_details('Soft Skills')
r_height = r_height - step - 6.5 * step
set_details('Hard Skills')

canvas.setFont("Times-Bold", 15)
set_color(txt)
canvas.drawString(25, height - 2 * cm, 'Employment History')
set_employment_history(data['Employment History'], canvas)
h_to_draw = height - 23.7 * cm
canvas.drawString(25, h_to_draw, 'Education')
h_to_draw = h_to_draw - 0.2 * cm
for key, value in data["Education"].items():
    text = bold_times_12.set_font(string=key) + ': ' + times_12.set_font(string=value)
    p = Paragraph(text, my_Style)
    wR, hR = p.wrapOn(canvas, r_width - step, height)
    h_to_draw -= (hR + .2 * step)
    p.drawOn(canvas, 0, h_to_draw)
h_to_draw = h_to_draw - .7 * cm
canvas.drawString(25, h_to_draw, 'Training courses')
h_to_draw = h_to_draw - 0.2 * cm
for key, value in data["Training courses"].items():
    text = bold_times_12.set_font(string=key) + ': ' + times_12.set_font(string=value)
    p = Paragraph(text, my_Style)
    wR, hR = p.wrapOn(canvas, r_width - step, height)
    h_to_draw -= (hR + .2 * step)
    p.drawOn(canvas, 0, h_to_draw)

canvas.showPage()

canvas.save()
