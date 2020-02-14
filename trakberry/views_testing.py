from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from trakberry.forms import robot_machine_form, toggletest_Form
from views_global_mods import machine_rates, Metric_OEE
from time import strftime
from datetime import datetime
import MySQLdb
import time
from django.core.context_processors import csrf

def fup(x):
	return x[2]
def frup(x):
	return x[11]

def gup(x):
	return x[5]

def nup(x):
	return x[4]

def tup(x):
	global tst, down_time
	tst.append(str(x[5]))

def eup(x):
		global st, nt
		nt.append(str(x[4]))
		st.append(str(x[5]))

def mup(x):
		global dt
		dt.append(str(x[7]))

def pup(x):
	global lt
	lt.append(str(x[11]))
# **********************************************
# *******  Robot Tuples  ***********************
def robot_tup(x):
		global st, nt,pt
		nt.append(str(x[1]))
		pt.append(str(x[6]))
		st.append(str(x[2]))
		if str(x[3]):
			nt.append(str(x[1]))
			pt.append(str(x[6]))
			st.append(str(x[3]))
		if str(x[4]):
			nt.append(str(x[1]))
			pt.append(str(x[6]))
			st.append(str(x[4]))
		if str(x[5]):
			nt.append(str(x[1]))
			pt.append(str(x[6]))
			st.append(str(x[5]))

def robot_aup(x):
	return x[2]
	
	# **********************************************
def test_array(request):
	global st, nt, pt
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_robot_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	st = []
	nt = []
	pt = []

	[robot_tup(x) for x in tmp]

	rlist = zip(nt,st,pt)

	return render(request,"test7.html",{'list':rlist})

# **********************************************

def machine_list_display():
	global st, nt, pt
	db, cur = db_open()
	sql = "SELECT * FROM tkb_robot_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	st = []
	nt = []
	pt = []

	[robot_tup(x) for x in tmp]
	rlist = nt
	rlist = zip(nt,st,pt)

	#rlist.append(st)
	#rlist.append(pt)
	#rlist = zip(nt,st,pt)
	return rlist
	#return render(request,"test6.html",{'list':rlist})

# **********************************************

def part_list_display():

	db, cur = db_set(request)
	a = ['' for x in range(0)]
	b = ['' for x in range(0)]
	
	ctr = 1
	sw = 0
	sql = "SELECT DISTINCT Part FROM tkb_inventory_fixed ORDER BY %s %s" %('Part','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	
	for i in tmp:
		if ctr > 3:
			sw = 1
			ctr = 0
		a.append(i[0])
		b.append(sw)
		ctr = ctr + 1
		sw = 0
		#a.append(i[1])
		
	
	xy = zip(a,b)
	return xy
	
	

def cust_list_display():

	db, cur = db_set(request)
	sql = "SELECT DISTINCT Customer FROM tkb_inventory_fixed"
	cur.execute(sql)
	tmp = cur.fetchall()

	return tmp

def emp_list_display():
	db, cur = db_set(request)
	sql = "SELECT Employee FROM tkb_employee ORDER BY %s %s" %('Employee','ASC')
	#sql = "SELECT Employee FROM tkb_employee"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	
	return tmp
	
	
def test_display(request):

	t=int(time.time())
	u = t - 1800
	global st, pt_ctr,nt, pt, dt, tst
	db, cursor = db_set(request)
	
  
	#sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp> '%d'" %(u)
	cursor.execute(sql)
	tmp = cursor.fetchall()

	st = []
	nt = []
	pt = []
	dt = []
	df = []
	[eup(x) for x in tmp if fup(x) == '574' and gup(x) == 1]
	#count[y] = sum(int(i) for i in st)

	lst = int(min(nt))

	for y in nt:
		diff = int(y) - int(lst)
		df.append(str(diff))
		lst = y
	
	# sort data
#	ct = len(nt)
#	for x in range(0, ct-1):
#		for xx in range(x+1, ct):
#			if int(df[xx])< int(df[x]):
#				ddf = df[x]
#				df[x] = df[xx]
#				df[xx] = ddf
#				nnt = nt[x]
#				nt[x] = nt[xx]
#				nt[xx] = nnt
				
		

	mlist = zip(nt,df)
	return render(request,"test5.html",{'list':mlist})
 
def create_table_1(request):
	# Create a Testing Table
	
	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_schedule""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_schedule(Id INT PRIMARY KEY AUTO_INCREMENT,Date Date, Description CHAR(30), Job_Name CHAR(50), Shift CHAR(30), Position CHAR(30), Employee CHAR(30))""")
  
	db.commit()
	db.close()
	return render(request,'done_test.html')

def form_robot_machine_enter(request):

	try:
		request.session["robot"]
		request.session["machine1"]
		request.session["machine2"]
		request.session["machine3"]
		request.session["machine4"]
		request.session["part"]
		
	except:
		request.session["robot"] = ""
		request.session["machine1"] = ""
		request.session["machine2"]= ""
		request.session["machine3"]= ""
		request.session["machine4"] = ""
		request.session["part"] = ""
	
	if request.POST:

		request.session["robot"] = request.POST.get("robot")
		request.session["machine1"] = request.POST.get("machine1")
		request.session["machine2"] = request.POST.get("machine2")
		request.session["machine3"] = request.POST.get("machine3")
		request.session["machine4"] = request.POST.get("machine4")
		request.session["part"] = request.POST.get("part")

		
		return robot_machine_update(request)
		
	else:
		form = robot_machine_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'robot_machine_enter_form.html',{'args':args})	
	
def robot_machine_update(request):	
    
	robot = request.session["robot"]
	machine1 = request.session["machine1"]
	machine2 = request.session["machine2"]
	machine3 = request.session["machine3"]
	machine4 = request.session["machine4"]
	part = request.session["part"]

	db, cur = db_set(request) 	
	cur.execute('''INSERT INTO tkb_robot_list(Robot, Machine1, Machine2, Machine3, Machine4,Part) VALUES(%s,%s,%s,%s,%s,%s)''', (robot, machine1, machine2, machine3, machine4,part))
	db.commit()

	db.close()
	

	return display_robot_machine(request)	

def display_robot_machine(request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_robot_list" 
	cur.execute(sql)
	tmp = cur.fetchall()	
	tmp2 = tmp[0]
	db.close()
	return render(request, "display_robot_machine.html", {'List':tmp})	
	
def toggletest(request):

	try:
		request.session["shift_test"]
		
	except:
		request.session["shift_test"] = ""

	
	if request.POST:

		request.session["shift_test"] = request.POST.get("shift_test")

		return render(request, "test8.html")	
		
	else:
		form = robot_machine_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'toggletest.html',{'args':args})		

def test668(request):
	#request.session["test"] = 78
	return render(request, "test.html")
	
def test_datalist(request):
	return render(request, "safari/simple_datalist4.html")	

def clear_login(request):
	del request.session["login_name"]
	return render(request, "clear_login.html")	
	
	
