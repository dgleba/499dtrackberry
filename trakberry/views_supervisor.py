from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm, sup_dispForm, sup_closeForm, report_employee_Form, sup_vac_filterForm, sup_message_Form
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP

from time import mktime
from datetime import datetime, date

from views_db import db_open, db_set

from django.core.context_processors import csrf

# update

def resetcheck(request):
	request.session["test99"] = 0
	return render(request,"test8.html")
	
	
	
	
def hour_check(request):
	# obtain current date from different module to avoid datetime style conflict
	t_name = request.session['login_tech']
	h = 6
	m = 15
	ch = 0
	send_email = 0
	t=int(time.time())
	tm = time.localtime(t)
	min = tm[4]
	hour = tm[3]
	current_date = find_current_date()
	#if min > m:
	if hour >= h and min > m:
		ch = 1

	db, cursor = db_set(request)  
	try:
		sql = "SELECT checking FROM tkb_email_conf where date='%s' and employee='%s'" %(current_date,t_name)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		checking = tmp2[0]
	except:
		checking = 0
		cursor.execute('''INSERT INTO tkb_email_conf(date) VALUES(%s)''', (current_date))
		db.commit()
		tmp2 = 0

	if ch == 1 and checking == 0:
		checking = 1
		pql =( 'update tkb_email_conf SET checking="%s" WHERE date="%s"' % (checking,current_date))
		cursor.execute(pql)
		db.commit()
		tql = "SELECT sent FROM tkb_email_conf where date='%s'" %(current_date)
		cursor.execute(tql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		sent = tmp2[0]
		if sent == 0:
			sent = 1
			rql =( 'update tkb_email_conf SET sent="%s" WHERE date="%s"' % (sent,current_date))
			cursor.execute(rql)
			db.commit()
			send_email = 1				
	db.close()	
	return send_email
	
def supervisor_display(request):

#	Below is a check to send an email for techs once a day. If yes then it reroutes from email_hour_check() 
	email_hour_check()
#	******************************************************************************************

	
	try:
		request.session["login_name"] 
		name_supervisor = request.session["login_name"]
		
	except:
		request.session["login_name"] = ""
		name_supervisor = ""
	
	if name_supervisor =="":
		return main_login_form(request)

		
  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	c = []
	date = []
	prob = []
	job = []
	priority = []
	id = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
	whos = []
	box_colour = []
   
  # Select prodrptdb db 
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	
	c = ["tech","Jim Barker"]

	
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	SQ_Sup = "SELECT * FROM pr_downtime1 where closed IS NULL" 

	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	
	ctr = 0
	for x in tmp:
	
		
		clr = "blue"
		if ctr > 3:
			clr = "red"
		tmp2 = (tmp[ctr])
		# assign job date and time to dt
		dt = tmp2[2]
		dt_t = time.mktime(dt.timetuple())
		# assign current date and time to dtemp
		dtemp = vacation_temp()
		dtemp_t = time.mktime(dtemp.timetuple())
		# assign d_diff to difference in unix
		d_diff = dtemp_t - dt_t
		
		if d_diff < 1801:
			clr = "#00B4E0"
		elif d_diff < 3601:
			clr = "#0096BA"
		elif d_diff < 10801:
			clr = "#006680"
		elif d_diff < 86400:
			clr = "#012933"
		else:
			clr = "#DE0707"
			
		temp1_job = tmp2[0]
		temp2_job = temp1_job[:15]
		job.append(temp2_job)
		prob.append(tmp2[1])
		
		priority.append(tmp2[3])
		id.append(tmp2[11])
		whos.append(tmp2[4])
		box_colour.append(clr)
		ctr = ctr + 1
		
	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			try:
				pr2 = float(priority[ii])
			except:
				pr2 = 97
			try:
				pr1 = float(priority[i])
			except:
				pr1 = 97
			if pr2 < pr1:
				jjob = job[i]
				job[i] = job[ii]
				job[ii] = jjob
				pprob = prob[i]
				prob[i] = prob[ii]
				prob[ii] = pprob
				pprior = priority[i]
				priority[i] = priority[ii]
				priority[ii] = pprior
				iid = id[i]
				id[i] = id[ii]
				id[ii]= iid
				wwhos = whos[i]
				whos[i] = whos[ii]
				whos[ii] = wwhos
				bbox_colour = box_colour[i]
				box_colour[i] = box_colour[ii]
				box_colour[ii] = bbox_colour
	
	list = zip(job,prob,id,whos,priority,box_colour)	
	db.close()
	n = "none"
	
	# Set Form Variables 
	if request.POST:
		request.session["test"] = 999
		a = request.POST
		try:
			b=int(a.get("one"))
		except:
			return render(request,'display_sup_refresh.html')	
		if b == -1:
			return done(request)
		if b == -2:
			request.session["call_route"] = 'supervisor'
			request.session["url_route"] = 'main.html'
			return done_tech(request)
		if b == -3:
			return done_elec(request)	
		if b == -4:
			return done_maint(request)		
		request.session["index"] = b
		#request.session["test"] = request.POST
		return done_edit(request)
	else:
		form = sup_dispForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	# *********************************************************************************************************
	# ******     Messaging portion of the Tech App  ************Not Working**********************************
	# *********************************************************************************************************
	try:
		N = request.session["login_name"]
	except:
		N = ''
	R = 0
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)	
		cur.execute(sql)
		tmp44 = cur.fetchall()
		tmp4 = tmp44[0]

		request.session["sender_name"] = tmp4[2]
		request.session["sender_name_last"] = tmp4[2]
		request.session["message_id"] = tmp4[0]

		aql = "SELECT COUNT(*) FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		cnt = tmp3[0]
	except:
		cnt = 0
		tmp4 = ''
		request.session["sender_name"] = ''
		request.session["message_id"] = 0
	db.close()
	Z_Value = 1
	if cnt > 0 :
		cnt = 1
		request.session["refresh_sup"] = 3
