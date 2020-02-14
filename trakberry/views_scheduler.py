from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_vacation import vacation_set_current2, vacation_temp
from views_mod1 import time_output
from views_db import db_open, db_set
from forms import toggletest_Form, views_scheduler_selectionForm
from trakberry.forms import emp_training_form, emp_info_form, job_info_form
import MySQLdb
# import time
# import datetime
from time import mktime
from datetime import datetime, date
from collections import Counter

from django.core.context_processors import csrf
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2

# ====================================================================================================
# ----------------------   Everything below are Modules for NEW Algorithm ----------------------------
# ====================================================================================================
def Job_Total(E_Working):
	JE = ['' for x in range(0)]
	for i in range(0,len(E_Working)):
		for ii in range(0,len(E_Working[i])):
			JE.append(E_Working[i][ii])
	EJ = Counter(JE).values()
	EEJ = Counter(JE).keys()
	for i in range(0,len(EEJ)):
		for ii in range(i+1,(len(EEJ))-1):
			if EJ[ii] < EJ[i]:
				temp_EJ = EJ[ii]
				EJ[ii] = EJ[i]
				EJ[i] = temp_EJ
				temp_EEJ = EEJ[ii]
				EEJ[ii] = EEJ[i]
				EEJ[i] = temp_EEJ
	CE = zip(EEJ,EJ)
	return CE

def Job_One_Search1(CE,E_Working,N_Working):
	Job = 0
	Name = ""
	search_break = 0
	if CE[0][1] == 1:
		Job = CE[0][0]
		for i in range(0,len(E_Working)):
			for ii in range(0,len(E_Working[i])):
				if Job == E_Working[i][ii]:
					Name = N_Working[i]
					search_break = 1
				if search_break == 1:
					break
			if search_break == 1:
				break			
	return Job, Name
	
# Find and return the group of Names,Job Lists for all those containing job 'y'
def Job_Search(y,A,B):
	Temp_E = ['' for x in range(0)]
	Temp_N = ['' for x in range(0)]
	for i in range(0,len(A)):
		if y in A[i]:
			Temp_E.append(A[i])
			Temp_N.append(B[i])
	return Temp_E,Temp_N

def JobLength_Sort(E_Temp2,N_Temp2):
	qty = len(E_Temp2)
	for i in range(0,qty):
		for ii in range(i+1,qty-1):
			if len(E_Temp2[ii]) < len(E_Temp2[i]):
				temp_E = E_Temp2[ii]
				E_Temp2[ii] = E_Temp2[i]
				E_Temp2[i] = temp_E
				temp_N = N_Temp2[ii]
				N_Temp2[ii] = N_Temp2[i]
				N_Temp2[i] = temp_N
	return E_Temp2,N_Temp2
	
	
# Remove the 'name' and all the assigned jobs from the list
def Assign_Name(E_Working,N_Working,name):
	ctr = -1  # Start counter -1 because we increment at the beginning of the loop
	qty = len(E_Working)
	E_Working_Temp = ['' for x in range(qty-1)]  # Assign E_Working_Temp to full values minus 1 for person deleted
	N_Working_Temp = ['' for x in range(0)]	
	for i in range(0,qty):
		if N_Working[i] != name:
			ctr = ctr + 1
			N_Working_Temp.append(N_Working[i])
			E_Working_Temp[ctr] = E_Working[i]
			
	return E_Working_Temp,N_Working_Temp	

# Deletes the job from all people's list
def Assign_Job(E_Working,job):
	qty = len(E_Working)
	E_Working_Temp = ['' for x in range(qty)]
	for x in range(0,qty):
		E_Working_Temp[x] = ['' for y in range(0)]

	for i in range(0,qty):
		for ii in range(0,len(E_Working[i])):
			if (E_Working[i][ii]) != (job):
				E_Working_Temp[i].append(E_Working[i][ii])						
	return E_Working_Temp
	
def Assign(E_Working,N_Working, A_Name, A_Job, Name, Job):	
	A_Name.append(Name)
	A_Job.append(Job)
	E_Working = Assign_Job(E_Working, Job)
	E_Working, N_Working = Assign_Name(E_Working, N_Working, Name)
	return E_Working, N_Working, A_Name, A_Job	

# ====================================================================================================
# ===================  End of Modules for New Algorithm     ==========================================
# ====================================================================================================
	
