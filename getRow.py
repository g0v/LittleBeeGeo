#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gspread
#https://pypi.python.org/pypi/gspread/0.1.0

email = raw_input("please key in your gmail account: ")
password = raw_input("please key in your gmail account's password: ")

print email , password

gc = gspread.login(email, password)

sheet = gc.open("小蜜蜂 已發放傳單區域回報區").sheet1

row_num = 1
values_list = sheet.row_values(row_num)

amount = 1
row_num = row_num + amount