#	 ********************************************************************************************************

#	cnt = 0
#	request.session["refresh_sup"] = 0
#	tmp4 =''
	Z_Value = 1
	tcur=int(time.time())

  # call up 'display.html' template and transfer appropriate variables.  
	#return render(request,"test3.html",{'total':tmp4,'Z':Z_Value,'})
	return render(request,"supervisor.html",{'L':list,'N':n,'cnt':cnt,'M':tmp4,'Z':Z_Value,'TCUR':tcur,'args':args})

def sup_message(request):	
	A = 'Chris Strutton'
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()

	db.close()

	if request.POST:
        			
		a = request.session["login_name"]
		b = request.POST.get("name")
		c = request.POST.get("message")

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return done(request)
		#return done(request)
		
	else:
		form = sup_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'sup_message_form.html', {'List':tmp,'A':A,'args':args})	
	
def sup_message_close(request):
	request.session["refresh_sup"] = 0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	db.close()
	return done(request)
	#return done_test1234(request)

def sup_message_reply0(request):
	return render(request, "done_sup_message_reply.html")
	
def sup_message_reply1(request):
	request.session["refresh_sup"]=0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	

	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return sup_message_reply2(request)
	
def sup_message_reply2(request):	
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	if request.POST:
        			
		a = request.session["login_name"]
		#b = request.POST.get("name")
		b = request.session["sender_name_last"]
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return done(request)
		#return done(request)
		
	else:
		form = sup_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'sup_message_reply_form.html', {'List':tmp,'args':args})	
def sup_d(request):
	return supervisor_display(request)
	
def supervisor_tech_call(request):
	request.session["whoisonit"] = 'tech'
	
	return supervisor_down(request)

def supervisor_elec_call(request):
	request.session["whoisonit"] = 'Electrician'
	return supervisor_down(request)

def supervisor_maint_call(request):
	request.session["whoisonit"] = 'Millwright'
	return supervisor_down(request)	
	
def supervisor_down(request):	

	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = request.session["whoisonit"]
		
		# take comment into tx and ensure no "" exist.  If they do change them to ''
		tx = problem
		tx = ' ' + tx
		tps = list(tx)
		
		

#		hh = [ord(c) for c in tps]
		
			
#		if tps[2] == "x":
#			if(39 in hh):
#				a = "Appostrophe 39"
#				return render(request,'test_temp2.html', {'v1':a})	
#			if(8217 in hh):
#				a = "Appostrophe 8127"
#				return render(request,'test_temp2.html', {'v1':a})		
			
#			return render(request,'test_temp2.html', {'v1':hh})	

			
			
			
		if (tx.find("'"))>0:
			#return render(request,'test_temp2.html', {'variable':tx})	
			#request.session["test_comment"] = tx
			#return out(request)
			ty = list(tx)
			ta = tx.find("'")
			#tb = tx.rfind("'")
			ty[ta] = ""
			#ty[tb] = "'"
			tc = "".join(ty)
			
			return render(request,'test_temp2.html', {'v1':ty,'v2':tc})	
		else:
			tc = tx
		problem = tc
		
		
		# call external function to produce datetime.datetime.now()
		t = vacation_temp()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		priority = str(priority)
		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit,t))
		db.commit()
		db.close()
		
		return done(request)
		
	else:
		request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	# Old Method
	rlist = machine_list_display()
	
	# New Method
	#db, cur =db_open()
	#sql = "SELECT * FROM vw_asset_eam_lp"
	#cur.execute(sql)
	#tmp = cur.fetchall()
	#rlist = tmp[0]
	
	
	#return render(request,"test6.html",{'list':rlist})
	#request.session["login_tech"] = "none"
	return render(request,'supervisor_down.html', {'List':rlist,'args':args})	


