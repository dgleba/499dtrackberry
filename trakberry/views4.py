from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
import decimal
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set
from datetime import datetime


def ios_test(request):
	# Creates a new backup table of tkb_cycletimes
	db, cur = db_set(request)  
	s1 = "SELECT p_cell FROM sc_prod_hr_target"
	cur.execute(s1)
	tmp = cur.fetchall()

	db.commit()
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})	

def ios_test2(request):
	# Searches all in sc_production1 unique asset num with machine >1
	l = 1
	len_part = 5
	id_start = 237056
	db, cur = db_set(request)

	sql = "SELECT DISTINCT partno FROM sc_production1 where LENGTH(partno) > '%d' and id > '%d' ORDER BY %s %s" %(len_part,id_start,'partno','ASC')


#	sql = "SELECT DISTINCT asset_num, machine, partno FROM sc_production1  where LENGTH(asset_num) >'%d' and LENGTH(machine) >'%d' ORDER BY %s %s,%s %s" %(l,l,'asset_num','ASC','id','DESC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})

def ios_test1(request):
	# Searches all in sc_production1 unique asset num with machine >1
	l = 1
	len_part = 5
	id_start = 237056
	pd = '2019-05-29'
	po = '50-9341'
	lft = 'OP'
	shf = '11pm-7am'
	dte = []
	db, cur = db_set(request)
	sql = "SELECT DISTINCT comments FROM sc_production1 where partno = '%s' and pdate  = '%s' and left(machine,2) = '%s' and shift  = '%s' " %(po,pd,lft,shf)
#	sql = "SELECT DISTINCT asset_num, machine, partno FROM sc_production1  where LENGTH(asset_num) >'%d' and LENGTH(machine) >'%d' ORDER BY %s %s,%s %s" %(l,l,'asset_num','ASC','id','DESC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	ctr = 0
	for i in tmp:
		ctr = ctr + 1


	return render(request, "kiosk/kiosk_test4.html",{'tmp':ctr})

	for x in tmp:
#		asset = x[0]
#		machine = x[1]
		part = x[0]
		try:
			aql = "SELECT COUNT(*) FROM sc_prod_parts WHERE parts_no = '%s'" %(part)
			cur.execute(aql)
			t2 = cur.fetchall()
			t3 = t2[0]
			cnt = t3[0]
		except:
			cnt = 0
		if int(cnt) < 1:
			cur.execute('''INSERT INTO sc_prod_parts(parts_no) VALUES(%s)''',(part))
			db.commit()
		
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})

def NotDone(request):
#	shift = '11pm-7am'
#	shift = '7am-3pm'
	shift = '3pm-11pm'

	pdate = '2019-05-23'
	job_missed = ['' for z in range(0)]
	part_missed = ['' for z in range(0)]

	db, cur = db_set(request)
	s1ql = "SELECT DISTINCT asset FROM tkb_cycletime"
	cur.execute(s1ql)
	tmp1 = cur.fetchall()
	

	s2ql = "SELECT asset_num FROM sc_production1 where shift = '%s' and pdate = '%s'" %(shift,pdate)
	cur.execute(s2ql)
	tmp2 = cur.fetchall()
	

	xx = 0
	for x in tmp1:
		ch = 0
		a = x[0]
		for y in tmp2:
			xx = xx + 1
			b = y[0]

			if a == b:
				ch = 1
#				job_missed.append(b)
#				part_missed.append(c)
#				hh = request.session["hh"]
		if ch == 0:
			job_missed.append(a)
#			part_missed.append(c)
#	List = zip(job_missed,part_missed)


	return render(request, "kiosk/kiosk_test4.html",{'tmp':job_missed})

