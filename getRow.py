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
sheetName = "小蜜蜂 已發放傳單區域回報區(return)"
#sheetName = "嗡嗡嗡"
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

row_amount = 1
row_num = row_num + row_amount

col_num = length(rowValues_list)
##and you can know how many column there is(col_count) or by the length of a row,
##and then next time you know how many rows you get (by head(cusor is moved) to get_all)