# Module to edit entry	
def supervisor_edit(request):	
	index = request.session["index"]
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)
	SQ_Sup = "SELECT * FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	tmp2=tmp[0]
	request.session["machinenum"] = tmp2[0]
	request.session["problem"] = tmp2[1]
	request.session["priority"] = tmp2[3]
	db.close()	
	
	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = 'tech'
		
		a = request.POST
		b=int(a.get("one"))
		
		db, cursor = db_set(request)
		cur = db.cursor()
		
		if b==-3:
			mql =( 'update pr_downtime1 SET machinenum="%s" WHERE idnumber="%s"' % (machinenum,index))
			cur.execute(mql)
			db.commit()
			tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,index))
			cur.execute(tql)
			db.commit()
			uql =( 'update pr_downtime1 SET priority="%s" WHERE idnumber="%s"' % (priority,index))
			cur.execute(uql)
			db.commit()
			db.close()

		if b==-2:
			tc = "Troubleshooting"
			request.session["tech_comment"] = tc
			t = vacation_temp()
			sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
			cur.execute(sql)
			db.commit()
			tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
			cur.execute(tql)
			db.commit()
			db.close()
		
		if b==-1:
			return done_sup_close(request)
		

		return done(request)
#		return render(request, "test.html", {'machine':machinenum , 'y':b})
		
	else:	
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'supervisor_edit.html', args)		

def done_tech(request):
	#request.session["test"] = 78
	return render(request, "done_tech.html")
def done_elec(request):
	#request.session["test"] = 78
	return render(request, "done_elec.html")	
def done_maint(request):
	#request.session["test"] = 78
	return render(request, "done_maint.html")	
def done_edit(request):
	return render(request, "done_edit.html")	
	
def done_sup_close(request):
	return render(request, "done_sup_close.html")	
	
def sup_close(request):
	if request.POST:
		tc = request.POST.get("reason")	
		index = request.session["index"]
		t = vacation_temp()
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
		cur.execute(tql)
		db.commit()
		db.close()		

		return done(request)
		
	else:
		form = sup_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'sup_close.html', args)			
	
def employee_vac_enter_init(request, index):
	tmp = index
	month = request.session["current_month"]
	try:
		year_st = request.session["current_year"]
	except:
		year_st = 2018

	A = 'month'
	a = month

	
	
	
	if int(month)<10:
		current_first = str(year_st) + "-" + "0" + str(month) 
	else:
		current_first = str(year_st) + "-" + str(month) 	
		
	if int(tmp)<10:
		current_first = current_first + "-" + "0" + str(tmp)
	else:
		current_first = current_first + "-" + str(tmp)
		
	request.session["current_first"] = current_first
	
	B = 'current first'
	b = current_first
	
	#return render(request, "testA.html", {'A':A,'a':a,'B':B,'b':b})
	
	
	return employee_vac_enter(request)

def employee_vac_enter_init2(request):	
	current_first = vacation_set_current2()
	request.session["current_first"] = current_first
	return employee_vac_enter(request)
	
	
# Employee Vacation Entry Form **************************	
def employee_vac_enter(request):
	curr = request.session["current_first"]
	try:
		request.session["date_st"]
		request.session["date_en"]
		request.session["employee"]
		request.session["shift"]
		request.session["typee"]
#		request.session["Id"]
		
	except:
		request.session["date_st"] = ""
		request.session["date_en"] = ""
		request.session["employee"]= ""
		request.session["shift"]= ""
		request.session["typee"] = ""
#		request.session["Id"] = ""	
	
	if request.POST:

		request.session["date_st"] = request.POST.get("date_st")
		request.session["date_en"] = request.POST.get("date_en")
		request.session["employee"] = request.POST.get("employee")
		request.session["shift"] = request.POST.get("shift")
		request.session["typee"] = request.POST.get("typee")

#		request.session["Id"] = request.POST.get("Id")
		
		return vacation_entry(request)
		
	else:
		form = report_employee_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'employee_vac_form.html',{'Curr':curr,'args':args})		



def vacation_entry(request):	
    
	st = request.session["date_st"]
	fi = request.session["date_en"]
	employee = request.session["employee"]
	shift = request.session["shift"]
	typee = request.session["typee"]
	
	A = 'st'
	B = 'en'
	a = st
	b = fi
	
	#return render(request, "testA.html", {'A':A,'a':a,'B':B,'b':b})
	
