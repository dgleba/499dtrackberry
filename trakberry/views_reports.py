from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from time import strftime
from datetime import datetime
from views_global_mods import machine_rates, Metric_OEE
import MySQLdb
import time

from views_db import db_open, db_set

def fup(x):
	return x[2]

def gup(x):
	return x[5]
	
def tup(x):
	return x[4]
def jup(x):
	return x[4]	
	
def eup(x):
	global st, nt
	nt.append(str(x[4]))
	st.append(str(x[5]))

def mup(x):
	global dt
	dt.append(str(x[7]))
		
# Updated April 21,2018
# Module to retrieve report information
# Chosen Date Report on Production
def production_report_date(request):
	machine_list = ['Trilobe','Optimized','8','8','8','8','8','8','8','8','8','8']
	m_s = ['' for x in range(36)]
	part = [0 for x in range(36)] 
	op = [0 for x in range(36)] 
	machine = [0 for x in range(36)]
	count = [0 for x in range(36)]
	count_cell = [0 for x in range(36)]
	count_count = [0 for x in range(36)]
	part = [0 for x in range(36)]
	required = [0 for x in range(36)]
	projection = [0 for x in range(36)]
	rate = [0 for x in range(36)]
	target = [0 for x in range(36)]
	hrate = [0 for x in range(36)]
	OEE = [0 for x in range(36)]
	loop_count = [0 for x in range(36)]
	down_time = [0 for x in range(36)]
	ttest = [0 for x in range(36)]

	diff_time = [0,0,0,0]
	diff = [0,0,0,0]
	cycle = [0,0,0,0]
	yellow = [0,0,0,0]
	red = [0,0,0,0]
	total = 0
	shift = [0 for x in range(36)]
	sh_col = [0 for x in range(36)]
	global st, pt_ctr,nt, pt, dt
	start_date = request.session["s_date"]
	try:
		temp = datetime.strptime(start_date,"%Y-%m-%d")
		start_stamp = int(time.mktime(temp.timetuple()))
		start_tuple = time.localtime(start_stamp)
	except:
		start_stamp=""
		start_tuple=""
	
	# Set start and finish time as timestamp for specific date (start_stamp)
	s = start_stamp - 3600
	f = start_stamp + 82800
	fi = start_stamp + 25200
	ff = start_stamp + 54000
	xx = s
	yy = fi
	yy_now = int(time.time())
	if yy_now < yy:
		yy = yy_now
		
	db, cursor = db_set(request)	
	
	stemp = temp
	stemp = start_date
	# Collect data for entire day and place in 'tmp'
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' AND part_timestamp < '%d'" %(s,f)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	cnt = 0
	
	for ctr in range(0,3):
		op_ctr = 1
		for y in range(0, 12):
			st = []
			nt = []
			pt = []
			dt = []
			
			# calculate xcnt which is counter for which cell to put cell total into
			#xcnt = int(cnt / 4)
			xcnt = cnt			
			xcnt = cnt - (3*int(float(cnt)/3))
			
			cnt_row = 0
			if cnt > 11 and cnt < 24:
				cnt_row = 1
			if cnt > 23:
				cnt_row = 2	
			
			xcnt = xcnt + cnt_row * 3
			
			
			
			#count_cell[cnt] = xcnt
			
			[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) > 0 and tup(x)>xx and tup(x)<yy ]
			count[cnt] = sum(int(i) for i in st)
			
			# uncomment below to use real one....next line down is just testing
			#count_cell[xcnt] = count_cell[xcnt] + count[cnt]
			ycnt = cnt - ((int(cnt / 3)) * 3) + (( int( cnt / 12 )) * 12 )
			
			try:
				count_cell[ ycnt ] = count_cell[ ycnt ] + count[cnt]
			except:
				count_cell[ cnt ] = 88
			
			
			machine[cnt] = machine_list[y]
			# set and increment op counter 
			op[cnt] = op_ctr
			op_ctr = op_ctr + 1
			if op_ctr > 3:
				op_ctr = 1

			[mup(x) for x in tmp if fup(x) == machine_list[y] and tup(x)>xx and tup(x)<yy]
			down_time[cnt] = sum(int(i) for i in dt)
			
			time_ran = (yy - xx) 
			
			rate = (count[cnt]/float(time_ran))
			projection[cnt] = round(rate * 28800,0)
			
			
			try:
				temp_part = [item[3] for item in tmp if item[4]==int(max(nt))]
				part[cnt] = temp_part[0]
				#	part[cnt] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
				
			except:
				part[cnt] = "---"				
			#	part[cnt] = "\n".join("50-3632")
					
			# Call module machine_rates to retrive the machine rate  mrate
			mrate = machine_rates(part[cnt],machine[cnt])
			
			required[cnt] = round(mrate*8,0)
			
			#  Old Calculation
			#target[cnt] = round((mrate/float(3600))*(time_ran - down_time[cnt]),0)
			
			# New Calculation that doesn't use downtime
			target[cnt] = mrate * 8
			
			hrate[cnt] = round(mrate *3600,2)
			total = total + count[cnt]	

			#target[cnt] = int(down_time[cnt])
			target[cnt] = int(target[cnt])
				
			sh_col[cnt] = ctr + 1
			if y == 0:
				shift[cnt] = ctr + 1

			# Assign OEE to MOEE and set it to proper formatting
			MOEE = Metric_OEE(yy,xx,down_time[cnt],count[cnt],mrate)
			temp_moee = int(MOEE)
			#return render(request, "test994.html", {'N':temp_moee})
			
			if MOEE > 0 :
				MOEE = int (MOEE * 1000)
				if temp_moee > 100 :
					MOEE = str ( MOEE ) 
					MOEE = MOEE[:3]  + ' %' 
				else:
					MOEE = str ( MOEE ) 
					MOEE = MOEE[:2]  + ' %' 
				OEE [ cnt ] = MOEE
			else:
				OEE [ cnt ] = '00.00%'
			#loop_count[cnt] = yy
			loop_count[cnt] = cnt
			h = str(cnt)
			hh = str(machine[cnt])
			m_s[cnt] = hh + h
			m_s[cnt] = int(cnt)
			#m_s[cnt] = int(m_s[cnt])
			

			cnt = cnt + 1
			
		xx = xx + 28800 
		yy = yy + 28800
		yy_now = int(time.time())
		if yy_now < yy:
			yy = yy_now
		
	request.session["machine_chart"] = "nope"
	list = zip(machine,count,part,shift,sh_col,OEE,target,op,loop_count,count_cell,m_s)
	#list = zip(machine,count,part,shift,sh_col,OEE,target,op,loop_count)
	return render(request, "report_page_day.html", {'List':list, 'S':stemp})
	#return render(request,"test4.html",{'List':list})
	
