from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import tech_closeForm, tech_loginForm, tech_searchForm, tech_message_Form
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_email import e_test
from views_supervisor import supervisor_tech_call
import MySQLdb
import time
import datetime

#import datetime as dt 
from django.core.context_processors import csrf

def out(request):
	#request.session["test"] = 78
	return render(request, "out.html")

# Module to Check if we need to send downtime report out
# via email.   This goes out through the Tech App refreshing	

def hour_check():
	# obtain current date from different module to avoid datetime style conflict

	h = 2
	m = 2
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
		sql = "SELECT checking FROM tkb_email_conf where date='%s'" %(current_date)
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
	
def reset_call_route(request):
	request.session["call_route"] = 'supervisor'
	return render(request, "out.html")

def tech_email_test(request):
	send_email = hour_check()
	if send_email == 1:
		return render(request, "email_downtime.html")
		
	return render(request, "email_downtime_cycle.html")
		
def tech(request):

#	send_email = hour_check()
#	if send_email == 1:
#		return e_test(request)	
		#return render(request, "email_downtime.html")

	try:
		request.session["login_tech"] 
	except:
		request.session["login_tech"] = "none"
	try:
		request.session["tech_ctr"] 
	except:
		request.session["tech_ctr"] = 0
  
	request.session["refresh_tech"] = 0
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
	tch = []

	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)   

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	# Retrieve information from Database and put 2 columns in array {list}
	# then send array to Template machinery.html
	c = ["tech","Jim Barker"]
	j = "tech"
	jj = "Tech"
	a1 = "Kevin Bisch"
	a2 = "Muoi Le"
	a3 = "Jim Barker"
	a4 = "Scott Smith"
	a5 = "Toby Kuepfer"
	a6 = "Terry Kennedy"
	a7 = "Paul Wilson"
	a8 = "Chris Strutton"
	a9 = "Al Vilandre"
	a10 = "Woodrow Sismar"
	
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	sqlT = "SELECT * FROM pr_downtime1 where closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s'" %(j,jj,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10)

	cursor.execute(sqlT)
	tmp = cursor.fetchall()
	
	ctr = 0
	for x in tmp:
		tmp2 = (tmp[ctr])
		temp_pr = tmp2[3]
		if temp_pr == "A":
			tp = 1
		elif temp_pr =="c":
			tp = 3
		elif temp_pr =="b" :
			tp = 2
		elif temp_pr =="B" :
			tp = 2
		elif temp_pr =="C" :
			tp = 3
		elif temp_pr =="D"	:
			tp = 4
		elif temp_pr =="E":
			tp = 5
		
		job.append(tmp2[0])
		prob.append(tmp2[1])
		priority.append(tp)
		id.append(tmp2[11])
		tmp3 = tmp2[4]
		if tmp3 == "tech":
			tmp3 = "TAKE CALL"
		if tmp3 == "Tech":
			tmp3 = "TAKE CALL"	
		tch.append(tmp3)
		ctr = ctr + 1
		
	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			if int(priority[ii]) < int(priority[i]):
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
				ttch = tch[i]
				tch[i] = tch[ii]
				tch[ii] = ttch
	if request.session["tech_ctr"] == ctr:
		request.session["tech_alarm"] = "/media/clock2.wav"
	else:
		request.session["tech_alarm"] = "/media/clock.wav"
		request.session["tech_ctr"] = ctr
	list = zip(job,prob,id,tch,priority)
	
	db.close()
	n = "none"
	if request.session["login_tech"] == "Jim Barker":
		request.session["login_image"] = "/static/media/tech_jim.jpg"
		request.session["login_back"] = "/static/media/back_jim.jpg"
	elif request.session["login_tech"] == "Dave Clark":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/tech_training.jpg"
	elif request.session["login_tech"] == "Scott Smith":
		request.session["login_image"] = "/static/media/tech_scott.jpg"
		request.session["login_back"] = "/static/media/back_scott.jpg"
	elif request.session["login_tech"] == "Kevin Bisch":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "Woodrow Sismar":
		request.session["login_image"] = "/static/media/tech_woodrow.jpg"
		request.session["login_back"] = "/static/media/back_woodrow.jpg"
	elif request.session["login_tech"] == "Al Vilandre":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"			
	elif request.session["login_tech"] == "Muoi Le":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"				
	else:
		request.session["login_image"] = "/static/media/tech_rick.jpg"
		request.session["login_back"] = "/static/media/back_rick.jpg"
		
  # call up 'display.html' template and transfer appropriate variables.  
  
  # *********************************************************************************************************
  # ******     Messaging portion of the Tech App  ***********************************************************
  # *********************************************************************************************************
	N = request.session["login_tech"]
	R = 0
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)	
		cur.execute(sql)
		tmp44 = cur.fetchall()
		tmp4 = tmp44[0]

		request.session["sender_name"] = tmp4[2]
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
	Z = 1
	if cnt > 0 :
		cnt = 1
		request.session["refresh_tech"] = 3
	# ********************************************************************************************************
	
	
	return render(request,"tech.html",{'L':list,'cnt':cnt,'M':tmp4,'N':n,'Z':Z})