#	idn = request.session["Id"]
	if typee == 'cover':
		ty = 1
	elif typee == 'special':
		ty = 2
	elif typee == 'note':
		ty = 3
	else:	
		ty = 0	
		
	date_st = datetime.strptime(st, '%Y-%m-%d')
	try:
		date_fi = datetime.strptime(fi, '%Y-%m-%d')
	except:
		date_fi = datetime.strptime(st, '%Y-%m-%d')
			
	month_st = date_st.month
	year_st = date_st.year
	day_st = int(date_st.day)
	day_fi = int(date_fi.day)
	mnt_start = int(date_st.month)
	mnt_end = int(date_fi.month)

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	
	# Set variables so Calander will start on this month and year after the edit.
	request.session["month"] = month_st
	request.session["year"] = year_st
	request.session["month_pick"] = 1
	
	#if int(day_st)<10:
	
	#	day_st = '0'+ day_st
	
	
	
	
	# Select prodrptdb db located in views_db
	
	#if day_st > day_fi:
	#	day_fi_temp = 31
	#	db, cur = db_set(request) 
	#	cur.execute('''INSERT INTO vacation(employee,shift,start,end,day_start,day_end,type) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (employee,shift,st,fi,day_st,day_fi_temp,ty))
	#	db.commit()
	#	db.close()
	#	day_st = 1
	
	
		
	db, cur = db_set(request) 	
	cur.execute('''INSERT INTO vacation(employee,shift,start,end,day_start,day_end,type,month_start,month_end) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (employee,shift,st,fi,day_st,day_fi,ty,mnt_start,mnt_end))
	db.commit()
	
	sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	
#	for x in tmp:
#		x_date = x[3]
		#x_date = datetime.strptime(x[3], '%Y-%m-%d')
#		x_day = x_date.day
#		x[3] = x_day

	# return to vacation_display once update is complete
	
	# Below code to reset Filter to Login Name's default every time
	#login_name = request.session["login_name"]
	#login_initial(request,login_name)
	
	
	#return vacation_display(request)
	return render(request,'testtest.html')
	
	# The below code was old code for entry finish but
	# it caused unfavourable results
	
	#dday, ctr, mnth = vacation_calander_init(month_st)
	#List = zip(ctr,dday)
	#return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Tmp':tmp,'Month_Number':month_st})


def vacation_month_fix(request):
	db, cur = db_set(request)
	
	
	a = 0
	
	
	cur.execute("SELECT * FROM vacation where month_start = '%s'" %(a))
	
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	num = cur.rowcount

	
	for x in xrange(0,num):
		
		tmp2 = tmp[x]
		ds = tmp2[2]
		de = tmp2[3]
		h = 999
		i = tmp2[6]
		h = ds.month
		try:
			j = de.month
		except:
			j = h
		if j == 0:
			j = h
		
		cur.execute("UPDATE vacation SET month_start = '%s', month_end = '%s' WHERE id_number = '%s'"% (h,j,i))
		db.commit()
		
	#db.commit()
	db.close()
	i = h
	
	return render(request,'test4.html',{'X':h})
	
	#for k in range(city_count):
    #cur.execute("UPDATE hqstock SET citylastprice = '%s' WHERE id = '%s'"% (CITYPRICE[k],   tID[k]))
    #cur.commit()

def reset_sfilter(request):
	request.session["sfilter1"] = ''
	request.session["sfilter2"] = ''
	request.session["sfilter3"] = ''
	request.session["sfilter4"] = ''
	request.session["sfilter5"] = ''
	request.session["sfilter6"] = ''
	request.session["sfilter7"] = ''
	request.session["sfilter8"] = ''
	request.session["sfilter9"] = ''
	request.session["sfilter10"] = ''
	request.session["sfilter11"] = ''
	request.session["sfilter12"] = ''
	request.session["sfilter13"] = ''
	request.session["sfilter14"] = ''
	request.session["sfilter15"] = ''
	request.session["sfilter16"] = ''
	request.session["sfilter17"] = ''
	return
	
def vacation_display_initial(request):
	request.session["month_pick"] = 0
	return vacation_display(request)
	
	
def vacation_display(request):
	
	# Check if someone is logged in first and if not rerout to login page
	try:
		if request.session["login_name"]  =="":
			return main_login_form(request)
	except:
		return main_login_form(request)


	# Call current datetime using external function because it would conflict with from datetime import datetime
	t = vacation_temp()
	month_st = t.month
	year_st = 2020
	day_st = t.day

	# Asssign session variable to today's month
	# dumb1, dumb2, month_tmp = vacation_calander_init_2017(month_st)
	dumb1, dumb2, month_tmp = vacation_calander_init(month_st)
	
	#return render(request,'test4.html',{'days':dumb1})
	
	
	request.session["month_now"] = month_tmp
	request.session["year"] = year_st

	try:
		MM = int(request.session["month"])
		YY = int(request.session["year"])
	except:
		MM = int(month_st)
		YY = int(year_st)
		
	if YY == 2018:
		request.session["Month_Current"] = MM + 12
	else:
		request.session["Month_Current"] = MM
	

	
	try:
		month_pick = request.session["month_pick"]
		A = MM
		B =  YY
	except:
		month_pick = 1
		A = 1
		B = 2018
		
	try:
		if request.session["month_pick"] == 1:
			month_st = MM
			year_st = YY
			#request.session["month_pick"] = 0
			
	except:
		request.session["month_pick"] = 0		
	
	#if request.session["test99"] == 1:
	#	request.session["test99"] = 0
	#	return render(request,'breakhh99.html')

	
	

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	request.session["current_first"] = current_first
	request.session["current_last"] = current_last
	request.session["current_day"] = day_st
	request.session["current_day_b"] = day_st
	request.session["current_month"] = month_st
	mm = int(month_st)
	try:
		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		shift15 = request.session["shift15"]
		shift16 = request.session["shift16"]
		shift17 = request.session["shift17"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"
			
	# Select prodrptdb db located in views_db
	db, cur = db_set(request) 
	
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:
		#sql = "SELECT * FROM vacation where shift = '%s' or shift = '%s' or shift = '%s' or shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, current_first, current_last)
		#sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, current_first, current_last)
		sql = "SELECT * FROM vacation where ((start between '%s' and '%s') or (end between '%s' and '%s')) and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last, current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, shift15, shift16, shift17)

	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	
	#return render(request,'test993.html',{'list':tmp})
	
	
	if year_st == 2020:
		dday, ctr, mnth = vacation_calander_init(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init_2018(month_st)
		
	request.session["current_month"] = month_st
	List = zip(ctr,dday)
	
	# Set Form Variables 
	if request.POST:
		#request.session["shift"] = request.POST.get("shift")
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'
			
		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'

		else:
			request.session["shift14"] = '--'

		if request.POST.get("shift15"):
			request.session["shift15"] = 'Q.A.'
			request.session["sfilter15"] = 'checked'

		else:
			request.session["shift15"] = '--'
			
		if request.POST.get("shift16"):
			request.session["shift16"] = 'Supervisor'
			request.session["sfilter16"] = 'checked'

		else:
			request.session["shift16"] = '--'

		if request.POST.get("shift17"):
			request.session["shift17"] = 'Furnace Setter'
			request.session["sfilter17"] = 'checked'

		else:
			request.session["shift17"] = '--'
		
		if request.POST.get("month"):
			xy = request.POST.get("month")
			xy = int(xy)
			jj = xy
			if xy > 12:
				request.session["year"] = 2021
				request.session["month"] = xy - 12
			else:
				request.session["year"] = 2020
				request.session["month"] = xy
		
			#return render(request,'test997.html',{'A':xy})
		request.session["month_pick"] = 1

		# testing Variable
		request.session["test99"] = 1
		return render(request,'vacation_shift.html')
		
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	try:
		request.session["shift"]
	except:
		request.session["shift"] = "All"
	
	
	
	A = 'List'
	a = List
	B = 'TMP'
	b = tmp
	#return render(request, "testAa.html", {'A':A,'a':a,'B':B,'b':b})
	#return render(request,'vacation_display_test.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})
	
	
	request.session["vacation_special"] = 0
	request.session["vacation_note"] = 0
	for xy in tmp:
		if xy[7] == 2:
			request.session["vacation_special"] = 1
		if xy[7] == 3:
			request.session["vacation_note"] = 1
			
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})

def vacation_display_jump(request):
	return vacation_display(request)
	
def vacation_display_increment(request):
	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()

	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		shift15 = request.session["shift15"]
		shift16 = request.session["shift16"]
		shift17 = request.session["shift17"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"

			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')
	

	# Increment the Month by one.  Increment Year by 1 if Month is 12
	month_st = date_st.month
	year_st = date_st.year
	a_month_st = month_st
	a_year_st = year_st
	
	# Asssign session variable to today's month
	dumb1, dumb2, month_tmp = vacation_calander_init(month_st)
	request.session["month_now"] = month_tmp
	
	if month_st == 12:
#		month_st = 1
#		year_st = year_st + 1
		month_st = 12     # Use this and not above two lines until completed next year
		year_st = year_st
		
	else:
		month_st = month_st + 1
	

	one = 1
	one_end = 31
	ma = str(month_st)
	if len(ma)<2:
		ma = '0' + ma
	current_first = str(year_st) + "-" + str(ma) + "-" + "01"
	current_last = str(year_st) + "-" + str(ma) + "-" + str(one_end)
	request.session["current_first"] = current_first
	
	
	
	request.session["current_test"] = month_st
	if request.session["current_month"] == month_st:
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	

	mm = int(month_st)
	

	# Select prodrptdb db located in views_db
	db, cur = db_set(request) 
	if shift1 == "All":
		#sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
		sql = "SELECT * FROM vacation where start between '%s' and '%s'" %(current_first, current_last)
	else:
		#sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, current_first, current_last)
		sql = "SELECT * FROM vacation where ((start between '%s' and '%s') or (end between '%s' and '%s')) and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last, current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, shift15, shift16, shift17)


	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	if year_st == 2020:
		dday, ctr, mnth = vacation_calander_init(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init_2018(month_st)

	
	# Below re route is for testing break
	if month_st == 21:
		x = len(monkey)
		y = len(current_first)
		return render(request,'test993.html',{'monkey':monkey,'len_monkey':x,'current_first':current_first,'len_first':y})
	
	
	request.session["current_month"] = month_st
	request.session["current_year"] = year_st
	request.session["month"] = month_st
	request.session["year"] = year_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'

		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'
		else:
			request.session["shift14"] = '--'
			
		if request.POST.get("shift15"):
			request.session["shift15"] = 'Q.A.'
			request.session["sfilter15"] = 'checked'

		else:
			request.session["shift15"] = '--'
			
		if request.POST.get("shift16"):
			request.session["shift16"] = 'Supervisor'
			request.session["sfilter16"] = 'checked'

		else:
			request.session["shift16"] = '--'
			
		if request.POST.get("shift17"):
			request.session["shift17"] = 'Furnace Setter'
			request.session["sfilter17"] = 'checked'

		else:
			request.session["shift17"] = '--'
			
		# testing Variable
		request.session["test99"] = 1
		request.session["month_pick"] = 1
		request.session["month"] = a_month_st
		request.session["year"] = a_year_st


	
		return render(request,'vacation_shift.html')
			
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	B = 'TMP'
	b = tmp
	A = 'M'
	a = mm
	
	request.session["vacation_special"] = 0
	request.session["vacation_note"] = 0
	for xy in tmp:
		if xy[7] == 2:
			request.session["vacation_special"] = 1
		if xy[7] == 3:
			request.session["vacation_note"] = 1
			
			
	#return render(request, "testAa.html", {'A':A,'a':a,'B':B,'b':b})
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})
#	return render(request,'vacation_display.html',{'Tmp':tmp})	

def vacation_display_decrement(request):	
	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()

	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		shift15 = request.session["shift15"]
		shift16 = request.session["shift16"]
		shift17 = request.session["shift17"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"

			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')
	
	# Decrement the Month by one.  Decrement Year by 1 if Month is 1
	month_st = date_st.month
	year_st = date_st.year
	a_month_st = month_st
	a_year_st = year_st
	
	# Asssign session variable to today's month
	dumb1, dumb2, month_tmp = vacation_calander_init_2017(month_st)
	request.session["month_now"] = month_tmp
	
	if month_st == 1:
#		month_st = 12
#		year_st = year_st - 1
		month_st = 1
		year_st = year_st
	else:
		month_st = month_st - 1
		
	one = 1
	one_end = 31
	ma = str(month_st)
	if len(ma) < 2:
		ma = '0'+ ma
		
	current_first = str(year_st) + "-" + str(ma) + "-" + "01"
	current_last = str(year_st) + "-" + str(ma) + "-" + str(one_end)
	request.session["current_first"] = current_first
	
	request.session["current_test"] = month_st
	request.session["current_month"] = int(request.session["current_month"]-1)
	if  request.session["current_month"]== int(month_st):
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	

	mm = int(month_st)
	# Select prodrptdb db located in views_db
	db, cur = db_set(request) 
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:		
		sql = "SELECT * FROM vacation where ((start between '%s' and '%s') or (end between '%s' and '%s')) and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last, current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, shift15, shift16, shift17)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	if year_st == 2020:
		dday, ctr, mnth = vacation_calander_init(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init(month_st)
		
	request.session["current_month"] = month_st
	request.session["current_year"] = year_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'

		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'
		else:
			request.session["shift14"] = '--'

		if request.POST.get("shift15"):
			request.session["shift15"] = 'Q.A.'
			request.session["sfilter15"] = 'checked'

		else:
			request.session["shift15"] = '--'
			
		if request.POST.get("shift16"):
			request.session["shift16"] = 'Supervisor'
			request.session["sfilter16"] = 'checked'

		else:
			request.session["shift16"] = '--'
			
		if request.POST.get("shift17"):
			request.session["shift17"] = 'Furnace Setter'
			request.session["sfilter17"] = 'checked'

		else:
			request.session["shift17"] = '--'
		
		request.session["test99"] = 1
		request.session["month_pick"] = 1
		request.session["month"] = a_month_st
		request.session["year"] = a_year_st
		return render(request,'vacation_shift.html')

			
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	
	request.session["vacation_special"] = 0
	request.session["vacation_note"] = 0
	for xy in tmp:
		if xy[7] == 2:
			request.session["vacation_special"] = 1
		if xy[7] == 3:
			request.session["vacation_note"] = 1
			
			
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})
	
	
def BB_vacation_display_decrement(request):	

	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()
		
	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"
			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')

	month_st = date_st.month
	year_st = date_st.year
	month_st = month_st - 1

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	request.session["current_first"] = current_first
	if request.session["current_month"] == month_st:
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	
	
	# Select prodrptdb db located in views_db
	db, cur = db_set(request) 
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:
		sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, current_first, current_last)
		
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	dday, ctr, mnth = vacation_calander_init(month_st)
	request.session["current_month"] = month_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Tmp':tmp,'args':args})	

def vacation_edit(request, index):	
	tmp = index
	request.session["index"] = index
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM vacation where id_number = '%s'" %(tmp)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		tmp="No"	
	db.close()
	return render(request,'vacation_delete.html',{'Tmp':tmp2})
		
		

def vacation_delete(request):
	index = request.session["index"]
	db, cur = db_set(request)
	dql = ('DELETE FROM vacation WHERE id_number="%s"' % (index))
	cur.execute(dql)
	db.commit()
	db.close()
	request.session["shift"] = 'All'
	return vacation_display(request)
	#return render(request,'test4.html',{'Tmp':tmp2})

	
	
	
def vacation_calander_init(month_st):
	dte = []
	ctr = []
	mnt = []
		
	dte.append([0])
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) # January
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]) # February
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) # March
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) #April
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) # May
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) # June
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #July
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #August
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) #September
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #October
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) #November
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #December
	
	ctr.append([0])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]) #jan		
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]) #February
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #Mar
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])#Apr
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])#May
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Jun
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])#july		
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])#aug	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])#Sep
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35])#Oct
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#nov	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])#dec

	
	mnt.append( '')
	mnt.append( 'January')
	mnt.append( 'February')
	mnt.append('March')
	mnt.append('April')
	mnt.append('May')
	mnt.append('June')
	mnt.append('July')
	mnt.append('August')
	mnt.append('September')
	mnt.append('October')
	mnt.append('November')
	mnt.append('December')
	
	days = dte[month_st]
	cctr = ctr[month_st]
	mnth = mnt[month_st]
	
	#return render(request,'test4323.html')
	return days,cctr,mnth

def vacation_calander_init_2017(month_st):
	dte = []
	ctr = []
	mnt = []
		
	dte.append([0])
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Jan
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])#Feb
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Mar
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Apr
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#May
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Jun
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Jul
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Aug
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Sep
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Oct
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Nov
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Dec
	
	ctr.append([0])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]) #Jan
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]) #Feb
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]) #Mar
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) #Apr
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]) #May
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]) #Jun
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #Jul	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])#Aug
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])#Sep
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])#Oct
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])#Nov
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])#Dec

	
	mnt.append( '')
	mnt.append( 'January')
	mnt.append( 'February')
	mnt.append('March')
	mnt.append('April')
	mnt.append('May')
	mnt.append('June')
	mnt.append('July')
	mnt.append('August')
	mnt.append('September')
	mnt.append('October')
	mnt.append('November')
	mnt.append('December')
	
	days = dte[month_st]
	cctr = ctr[month_st]
	mnth = mnt[month_st]
	#return render(request,'test4323.html')
	return days,cctr,mnth

# Calander Init for 2018
def vacation_calander_init_2018(month_st):
	dte = []
	ctr = []
	mnt = []
		
	dte.append([0])
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Jan
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])#Feb
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Mar
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Apr
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#May
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Jun
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Jul
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Aug
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Sep
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Oct
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])#Nov
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])#Dec
	
	ctr.append([0])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]) #Jan
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]) #Feb
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]) #Mar
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]) #Apr
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]) #May
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]) #Jun
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) #Jul	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])#Aug
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])#Sep
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])#Oct
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])#Nov
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])#Dec

	
	mnt.append( '')
	mnt.append( 'January')
	mnt.append( 'February')
	mnt.append('March')
	mnt.append('April')
	mnt.append('May')
	mnt.append('June')
	mnt.append('July')
	mnt.append('August')
	mnt.append('September')
	mnt.append('October')
	mnt.append('November')
	mnt.append('December')
	
	days = dte[month_st]
	cctr = ctr[month_st]
	mnth = mnt[month_st]
	#return render(request,'test4323.html')
	return days,cctr,mnth
	

def check_email_problem(request):
	email_hour_check()
	return render(request, "kiosk/kiosk_test6.html")
	
# Below is Code to Email Tech Reports Based on the Supervisor Refreshing at a certain Time
def email_hour_check():
	# obtain current date from different module to avoid datetime style conflict

	h = 6
	h2 = 13
	m = 40
	ch = 0
	send_email = 0
	t=int(time.time())
	tm = time.localtime(t)
	mn = tm[4]
	hour = tm[3]
	current_date = find_current_date()
	#hour = 9
	if hour >= h:
		ch = 1

		db, cursor = db_open()  
		try:
			sql = "SELECT sent FROM tkb_email_conf where date='%s'" %(current_date)
			cursor.execute(sql)
			tmp = cursor.fetchall()
			tmp2 = tmp[0]

			try:
				sent = tmp2[0]
			except:
				sent = 0
		except:
			sent = 0
			
		if sent == 0:
			checking = 1
			employee = 1
			cursor.execute('''INSERT INTO tkb_email_conf(date,checking,sent,employee) VALUES(%s,%s,%s,%s)''', (current_date,checking,checking,employee))
			db.commit()
			
		
			
#			Email Reports from techs
			tech_report_email()
		
		#elif hour >=h2:
		#	try:
		#		tql = "SELECT employee FROM tkb_email_conf where date='%s'" %(current_date)
		#		cursor.execute(tql)
		#		tmp3 = cursor.fetchall()
		#		tmp4 = tmp3[0]
		#		try:
		#			ssent = tmp4[0]
		#		except:
		#			ssent = ''
		#	except:
		#		ssent = ''
		#	if ssent != 'y':
		#		checking = 1
		#		echecking = 'y'
		#		cursor.execute('''INSERT INTO tkb_email_conf(date,checking,employee) VALUES(%s,%s,%s)''', (current_date,checking,echecking))
		#		db.commit()
		#		
		#		tech_report_email()
		else:
			return
			
		db.close()
			
	return 
	
# Send tech emails to T Tobey for all those that have information in
def tech_report_email():
	# Current tech will be request.session.login_tech
	# Initialize counter for message length
	m_ctr = 0
	subjectA = []
	
	# db, cursor = db_set(request)
	db, cursor = db_open()
	tql = "SELECT * FROM tkb_techs"
	cursor.execute(tql)
	tmpA = cursor.fetchall()
	
	for x in tmpA:
		m_ctr = 0
		name = x[1]
		#return render(request,'done_test3.html',{'name':name})
		sql = "SELECT * FROM pr_downtime1 WHERE whoisonit = '%s' ORDER BY completedtime DESC limit 60" %(name)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		job_assn = []
		job_date = []
		job_solution = []
		a = []
		b = []
		c = []
		d = []
	
		message_subject = 'Tech Report from :' + name
		# set request.session.email_name as the full email address for link
		
		
		
		#email_name = ["stackpolepmds@gmail.com","dave7995@gmail.com"]
		#toaddrs = "; ".join(email_name)
		
		
		# Add name to email list
		# toaddrs = ["dclark@stackpole.com"]

		toaddrs = ["dclark@stackpole.com","ttobey@stackpole.com","dmilne@stackpole.com","jbarker@stackpole.com","tkuepfer@stackpole.com","lvaters@stackpole.com","pwilson@stackpole.com","mle@stackpole.com","pbui@stackpole.com","ssmith@stackpole.com","sherman@stackpole.com","nkleingeltink@stackpole.com","kbaker@stackpole.com","jpankratz@stackpole.com","kfaubert@stackpole.com","kfrey@stackpole.com","ghundt@stackpole.com","dpeachy@stackpole.com"]
		#toaddrs = ["dclark@stackpole.com"]
		fromaddr = 'stackpole@stackpole.com'
		frname = 'Dave'
		server = SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('StackpolePMDS@gmail.com', 'stacktest6161')
	
	
	
		message = "From: %s\r\n" % frname + "To: %s\r\n" % toaddrs + "Subject: %s\r\n" % message_subject + "\r\n" 
		#message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
		
		message = message + message_subject + "\r\n\r\n" + "\r\n\r\n"
		for x in tmp:
			# assign job date and time to dt
			dt = x[7]
			dtt = str(x[7])
			dt_t = time.mktime(dt.timetuple())
			# assign current date and time to dtemp
			dtemp = vacation_temp()
			dtemp_t = time.mktime(dtemp.timetuple())
			# assign d_diff to difference in unix
			d_dif = dtemp_t - dt_t
			# kkd= request.session["sskk"]
			if d_dif < 86400:
				message = message + '[' + dtt[:16]+'] ' + x[0] + ' - ' + x[1] + ' --- ' + x[8] + "\r\n\r\n"
				m_ctr = m_ctr + 1
			# retrieve left first character of login_name only
			name_temp1 = name[:1]
			# retrieve last name of login name only 
			name_temp2 = name.split(" ",1)[1]

		if m_ctr > 0:
			server.sendmail(fromaddr, toaddrs, message)
		server.quit()
	
	db.close()
	return
