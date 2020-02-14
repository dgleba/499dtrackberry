from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views import display, test, display_time
from views_db import db_open, db_set
from views_global_mods import machine_rates
from views_reports import production_report, production_report_date
from trakberry.forms import part_number, report_dateForm
import MySQLdb
from time import strftime
from datetime import datetime
import time
from django.core.context_processors import csrf

# Updated June 10,2015

# Module to simulate Machine Inputs for M/C  677 , 748 , 749 , 750


def fup(x):
	return x[2]
	
def tup(x):
	global tst, down_time
	tst.append(str(x[5]))
	
def nup(x):
	return x[4]
	
def mup(x):
	global dt
	dt.append(str(x[7]))	
			
# Module to Take entry simulate Pi 
# Eventually this module will link create and enter data into MySQL from button presses to simulate machine operation
# so we can run the view on another terminal to test.
def edit_part(request):
	request.session["details_track"] = 1
	p = 101
	
	mc = ""
	prt = ""
	try:
		request.session["prt"]
	except:
		request.session["prt"] = "" 
	try:
		request.session["mc"]
	except:
		request.session["mc"] = ""
		
	if request.POST:

		mc = request.POST.get("mc")
		request.session["mc"] = mc
		prt = request.POST.get("part")
		request.session["prt"] = prt	
		t = int(time.time())
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		sql =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,part_number) values("%s","%s","%s","%s")' % (p,mc,t,prt) )
		
		cur.execute(sql)
		db.commit()
		db.close()		

		request.session["details_track"] = 0	
		return display(request)
		
	else:
		form = part_number()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tb_edit_partnumber.html', args)
	
def select_date(request):

	
	try:
		request.session["s_date"]
	except:
		request.session["s_date"] = ""
	try:
		request.session["e_date"]
	except:
		request.session["e_date"] = ""		
	try:
		request.session["machine"]
	except:
		request.session["machine"] = ""				

		
	if request.POST:

		request.session["s_date"] = request.POST.get("start_date")
		request.session["e_date"] = request.POST.get("end_date")
		request.session["machine"] = request.POST.get("machine")

		return production_report(request)
		
	else:
		form = report_dateForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'report_form.html', args)	
	
# *****************************************************
# Select Date for Daily Report Display  ***************
# *****************************************************
def select_day(request):
	# Pause Tracking While looking at reports
	request.session["details_track"] = 1
	
	try:
		request.session["s_date"]
	except:
		request.session["s_date"] = ""
	try:
		request.session["e_date"]
	except:
		request.session["e_date"] = ""
	try:
		request.session["machine"]
	except:
		request.session["machine"] = ""

	if request.POST:

		request.session["s_date"] = request.POST.get("start_date")
		#request.session["e_date"] = request.POST.get("end_date")
		request.session["e_date"] = ""
		request.session["machine"] = request.POST.get("machine")

		return production_report_date(request)
		
	else:
		form = report_dateForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'report_form_date.html', args)

# ************************************************************
# Select Date For Snapshot Report  ***************************
# ************************************************************
def select_datetime(request):
	
	try:
		request.session["s_date"]
	except:
		request.session["s_date"] = ""
	try:
		request.session["e_date"]
	except:
		request.session["e_date"] = ""		
	try:
		request.session["machine"]
	except:
		request.session["machine"] = ""				

		
	if request.POST:

		request.session["s_date"] = request.POST.get("start_date")
		#request.session["e_date"] = request.POST.get("end_date")
		request.session["e_date"] = ""
		request.session["machine"] = request.POST.get("machine")
		return display_time(request)
		
	else:
		form = report_dateForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'report_form_snap.html', args)	
	
# Module to obtain graphdata for a current tracking machine and send it to display on a graph	
def graph_gf6(request, index):
	global dt
	
	request.session["machine_graph"] = index

	m = str(index)
	part = '50-3632'

	machine_rate = machine_rates(part,m)
	
	t=int(time.time())
	tm = time.localtime(t)
	
	shift_start = -1
	if tm[3]<23 and tm[3]>=15:
		shift_start = 15
	elif tm[3]<15 and tm[3]>=7:
		shift_start = 7
	cur_hour = tm[3]
	if cur_hour == 23:
		cur_hour = -1
	
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])

	db, cursor = db_set(request)
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d' and machine = '%s'" %(u,t,m)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	
	mrr = machine_rate / float(60)

	dt = []
	[mup(x) for x in tmp if fup(x) == m]
	down_time = sum(int(i) for i in dt)
	
	
	mrr = (machine_rate*(28800-down_time))/float(28800)
	gr_list, brk1, brk2, multiplier  = Graph_Data(t,u,m,tmp,mrr)
	
	# Test Return value
	#return render(request, "test4.html",{'X':multiplier})
	
	
	return render(request, "graph_gf6.html",{'GList':gr_list})		
	
