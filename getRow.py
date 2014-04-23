#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gspread
#https://pypi.python.org/pypi/gspread/0.1.0

##NOTICE::
##the users need to login into the google spreadsheet first,
##and then provide their accounts and passwords here.

###remember:: delete your OWN account
email = raw_input("please key in your gmail account: ")
password = raw_input("please key in your gmail account's password: ")
print email , password


###try if c = gspread.Client(auth=('user@example.com', 'qwertypassword'))
###needed to be login on g-spread first or not
#gc = gspread.login(email, password)
gc = gspread.Client(auth=(email, password))
gc.login()

#sheet = gc.open("小蜜蜂 已發放傳單區域回報區").sheet1
#sheetName = "小蜜蜂 已發放傳單區域回報區(return)"
sheetName = "嗡嗡嗡"
sheetName_uni = unicode(sheetName, 'utf-8', 'ignore')
print sheetName_uni
sheet = gc.open(sheetName_uni).sheet1

#sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/18pLzqR1vJWWFR7lE9ZQnUViysOj-C_o6SVgsp1F3lOQ/')
##NOTICE::
##open_by_url api is not working for the new version of google spreadsheet now,
##so please use opne by title api.

row_num = 1
rowValues_list = sheet.row_values(row_num)
print rowValues_list
#col_dataCount = len(rowValues_list)
#print col_dataCount

row_count = 1
row_num = row_num + row_count

##this API will get the column amount of the whole spreadsheet, including the empty cells 
#col_amount = sheet.col_count
#print col_amount

#Get all values from the first column
colValues_list = sheet.col_values(1)
#Get how many rows by the length of the first column minus the title row
row_amount = len(colValues_list) - 1
for i in colValues_list:
    print i
#print row_amount

row_count = row_amount

print row_count

##and you can know how many column there is(by col_count),
##and then next time you know how many rows you get (by head(cusor is moved) to get_all)