def median(lst):
    n = len(lst)
    if n < 1:
		return None
    if n % 2 == 1:
		return sorted(lst)[n//2]
    else:
		return sum(sorted(lst)[n//2-1:n//2+1])/2.0

def medium_production2(request):
	db, cur = db_set(request)

	asset1 = "683"
	tuple1 = ['' for x in range(0)]
	shifthrs1=8
	bql = "Select actual_produced From sc_production1 where asset_num = '%s' and shift_hours_length = '%d' ORDER BY id DESC limit 10" %(asset1,shifthrs1) 
	cur.execute(bql)
	tmp3 = cur.fetchall()
	for i in tmp3:
		tuple1.append(i[0])
	lst = list(tuple1)
	lst2 = median(lst)
	request.session["lst2"] = lst2
	request.session["Asset"] = asset1

	db.close()
	return render(request, "kiosk/kiosk_test7.html",{'tmp':lst})
	
def medium_production(request):
	# db, cur = medium_initial(request)
	db, cur = db_set(request)

	# bql = "Select max(id) From sc_production1"
	# cur.execute(bql)
	# tmp3 = cur.fetchall()
	# tmp4 = tmp3[0]
	# max_id = int(tmp4[0])

	# bql = "Select createdtime from sc_production1 where id = '%s'" % (max_id)
	# cur.execute(bql)
	# tmp3 = cur.fetchall()
	# tmp4 = tmp3[0]
	# last_date = tmp4[0]
	# m = last_date.month


	# h = 9/0

	cur.execute("""DROP TABLE IF EXISTS tkb_couldbe""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_couldbe LIKE tkb_cycletime""")
	cur.execute('''INSERT tkb_couldbe Select * From tkb_cycletime''')
	cur.execute("Alter Table tkb_couldbe ADD medium Char(30)")
	cur.execute("Alter Table tkb_couldbe ADD target int(30)")
	cur.execute("Alter Table tkb_couldbe ADD percent decimal(10)")
	db.commit()

	sql = "Select * From tkb_couldbe"
	cur.execute(sql)
	tmp4 = cur.fetchall()
	for ii in tmp4:
		ctr = 0
		tot = 0

		try:
			asset1 = ii[1]
			part = ii[2]
			tuple1 = ['' for x in range(0)]
			shifthrs1=8
			iid = 525492

			try:
				cql = "Select cycletime from tkb_cycletime where asset = '%s' and part = '%s'" % (asset1,part)
				cur.execute(cql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				ctime = tmp4[0]
				ctime = float(ctime)
				trg = 28800 / ctime
			except:
				trg = 10000
				
			bql = "Select actual_produced From sc_production1 where asset_num = '%s' and partno = '%s' and shift_hours_length = '%d' and id > '%d' ORDER BY id DESC limit 35" %(asset1,part,shifthrs1,iid) 
			cur.execute(bql)
			tmp3 = cur.fetchall()
			for i in tmp3:
				tuple1.append(i[0])
			lst = list(tuple1)
			lst2 = median(lst)
			tot = int(lst2)
			tot = str(tot)
			trg = int(trg)

			per = int(tot) / trg
			# per = per * 100

			cql = ('update tkb_couldbe SET medium = "%s" WHERE asset = "%s" and part = "%s"' % (tot,asset1,part))
			cur.execute(cql)
			db.commit()
			cql = ('update tkb_couldbe SET target = "%s" WHERE asset = "%s" and part = "%s"' % (trg,asset1,part))
			cur.execute(cql)
			db.commit()
			cql = ('update tkb_couldbe SET percent = "%s" WHERE asset = "%s" and part = "%s"' % (per,asset1,part))
			cur.execute(cql)
			db.commit()

		except:
			dummy = 1
		
		#rr = request.session["pumpkin"]
	db.close()
	
	return render(request, "kiosk/kiosk_test7.html")

def medium_initial(request):
  	# Below will test for a variable and if it doesn't exist then make the column with a value assigned
  	db, cursor = db_set(request)
	x = 5
 	try:
  		sql = "SELECT part FROM tkb_couldbe where id = '%d'" % (x)
  		cursor.execute(sql)
 		tmp = cursor.fetchall()
  	except:
		cursor.execute("Alter Table tkb_couldbe ADD part Char")
    	db.commit()
  	return db, cursor


def IsDone(request):
	id1 = 1
	name1 = '"Dave"'
#	name1 = str(name1)

#	cur.execute("""SELECT COUNT(*) FROM test WHERE attribute = %s AND unit_id IN %s""", (a, unit_ids))
	
#	cql =" ('update role SET name="%s" WHERE Id="%s" ' %(name1,id1)) "

	name1 = '"Dave"'
	cql = ("""update role SET name = %s WHERE Id = %s""" % (name1,id1))
	dql = str(cql)

	yy = request.session["ymym"]
#	cql = ('update role SET name="%s" WHERE Id="%s"' %(name1,id1))
	db, cur = db_set(request)
	cur.execute(dql)
	db.commit()
	db.close()

	return render(request, "kiosk/kiosk_test5.html")


	shift = '11pm-7am'
#	shift = '7am-3pm'
#	shift = '3pm-11pm'
	y = request.session['helpppee']
	pdate = '2019-05-10'
	job_missed = ['' for z in range(0)]
	part_missed = ['' for z in range(0)]

	db, cur = db_set(request)
	s1ql = "SELECT DISTINCT asset FROM tkb_cycletime"
	cur.execute(s1ql)
	tmp1 = cur.fetchall()
	
	s2ql = "SELECT asset_num,partno FROM sc_production1 where shift = '%s' and pdate = '%s'" %(shift,pdate)
	cur.execute(s2ql)
	tmp2 = cur.fetchall()
	
	xx = 0
	for x in tmp1:
		ch = 0
		a = x[0]
		for y in tmp2:
			xx = xx + 1
			b = y[0]
			c = y[1]
			if a == b:
				ch = 1
				job_missed.append(b)
				part_missed.append(c)
#				hh = request.session["hh"]
		if ch == 0:
			dummy = 1
#			job_missed.append(a)
#			part_missed.append(c)
	List = zip(job_missed,part_missed)


	return render(request, "kiosk/kiosk_test5.html",{'tmp':List})

def multidrop(request):
	db, cur = db_set(request)
	sql = "SELECT asset FROM tkb_cycletime"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp
	db.close()
	request.session["tmp2"] = tmp2
	request.session["ttm"] = '''"BY": "Bankock",
    "BD": "Bangladesh",'''
	request.session["bobu"] = "BobsYourUncle"

	#if request.POST:
	if 'button1' in request.POST:
		filter1 = str(request.POST.get("d1"))
		request.session["filter1"] = filter1
	

		return render(request, "mgmt_display_test2.html")

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "mgmt_display_test.html",{'args':args})

def scantest(request):
	if request.POST:
		filter1 = request.POST.get("var1")
		request.session["filter1"] = filter1

		return render(request, "kiosk/scantest.html")

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/scantestform.html",{'args':args})

def target_fix1(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-5404"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})

def target_fix_5404(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-5404"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})

def target_fix_5401(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-5401"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})

def target_fix_5399(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-5399"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})

def target_fix_5214(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-5214"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})

def target_fix_3214(request):
	db, cur = db_set(request)  
	pr = '27'
	pr2 = "50-3214"
	pid = 452784
	sql = "Select * From sc_production1 where id >= '%d' and partno = '%s' " %(pid,pr2) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0
	for i in tmp:
		 try:
			asset = i[1]
			part1 = i[3]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s'  and part = '%s'" % (asset,part1)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			machine1 = tmp3[5]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			cql = ('update sc_production1 SET machine = "%s" WHERE id ="%s"' % (machine1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1
		 except:
		 	dummy = 1
	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})





	
	