# Module to obtain graphdata for a past report of a machine and send it to display on a graph	
def graph_gf6_report(request,index):
	mm=str(index)
	
	# take the first 4 digits as your machine number
	machine_number = mm[:4]
	
	if machine_number == 'Tril':
		machine_number = 'Trilobe'
		shift_number = mm[7:9]
		part = '50-1467'
	elif machine_number == 'Opti':
		machine_number = 'Optimized'
		shift_number = mm[9:9]
		part = '50-1437'
	else:
		# take the remaining digits as your shift association
		shift_number=mm[4:9]
		machine_number=int(machine_number)
		part = '50-9341'
		
	shift_number=int(shift_number)
	
	global dt
	request.session["machine_graph"] = machine_number
	m = str(machine_number)


	machine_rate = machine_rates(part,m)
	
#	t=int(time.time())
#	tm = time.localtime(t)
	
#	shift_start = -1
#	if tm[3]<23 and tm[3]>=15:
#		shift_start = 15
#	elif tm[3]<15 and tm[3]>=7:
#		shift_start = 7
#	cur_hour = tm[3]
#	if cur_hour == 23:
#		cur_hour = -1
	
#	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])
#	u = 1474052400
#	t = 1474081200
	start_date = request.session["s_date"]
	try:
		temp = datetime.strptime(start_date,"%Y-%m-%d")
		start_stamp = int(time.mktime(temp.timetuple()))
	except:
		start_stamp=""
		start_tuple=""
	
	# Set start and finish time as timestamp for specific date (start_stamp)
#	s = start_stamp - 3600
#	f = start_stamp + 82800
#	fi = start_stamp + 25200
#	ff = start_stamp + 54000
	if shift_number < 12:
		u_adj = -3600
		t_adj = 25200
	elif shift_number < 24:
		u_adj = 25200
		t_adj = 54000
	else:
		u_adj = 54000
		t_adj = 82800


#	u = 1473994800
#	t = 1474023600
	u = int(start_stamp) + int(u_adj)
	t = int(start_stamp) + int(t_adj)
	
	db, cursor = db_set(request)
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d' and machine = '%s'" %(u,t,m)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	machine = tmp[2]
	counter = tmp[6]
	
	
	list = zip(machine,counter)
	
	mrr = machine_rate / float(60)

	dt = []
	[mup(x) for x in tmp if fup(x) == m]
	down_time = sum(int(i) for i in dt)
	
	
	mrr = (machine_rate*(28800-down_time))/float(28800)
	gr_list, brk1, brk2, multiplier  = Graph_Data(t,u,m,tmp,mrr)
	
	# Test Return value
	#return render(request, "test4.html",{'list':tmp})
	
	
	return render(request, "graph_gf6.html",{'GList':gr_list})	
	
def Graph_Data(t,u,machine,tmp,multiplier):
	global tst
	cc = 0
	cr = 0
	cm = 0
	# last_by used for comparison
	last_by = 0
	temp_ctr = 0
	brk1 = 0
	brk2 = 0
	multiplier = multiplier / float(60)
	
	tm_sh = int((t-u)/60)
	px = [0 for x in range(tm_sh)]
	by = [0 for x in range(tm_sh)]
	ay = [0 for x in range(tm_sh)]
	cy = [0 for x in range(tm_sh)]
	for ab in range(0,tm_sh):

		px[ab] =u + (cc*60)
		yy = px[ab]
		cc = cc + 1
		cr = cr + multiplier
		cm = cr * .8
		tst = []
		[tup(x) for x in tmp if fup(x) == machine and nup(x) < yy]
		by[ab] = sum(int(i) for i in tst)
		ay[ab] = int(cr)
		cy[ab] = int(cm)
		
		# *** Calculate the longest break time in minutes
		# *** and assign to brk_ctr
		if by[ab] == last_by:
			temp_ctr = temp_ctr + 1
		else:
			if temp_ctr > brk1:
				brk1 = temp_ctr
			elif temp_ctr > brk2:
				brk2 = temp_ctr
			temp_ctr = 0
			last_by = by[ab]
		# ************************************************

	tm_sh = tm_sh - 1
	lby = by[tm_sh]
	lay = ay[tm_sh]
	lpx = px[tm_sh]
	gr_list = zip(px,by,ay,cy)	
	
	#return gr_list, brk1, brk2, tm_sh
	return gr_list, brk1, brk2, multiplier
	
	
	