def tech_message_close(request):
	request.session["refresh_tech"] = 0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech(request)

def tech_message_reply1(request):
	request.session["refresh_tech"]=0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech_message_reply2(request)
	
	
def job_call(request, index):	
    
	tec = request.session["login_tech"]

	# Select prodrptdb db located in views_db
	db, cur = db_set(request)  
	sql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (tec,index))
	cur.execute(sql)
	db.commit()
	db.close()

	return tech(request)

def job_close(request, index):	
	

	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)  
		

	sql = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	
	try:
		request.session["tech_comment"]
	except:
		request.session["tech_comment"] = ""

		
	if request.POST:
		
		# take comment into tx and ensure no "" exist.  If they do change them to ''
		
		tx = request.POST.get("comment")
		tx = ' ' + tx
		if (tx.find('"'))>0:
			#request.session["test_comment"] = tx
			#return out(request)
			ty = list(tx)
			ta = tx.find('"')
			tb = tx.rfind('"')
			ty[ta] = "'"
			ty[tb] = "'"
			tc = "".join(ty)
		else:
			tc = tx
		request.session["tech_comment"] = tc
		t = datetime.datetime.now()
		

		# Select prodrptdb db located in views_db
		db, cur = db_set(request)  

		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		db.close()
		
		db, cur = db_set(request)  
		tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
		cur.execute(tql)
		db.commit()
		db.close()

		return tech(request)
		
	else:
		form = tech_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_close.html', args)	
		
def tech_logout(request):	

	if request.POST:
        			
		tec = request.POST.get("user")
		pwd = request.POST.get("pwd")

	
		request.session["login_tech"] = tec
		
		
		
		return tech(request)
		
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_tech"] = "none"
	return render(request,'tech_login.html', args)	
	
def job_pass(request, index):	
	
	db, cursor = db_set(request)  
	sql = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	db.close()
	try:
		request.session["tech_comment"]
	except:
		request.session["tech_comment"] = ""

		
	if request.POST:

		tc = request.POST.get("comment")
		request.session["tech_comment"] = tc
		tp = request.POST.get("pass")
		request.session["tech_pass"] = tp
		t = datetime.datetime.now()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)

		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		db.close()
		
		db, cur = db_set(request)  
		tql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (tp,index))
		cur.execute(tql)
		db.commit()
		db.close()

		return tech(request)
		
	else:
		form = tech_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_pass.html', args)		

							  
def tech_recent(request):

	
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM pr_downtime1 ORDER BY called4helptime DESC limit 60" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["tech_display"] = 1
	return render(request,"tech_search_display.html",{'machine':tmp})

def tech_map(request):

	return render(request,"tech_map.html")	

def tech_history(request):	

	if request.POST:
        			
		machine = request.POST.get("machine")
		request.session["machine_search"] = machine
		db, cur = db_set(request)  		
		sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,3) = '%s' ORDER BY called4helptime DESC limit 20" %(machine)
		cur.execute(sql)
		tmp = cur.fetchall()
		db.close
		request.session["tech_display"] = 0
		return render(request,"tech_search_display.html",{'machine':tmp})
		
	else:
		
		form = tech_searchForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_search.html', args)		

def tech_tech_call(request):
	request.session["call_route"] = 'tech'
	request.session["url_route"] = 'tech.html'
	return supervisor_tech_call(request)
						  

def tech_message(request):	
	A = 'Chris Strutton'
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()

	db.close()

	if request.POST:
        			
		a = request.session["login_tech"]
		b = request.POST.get("name")
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'tech_message_form.html', {'List':tmp,'A':A,'args':args})	

def tech_message_reply2(request):	
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	if request.POST:
        			
		a = request.session["login_tech"]
		b = request.POST.get("name")
		b = request.session["sender_name"]
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'tech_message_reply_form.html', {'List':tmp,'args':args})	
	
def modal_test(request):	
	a = 1
	b = 1
	request.session["modal_1"] = a
	return render(request,'modal_test.html',{'b':b})
