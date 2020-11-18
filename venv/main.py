from datetime import date, timedelta
from time import strptime
from pylatex import Document, LongTabu, HFill, Command, NoEscape, Package, Tabularx, Enumerate
import calendar, locale
from pylatex.utils import bold

day1 = "четверг"
day2 = "воскресенье"
year = 2020
month = "Ноябрь"
cleaners = ["Сергей", "Иван"]

def get_month_number(month_name):
    try:
        a = list(calendar.month_name).index(month_name)
    except:
        a = -1
    return a

def get_day_number(day_name):
    try:
        a = list(calendar.day_name).index(day_name)
    except:
        a = -1
    return a

def get_all_nth_days_in_month(day, month):
    temp_date = date(year, month,1)
    array = []
    try:
        while temp_date.weekday() != day:
            temp_date += timedelta(days = 1)
        while temp_date.month == month:
            array.append(temp_date.day)
            temp_date += timedelta(days = 7)
    except:
        return -1
    finally:
        return array

def create_table_pattern(array):
    a = ""
    for i in array:
        a += "|X"
    a += "|X|"
    return a

def create_row(names, days_amount, order):
    a = [""] * days_amount
    for i in range(len(a)):
        if (i + order + 1 - (days_amount % len(names))) % len(names) == 0:
            a[i] = "*"
    return [names[order]] + a[::-1]

locale.setlocale(locale.LC_ALL, 'ru_RU')
dates = get_all_nth_days_in_month(get_day_number(day1), get_month_number(month)) + get_all_nth_days_in_month(get_day_number(day2), get_month_number(month))
dates.sort(reverse=False)

doc = Document()
doc.documentclass = Command(
    'documentclass',
    options=['14pt', 'a4paper'],
    arguments=['article'],
)

doc.packages.append(Package('babel', options=["russian"]))
doc.packages.append(Package('extsizes', options=["14pt"]))
doc.packages.append(Package('inputenc', options=["utf8"]))
doc.packages.append(Package('color', options=["usenames,dvipsnames"]))
doc.packages.append(Package('geometry', options=["left=20mm, top=15mm, right=15mm, bottom=15mm, footskip=10mm"]))
doc.packages.append(Package('setspace'))
doc.packages.append(Package('amsmath'))


doc.preamble.append(Command('title','Уборка 1205'))
doc.preamble.append(Command('author',''))
doc.preamble.append(Command('date', str(month)+' '+str(year)))

doc.append(NoEscape(r'\maketitle'))
doc.append(Command("thispagestyle", "empty"))


with doc.create(Tabularx(create_table_pattern(dates))) as data_table:
    header_row1 = [""]+dates
    data_table.add_hline()
    data_table.add_row(header_row1, mapper=[bold])
    data_table.add_hline()
    for i in range(len(cleaners)):
        data_table.add_row(create_row(cleaners, len(dates), i))
        data_table.add_hline()

doc.append(Command("newline"))
doc.append(Command("newline"))

doc.append("Уборка включает в себя:")
with doc.create(Enumerate()) as enum:
    enum.add_item("Ванная комната: ванная, полы, пыль с доступных поверхностей")
    enum.add_item("Туалет: полы, унитаз")
    enum.add_item("Коридор: полы")

doc.generate_tex("generated")
