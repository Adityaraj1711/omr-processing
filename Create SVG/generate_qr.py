import qrcode.image.svg
import datetime
from bs4 import BeautifulSoup as bso
today_date = datetime.date.today()


# define a method to choose which factory method to use
# possible values 'basic' 'fragment' 'path'
method = "basic"
qr_size = 6
company_name = input('enter name of company: ')
take_paper_code = input('enter paper code? (y/n): ')
question_code = 'NULL'
if take_paper_code == 'y' or take_paper_code == 'Y':
    question_code = input('enter paper code')
exam_date = ''
take_exam_date = input('want to enter the exam date? (y/n): ')
if take_exam_date == 'y' or take_exam_date == 'Y':
    exam_date = input('enter date( format is dd-mm-yyyy): ')
else:
    exam_date = datetime.date.today().strftime('%d-%m-%Y')
variant_no = int(input('enter variant number: '))
question_count = int(input('enter number of questions: '))

data = company_name + ' ' + question_code + ' ' + exam_date + ' ' + str(variant_no) + ' ' + str(question_count)

show_error = False
if method == 'basic':
    # Simple factory, just a set of rectangles.
    factory = qrcode.image.svg.SvgImage
elif method == 'fragment':
    # Fragment factory (also just a set of rectangles)
    factory = qrcode.image.svg.SvgFragmentImage
elif method == 'path':
    # Combined path factory, fixes white space that may occur when zooming
    factory = qrcode.image.svg.SvgPathImage

# Set data to qrcode
img = qrcode.make(data, image_factory=factory)

# Save svg file somewhere
img.save("qrcode.svg")

file = open('./qrcode.svg', encoding='utf-8')
new_file = str(file.read()).split('mm')

final_qr = new_file[0][0]
for idx, val in enumerate(new_file[:-1]):
    char = val[-1]
    number = ''
    i = -1
    while char != '"':
        number += char
        char = val[i-1]
        i -= 1
    number = number[::-1]
    final_qr += val[1:i]
    try:
        if len(number) != 0:
            final_qr += str('"' + str(int(number)*qr_size) + '"')
    except:
        print('error in qr code generation')
        show_error = True
final_qr += new_file[-1][1:]

with open('newqrcode.svg', 'a+') as svg:
    svg.truncate(0)
    svg.write(final_qr)

s = ''
with open('newqrcode.svg') as svg:
    our_soup = bso(svg.read(), 'lxml')
    all_child = our_soup.find('svg')
    for child in all_child.findChildren():
        s += str(child)[:-8] + '/>\n'

with open('svg/part2.svg', 'a+') as write_file:
    write_file.truncate(0)
    write_file.write(s)

svg_file_name = input('Enter the svg file name you want to save : ')

with open('omr_svg/' + svg_file_name + '.svg', 'w') as svg_file:
    file = ''
    with open('svg/part1.svg', 'r') as p1:
        file += str(p1.read()) + '\n'
    with open('svg/part2.svg', 'r') as p2:
        file += str(p2.read()) + '\n'
    with open('svg/part3.svg', 'r') as p3:
        file += str(p3.read()) + '\n'
    svg_file.write(file)
