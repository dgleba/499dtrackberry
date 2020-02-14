from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from trakberry.forms import login_Form, login_password_update_Form
from datetime import datetime

import MySQLdb
import time
import os
import smtplib
from smtplib import SMTP
import xlrd
#import pandas
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2,vacation_set_current6, vacation_set_current4


#  Testing View for Excel Reading

def excel_test(request):
	
	# if needed this assigns mlist to the current path
#	mlist = os.getcwd()
	
#	Change to directory where imported inventory.xlsm is located
#		Use this for local testing
	label_link = 'c:/Projects/'
#		Use this one for actual server
	# label_link = '/home/file/import1/Inventory/importedxls'
	
	sheet = 'inventory.xlsx'
	sheet_name = 'Sheet1'
	os.chdir(label_link)
	
	book = xlrd.open_workbook(sheet)
	
	#working = book.sheet_by_index(1)
	working = book.sheet_by_name(sheet_name)
	
	# First variable is ROW 
	# Second variable is COLUMN
	
	tot = 28
	toc = 1

	tdate = tot+1
	jj = 0
	kk = 1

	a = [[] for x in range(1900)]
	b = [[] for y in range(1900)]
	d = [[] for z in range(1900)]
	for i in range(toc,tot):
		x = str(working.cell(i,0).value)
		# b[kk].append(x)
		# kk = kk + 1
		
		for ii in range(1,39):
			#x = working.cell(i,ii).value
			#if x > 0 and x < 10000000:
			#	x = int(x)
			#	dummy = 1
			#else:
			#	if len(str(x)) < 5:
			#		x = 0
			#	else:
			dummy = 1
			yy = len(x)
			# if len(str(working.cell(i,ii).value)) > 5:
			if len(x) > 3:
				#x = str(working.cell(i,ii).value) + "(" + str(working.cell(204,ii).value) + ")"
				y = str(working.cell(i,ii).value) 
				if len(y) < 1:
					y = 0
				else:
					y = float(y)
					y = int(y)
				# y = str(working.cell(0,ii).value) 
				
				# z = x + "(" + y + ")"
				a[jj].append(x)
				b[jj].append(y)
				d[jj].append(ii)
				jj = jj + 1
	#a = working.cell(1,0).value
	# Date
	c = working.cell(41,0).value
	# # yy = 9/0
	excel_date = int(c)
	dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date)
	ddt = vacation_set_current6(dt)

	# t = 9/0
	# excel_date = int(c)
	# dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)


	#tt = vacation_temp()

	e = zip(a,b,d)
	inventory_initial(request)
	db, cur = db_set(request)
	ctr = 0
	for i in e:
		p = ''.join(i[0])
		try:
			q = int("".join(map(str,i[1])))
			c = int("".join(map(str,i[2])))
		except:
			q = 0
			c = 0
		ctr = ctr + 1
		# if ctr > 3:
		# 	lenp = len(p)
		# 	x = 9/0
		if len(p)>1:

			cur.execute('''INSERT INTO tkb_inventory(Date,Part,Qty,Category) VALUES(%s,%s,%s,%s)''', (ddt,p,q,c))
			db.commit()

	db.close()



	return render(request,"test4.html",{'D':ddt,'A':e})
	
	
	#adate = working.cell(tdate,1).value
	#b = working.cell(7,0).value
	#mlist = book.sheet_names()
	#mlist.encode('ascii','ignore')
	#c = a[5][5]
	#mlist = xl_workbook.nsheets

	#mlist = os.listdir('.')
	

	#mlist = 'Done'
	


#	tx = ' ' + tx
#	if (tx.find('"'))>0:
#		#request.session["test_comment"] = tx
#		#return out(request)
#		ty = list(tx)
#		ta = tx.find('"')
#		tb = tx.rfind('"')
#		ty[ta] = "'"
#		ty[tb] = "'"
#		tc = "".join(ty)

	#mlist = mlist + 4


	
	#b = 35
	
#	Only uncomment below line to re do table completely	
# inventory_initial()

#	Select today as the date to put in for entry
	# current_first = vacation_set_current4(dt)
	
	db, cur = db_set(request)
#  Below Section will insert a as a new entry
# It uses Try and Except to see if one for that date exists

# Above won't work.   Need to confirm todays date is in inventory


