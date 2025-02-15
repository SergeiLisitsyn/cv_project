from PIL import Image, ImageFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
import yaml
from yaml.loader import SafeLoader

left_padding = 0
bottom_padding = 0
width, height = A4
step = 0.5 * cm
# dark, light, medium, txt  = (219, 228, 250), (22, 62, 162), (11, 147, 235), (7, 21, 54)
light, dark, medium, txt = (219, 228, 250), (10, 16, 69), (11, 147, 235), (7, 21, 54)

canvas = Canvas("example_1.pdf")
# Constants for right column
r_height = height - 5 * cm
r_width = width * 0.66 + step / 2
text_length = width * 0.34 - step

my_Style = ParagraphStyle('My style',
                          fontName="Helvetica-Oblique",
                          backColor='#EDF2FD',
                          fontSize=12,
                          borderColor='#EDF2FD',
                          borderWidth=0,
                          borderPadding=(5, 5, 5),
                          leading=16,
                          alignment=4,
                          leftIndent=10,
                          textColor='#071536'
                          )

my_Style_2 = ParagraphStyle('My style 2',
                          fontName="Helvetica-Oblique",
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

# load of parameters
with open('D:\Work\python\pdf\cv\my_parameters.yaml', encoding='utf-8') as f:
    data = yaml.load(f, Loader=SafeLoader)
for key, value in data.items():
    print(f"{key} - {value}")

def set_Employment_History(data, canvas):
    """ set data from Employment history part """
    h  = height - step
    h_to_draw = height - 2.2 * cm
    for company, category in data.items():

        text = f'<font face="times-bold" fontSize= "11">  {company} - {category["Place"]}; ' \
               f'Position - {category["Position"]}</font> <BR/> <font color="#EDF2FD"> **** </font><font face="times" fontSize= "12" > {category["Dates"]} </font> <BR/> '
   #            <i>{category["Responsibility"]}</i>
        sample = Paragraph(text, my_Style)
        #print(r_width , h)
        wR, hR = sample.wrapOn(canvas, r_width-step, height)
        #print(f'width: {wR}, height: {hR}')
        h_to_draw -= (hR + .2 * step)
        #print(f"draw_height: {h_to_draw}")
        sample.drawOn(canvas, 0, h_to_draw)
        for key, value in category.items():
            if key not in ["Place", "Position", "Dates"]:
                print(f"{key} - {value}")
                line = f'{key}: {value}  <BR/>'

                p = Paragraph(line, my_Style)
                wR, hR = p.wrapOn(canvas, r_width-step, height)
                h_to_draw -= (hR + .2 * step)
                p.drawOn(canvas, 0, h_to_draw)

    print("Employment History is putted")



class Counter:
    COUNT = 0

    def count(self):
        Counter.COUNT += 1
        return Counter.COUNT

    def count_reset(self):
        Counter.COUNT = 0
        return Counter.COUNT


counter = Counter()


def set_Color(color):
    return canvas.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)



def set_Details_par(name, canvas):
    canvas.setFillColor('#EDF2FD')
    height = r_height
    text = f""" <font face="helvetica-bold" fontSize= "16"> {name} </font>  <BR/>"""
    for key, value in data[name].items():
        line = f'{key}: {value}  <BR/>'
        text += line
        p = Paragraph(text, my_Style_2)
        rW, rH = p.wrapOn(canvas, text_length -1, 500)
        p.drawOn(canvas, r_width, r_height - rH)
    print("Details is putted")
    return r_height - rH

def set_Details(name):
#    canvas.setFillColor('#EDF2FD')
    canvas.setFont("Helvetica-Bold", 16)
    height = r_height
    canvas.drawString(r_width, height, name)
    counter.count()
    height -= .5 * step
    canvas.setFont("Helvetica-Oblique", 12)
    text = data[name]
    for key, value in text.items():
        height -= step
        line = f'{key}: {value}'
        print(line)
        print(canvas.stringWidth(line, "Helvetica-Oblique", 10), .33  * width + step/2)
        if canvas.stringWidth(line, "Helvetica-Oblique", 12) < .33  * width + step/2:
            canvas.drawString(r_width, height, line)
            counter.count()
        else:
            list_line = line.split(',')
            print(list_line)
            canvas.drawString(r_width, height, list_line[0])
            counter.count()
            height -= step
            for line in list_line[1:]:
                canvas.drawString(r_width + cm, height, f" - {line};")
                if line != list_line[-1]:
                    counter.count()
                    height -= step
    print("Details is putted")


def set_Links(name, canvas):
    text = data[name]
    set_Color(light)
    canvas.setFont("Helvetica-Bold", 16)
    h = r_height - step
    #canvas.drawString(r_width, h, "Public profile & URL")
    #counter.count()
    canvas.setFont("Helvetica-Oblique", 10)
    h -= step
    for key, line in text.items():
        file_name = key + '.png'
        canvas.drawImage(file_name, r_width, h - step / 3, width=step, height=step, mask='auto')
        if canvas.stringWidth(line, "Helvetica-Oblique", 10) < text_length:
            canvas.drawString(r_width + step + 6, h, line)
            counter.count()
            h -= step
        else:
            list_line = line.split('-')
            new_line = ("-").join(list_line[:-1])
            canvas.drawString(r_width + step + 6, h, new_line)
            counter.count()
            h -= step
            n_width = width - step - canvas.stringWidth(("-").join(list_line[-1:]), "Helvetica-Oblique", 12)
            canvas.drawString(n_width, h, '-' + ("-").join(list_line[-1:]))
            counter.count()
            h -= step
    print("Public profile & URL is putted")
    print(Counter.COUNT)


