from math import *
from TechlogMath import *
from operator import *
import sys
if sys.version_info[0]==3:
    from six.moves import range

PI     = 3.14159265358979323846
PIO2   = 1.57079632679489661923
PIO4   = 7.85398163397448309616E-1
SQRT2  = 1.41421356237309504880
SQRTH  = 7.07106781186547524401E-1
E      = exp(1)
LN2    = log(2)
LN10   = log(10)
LOG2E  = 1.4426950408889634073599
LOG10E = 1.0 / LN10
MissingValue = -9999
def iif(condition, trueResult=MissingValue, falseResult=MissingValue):
	if condition:
		return trueResult
	else:
		return falseResult

#Declarations
#The dictionary of parameters v2.0
#name,bname,type,family,measurement,unit,value,mode,description,group,min,max,list,enable,iscombocheckbox,isused
parameterDict = {}
try:
	if Parameter:
		pass
except NameError:
	class Parameter:
		def __init__(self, **d):
			pass

__author__ = """Taras DOLGUSHIN (dolgushin.tyu)"""
__date__ = """2022-11-22"""
__version__ = """1.0"""
__pyVersion__ = """3"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""
__applyMode__ = """0"""
__awiEngine__ = """v2"""
__layoutTemplateMode__ = """"""
__includeMissingValues__ = """True"""
__keepPreviouslyComputedValues__ = """True"""
__areInputDisplayed__ = """True"""
__useMultiWellLayout__ = """True"""
__idForHelp__ = """"""
__executionGranularity__ = """full"""
#DeclarationsEnd
import TechlogDialogAdvanced as tda
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import win32com.client 
import datetime
import os
import re

excel = win32com.client.Dispatch('excel.application')
pathTarget =(r'\\10.62.176.27\PetroEngineering_1\Петроинжиниринг\01. ННГ\14. КонтролСкважины Отчеты')

listDir = []
for path in os.listdir(pathTarget):
	listDir.append(path)

dlg = tda.dialogAdvanced("Folder seeker")
dlg.addListBox('folder selector', 'Folder Selector', listDir)
dlg.execDialog()
targetDir = dlg.getListBox('folder selector')

listFile = []
for title in targetDir:
	pathTargetFldr = os.path.join(pathTarget, title)
	for path in os.listdir(pathTargetFldr):
		if os.path.isfile(os.path.join(pathTargetFldr, path)):
			listFile.append(path)

listFileClean = []
for fileClean in listFile:
	if 'Контрольные скважины' in fileClean:
		listFileClean.append(fileClean)
listFileClean.sort(reverse=True)

dlg = tda.dialogAdvanced("Reports simplifier")
dlg.addListBox('file selector', 'File Selector', listFileClean)
dlg.execDialog()
targetFile = dlg.getListBox('file selector')

for fileXls in targetFile:
	report_date = fileXls.split('_')[2]
	report_time = fileXls.split('_')[3]
	pathFinal = os.path.join(os.path.join(pathTarget, title), fileXls)
	wb = excel.Workbooks.Open(pathFinal)
	sheet = wb.ActiveSheet
	
	#Функция для поиска строки с нужным заголовком контрольки
	def oper_name_cell(text, qrow, col):
		result = []
		for row in range(1, qrow):
			if sheet.Cells(row,col).value == text:
				result = row
		return result, col
	
	#Функция выгрузки данных из контрольки в список Питона
	def load_data(sheet, chapter_cell, column):
		chapter_list = []
		#last_row = sheet.Cells(chapter_cell[0], column).CurrentRegion.Cells(sheet.Cells(burenie_cell[0], column).CurrentRegion.Cells.Count).Row
		cells_counter = sheet.Cells(chapter_cell[0], column).CurrentRegion.Rows.Count
		last_row = chapter_cell[0] + cells_counter
		for i in range(chapter_cell[0]+4, last_row+1):
			target_value = sheet.Cells(i, column).value
			chapter_list.append(target_value)
		return chapter_list
		
	def sheet_normalization(sheet_norm):
		sheet_norm.Columns(1).AutoFit()
		sheet_norm.Columns(1).VerticalAlignment = -4108
		sheet_norm.Columns(2).AutoFit()
		sheet_norm.Columns(2).VerticalAlignment = -4108
		sheet_norm.Columns(2).HorizontalAlignment = -4108
		sheet_norm.Columns(3).ColumnWidth = 70
		sheet_norm.Columns(3).WrapText = True
		sheet_norm.Columns(3).VerticalAlignment = -4108
		sheet_norm.Columns(4).ColumnWidth = 70
		sheet_norm.Columns(4).WrapText = True
		sheet_norm.Columns(4).VerticalAlignment = -4108
		return
	
	qrow= 500																		#Заведомо большОе количество строк для поиска заголовков
	col = 9 																				#Колонка где искать заголовки контрольки
	burenie_cell = oper_name_cell('Бурение', qrow, col)
	vns_cell = oper_name_cell('Ввод новых (освоение)', qrow, col)
	otkazy_cell = oper_name_cell('Текущие отказы на базовом фонде', qrow, col)
	zarezka = oper_name_cell('Зарезка бокового ствола', qrow, col)
	
	oilfield_name = load_data(sheet, burenie_cell, 10)
	well_num = load_data(sheet, burenie_cell, 11)
	pad_num = load_data(sheet, burenie_cell, 12)
	construction = load_data(sheet, burenie_cell, 14)
	start_drilll = load_data(sheet, burenie_cell, 17)
	type_gtm = load_data(sheet, burenie_cell, 21)
	status_morning = load_data(sheet, burenie_cell, 60)
	status_evening = load_data(sheet, burenie_cell, 61)
	
	oilfield_name_vns = load_data(sheet, vns_cell, 10)
	well_num_vns = load_data(sheet, vns_cell, 11)
	pad_num_vns =  load_data(sheet, vns_cell, 12)
	grp_vns =  load_data(sheet, vns_cell, 14)
	q_liq_vns = load_data(sheet, vns_cell, 44)
	wc_vns = load_data(sheet, vns_cell, 45)
	q_oil_vns = load_data(sheet, vns_cell, 46)
	status_morning_vns = load_data(sheet, vns_cell, 60)
	status_evening_vns = load_data(sheet, vns_cell, 61)
	
	oilfield_name_otk = load_data(sheet, otkazy_cell, 10)
	well_num_otk = load_data(sheet, otkazy_cell, 11)
	q_liq_otk = load_data(sheet, otkazy_cell, 44)
	wc_otk = load_data(sheet, otkazy_cell, 45)
	q_oil_otk = load_data(sheet, otkazy_cell, 46)
	status_morning_otk = load_data(sheet, otkazy_cell, 60)
	status_evening_otk = load_data(sheet, otkazy_cell, 61)
	
	oilfield_name_zar = load_data(sheet, zarezka, 10)
	well_num_zar = load_data(sheet, zarezka, 11)
	pad_num_zar = load_data(sheet, zarezka, 12)
	construction_zar = load_data(sheet, zarezka, 14)
	q_liq_zar = load_data(sheet, zarezka, 44)
	wc_zar = load_data(sheet, zarezka, 45)
	q_oil_zar = load_data(sheet, zarezka, 46)
	status_morning_zar = load_data(sheet, zarezka, 60)
	status_evening_zar = load_data(sheet, zarezka, 61)
	
	wb.Saved = True
	wb.Close()
	
	#Скрипт создания и настройки нового краткого отчета
	wb_new = excel.Workbooks.Add()
	
	sheet_otkazy = excel.Worksheets.Add()
	sheet_otkazy.Name = 'отказы_' + report_date
	
	sheet_zar = excel.Worksheets.Add()
	sheet_zar.Name = 'ЗБС_' + report_date
	
	sheet_vns = excel.Worksheets.Add()
	sheet_vns.Name = 'ВНС_' + report_date
	
	sheet_bur = excel.Worksheets.Add()
	sheet_bur = wb_new.ActiveSheet
	sheet_bur.Name = 'бурение_' + report_date
	sheet_bur.Rows(1).Font.Bold = True
	sheet_bur.Rows(1).HorizontalAlignment = -4108
	sheet_bur.Cells(1, 1).value = "Месторождение"
	sheet_bur.Cells(1, 2).value = "Скважина"
	sheet_bur.Cells(1, 3).value = "Куст"
	sheet_bur.Cells(1, 4).value = "Оборудование"
	sheet_bur.Cells(1, 5).value = "Факт нач бур-я"
	sheet_bur.Cells(1, 6).value = "6:00"
	sheet_bur.Cells(1, 7).value = "18:00"
	sheet_bur.Cells(1, 8).value = "Вид ГТМ"
	for j in range(len(oilfield_name)):
		sheet_bur.Cells(j+2, 1).value = oilfield_name[j]
		sheet_bur.Cells(j+2, 2).value = well_num[j]
		sheet_bur.Cells(j+2, 3).value =pad_num[j]
		try:
			sheet_bur.Cells(j+2, 4).value = construction[j].split('\n')[0]
		except:
			pass
		sheet_bur.Cells(j+2, 5).value =start_drilll[j]
		sheet_bur.Cells(j+2, 6).value = status_morning[j]
		sheet_bur.Cells(j+2, 7).value = status_evening[j]
		try:
			sheet_bur.Cells(j+2, 8).value = (type_gtm[j].split('\n')[0] + ' '+ type_gtm[j].split('\n')[1])
		except:
			pass
		
	sheet_bur.Columns(1).AutoFit()
	sheet_bur.Columns(1).VerticalAlignment = -4108
	sheet_bur.Columns(2).AutoFit()
	sheet_bur.Columns(2).VerticalAlignment = -4108
	sheet_bur.Columns(2).HorizontalAlignment = -4108
	sheet_bur.Columns(3).AutoFit()
	sheet_bur.Columns(3).VerticalAlignment = -4108
	sheet_bur.Columns(3).HorizontalAlignment = -4108
	sheet_bur.Columns(4).ColumnWidth = 30
	sheet_bur.Columns(4).Font.Size = 8
	sheet_bur.Columns(4).WrapText = True
	sheet_bur.Columns(4).HorizontalAlignment = -4131
	sheet_bur.Columns(4).VerticalAlignment = -4160
	sheet_bur.Cells(1, 4).Font.Size = 11
	sheet_bur.Cells(1, 4).HorizontalAlignment = -4108
	sheet_bur.Columns(5).ColumnWidth = 17
	sheet_bur.Columns(5).WrapText = True
	sheet_bur.Columns(5).HorizontalAlignment = -4108
	sheet_bur.Columns(5).VerticalAlignment = -4108
	sheet_bur.Columns(6).ColumnWidth = 70
	sheet_bur.Columns(6).WrapText = True
	sheet_bur.Columns(6).VerticalAlignment = -4108
	sheet_bur.Columns(7).ColumnWidth = 70
	sheet_bur.Columns(7).WrapText = True
	sheet_bur.Columns(7).VerticalAlignment = -4108
	sheet_bur.Columns(8).ColumnWidth = 8.5
	sheet_bur.Columns(8).Font.Size = 8
	sheet_bur.Columns(8).HorizontalAlignment = -4108
	sheet_bur.Columns(8).VerticalAlignment = -4108
	sheet_bur.Cells(1, 8).Font.Size = 11
	sheet_bur.Cells(1, 8).HorizontalAlignment = -4108
	
	
	sheet_vns.Rows(1).Font.Bold = True
	sheet_vns.Rows(1).HorizontalAlignment = -4108
	sheet_vns.Rows(1).VerticalAlignment = -4108
	sheet_vns.Cells(1, 1).value = "Месторождение"
	sheet_vns.Cells(1, 2).value = "Скважина"
	sheet_vns.Cells(1, 3).value = "Куст"
	sheet_vns.Cells(1, 4).value = "6:00"
	sheet_vns.Cells(1, 5).value = "18:00"
	sheet_vns.Cells(1, 6).value = "пар_раб_м3"
	sheet_vns.Cells(1, 7).value = "пар_раб_%"
	sheet_vns.Cells(1, 8).value = "пар_раб_тн"
	sheet_vns.Cells(1, 9).value = "ГРП порты и тоннаж"
	for j in range(len(oilfield_name_vns)):
		sheet_vns.Cells(j+2, 1).value = oilfield_name_vns[j]
		sheet_vns.Cells(j+2, 2).value = well_num_vns[j]
		sheet_vns.Cells(j+2, 3).value = pad_num_vns[j]
		sheet_vns.Cells(j+2, 4).value = status_morning_vns[j]
		sheet_vns.Cells(j+2, 5).value = status_evening_vns[j]
		sheet_vns.Cells(j+2, 6).value = q_liq_vns[j]
		sheet_vns.Cells(j+2, 7).value = wc_vns[j]
		sheet_vns.Cells(j+2, 8).value = q_oil_vns[j]
		try:
			sheet_vns.Cells(j+2, 9).value =(((grp_vns[j].split('ГРП:')[1])).split('Оборудование:')[0]).strip()
		except:
			sheet_vns.Cells(j+2, 9).value = ' '
	sheet_vns.Columns(1).AutoFit()
	sheet_vns.Columns(1).VerticalAlignment = -4108
	sheet_vns.Columns(2).AutoFit()
	sheet_vns.Columns(2).VerticalAlignment = -4108
	sheet_vns.Columns(2).HorizontalAlignment = -4108
	sheet_vns.Columns(3).AutoFit()
	sheet_vns.Columns(3).VerticalAlignment = -4108
	sheet_vns.Columns(3).HorizontalAlignment = -4108
	sheet_vns.Columns(4).ColumnWidth = 50
	sheet_vns.Columns(4).WrapText = True
	sheet_vns.Columns(4).VerticalAlignment = -4108
	sheet_vns.Columns(5).ColumnWidth = 50
	sheet_vns.Columns(5).WrapText = True
	sheet_vns.Columns(5).VerticalAlignment = -4108
	sheet_vns.Columns(6).AutoFit()
	sheet_vns.Columns(6).NumberFormat = '0'
	sheet_vns.Columns(6).HorizontalAlignment = -4108
	sheet_vns.Columns(6).VerticalAlignment = -4108
	sheet_vns.Columns(7).AutoFit()
	sheet_vns.Columns(7).NumberFormat = '0'
	sheet_vns.Columns(7).HorizontalAlignment = -4108
	sheet_vns.Columns(7).VerticalAlignment = -4108
	sheet_vns.Columns(8).AutoFit()
	sheet_vns.Columns(8).NumberFormat = '0'
	sheet_vns.Columns(8).HorizontalAlignment = -4108
	sheet_vns.Columns(8).VerticalAlignment = -4108
	sheet_vns.Columns(9).Font.Size = 8
	sheet_vns.Columns(9).WrapText = True
	sheet_vns.Columns(9).ColumnWidth = 50
	sheet_vns.Columns(9).VerticalAlignment = -4108
	sheet_vns.Rows(1).Font.Size = 11
	
	
	sheet_otkazy.Rows(1).Font.Bold = True
	sheet_otkazy.Rows(1).HorizontalAlignment = -4108
	sheet_otkazy.Cells(1, 1).value = "Месторождение"
	sheet_otkazy.Cells(1, 2).value = "Скважина"
	sheet_otkazy.Cells(1, 3).value = "6:00"
	sheet_otkazy.Cells(1, 4).value = "18:00"
	sheet_otkazy.Cells(1, 5).value = "пар_раб_м3"
	sheet_otkazy.Cells(1, 6).value = "пар_раб_%"
	sheet_otkazy.Cells(1, 7).value = "пар_раб_тн"
	for j in range(len(oilfield_name_otk)):
		sheet_otkazy.Cells(j+2, 1).value = oilfield_name_otk[j]
		sheet_otkazy.Cells(j+2, 2).value = well_num_otk[j]
		sheet_otkazy.Cells(j+2, 3).value = status_morning_otk[j]
		sheet_otkazy.Cells(j+2, 4).value = status_evening_otk[j]
		sheet_otkazy.Cells(j+2, 5).value = q_liq_otk[j]
		sheet_otkazy.Cells(j+2, 6).value = wc_otk[j]
		sheet_otkazy.Cells(j+2, 7).value = q_oil_otk[j]
	sheet_normalization(sheet_otkazy)
	sheet_otkazy.Columns(5).AutoFit()
	sheet_otkazy.Columns(5).NumberFormat = '0'
	sheet_otkazy.Columns(5).HorizontalAlignment = -4108
	sheet_otkazy.Columns(6).AutoFit()
	sheet_otkazy.Columns(6).NumberFormat = '0'
	sheet_otkazy.Columns(6).HorizontalAlignment = -4108
	sheet_otkazy.Columns(7).AutoFit()
	sheet_otkazy.Columns(7).NumberFormat = '0'
	sheet_otkazy.Columns(7).HorizontalAlignment = -4108
	
	sheet_zar.Rows(1).Font.Bold = True
	sheet_zar.Rows(1).HorizontalAlignment = -4108
	sheet_zar.Cells(1, 1).value = "Месторождение"
	sheet_zar.Cells(1, 2).value = "Скважина"
	sheet_zar.Cells(1, 3).value = "Куст"
	sheet_zar.Cells(1, 4).value = "Оборудование"
	sheet_zar.Cells(1, 5).value = "6:00"
	sheet_zar.Cells(1, 6).value = "18:00"
	sheet_zar.Cells(1, 7).value = "пар_раб_м3"
	sheet_zar.Cells(1, 8).value = "пар_раб_%"
	sheet_zar.Cells(1, 9).value = "пар_раб_тн"
	for j in range(len(oilfield_name_zar)):
		sheet_zar.Cells(j+2, 1).value = oilfield_name_zar[j]
		sheet_zar.Cells(j+2, 2).value = well_num_zar[j]
		sheet_zar.Cells(j+2, 3).value = pad_num_zar[j]
		try:
			sheet_zar.Cells(j+2, 4).value = (construction_zar[j].split('Оборудование:')[0]).strip()
		except:
			pass
		sheet_zar.Cells(j+2, 5).value = status_morning_zar[j]
		sheet_zar.Cells(j+2, 6).value = status_evening_zar[j]
		sheet_zar.Cells(j+2, 7).value = q_liq_zar[j]
		sheet_zar.Cells(j+2, 8).value = wc_zar[j]
		sheet_zar.Cells(j+2, 9).value = q_oil_zar[j]
	sheet_zar.Columns(1).AutoFit()
	sheet_zar.Columns(1).VerticalAlignment = -4108
	sheet_zar.Columns(2).AutoFit()
	sheet_zar.Columns(2).VerticalAlignment = -4108
	sheet_zar.Columns(2).HorizontalAlignment = -4108
	sheet_zar.Columns(3).AutoFit()
	sheet_zar.Columns(3).VerticalAlignment = -4108
	sheet_zar.Columns(3).HorizontalAlignment = -4108
	sheet_zar.Columns(4).ColumnWidth = 30
	sheet_zar.Columns(4).Font.Size = 8
	sheet_zar.Columns(4).WrapText = False
	sheet_zar.Columns(4).HorizontalAlignment = -4131
	sheet_zar.Columns(4).VerticalAlignment = -4160
	sheet_zar.Cells(1, 4).Font.Size = 11
	sheet_zar.Cells(1, 4).HorizontalAlignment = -4108
	sheet_zar.Columns(5).ColumnWidth = 70
	sheet_zar.Columns(5).WrapText = True
	sheet_zar.Columns(5).VerticalAlignment = -4108
	sheet_zar.Columns(6).ColumnWidth = 70
	sheet_zar.Columns(6).WrapText = True
	sheet_zar.Columns(6).VerticalAlignment = -4108
	sheet_zar.Columns(7).AutoFit()
	sheet_zar.Columns(7).NumberFormat = '0'
	sheet_zar.Columns(7).HorizontalAlignment = -4108
	sheet_zar.Columns(8).AutoFit()
	sheet_zar.Columns(8).NumberFormat = '0'
	sheet_zar.Columns(8).HorizontalAlignment = -4108
	sheet_zar.Columns(9).AutoFit()
	sheet_zar.Columns(9).NumberFormat = '0'
	sheet_zar.Columns(9).HorizontalAlignment = -4108
	
	sheet_otkazy = excel.Worksheets('Лист1').Delete()
	
	wb_new.SaveAs(os.path.join(pathTargetFldr, ('short_report_' + report_date + '_' + report_time + '.xlsx')))
	os.startfile(os.path.join(pathTargetFldr, ('short_report_' + report_date + '_' + report_time + '.xlsx')))