# The below Code was for Inventory

	x = 1
	for i in range(1,jj):
		#y = a[i]
		y = str(a[i][0])
		#y = "a"
		yy = str(b[i][0])
		cur.execute('''INSERT INTO tkb_inventory(Employee,Shift) VALUES(%s,%s)''', (y,yy))
		db.commit()
	request.session["test_excel"] = "Added New One"

	db.close()


	return render(request,"test4.html",{'Date':current_first})

	
	# If there's a current date already there put it into temp_a[][] compare to a[][]
	ch = 0
	
	sql = "SELECT * FROM tkb_inventory where Date_Entered = '%s'" %(current_first)
	cur.execute(sql)
	tmp = cur.fetchall()
	
	i = 0    # Initialize ctr i to use as row increment in both arrays
	try:
		for j in tmp:
			i = i + 1
		
			pn_1 = str(j[2])
			in_1 = j[4]
			va_1 = j[3]
		
			ij = 0
			for h in a:
				if ij > 0:  # First row of a is empty.
					#return render(request,"test5.html",{'a':a,'b':pp,'AA':oo})
					if pn_1 == str(h[0]):  # Results in a positive match of part number with 'a' and 'j'
						aa = (h[in_1])
						bb = va_1
						
						
						return render(request,"test5_match.html",{'aa':aa,'bb':bb})  # results in a positive hit of part number
						
				ij = ij + 1

			return render(request,"test5_nomatch.html")
					
#				if ij > 0:
#				return render(request,"test5.html",{'a':a,'b':j,'AA':h})
#				ij = ij + 1

				
				# j[3] is the value 
				# j[4] is the index (Column)
				# j[0] is the part number
				
			bb = j[3]
			x = round((a[1][10]),0)
			if bb == x :
				ch = 1
			else:
				ch = 0
			return render(request,"test5.html",{'a':a,'b':j,'AA':x})
				
#			for ii in range(1,35):
#				return render(request,"test5.html",{'a':a,'b':j,'AA':a[i+1]})
#				if a[i,ii] != j[ii]:
#					ch = 1
	except:

		return render(request,"test5_error.html")
	
	if ch == 1:
		return render(request,"test5_nomatch.html")
	elif ch == 0:
		return render(request,"test5_match.html")
	
	db.close()
	return render(request,"test5.html",{'a':a,'b':current_first})
 
def inventory_initial(request):

	# create inventory table if one doesn't exist
	db, cursor = db_set(request)  
#	Use below line to recreate the table format
	cursor.execute("""DROP TABLE IF EXISTS tkb_inventory""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_inventory(Id INT PRIMARY KEY AUTO_INCREMENT,Date Date,Part Char(80),Qty Int(20), Category Int(10))""")
	db.commit()
	db.close()
	return

	
def manpower_initial():

	# create inventory table if one doesn't exist
	db, cursor = db_set(request)  
#	Use below line to recreate the table format
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Trained CHAR(160))""")
	db.commit()
	db.close()
	return
	
# Update DB so it has current manpower
def manpower_update(request):
	label_link = '/home/file/import1/Inventory/importedxls'
	sheet = 'inventory.xlsx'
	sheet_name = 'Sheet1'
	os.chdir(label_link)
	book = xlrd.open_workbook(sheet)
	working = book.sheet_by_name(sheet_name)
	tot = 246  # Row on Excel Sheet
	toc = 35   # Col on Excel Sheet
	tdate = tot+1
	jj = 1
	a = [[] for x in range(600)]
	b = [[] for y in range(600)]
	for i in range(205,tot):
		for ii in range(0,17):
			if len(str(working.cell(i,ii).value)) > 5:
				x = str(working.cell(i,ii).value) 
				y = str(working.cell(204,ii).value) 
				z = x + "(" + y + ")"
				a[jj].append(x)
				b[jj].append(y)
				jj = jj + 1
	manpower_initial()   # Initialize the Manpower list
	db, cur = db_set(request)
	x = 1
	for i in range(1,jj):
		y = str(a[i][0])
		yy = str(b[i][0])
		cur.execute('''INSERT INTO tkb_manpower(Employee,Shift) VALUES(%s,%s)''', (y,yy))
		db.commit()
	db.close()
	return render(request,"test4.html")


	
	
	
	
	
	
	
	
	
	
	