def set_Languages(name):
    text = data[name]
    set_Color(light)
    canvas.setFont("Helvetica-Bold", 16)
#    h = r_height - step * counter.COUNT - 8 * cm
    h = r_height
    canvas.drawString(r_width, h, name)
    counter.count()
    canvas.setFont("Helvetica-Oblique", 12)
    for key, value in text.items():
        h -= step
        line = f'{key}'
        canvas.drawString(r_width, h, line)
        counter.count()
        h -= step / 2
        canvas.rect(r_width, h, text_length, 0.1 * cm, fill=1)
        set_Color(medium)
        canvas.rect(r_width + text_length * value / 5, h, text_length * (5 - value) / 5, 0.1 * cm, fill=1)
        set_Color(light)
    print(Counter.COUNT)
    print("Langages are putted")


def set_line_lengh(text, font, size):
    line_length = width * 0.66 - 2 * step
    lines = []
    if canvas.stringWidth(text, font, size) >= line_length:
        text_list = text.split(' ')
        i = 0
        while i < len(text_list):
            line = ''
            while canvas.stringWidth(line, font, size) < line_length:
                line = line + text_list[i] + ' '
                i += 1
            lines.append(line)
    else:
        lines.append(text)
    return lines

def put_contacts(c, dates):
    table_data = []
    text_length = width * 0.34 - 30
    print(f'text_length: {text_length}')
    hD = r_height

    #canvas.drawString(r_width, hD, dates)
    #hD -= step

    for key, value in data[dates].items():
        img = Image(f"{key}.png", 25, 25)
        text_line = value
        real_length = c.stringWidth(text_line, "Helvetica-Oblique", 12)
        print(f'real_length: {real_length}')
        if real_length > text_length:
            lines = value.split('-')
            new_line = ("-").join(lines[:-1])
            text_line = (" ").join([new_line, "-" + lines[-1]])
            if c.stringWidth(text_line, "Helvetica-Oblique", 12) > text_length:
                lines = value.split('/')
                new_line = ("/").join(lines[:-1]) +'/'
                text_line = (" ").join([new_line, lines[-1]])
        text = Paragraph(text_line, my_Style_2)
        table_data.append([img, text])

    #print(table_data)
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1),  '#0A1045'),
                               ("FONT", (1, 0), (-1, -1), "Helvetica-Oblique", 12),
                               ("LEFTPADDING", (0, 0), (-1, -1), 1),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                               ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (1, 1), (-1, -1), 1),
                               ('TEXTCOLOR', (1, 0), (-1, -1),'#EDF2FD')]))
    table_width = width * 0.34

    w, h = table.wrapOn(c, 50, table_width)
    print(h, w)
    wR = width * 0.66 + 10
    hR = hD - h
    table.drawOn(c, wR, hR)
    print("contacts is putted")
    return hR

set_Color(dark)
canvas.rect(left_padding, bottom_padding, width, height, fill=1)

canvas.setFillColor('#EDF2FD')
canvas.rect(left_padding, bottom_padding, width * 0.66, height, fill=1)
text = data['Moto']['Voltair']
set_Color(txt)
canvas.setFont("Helvetica-Oblique", 12)
canvas.drawString(width * 0.66 - canvas.stringWidth(text.split('.')[0], "Helvetica-Oblique", 12) - step, height - cm,
                  text.split('.')[0] + ".")
canvas.drawString(width * 0.66 - canvas.stringWidth(text.split('.')[1], "Helvetica-Oblique", 12) - 14,
                  height - cm - step, text.split('.')[1])
canvas.setFont("Helvetica", 16)
set_Color(txt)
set_Details('Details')
r_height = set_Details_par('Details', canvas) - .5 * step
d = 5 * cm - 2 * step
x = width * 0.83 - d / 2
y = height - 5 * cm + step
canvas.drawImage('my_photo.png', x, y, width=d, height=d, mask='auto')

r_height = put_contacts(canvas, 'Public profile & URL') - 2 * step

set_Details('Languages')
r_height = r_height - step - 5.5 * step
set_Details('Soft Skills')
r_height = r_height - step - 6.5 * step
set_Details('Hard Skills')
#r_height -= 1 * cm
#set_Languages('Skils')
canvas.setFont("Times-Bold", 15)
set_Color(txt)
canvas.drawString(25, height - 2 * cm, 'Employment History')
set_Employment_History(data['Employment History'], canvas)
h_to_draw = height - 23.4 * cm
canvas.drawString(25, h_to_draw, 'Education')
h_to_draw = h_to_draw - 0.2 * cm
for key, value in data["Education"].items():
    text = f'<font face="times-bold" fontSize= "12">  {key}: </font><font face="times" fontSize= "12" > {value} </font>'

    p = Paragraph(text, my_Style)
    wR, hR = p.wrapOn(canvas, r_width - step, height)
    h_to_draw -= (hR + .2 * step)
    p.drawOn(canvas, 0, h_to_draw)
h_to_draw = h_to_draw - .7 * cm
canvas.drawString(25, h_to_draw, 'Training coures')
h_to_draw = h_to_draw - 0.2 * cm
for key, value in data["Training coures"].items():
    text = f'<font face="times-bold" fontSize= "12">  {key}: </font><font face="times" fontSize= "12" > {value} </font>'
    p = Paragraph(text, my_Style)
    wR, hR = p.wrapOn(canvas, r_width - step, height)
    h_to_draw -= (hR + .2 * step)
    p.drawOn(canvas, 0, h_to_draw)

#set_Details_par('Training coures', canvas)
canvas.showPage()

canvas.save()