# Backup of formated Production Date 
def production_report_date_2(request):
	machine_list = ['1501','1515','1515','1506','1507','1501','1519','8','8','1520','8','8']
	m_s = ['' for x in range(36)]
	part = [0 for x in range(36)] 
	op = [0 for x in range(36)] 
	machine = [0 for x in range(36)]
	count = [0 for x in range(36)]
	count_cell = [0 for x in range(36)]
	count_count = [0 for x in range(36)]
	part = [0 for x in range(36)]
	required = [0 for x in range(36)]
	projection = [0 for x in range(36)]
	rate = [0 for x in range(36)]
	target = [0 for x in range(36)]
	hrate = [0 for x in range(36)]
	OEE = [0 for x in range(36)]
	loop_count = [0 for x in range(36)]
	down_time = [0 for x in range(36)]
	ttest = [0 for x in range(36)]

	diff_time = [0,0,0,0]
	diff = [0,0,0,0]
	cycle = [0,0,0,0]
	yellow = [0,0,0,0]
	red = [0,0,0,0]
	total = 0
	shift = [0 for x in range(36)]
	sh_col = [0 for x in range(36)]
	global st, pt_ctr,nt, pt, dt
	start_date = request.session["s_date"]
	try:
		temp = datetime.strptime(start_date,"%Y-%m-%d")
		start_stamp = int(time.mktime(temp.timetuple()))
		start_tuple = time.localtime(start_stamp)
	except:
		start_stamp=""
		start_tuple=""
	
	# Set start and finish time as timestamp for specific date (start_stamp)
	s = start_stamp - 3600
	f = start_stamp + 82800
	fi = start_stamp + 25200
	ff = start_stamp + 54000
	xx = s
	yy = fi
	yy_now = int(time.time())
	if yy_now < yy:
		yy = yy_now
		
	db, cursor = db_set(request)	
	
	stemp = temp
	stemp = start_date
	# Collect data for entire day and place in 'tmp'
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' AND part_timestamp < '%d'" %(s,f)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	cnt = 0
	
	for ctr in range(0,3):
		op_ctr = 1
		for y in range(0, 12):
			st = []
			nt = []
			pt = []
			dt = []
			
			# calculate xcnt which is counter for which cell to put cell total into
			#xcnt = int(cnt / 4)
			xcnt = cnt			
			xcnt = cnt - (3*int(float(cnt)/3))
			
			cnt_row = 0
			if cnt > 11 and cnt < 24:
				cnt_row = 1
			if cnt > 23:
				cnt_row = 2	
			
			xcnt = xcnt + cnt_row * 3
			
			
			
			#count_cell[cnt] = xcnt
			
			[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) > 0 and tup(x)>xx and tup(x)<yy ]
			count[cnt] = sum(int(i) for i in st)
			
			# uncomment below to use real one....next line down is just testing
			#count_cell[xcnt] = count_cell[xcnt] + count[cnt]
			ycnt = cnt - ((int(cnt / 3)) * 3) + (( int( cnt / 12 )) * 12 )
			
			try:
				count_cell[ ycnt ] = count_cell[ ycnt ] + count[cnt]
			except:
				count_cell[ cnt ] = 88
			
			
			machine[cnt] = machine_list[y]
			# set and increment op counter 
			op[cnt] = op_ctr
			op_ctr = op_ctr + 1
			if op_ctr > 3:
				op_ctr = 1

			[mup(x) for x in tmp if fup(x) == machine_list[y] and tup(x)>xx and tup(x)<yy]
			down_time[cnt] = sum(int(i) for i in dt)
			
			time_ran = (yy - xx) 
			
			rate = (count[cnt]/float(time_ran))
			projection[cnt] = round(rate * 28800,0)
			
			
			try:
				temp_part = [item[3] for item in tmp if item[4]==int(max(nt))]
				part[cnt] = temp_part[0]
				#	part[cnt] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
				
			except:
				part[cnt] = "---"				
			#	part[cnt] = "\n".join("50-3632")
					
			# Call module machine_rates to retrive the machine rate  mrate
			mrate = machine_rates(part[cnt],machine[cnt])
			
			required[cnt] = round(mrate*8,0)
			target[cnt] = round((mrate/float(3600))*(time_ran - down_time[cnt]),0)
			hrate[cnt] = round(mrate *3600,2)
			total = total + count[cnt]	

			#target[cnt] = int(down_time[cnt])
			target[cnt] = int(target[cnt])
				
			sh_col[cnt] = ctr + 1
			if y == 0:
				shift[cnt] = ctr + 1

			# Assign OEE to MOEE and set it to proper formatting
			MOEE = Metric_OEE(yy,xx,down_time[cnt],count[cnt],mrate)
			
			
			if MOEE > 0 :
				MOEE = int (MOEE * 1000)
				MOEE = str ( MOEE ) 
				MOEE = MOEE[:2] + '.' + MOEE[1:] + '%' 
				OEE [ cnt ] = MOEE
			else:
				OEE [ cnt ] = '00.00%'
			#loop_count[cnt] = yy
			loop_count[cnt] = cnt
			h = str(cnt)
			hh = str(machine[cnt])
			m_s[cnt] = hh + h
			m_s[cnt] = int(m_s[cnt])