def current_schedule(request):
	db, cur = db_set(request) 
	sql = "SELECT * FROM tkb_jobs ORDER BY %s %s, %s %s" %('Description', 'ASC', 'Job_Name','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	return render(request,"test3.html",{'total':tmp})

def set_rotation(request):
	db, cur =db_open()
	x = 0			
	mql = ('update tkb_employee_matrix SET Rotation="%s"' % (x))
	cur.execute(mql)
	db.commit()
	
	db.close()
	
	return render(request, "done_test.html")

# Display the Job Rotation for the shift 
def rotation_info_display(request):
	try:
		request.session["position"]
	except:
		request.session["position"] = 'CNC'
	position = request.session["position"]
	
	db, cur = db_set(request)
	curr_shift = request.session["matrix_shift"]
	sql = "SELECT * FROM tkb_employee_matrix WHERE Shift = '%s' and Position = '%s' ORDER BY %s %s , %s %s" %(curr_shift,position,'Employee', 'ASC','Job','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()

	cql = "SELECT COUNT(*) from tkb_jobs WHERE Position = '%s'" % (position)
	cur.execute(cql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	job_ctr = tmp3[0]
		
	jql = "SELECT * FROM tkb_jobs WHERE Position = '%s' ORDER BY  %s %s, %s %s" %(position,'Description','ASC','Job_Name','ASC')
	cur.execute(jql)
	jmp = cur.fetchall()


	ct = 1
	jct = 0

	j = []
	jc = []
	pj = ""
	for i in jmp:

		if ct == 1:
			pj = i[1]
		if i[1] != pj:
			j.append(str(pj))
			jc.append(jct)
			pj = i[1]
			jct = 0

		ct = ct + 1
		jct = jct + 1

	# *************  ??  **************
	j.append(str(pj))
	jc.append(jct)
	# *********************************

	db.close()
	a = 1
	c =int(job_ctr + 1)
	
	tjobs = zip(j,jc)
	
	ctr1 = 0
	k = []
	sw = -1
	c1 = '#DCDDDE'
	c2 = '#ffffff'
	jb = ""
	for i in tmp:
		if i[2] != jb:
			sw = sw * -1
			if sw == 1:
				ccc = c1
			else:
				ccc = c2
			jb = i[2]
		ctr1 = ctr1 + 1	
		if ctr1 == (job_ctr+1):
			sw = 1
			ctr1 = 1
		if ctr1 == 1:
			ccc = c1
			
				
		k.append(str(ccc))	
				
	#return render(request, "test67.html", {'tjobs':tjobs})
	col_jobs = float(94 / job_ctr)
	
	# Form for shift selection
	if request.POST:
		shift = request.POST.get("shift")
		request.session["matrix_shift"] = shift
		position = request.POST.get("position")
		request.session["position"] = position
		return rotation_info_reload(request)
	else:
		form = toggletest_Form
	args ={}
	args.update(csrf(request))
	args['form'] = form
	
	tmp4 = map(None,tmp,k)
	#tmp4 = zip(tmp,jc)	
	#return render(request, "test67.html", {'List':tmp,'List2':tmp4,'List3':jc})	
	return render(request, "rotation_info_display.html", {'List':tmp4,'B':job_ctr,'A':a,'C':c,'Jobs':jmp,'tjobs':tjobs,'D':col_jobs,'args':args})

def rotation_update(request, index):
	db, cur =db_open()
	sql = "SELECT Rotation FROM tkb_employee_matrix where Id='%s'" %(index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	
	#return render(request, "test99_1.html", {'test':tmp})
	
	
	level = int(tmp2[0])

	new_level = 0
	
	if level == 0:
		new_level = 1
	if level == 1:
		new_level = 0

	level = new_level				
	mql = ('update tkb_employee_matrix SET Rotation="%s" WHERE Id="%s"' % (level,index))
	cur.execute(mql)
	db.commit()
	
	db.close()
	
	return render(request, "done_rotation.html")	
	
def rotation_info_reload(request):
	return render(request, "done_rotation.html")		

def schedule_set(request):
	current_first = vacation_set_current2()
	request.session["current_first"] = current_first
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_jobs ORDER BY  %s %s, %s %s" %('Description','ASC','Job_Name','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	return render(request, "schedule_info_display.html", {'List':tmp})


# ****************************************************
# *     Scheduling Section                           *
# ****************************************************

#	+++++ Module for ensuring priority is numbered sequentially again after changes  +++++++++++++++++++++++
def schedule_init(request):
	r = 1
	rv = 0
	try:
		shift = request.session["matrix_shift"]
	except:
		shift = request.session["shift_priority"]
		
	db, cur = db_set(request)	
	aql = "SELECT COUNT(*) from tkb_employee_matrix WHERE Shift = '%s' and Rotation = '%s'" %(shift,r)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	job_count = tmp3[0]
	
	bql = "SELECT * FROM tkb_employee_matrix WHERE Shift = '%s' and Rotation = '%s' ORDER BY %s %s , %s %s" %(shift,r,'Employee', 'ASC','Priority','ASC')	
	cur.execute(bql)
	tmp = cur.fetchall()
	
	ct = 1
	current_employee = ''
	new_employee = 'start'
	for x in tmp:
		i_d = x[0]
		new_employee = x[1]
		if new_employee != current_employee:
			current_employee = new_employee
			ct = 1
		sql = ('update tkb_employee_matrix SET Priority="%s" WHERE Id ="%s"' % (ct, i_d))
		cur.execute(sql)
		db.commit()
		ct = ct + 1
	db.close()	 
	return
	#return render(request,'display_schedule.html',{'list':list2,'qq':qq})
	return render(request,'test22.html',{'tmp':tmp,'ID':shift})
	

# Set Schedule in table along with preselected jobs that could run
def schedule_set2(request):
	rv = 0
	# Testing rerout variable
	current_first = vacation_set_current2()
	request.session["date_curr"] = current_first
	
	request.session["loop_count"] = 0
	request.session["loop_name"] = ''
	request.session["button1"] = 'yes'
	request.session["job_n"] = 0
	request.session["route"] = 1
	request.session["add_route"] = 0
	request.session["stop_1"] = 0
	rotation = 1
	try:
		shift = request.session["matrix_shift"]
	except:
		shift = 'Cont A Nights CSD 2'
		request.session["matrix_shift"] = shift
		
	db, cur = db_set(request)
	
	employee = '---'
	final = 0
	dql = ('DELETE FROM tkb_schedule WHERE Finalize = "%s"'% (final))
	cur.execute(dql)
	db.commit()
	
	try:
		cql = "SELECT MAX(Id) from tkb_schedule"
		cur.execute(cql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		ctr_sched = tmp3[0]
		id_ctr = ctr_sched + 1
	except:
		id_ctr = 0	
			
	# Select all the Job_Names and Descriptions linked together that this shift rotation is eligible for
	# tmp(0) = Job_Name  :  tmp[1] = Description  :  tmp[2] = number of this combos in selected list
	sql = "SELECT Job_Name , Description, count(*) as total from tkb_employee_matrix where  Shift='%s' and Rotation='%s' GROUP by Job_Name, Description" % (shift,rotation)
	cur.execute(sql)
	tmp = cur.fetchall()
	
	position = request.session['position']
	Asql = "SELECT * from tkb_jobs WHERE Position = '%s' ORDER BY %s %s , %s %s" % (position, 'Description', 'ASC', 'Job_Name', 'ASC')
	cur.execute(Asql)
	Amp = cur.fetchall()
	
	for a in Amp:
		#id_ctr = id_ctr + 1
		selection = 0
#		for x in tmp:
#			if x[1] == '6L Output' or x[1] == '6L Input':
			#if x[1] == a[1] and x[0] == a[5]:
#				selection = 1

		# Temporary Code to force Continental Shift as default for Schedule start
		
		
		cvar = 0
		rvar = 1
		if shift == 'Cont B Days CSD 2' or shift == 'Cont B Nights CSD 2' or shift == 'Cont A Days CSD 2' or shift == 'Cont A Nights CSD 2':
			cvar = 1
			rvar = 0
			qvar = 0
		elif shift == 'Aft CSD 2' or shift == 'Day CSD 2' or shift =='Mid CSD 2':
			cvar = 1
			rvar = 1
			qvar = 0
		if position == 'Production':
			qvar = 1
			cvar = 0
			rvar = 0
			
		if a[1] == '6L Output' or a[1] == '6L Input':
			
			selection = cvar
		elif a[1] == 'GF6 Input' or a[1] == 'GF6 Reaction' or a[1] == 'ZF':
			selection = rvar
		else:
			selection = qvar
		
		# Add the number of jobs that Template a[7] requires.    0 if it is 0
		if a[7] > 0:
			for x in range (0,a[7]):
				id_ctr = id_ctr + 1
				cur.execute ('''INSERT INTO tkb_schedule(Description,Job_Name,Position,Shift,Selection,Id) VALUES(%s,%s,%s,%s,%s,%s)''',(a[1],a[5],a[6],shift,selection,id_ctr))
				db.commit()
				
	db.close()	
	return schedule_set3(request)

def schedule_set2b(request):
	db, cur = db_set(request)
	selection = 1
	a = '6L Output'
	b = 'Op 20 (Offline)'
	c = 'CNC'
	shift = 'Cont A Nights CSD 2'
	id_ctr = 99
	
	sql = "SELECT max(Id) from tkb_schedule"
	cur.execute(sql)
	mx = cur.fetchall()
	mxx = mx[0]
	mxxx = mxx[0]
	id_ctr = int(mxxx) + 1
	
	cur.execute ('''INSERT INTO tkb_schedule(Description,Job_Name,Position,Shift,Selection,Id) VALUES(%s,%s,%s,%s,%s,%s)''',(a,b,c,shift,selection,id_ctr))
	db.commit()
	db.close()
	return render(request,'done_add_test.html')	
	#return schedule_set3(request)
	
	
def schedule_set3(request):	
	
	
		
	#shift = 'Cont A Nights CSD 2'	
	finalize = 1
	try:
		shift = request.session["matrix_shift"]
	except:
		shift = 'Cont A Nights CSD 2'
		request.session["matrix_shift"] = shift
	
	db, cur = db_set(request)
	Bsql = "SELECT Description, count(*) as total from tkb_schedule where  Shift='%s'  and Finalize != '%s' GROUP by Description ORDER BY %s %s" % (shift,finalize,'Description','ASC')
	cur.execute(Bsql)
	bmp = cur.fetchall()
	
	Csql = "SELECT Id, Description, Job_Name, Selection from tkb_schedule where  Shift='%s' and Finalize != '%s' ORDER BY %s %s , %s %s" % (shift,finalize,'Description','ASC','Job_Name','ASC')
	cur.execute(Csql)
	cmp = cur.fetchall()
		
	db.close()
	ctr = 0

	sch = []
	cc = []
	v = []
	for x in cmp:
		if (bmp[ctr][0]) != (x[1]):
			ctr = ctr + 1
		try:	
			sch.append(str(bmp[ctr][0]))
			sch.append(bmp[ctr][1])
		except:
			sch.append('---')
			sch.append('---')
		sch.append(str(x[2]))
		cc.append(str(ctr))  # 

	aa = []
	bb = []
	dd = []
	ff = []
	gg = []
	kk = []
	ll = []
	prev = ''
	cct = 0
	ee = bmp[0][1]
	qq = '---'
	
	
	
		
		
	for i in cmp:
		ll.append(i[1])
		if prev == i[1]:
			bb.append('---')

		if i[1] != prev:
			prev = i[1]
			bb.append(i[1])

			ee = bmp[cct][1]
			cct = cct + 1	
#		bb.append(i[1])
		
#		if i[1] != prev:
#			prev = i[1]
		kk.append('') #Assigned Employee
		ff.append(ee)	 # Row Span (Number of Job Names for this Description)
		aa.append(str(i[0]))  # Id 
		dd.append(i[2])  #  Job Name
		gg.append(i[3])  # Selection (1 or 0)
		
		# aa 	ID
		# bb	Job Category
		# dd	Job Name
		# cc	 # of different jobs
		# ff 	Row span for that Job
		
	list = zip(aa,bb,dd,cc,ff,gg,kk,ll)
	
	
		
	
	#if request.session["add_route"] == 1:
	#return render(request,'test993.html',{'list':list})
	return schedule_set4(request,list)          # Actual next line
	
def schedule_set4(request,list):

	shift = request.session["matrix_shift"]
	try:
		position = request.session["position"]
	except:
		position = 'CNC'
	qty_jobs, qty_employee, tmp_count = schedule_qty(shift,position)
	A='Jobs'
	B='Employee'
	#return render(request, "testA.html", {'A':A,'a':qty_jobs,'B':B,'b':qty_employee})
	
	request.session['qty_jobs'] = qty_jobs
	request.session['qty_employee'] = qty_employee
	
	#Set Form Variables
	qq = '---'
	choice = []
	choice2 = []
	choice3 = []
	ac = []
	bc = []
	y = 1
	n = 0
	tn = []
	
	index = 0
	if request.POST:
		n_position = request.POST.get("position")
		try:
			position = request.session["position"]
		except:
			request.session["position"] = 'CNC'
			position = request.session['position']
		if n_position != position:
			request.session['position'] = n_position
			return render(request,'redirect_schedule1.html')

		#joe = 'happy time'
		#return render(request,'test996.html',{'list':joe})	
		request.session["date_curr"] = request.POST.get("date_curr")
		shft = request.POST.get("shift")
		if shft != shift:
			request.session["matrix_shift"] = shft
			return render(request,'redirect_schedule1.html')
		
		
		# Add Job (index) or Del Job(dindex) button action
		if 'index' in request.POST:
			index = request.POST.get("index")
			return schedule_add_job(request,index)
		if 'dindex' in request.POST:
			dindex = request.POST.get("dindex")
			return schedule_delete(request,dindex)
	
#		db, cur = db_set(request)
#		for x in list:
			tn.append(x[0])
#			if request.POST.get(str(x[0])):
#				aaa = x[0]
#				bbb = y
#				choice.append(x[0])
#				choice2.append(y)
#				choice3.append(x[2])
#			else:
#				aaa = x[0]
#				bbb = n
#				choice.append(x[0])
#				choice2.append(n)
#				choice3.append(x[2])
#			chc = zip(choice,choice2,choice3)
#			ac.append(aaa)
#			bc.append(bbb)
#			sql = ('update tkb_schedule SET Selection="%s" WHERE Id ="%s"' % (bbb, aaa))
#			cur.execute(sql)
#			db.commit()
			
			
			
			
#		db.close()
#		abc = zip(ac,bc)
		
		#   ******************************************************************************
		#   **  Below lines are for rerouting and testing.  Delete when running main   ***
		#   ******************************************************************************
		#if request.session["add_route"] == 2:
		#	return render(request,'test993.html',{'list':abc,'list2':list})
		#   ******************************************************************************
		
		
		
		db, cur = db_set(request)
		dt = request.session["date_curr"]
		csql = "SELECT count(*) as total from tkb_schedule where  Shift='%s'  and Date = '%s'" % (shift,dt)
		cur.execute(csql)
		t1 = cur.fetchall()
		t2 = t1[0]
		count_check = t2[0]
		
		# Fail if schedule already made for date selected
		if count_check > 0:
			request.session['qty_fail'] = 0
			return render(request,'display_schedule_fail2.html')

		return schedule_set5(request,list)
		return render(request,'display_schedule_formRefresh.html', {'a':list})

 #           return schedule_set5(request,chc)


	else:
		form = views_scheduler_selectionForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	ttt = 1
	ttt = str(ttt)


		
#	try:
#		add_job = request.session["add_job2"]
#	except:
#		add_job = 0
		
#	if add_job == 0:
#		current_first = vacation_set_current2()
#	else:
#		current_first = request.session["date_curr"]
#	request.session["add_job2"] = 0
	
	# Break loop to test data section
	#if request.session["add_route"] == 2:
	#	return render(request,'test993.html',{'list':list})	
	#if request.session["add_route"] == 1:
	#	request.session["add_route"] = 2
			
		
	current_first = request.session["date_curr"]
	
#    return schedule_set5(request,list)
	return render(request, "display_schedule_form.html", {'list':list,'qq':qq,'ttt':ttt,'Curr':current_first,'args':args})
 
	return render(request,'display_schedule_formRefresh.html', {'a':list})
    
# Set Employee names and their Jobs in two seperate arrays N[] and E[]

# Returns Number of Jobs Selected and Number of Employees to choose from
def schedule_qty(shift,position):
	selection = 1
	finalize = 1
	v = 0
	db, cur = db_set(request)
	JCsql = "SELECT count(*) from tkb_schedule where  Shift='%s' and Position='%s' and Selection='%s' and Finalize !='%s'" % (shift,position,selection,finalize)
	cur.execute(JCsql)
	tmp = cur.fetchall()	
	tmp2 = tmp[0]
	tmp_J_count = tmp2[0]   # Count for number of jobs
	qty_jobs = tmp_J_count
	
	#Csql = "SELECT count(*) from tkb_employee_temp where  Shift='%s' and Position='%s'" % (shift,position)
	#Csql = "SELECT DISTINCT from tkb_employee_matrix where Shift='%s' and Position='%s' and Off='%s'" % (shift,position,v)
	Csql = "SELECT count(*) from tkb_employee where  Shift='%s' and Position='%s' and Off='%s'" % (shift,position,v)
	cur.execute(Csql)
	tmp = cur.fetchall()	
	tmp2 = tmp[0]
	tmp_count = tmp2[0]   # Count for number of employees
	qty_employee = tmp_count
	#return render(request,'nothing.html')
	return (qty_jobs,qty_employee,tmp_count)
	
def schedule_set5(request,list):

	r1= time_output()
	position = request.session['position']
	rotation = 1
	selection = 1
	finalize = 1
	rv = 0
	
		
	db, cur = db_set(request)
	try:
		shift = request.session["matrix_shift"]
	except:
		shift = request.session["shift_priority"]
	
	# Copy Employees to schedule into tkb_employee_temp
	
	sql_d = "DELETE FROM tkb_employee_temp WHERE Shift='%s' and Position='%s'" % (shift,position)
	cur.execute(sql_d)
	db.commit()
	
	MNsql = "INSERT tkb_employee_temp Select * From tkb_employee where Shift='%s' and Position='%s' and Off='%s' ORDER BY %s %s" % (shift,position,rv,'Rank','ASC')
	cur.execute(MNsql)
	db.commit()
	#return render(request,'test993.html', {'jobs':shift , 'employees':position})  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX #
	Jsql = "SELECT Employee, Rank from tkb_employee_temp where  Shift='%s' and Position='%s' ORDER BY %s %s" % (shift,position,'Rank','ASC')
	cur.execute(Jsql)
	#ttmp = cur.fetchall()
	tmp_employees = cur.fetchall()
	
	#return render(request, "test994.html", {'N':tmp_employees})
	
	qty_jobs, qty_employee, tmp_count = schedule_qty(shift,position)
	
	request.session['qty_jobs'] = qty_jobs
	request.session['qty_employee'] = qty_employee
	request.session['qty_diff'] = 1

	# ******* Below section to break and view Variables *******************
#	www = [ 0 for x in range(3)]
#	www[5]=9
# ************************************************************	
#   ******************************************************************************
#   

	A='Qty_Jobs'
	B='Qty_Employee'
	C='Shift'
	D='position'
	#return render(request, "testA.html", {'A':A,'a':qty_jobs,'B':B,'b':qty_employee,'C':C,'c':shift,'D':D,'d':position})
	# Check to see if employees available doesn't equal jobs needed
	if qty_jobs != qty_employee:
		return render(request,'display_schedule_fail.html')	

	
	E = [[] for x in range(tmp_count)]
	XE = [[] for x in range(tmp_count)]
	N = ['' for x in range(tmp_count)]
	NE = ['' for x in range(tmp_count)]
	XN = ['' for x in range(tmp_count)]
	XEE = ['' for x in range(tmp_count)]
	JE = ['' for x in range(tmp_count)]
	ctr = [ 0 for x in range(tmp_count)]
	co = 0
	counter = 0
	for y in tmp_employees:
		counter = counter + 1
		N[co] = y[0]
		p = y[0]
		
# Below section can be added back if module doesn't work  *******************************************		
#		Hsql = "SELECT Description, Job_Name from tkb_employee_matrix where Rotation ='%s' and Employee ='%s'" % (rotation,p)
#		Hsql = "SELECT Description, Job_Name from tkb_employee_matrix where Rotation ='%s' and Employee ='%s' ORDER BY %s %s" % (rotation,y[0],'Priority','ASC')
#		cur.execute(Hsql)
#		tmp3 = cur.fetchall()
#  **************************************************************************************************


		tmp3 = join_query(p,shift)
		
		# testing below to stop on a certain employee
		#if counter > 4:
		#	dummy = 4
		#	return render(request, "test994.html", {'N':tmp3,'P':p,'C':counter})
		# end testing
		
		
		tmp_matrix = tmp3[0]
		tmp_description = tmp_matrix[0]
		tmp_job = tmp_matrix[1]
		
		prev_tmp_job_id = 0
		job_mult = .1
#		try:
		#return render(request, "test994.html", {'N':tmp3,'E':E,'P':p})
		for z in tmp3:
			ztest1 = str(z[0])
			ztest2 = z[1]
			
			Dsql = "SELECT Id from tkb_jobs where Description ='%s' and Job_Name = '%s'" % (z[0],z[1])
			cur.execute(Dsql)
			tmp4 = cur.fetchall()
			# change back to tmp4[0]
			tmp7 = tmp4[0]
			tmp_job_id = tmp7[0]
			
			if tmp_job_id == prev_tmp_job_id:
				prev_tmp_job_id = tmp_job_id
				tmp_job_id = tmp_job_id + job_mult
				job_mult = job_mult + .1
			else:
				prev_tmp_job_id = tmp_job_id
				job_mult = .1
				
			
			JE.append(tmp7[0])
			E[co].append(tmp_job_id)
			
		#return render(request, "test8.html", {'N':E})
		co = co + 1
#		except:
#			db.close()
#			return render(request,'test1.html')
			 
	db.close()
	
	# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
	#return render(request, "test994.html", {'N':N,'E':E,'P':p})
	# ***************************************************
	
		
		
		
#	return render(request,'display_schedule_test1.html', {'list':list2,'k':k,'lista':list})	
	#return render(request,'display_schedule_formRefresh.html',{'a':t2_employees,'b':N,'c':N[1],'d':E})
	# Schedule Algorithm using N[i] Names of Employees and E[i] Jobs for each of the employees in an array for each
	tmp_ctr = 0
	A = []
	bk = 0
	ptr = 0
	no_match = 0
	r3 = 0
	
	# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
	#x = zip(N,E)
	#return render(request, "test992.html", {'X':x,'T':r3})
	# ***************************************************
	
	
	nnoo = 0



	#Sort E and N  for optimal speed  ****************************
	for i in range (0,qty_employee-1):
		for ii in range (i+1,qty_employee):
			if len(E[ii]) < len(E[i]):
				tmp = E[ii]
				E[ii] = E[i]
				E[i] = tmp
				tmp = N[ii]
				N[ii] = N[i]
				N[i] = tmp
	# ****************************************
	
	
	
	# Determine how many Jobs are in each persons matrix
	EJ = Counter(JE).values()
	EEJ = Counter(JE).keys()
	
	
	for j in range (0,len(EJ)-1):
		for jj in range (j+1, len(EJ)):
			if EJ[jj] < EJ[j]:
				tmp = EJ[j]
				EJ[j] = EJ[jj]
				EJ[jj] = tmp
				tmp = EEJ[j]
				EEJ[j] = EEJ[jj]
				EEJ[jj] = tmp
	cty = 0

	# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
	#x = zip(N,E)
	#return render(request, "test992.html", {'X':x,'T':r3})
	# ***************************************************
	#XN = N
	#XE = E
	for j in range (0,len(EEJ)):

		for jj in range (0,len(E)):
			if EEJ[j] in E[jj]:
				cty = cty + 1
				XE[cty-1] = E[jj]
				XN[cty-1] = N[jj]
				XEE[cty-1] = EEJ[j]
				#if cty ==2:
				#	return render(request, "test997.html", {'A':N})
				E.pop(jj)
				N.pop(jj)
				#if cty ==10:
				#	return render(request, "test997.html", {'A':XN})
				break

	
	for jjj in range(0,len(E)):
		XE[cty] = E[jjj]
		XN[cty] = N[jjj]
		cty = cty + 1
		

	NE = EEJ
	E = XE
	N = XN
	YE = E
	YN = N 

	
	#Sort E and N  for optimal speed  ****************************
	#for i in range (0,qty_employee-1):
	#	for ii in range (i+1,qty_employee):
	#		if len(E[ii]) < len(E[i]):
	#			tmp = E[ii]
	#			E[ii] = E[i]
	#			E[i] = tmp
	#			tmp = N[ii]
	#			N[ii] = N[i]
	#			N[i] = tmp
	# ****************************************
	

	
	
	# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
	x = zip(N,E)
	#return render(request, "test992.html", {'X':x,'JE':JE,'EJ':EJ,'EEJ':EEJ,})
	# ***************************************************
	
	# Test Algorithm
	for i in range(0,len(XE)):
		try:
			job1 = XE[i][0]
			name1 = XN[i]
		except:
			job1 = -1
		YE = job1
		YN = name1
		
		for a in range(i+1,len(XE)):
			if job1 in XE[a]:
				YN = XE[a]
				YE = YE + job1
		
		
		#return render(request, "test999.html", {'X':x})	
		#return render(request, "test992.html", {'X':x,'Y':YN,'EJ':job1,})
	
	
	
	
	# *********************** 
	#    Scheduler Engine     
	# *********************** 

# ---------------------------------------------------------------------------------------------------
# -------------   Everything below to * is OLD Algorithm ----------------------------------------------
# ---------------------------------------------------------------------------------------------------	
#	while True:
#		tmp_ctr = tmp_ctr + 1
#		
#			
#		A.append(E[ptr][ctr[ptr]])
#		if len(A) != len (set(A)):
#			A.pop()
#			ctr[ptr] = ctr[ptr] + 1
#			while True:
#				if ctr[ptr] <= (len(E[ptr]) - 1):
#					break
#				if (ctr[ptr] > (len(E[ptr])-1)) and ptr == 0:
#					no_match = 1
#					break
#				ctr[ptr] = 0
#				ptr = ptr - 1
#				ctr[ptr] = ctr[ptr] + 1
#				A.pop()
#		else:
#			ptr = ptr + 1
#		if no_match == 1:
#			nnoo = 1
#			break
#		if ptr > (qty_employee-1):
#			break
#		
#		# Cut off counter
#		if tmp_ctr > 500000:
#			break
# ---------------------------------------------------------------------------------------------------
# ---------------------   End of OLD Algorithm     --------------------------------------------------
# ---------------------------------------------------------------------------------------------------	



# ====================================================================================================
# ====================   Everything below to * is NEW Algorithm ======================================
# ====================================================================================================
	

	qty_employee = len(N)
	fail_code = 0
	code1=0
	code2=0
	code3=0
	code4=0
	code5=0

	Temp_E = ['' for x in range(0)]
	Temp_N = ['' for x in range(0)]
	a1 = ['' for x in range(0)]
	a2 = ['' for x in range(0)]
	a3 = ['' for x in range(0)]

	w1 = ['' for x in range(0)]

	E_Working = ['' for x in range(0)]
	N_Working = ['' for x in range(0)]
	A_Job = ['' for x in range(0)]
	A_Name = ['' for x in range(0)]
	
	bk = 0	
	ptr = 0
	max_ptr = 0
	no_match = 0
	
	incomplete = 0
	route = 1
	E_Working = E
	N_Working = N
	
	# Algorithm Start
	while True:

		# Route 1 is used as main route and always checks if there is Job Qty with only 1 possible solution first
		if route == 1:	
			# obtain qty of E's containing each specific E value
			# (1) Sort (JobQty,Job)
			CE = Job_Total(E_Working) 
		
			# Failsafe if Won't Work
			if len(CE) != len(N_Working):
				dummy = 1
				# Need something better here
			
				#quit()

			# Check failure or completion
			try:
				if CE[0][0]<1:
					code1=1
					break  #quit loop because no solution from here on 
			except:
				incomplete = 1
				break	
			#break # Stops loop here for testing
		
			Job, Name = Job_One_Search1(CE,E_Working,N_Working)
			E_Working, N_Working = JobLength_Sort(E_Working, N_Working)
		
			# If there is only 1 solution for a job assign it and loop back to this Route
			if Job != 0 :
				E_Working, N_Working, A_Name, A_Job = Assign(E_Working, N_Working, A_Name, A_Job, Name, Job)
				route = 1
			else:
				route = 2
	

		E_Working, N_Working = JobLength_Sort(E_Working, N_Working)	
	
		# Check if the length of the first sorted E Value is 1.  If so assign it to the job.
		if route == 2:
			if len(E_Working[0]) == 1:
				Job = E_Working[0][0]
				Name = N_Working[0]
				E_Working, N_Working, A_Name, A_Job = Assign(E_Working,N_Working,A_Name,A_Job,Name,Job)

				route = 1
			else:
				route = 3	
		
		# Select the 1st priority job of the sorted by job qtys person and assign
		if route == 3:
		
			# ************  The below 2 lines are used if we select using least job qty and based on priority ******
			try:
				Job = E_Working[0][0]
				Name = N_Working[0]
			except:
				break

		
			# ******* The below 4 lines are used if we select using Jobs quantity selection *****
			#Temp_E, Temp_N = Job_Search(y,E_Working,N_Working)
			#CE = Job_Total(E_Working)
			#Job = CE[0][0]
			#Name = Temp_N[0]
		

			E_Working, N_Working, A_Name, A_Job = Assign(E_Working,N_Working,A_Name,A_Job,Name,Job)
			route = 1
# Algorithm End 


	

	
# **********************************************************************************
# ***********  CLEAN UP AND FINISH UP **********************************************
# **********************************************************************************

	# A is the finished first pass 
	A = zip(A_Name,A_Job)   		# A is the Finished first pass complete A_Name,A_Job
	NE = zip(N_Working,E_Working)   # NE is the Remaining of the Finished first pass
	NEE = zip(N,E)					# NEE is the Full original list for comparisons
	
	
	#return render(request, "test999.html", {'A':A,'NE':NE,'NEE':NEE})
	

	# This code will determine if List was completed.
	if (len(NE)) == 0:
		dummy = 1
		code2=1
		#quit()   # Use return in the main program
	
	else:  # List Incomplete so do the loop to fill it

		# ************************************************

		# At this point down we should LOOP through NE and assign variable name_switch1

		name_switch1 = NE[0][0]  # Assign name_switch1 as the name in this cycle to switch for some other one name_switch2
							# It would be NE[v][0] where v is the loop of all len(NE)
	
		# End Program here to test
		#quit()
		# ************************
		
	
		# find the jobs not staffed
		CE = Job_Total(E)  # List with all Original required jobs
		for i in range(len(CE)):
			a1.append(CE[i][0])  # Generate a1 as list of all jobs needed
	
		for i in range(len(A_Job)):
			a2.append(A_Job[i])  # Generate a2 as list of all jobs assigned
		
		
		
		
		for i in range(len(a1)):
			test1 = 0
			for ii in range(len(a2)):
				if int(a2[ii]) == int(a1[i]):
					test1 = 1
			if test1 == 0:
				a3.append(a1[i]) # Generate a3 as list of all jobs not assigned


		xne = NE[0][0]
		name_switch1 = xne

		return render(request, "test999.html", {'A':a1,'NE':a3,'NEE':NE})
		
		try:
			job_switch1 = a3[0]
		except:
			fail_code = 3
			code3 = 1
			
		if fail_code == 0:	
			name_switch2 = ''
			job_switch2 = ''
			name_switch_p = ''
			job_switch_p = ''
			for x in range(0,len(N)):  # N Being the complete list of original names
				if xne == N[x]:        # xne is the person not staffed
					w1 = E[x]          # E[x] is all original jobs for xne person
					#print"THIS ONE:",N[x],w1
					break
			#for x in range(0,len(NE)):
			#	print NE[x],	
			#print xne,			
			#print w1
			
			
			
	
	
			# Code to find first person backwards through list that does job a3[0]
			U=0
			while True:
				U = U + 1
				br = 0
				for i in reversed (range(len(E))):
					check_1 = 0
					for ii in range(len(E[i])):
						if E[i][ii] == job_switch1:				# a3[0] is the job not staffed
					
							br == 1
							# Check if job assigned in A where N[i] is name is in E list for a3
							name_switch_p = N[i]
				
							# Assign job_switch1 as the job assigned to potential switcher
							for k in range(len(A)):
								if A[k][0] == N[i]:
									job_switch2 = A[k][1]
									job_switch_p = A[k][1]
						
							for m in range(len(w1)):
								if job_switch2 in w1:
									check_1 = 1
								if check_1 == 1:
									break

							if check_1 == 1:
								name_switch2 = N[i]


						if check_1 == 1:
							break	
			
					if check_1 == 1:
						break
				
				if check_1 == 0:
					new_items = [x if x!=job_switch_p else job_switch1 for x in A_Job]
					A_Job = new_items
					job_switch1 = job_switch_p
					A=zip(A_Name,A_Job)
					code4 = 1
			
				else:
					# Switch non assigned into A and assign A
					new_items = [x if x!=name_switch2 else name_switch1 for x in A_Name]
					A_Name = new_items
					A_Name.append(name_switch2)
					A_Job.append(job_switch1)
					A=zip(A_Name,A_Job)
					code5 = 1
					break

					
	
	try:
		U
	except:
		U = 99
	return render(request, "test5.html", {'A1':code1,'A2':code2,'A3':code3,'A4':code4,'A5':code5,'U':U})
# ====================================================================================================
# ====================  End of NEW Algorithm      ====================================================
# ====================================================================================================
	#A = zip(A_Name,A_Job)
	#return render(request, "test999.html", {'A':A})	
	listX = zip(A_Name,A_Job)
	#listX = zip(N,A)
	r2 = time_output()
	r3 = r2-r1
	
	ctr_global = tmp_ctr
	#return render(request, "test992.html", {'X':listX})
	# ***********************
	
	# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
	#return render(request, "test992.html", {'X':listX,'N':N})
	#return render(request, "test994.html", {'N':N,'E':A,'L':E,'noo':tmp_ctr,'Ptr':ptr,'Qty':qty_employee})
	# ***************************************************
	#return render(request, "test999.html", {'A':listX,'NE':NE,'NEE':NEE})
	if no_match != 1:
		TY = []
		#listT = zip(N,A)
		listT = zip(A_Name,A_Job)
		ctr = 0
		e_dash = '---'
		D=[]
		J=[]
		db, cur = db_set(request)
		for x in listT:
			ctr = ctr + 1
			jx = int(x[1]) # ID for the Job assigned
			sql1 = "SELECT Description,Job_Name from tkb_jobs where Id ='%s'" % (jx)
			cur.execute(sql1)
			tmpA = cur.fetchall()
			tmpB = tmpA[0]
			description  = tmpB[0]
			job = tmpB[1]
			TY.append(x[0])
			TY.append(description)
			TY.append(job)
			D.append(description)
			J.append(job)
			
			# Choose Minimum Row entry Id of the potential entry so it isn't entered in multiple rows by mistake
			sql3 = "SELECT Min(Id) from tkb_schedule WHERE Description ='%s' and Job_Name ='%s' and Shift = '%s' and Position = '%s' and Employee = '%s'" % (description,job,shift,position,e_dash)
			cur.execute(sql3)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			min_id = tmp2[0]
			
			# Update only one row not every row that has this criteria.  BUG BELOW
			sql2 = ('update tkb_schedule SET Employee="%s" WHERE Description ="%s" and Job_Name ="%s" and Shift = "%s" and Position = "%s" and Employee = "%s" and Id = "%s"' % (x[0], description,job,shift,position,e_dash,min_id))
			#sql2 = ('update tkb_schedule SET Employee="%s" WHERE Description ="%s" and Job_Name ="%s" and Shift = "%s" and Position = "%s" and Employee = "%s"' % (x[0], description,job,shift,position,e_dash))
			
			cur.execute(sql2)
			db.commit()
		db.close()
		k=zip(A_Name,D,J)
		
		#return render(request, "test999.html", {'A':listX,'NE':list,'NEE':k})
		
		
		# TEST FOR VALUES....REMOVE WHEN DONE !!!!!  ********
		#return render(request, "test994.html", {'L':k})
		# ***************************************************
		#return render(request, "test994.html", {'N':N,'E':E,'L':listX})
		
		#return render(request,"test67.html",{'list':list})
		aa = []
		bb = []
		cc = []
		dd = []
		ee = []
		ff = []
		gg = []
		hh = []
		mm = []
		pops = 0
		xctr = 0
		
		j_qty = 1
		j_job = ''
		j_des = ''
		#  
#		list = zip(aa,bb,dd,cc,ff,gg,kk,ll)	


# ************************************************************************
# **             Bug Below.  Won't allocate for multiple jobs   **********
# ************************************************************************
		#return render(request,"test67.html",{'list':list})
		for y in list:
			
			if y[5] == 1:
				if y[2] == j_job and y[7] == j_des:
					j_qty = j_qty + 1
				else:
					j_qty = 1
					j_job = y[2]
					j_des = y[7]
				
				aa.append(y[0])
				bb.append(y[1])
				cc.append(y[2])
				dd.append(y[3])
				ee.append(y[4])
				ff.append(y[5])
				gg.append(y[6])
			#mm.append(j_qty)
				ck = 0
				ctr = 1
				for x in k:
					if x[1] == y[7] and x[2] == y[2]:
						if j_qty > ctr:
							ctr = ctr + 1
						else:	
							hh.append(x[0])
							#hh.append(y[7])
							#hh.append(y[2])
							#hh.append(j_qty)
							ck = 1
							break
				
				if ck == 0:
					hh.append('---')
		
		
		#return render(request,"test67.html",{'list':hh,'list2':k})
		list2 = zip(aa,bb,cc,dd,ee,ff,gg,hh)
		#return render(request,"test67.html",{'A':hh,'B':k,'C':listX,'D':list2})
		qq = '---'
		request.session['current_shift'] = shift
		request.session['current_position'] = position
		
		#return render(request,'test994.html',{'N':list,'E':list2,'L':k, 'pops':pops})
		request.session['list_test'] = list2
		request.session['qq'] = qq
		request.session['r3'] = r3
		
		return render(request,'display_schedule.html',{'list':list2,'qq':qq,'T':r3,'ctr_global':ctr_global})

	else:
		request.session['qty_fail'] = 0
		return render(request,'display_schedule_fail.html')										


	#return render(request,'display_schedule_formRefresh.html',{'a':t2_employees,'b':N,'c':N[1],'d':E})

def join_query(emp,shift):
	x = 1
	final = 1
	
	db, cur = db_set(request)
	#sql = "SELECT Description,Job_Name from tkb_schedule where Selection ='%s'" % (x)
	#sql = "SELECT tkb_schedule.Job_Name, tkb_schedule.Description from tkb_schedule LEFT JOIN tkb_employee_matrix ON tkb_schedule.Selection ='%s' AND tkb_employee_matrix.Rotation = '%s'"%(x,x)
	sql1 = "SELECT Job_Name, Description from tkb_schedule WHERE Selection ='%s' and Finalize != '%s'"%(x,final)
	cur.execute(sql1)
	list1 = cur.fetchall()
	
#	sql2 = "SELECT Job_Name, Description from tkb_employee_matrix WHERE Rotation ='%s' AND Shift='%s' AND Employee='%s'"%(x,shift,emp)
	sql2 = "SELECT Job_Name, Description from tkb_employee_matrix WHERE Rotation ='%s' AND Shift='%s' AND Employee='%s' ORDER BY %s %s"%(x,shift,emp,'Priority','ASC')

	cur.execute(sql2)
	list2 = cur.fetchall()
	a = []
	b = []
	for i in list2:
		for ii in list1:
			if i[0] == ii[0] and i[1] == ii[1]:
				a.append(str(i[1]))
				b.append(str(i[0]))
	
	c = zip(a,b)			
	
	return c			
#	return render(request,'test21.html',{'list1':list1,'list2':list2,'list3':c})

def schedule_add_job(request,index):

	lp = request.session["loop_count"]
	lp = lp + 1
	request.session["loop_count"] = lp
	ln = request.session["loop_name"]
	ln = ln + '(' + str(lp) +')' + request.session["button1"]
	request.session["loop_name"] = ln
	
	request.session["add_a_job"] = 1
	request.session["add_job2"] = 1
	try:
		v = request.session["add_job"]
		v = v + 1
		request.session["add_job"] = v
	except:
		request.session["add_job"] = 1
	return schedule_add(request,index)
	
def schedule_add(request,index):


	aj = request.session["job_n"]
	aj = aj + 1
	request.session["job_n"] = aj

	v = request.session["add_job"]
	w = request.session["add_a_job"]

	if aj < 25:
		#if aj == 2:
		#	return render(request,'test997.html')
		zh = request.session["route"]
		zh = int(zh)
		zh = zh + 1
		request.session["route"] = zh
		db, cur = db_set(request)
		sql = "SELECT * from tkb_schedule where  Id='%s'" % (index)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		tmp1 = tmp2[0]		
		sql3 = "SELECT MAX(Id) FROM tkb_schedule" 
		cur.execute(sql3)
		x1 = cur.fetchall()
		x2 = x1[0]
		x3 = x2[0]
		x3 = x3 + 1
	
		tmp = tmp1[3]
		description = tmp1[2]
		job_name = tmp1[3]
		shift = tmp1[4]
		position = tmp1[5]
		employee = '---'
		selection = 1
		finalize = 0
		
		#if request.session["stop_1"] == 1:
		#	return render(request,'test995.html',{'tmp':index})
			
		cur.execute('''INSERT INTO tkb_schedule(Id,Description,Job_Name,Shift,Position,Employee,Selection,Finalize) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (x3,description,job_name,shift,position,employee,selection,finalize))
		db.commit()
		db.close()
		
		if request.session["stop_1"] == 0:
			request.session["stop_1"] = 1
			
			
		request.session["add_a_job"] = 0
		request.session["add_route"] = 1
	else:
		request.session["add_job"] = 0
		request.session["add_a_job"] = 0
		
	
	
	#return schedule_set3(request)
	return render(request,'done_schedule_set3.html')
	
def schedule_delete(request,index):
	aj = request.session["job_n"]
	aj = aj - 1 
	request.session["job_n"] = aj
	db, cur = db_set(request)

	dql = ('DELETE FROM tkb_schedule WHERE Id="%s"' % (index))
	cur.execute(dql)
	db.commit()
	db.close()
	
	
	return render(request,'done_schedule_set3.html')
	
	
	
def schedule_finalize(request):
	shift = request.session['current_shift']
	position = request.session['current_position']
	employee = '---'
	eee='yes'
	final = 1
	finalize = 0
#	i = vacation_temp()

#   Use below to assign selected date from form to i
	i = request.session['date_curr']


	
	db, cur = db_set(request)
	sql1 = ('update tkb_schedule SET Date = "%s", Finalize="%s" WHERE Shift ="%s" and Position ="%s" and Finalize != "%s" and Employee != "%s"' % (i,final,shift,position,final,employee))
	cur.execute(sql1)
	db.commit()
	
	sql2 = "DELETE FROM tkb_schedule WHERE Shift='%s' and Position='%s' and Employee = '%s'" % (shift,position,employee)
	cur.execute(sql2)
	db.commit()
	
	# Select Employee and Job names from entered data
	sql3 = "SELECT Employee,Job_Name,Description from tkb_schedule WHERE Date ='%s' and Shift = '%s' and Position = '%s'" % (i, shift, position)
	cur.execute(sql3)
	list3 = cur.fetchall()
	# Assign 99 value to matrix priority for that job then init again so that it places that job at the end of priority chain
	x = 99
	for i in list3:
		sql4 = ('update tkb_employee_matrix SET Priority = "%s" WHERE Employee ="%s" and Job_Name ="%s" and Description = "%s"' % (x, i[0],i[1],i[2]))
		cur.execute(sql4)
		db.commit()




	for h in range(0,3):
		# Increment Rank of Employee order in tkb_employee
		aql = "SELECT * FROM tkb_employee WHERE Shift = '%s' and Position = '%s' ORDER BY %s %s , %s %s" %(shift,position,'Rank', 'ASC','Employee','ASC')	
		cur.execute(aql)
		tmp = cur.fetchall()
		
		ct = 2
		for x in tmp:
			i_d = x[0]
			sql = ('update tkb_employee SET Rank = "%s" WHERE Id ="%s"' % (ct, i_d))
			cur.execute(sql)
			db.commit()
			ct = ct + 1
	
		sql5 = "SELECT Max(Rank) from tkb_employee WHERE Shift = '%s' and Position = '%s'" %(shift,position)
		cur.execute(sql5)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		tmp3 = tmp2[0]
	
		ct = 1
		sql6 = ('update tkb_employee SET Rank = "%s" WHERE Rank ="%s" and Shift ="%s" and Position = "%s"' % (ct,tmp3,shift,position))
		cur.execute(sql6)
		db.commit()




	#return render(request, "test994.html", {'N':tmp_employees})
	#return render(request,'redirect_schedule2.html')	
	
	
	db.close()
	schedule_init(request)
	

	
	return schedule_set4(request,list) 
	
# Clears tkb_employee_temp table and tkb_schedule table
def schedule_reset_data(request):
	db, cur = db_set(request)
	sql1 = "DELETE FROM tkb_schedule"
	cur.execute(sql1)
	db.commit()
	sql2 = "DELETE FROM tkb_employee_temp"
	cur.execute(sql2)
	db.commit()
	db.close()
	return render(request,'done_delete_schedule.html')
	
def schedule_redisplay1(request):
	list2 = request.session['list_test']
	qq = request.session['qq']
	r3 = request.session['r3']
	
	return render(request,'display_schedule_redo.html',{'list':list2,'qq':qq,'T':r3})
	
# Use this module to Automaticlly force all trained to be clicked for rotation
def schedule_rotation_start(request):
	db, cur = db_set(request)
	shift = 'Day CSD 2'
	position = 'Production'
	ct = 1
	v = 2
	sql = ('update tkb_employee_matrix SET Rotation = "%s" WHERE Level ="%s" and Shift ="%s" and Position = "%s"' % (ct,v,shift,position))
	cur.execute(sql)
	db.commit()
	db.close()
	return render(request, "done_test.html")
	
	
	
	
	
	
	
	
	
	
