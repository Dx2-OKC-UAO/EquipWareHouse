import xlsxwriter
import openpyxl
from datetime import datetime
import os


def create_file():
    day = datetime.now()
    now = day.strftime("%Y_%m_%d_%H_%M_%S")
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    fin = 'Отчет ' + now + '.xlsx'
    workbook.save(fin)
    os.rename(fin, ('Отчеты/' + fin))
    return fin


def create_file_between():
    day = datetime.now()
    now = day.strftime("%Y_%m_%d_%H_%M_%S")
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    fin = 'Отчет по промежутку ' + now + '.xlsx'
    workbook.save(fin)
    os.rename(fin, ('Отчеты/' + fin))
    return fin