#			m_s[cnt] = str(str(machine[cnt]) + '|' + str(cnt))
			cnt = cnt + 1
			
		xx = xx + 28800 
		yy = yy + 28800
		yy_now = int(time.time())
		if yy_now < yy:
			yy = yy_now
		
	request.session["machine_chart"] = "nope"
	list = zip(machine,count,part,shift,sh_col,OEE,target,op,loop_count,count_cell,m_s)
	#list = zip(machine,count,part,shift,sh_col,OEE,target,op,loop_count)
	return render(request, "report_page_day.html", {'List':list, 'S':stemp})
	#return render(request,"test4.html",{'List':list})
def production_report_date_B(request):

	# Assign machine names.  Later this can be input as a table for now it 
	# will be hardcoded
	machine_list = [677,748,749,750]
#	total = [0,0,0,0]
#	part = [0,0,0,0]

	# inintialze for 12 now but should be table value based on number of machines x 3 shifts
	total = [0 for x in range(12)] 
	part = [0 for x in range(12)] 
	machine = [0 for x in range(12)]
	stamp = [0 for x in range(12)]
	tctr = [0 for x in range(12)]
	part_total = ["50-3632","50-0786","50-4916"]
	shift = [0 for x in range(12)]
	# Number of Machines
	num_machines = 4
	
	start_date = request.session["s_date"]
	
	
	try:
		temp = datetime.strptime(start_date,"%Y-%m-%d")
		start_stamp = int(time.mktime(temp.timetuple()))
		start_tuple = time.localtime(start_stamp)
	except:
		start_stamp=""
		start_tuple=""

	
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)
	ctr = 0
	ctr2 = 0
	# Loop to respective number of machines, this will be tabled later on
	for i in range(0, 3):
		st = start_stamp - 3600
		fi = start_stamp + 25200
		
		for ii in range(0, num_machines):
		
			try:
				sql = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[ii], st, fi)
				cursor.execute(sql)
				tmp = cursor.fetchall()
				tmp2 = tmp[0]
				total[ctr] = tmp2[0]
			
		
				sqm = "SELECT (part_number) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[ii], st, fi)
				cursor.execute(sqm)
				tmp = cursor.fetchall()
				tmp2 = tmp[0]
				part[ctr] = tmp2[0]
			except:
				total[ctr] = 0
				part[ctr] = 0

				
			
			machine[ctr] = machine_list[ii]
			stamp[ctr] = start_stamp
			tctr[ctr] = ctr2

			if ctr == 0:
				shift[ctr] = ctr2+1
			elif ctr == 4:
				shift[ctr] = ctr2+1
			elif ctr == 8:
				shift[ctr] = ctr2+1
			elif ctr == 3:
				shift[ctr] = 99	
			elif ctr == 7:
				shift[ctr] = 99

			try:
				if tctr[ctr-1] == tctr[ctr]:
					tctr[ctr] = -1
			except:
				tctr[ctr] = ctr2
			ctr = ctr + 1
			
		start_stamp = start_stamp + 28800
		ctr2 = ctr2 + 1
		
	list = zip(machine,total,part,shift)
	return render(request, "report_page_day.html", {'List':list, 'S':start_tuple})

def production_report(request):

	machine_list = [677,748,749,750]
	total = [0,0,0,0]
	part = [0,0,0,0]
	
	start_date = request.session["s_date"]
	end_date = request.session["e_date"]
	
#	temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
	temp = datetime.strptime(start_date,"%Y-%m-%d")
	start_stamp = int(time.mktime(temp.timetuple()))
	start_tuple = time.localtime(start_stamp)

#	temp = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")
	temp = datetime.strptime(end_date,"%Y-%m-%d")
	end_stamp = int(time.mktime(temp.timetuple()))
	end_tuple = time.localtime(end_stamp)	

	db, cursor = db_set(request)
	cursor = db.cursor()
	
	for i in range(0, 4):
	
		sql = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[i], start_stamp, end_stamp)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		total[i] = tmp2[0]
		
		sqm = "SELECT (part_number) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[i], start_stamp, end_stamp)
		cursor.execute(sqm)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		part[i] = tmp2[0]
	
	list = zip(machine_list,total,part)
	return render(request, "report_page.html", {'List':list , 'S':start_tuple, 'E':end_tuple})
