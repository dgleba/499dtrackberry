from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views2 import main_login_form
from trakberry.views_testing import emp_list_display
from forms import toggletest_Form
from trakberry.forms import emp_training_form, emp_info_form, job_info_form
import MySQLdb
import time
import datetime
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

# Create the training matrix table ******************TEST******
def create_matrix(request):
	# Construct Training Matrix Table
	#
  
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_employee""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(30), Clock INT(10), Position CHAR(30), Shift CHAR(30))""")
  
	db.commit()
	db.close()
	return render(request,'done_test.html')

def create_jobs(request):
	# Construct Jobs Table

	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_jobs""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_jobs(Id INT PRIMARY KEY AUTO_INCREMENT, Description CHAR(30), OP CHAR(30), Part CHAR(30), Machine INT(10))""")
  
	db.commit()
	db.close()
	return render(request,'done_test.html')
	
# Employee Training Entry ******************
def emp_training_enter(request):

	try:
		request.session["employee"]
		request.session["part"]
		request.session["op"]
		request.session["machine"]
		request.session["level"]
		
	except:
		request.session["employee"] = ""
		request.session["part"] = ""
		request.session["op"]= ""
		request.session["machine"]= ""
		request.session["level"] = ""
	
	if request.POST:

		request.session["employee"] = request.POST.get("employee")
		request.session["part"] = request.POST.get("part")
		request.session["op"] = request.POST.get("op")
		request.session["machine"] = request.POST.get("machine")
		request.session["level"] = request.POST.get("level")

		
		return emp_training_update(request)
		
	else:
		form = emp_training_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'emp_training_enter_form.html',{'args':args})		

def emp_info_enter(request):
	
	request.session["batch"] = 0
	try:
		request.session["employee"]
		request.session["clock"]
		request.session["shift"]
		request.session["position"]
		
	except:
		request.session["employee"] = ""
		request.session["clock"] = 0
		request.session["shift"]= ""
		request.session["position"]= ""

	if request.POST:

		request.session["employee"] = request.POST.get("employee")
		request.session["clock"] = request.POST.get("clock")
		request.session["shift"] = request.POST.get("shift")
		request.session["position"] = request.POST.get("position")
		#return render(request,"test99_1.html",{'test':tmp2})
		return emp_info_update(request)
		
	else:
		form = emp_info_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	#return render(request,'emp_info_enter_form.html',{'args':args})
	
	rlist = emp_list_display()
	#request.session["login_tech"] = "none"
	return render(request,'emp_info_enter_form.html', {'List':rlist,'args':args})
			

def emp_info_update_status(request,index):
	info_index = index
	request.session["index"] = index
	db, cur = db_set(request)
	sql = "SELECT Employee FROM tkb_employee_matrix WHERE Id ='%s'" %(info_index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	emp = tmp2[0]
	
	aql = "SELECT * FROM tkb_employee WHERE Employee ='%s'" %(emp)
	cur.execute(aql)
	ump = cur.fetchall()
	ump2 = ump[0]
	
	request.session["employee_old"] = emp

	if request.POST:

		request.session["employee"] = request.POST.get("employee")
		request.session["clock"] = request.POST.get("clock")
		request.session["shift"] = request.POST.get("shift")
		request.session["position"] = request.POST.get("position")
	
		return emp_info_update_change(request)
		
	else:
		form = emp_info_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'emp_info_update_form.html',{'ump2':ump2,'args':args})
	
def emp_info_absent(request,index):
	info_index = index
	request.session["index"] = index
	db, cur = db_set(request)
	sql = "SELECT Employee, Off FROM tkb_employee_matrix WHERE Id ='%s'" %(info_index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	emp = tmp2[0]
	v = tmp2[1]
	
	if v ==0:
		v=1
	else:
		v=0

	sql = ('update tkb_employee_matrix SET Off = "%s" WHERE Employee ="%s"' % (v,emp))
	cur.execute(sql)
	db.commit()
	
	tql = ('update tkb_employee SET Off = "%s" WHERE Employee ="%s"' % (v,emp))
	cur.execute(tql)
	db.commit()
	
	db.close()
	
	return render(request, "done_rotation.html")

	
	
	
def emp_matrix_delete(request):	
	
	#tmp = index
	tmp = request.session["index"]
	db, cur = db_set(request)
	sql = "SELECT Employee FROM tkb_employee_matrix WHERE Id ='%s'" %(tmp)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	emp = tmp2[0]
	
	dql = ('DELETE FROM tkb_employee_matrix WHERE Employee = "%s"' % (emp))
	cur.execute(dql)
	db.commit()
	eql = ('DELETE FROM tkb_employee WHERE Employee = "%s"' % (emp))
	cur.execute(eql)
	db.commit()	
	
	db.close()
	
	#return render(request,'test22.html',{'level':emp})
	
	return matrix_info_display(request)
	
def emp_training_update(request):	
    
	employee = request.session["employee"]
	part = request.session["part"]
	op = request.session["op"]
	machine = request.session["machine"]
	level = request.session["level"]

	db, cur = db_set(request) 	
	cur.execute('''INSERT INTO tkb_employee_matrix(Employee, Part, Op, Machine, Level) VALUES(%s,%s,%s,%s,%s)''', (employee,part,op,machine,level))
	db.commit()

	db.close()
	

	return render(request,'done_test.html')
	
def emp_info_update_change(request):	
    
	employee = request.session["employee"]
	employee_old = request.session["employee_old"]
	clock = request.session["clock"]
	shift = request.session["shift"]
	position = request.session["position"]

	db, cur = db_set(request) 	
	cur.execute("UPDATE tkb_employee SET Employee = '%s', Clock = '%s', Position = '%s', Shift = '%s' WHERE Employee = '%s'"% (employee,clock,position,shift,employee_old))
	db.commit()
	cur.execute("UPDATE tkb_employee_matrix SET Employee = '%s', Shift = '%s' WHERE Employee = '%s'"% (employee ,shift, employee_old))
	db.commit()	
	db.close()
		
	
	return matrix_info_reload(request)
	
def emp_info_update(request):	
    
	employee = request.session["employee"]
	clock = request.session["clock"]
	shift = request.session["shift"]
	position = request.session["position"]

	db, cur = db_set(request) 	
	cur.execute('''INSERT INTO tkb_employee(Employee, clock, position, shift) VALUES(%s,%s,%s,%s)''', (employee,clock,position,shift))
	db.commit()
	db.close()
	
	emp_info_update_matrix(employee,shift,position)
	
	
	batch_check = request.session["batch"]
	if batch_check == 1:
		return(request)
		
	return matrix_info_reload(request)


# Initialize Matrix with current employees and jobs.   Run once on start and never again. !!!
def emp_matrix_initialize(request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_employee"
	cur.execute(sql)
	tmp = cur.fetchall()
	
	tql = "SELECT * FROM tkb_jobs"
	cur.execute(tql)
	smp = cur.fetchall()

	cur.execute("""DROP TABLE IF EXISTS tkb_employee_matrix""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(30), Description CHAR(30), Part CHAR(30), OP CHAR(30), Machine INT(10), Level INT(30), Job INT(10))""")
	
	#cur.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_matrixx LIKE tkb_employee_matrix""")

	level = 0
	
	for i in tmp:
		tmp2 = i[1]
		emp = tmp2
		ctr = 1
		for j in smp:
			machine = j[4]
			part = j[3]
			description = j[1]
			op = j[2]
			
			cur.execute('''INSERT INTO tkb_employee_matrix(Employee,Description,Machine,Op,Part,Level,Job) VALUES(%s,%s,%s,%s,%s,%s,%s)''', [emp,description,machine,op,part,level,ctr])
			ctr = ctr + 1
	db.commit()
	db.close()
	matrix_job_order()
	return render(request,'done_test.html',{'tmp2':emp})
	
	
# Update Matrix to add new employee with all jobs listed and start them untrained
def emp_info_update_matrix(emp,shift,position):
	
	db, cur = db_set(request)
	tql = "SELECT * FROM tkb_jobs WHERE Position = '%s'" %(position)
	cur.execute(tql)
	smp = cur.fetchall()


	level = 0
		
	for j in smp:
		machine = j[5]
		description = j[1]
		
		cur.execute('''INSERT INTO tkb_employee_matrix(Employee,Description,Job_Name,Level,Shift,Position) VALUES(%s,%s,%s,%s,%s,%s)''', [emp,description,machine,level,shift,position])
	db.commit()
	db.close()
	matrix_job_order(position)
	return 

def emp_matrix_rotation_fix(request):
	R1 = 0
	R2 = 1
	db, cur = db_set(request)
	mql = ('update tkb_employee_matrix SET Rotation="%s"' % (R1))
	cur.execute(mql)
	db.commit()
	db.close()
	emp = 'DONE'
	return render(request,'done_test.html',{'tmp2':emp})
	
def job_info_update_matrix(description,job_name,position):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_employee WHERE Position = '%s'"%(position)
	cur.execute(sql)
	tmp = cur.fetchall()

	level = 0
	
	for i in tmp:
		tmp2 = i[1]
		emp = tmp2
		pos = i[3]
		shift = i[4]
		cur.execute('''INSERT INTO tkb_employee_matrix(Employee,Description,Job_Name,Level,Shift,Position) VALUES(%s,%s,%s,%s,%s,%s)''', [emp,description,job_name,level,shift,position])
		db.commit()
	
	db.close()
	matrix_job_order(position)
	return 


# Reorder the Job Number for Matrix based on Order Criteria
def matrix_job_order(position):
	db, cur = db_set(request)
	cql = "SELECT COUNT(*) FROM tkb_jobs WHERE Position = '%s'"%(position)
	cur.execute(cql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	job_ctr = tmp3[0]
	
	sql = "SELECT * FROM tkb_employee_matrix WHERE Position = '%s' ORDER BY %s %s , %s %s, %s %s" %(position,'Employee', 'ASC','Description','ASC','Job_Name','ASC')
	cur.execute(sql)
	xmp = cur.fetchall()
	ctr = 1
	
	for i in xmp:
		
		p_id = i[0]
		mql = ('update tkb_employee_matrix SET Job="%s" WHERE Id="%s"' % (ctr,p_id))
		cur.execute(mql)
		db.commit()
		ctr = ctr + 1
		if ctr > job_ctr:
			ctr = 1
	return
	
def matrix_job_test(request):
	db, cur = db_set(request)
	
	cql = "SELECT COUNT(*) from tkb_jobs"
	cur.execute(cql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	job_ctr = tmp3[0]
	
	sql = "SELECT * FROM tkb_employee_matrix ORDER BY %s %s , %s %s, %s %s" %('Employee', 'ASC','Description','ASC','Job_Name','ASC')
	cur.execute(sql)
	xmp = cur.fetchall()
	ctr = 1
	
	for i in xmp:
		
		p_id = i[0]
		mql = ('update tkb_employee_matrix SET Job="%s" WHERE Id="%s"' % (ctr,p_id))
		cur.execute(mql)
		db.commit()
		ctr = ctr + 1
		if ctr > job_ctr:
			ctr = 1
			
	pql = "SELECT * FROM tkb_employee_matrix ORDER BY %s %s , %s %s, %s %s" %('Employee', 'ASC','Description','ASC','Job_Name','ASC')
	cur.execute(pql)
	amp = cur.fetchall()
	return render(request,"test21.html", {'X':amp})


def emp_info_display(request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_employee" 
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	return render(request, "emp_info_display.html", {'List':tmp})

def job_info_display(request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_jobs ORDER BY %s %s,%s %s" %('Description','ASC','Job_Name','ASC') 
	cur.execute(sql)
	tmp = cur.fetchall()	
	tmp2 = tmp[0]
	db.close()
	return render(request, "job_info_display.html", {'List':tmp})
	
def matrix_info_init(request):
	
	# Check if someone is logged in first and if not rerout to login page
	try:
		if request.session["login_name"]  =="":
			return main_login_form(request)
	except:
		return main_login_form(request)
		
	x = request.session["shift_primary"]
	if x == "Cont A Nights":
		x = "Cont A Nights CSD 2"
	if x == "Cont A Days":
		x = "Cont A Days CSD 2"
	if x == "Cont B Days":
		x = "Cont B Days CSD 2"		
	if x == "Cont B Nights":
		x = "Cont B Nights CSD 2"
	if x == "CSD2 Day":
		x = "Day CSD 2"	
	if x == "CSD2 Aft":
		x = "Aft CSD 2"	
	if x == "CSD2 Mid":
		x = "Mid CSD 2"						
					
	request.session["matrix_shift"] = x
	return matrix_info_display(request)
	
def matrix_info_reload(request):
	return render(request, "done_matrix.html")	
	
def matrix_info_display(request):
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

	cql = "SELECT COUNT(*) from tkb_jobs WHERE Position = '%s'" %(position)
	cur.execute(cql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	job_ctr = tmp3[0]


	jql = "SELECT * FROM tkb_jobs WHERE Position = '%s' ORDER BY  %s %s, %s %s" %(position,'Description','ASC','Job_Name','ASC')
	cur.execute(jql)
	jmp = cur.fetchall()

	#return render(request, "test22.html", {'jmp':jmp,'job_ctr':job_ctr,'tmp':tmp})
	
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
	ctr2 = 1
	k = []
	kk = []
	clr = []
	clr_var = 1
	sw = -1
	c1 = '#DCDDDE'
	c2 = '#ffffff'
	c3='#c6cad1'
	ddd = '#ffffff'
	jb = ""
	nb = ""
	for i in tmp:
		if i[1] != nb:
			if ddd == c3:
				ddd = c2
			else:
				ddd = c3
			nb = i[1]
		
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
		clr.append(str(ddd))
		kk.append(ctr2)
			
		ctr2 = ctr2 + 1
				
	#return render(request, "test67.html", {'tjobs':tjobs})
	try:
		col_jobs = float(94 / job_ctr)
	except:
		col_jobs = 0
		
	# Form for shift selection and Save Function
	if request.POST:
		# Variable '1' if Save button pressed
		save_b = request.POST.get('save')
		if save_b == '1':
			ctr4 = 1
			h = []
			for j in tmp:
				ctrr = str(ctr4)
				hhh = request.POST.get(ctrr)
				h.append(str(hhh))
				#hhh=str(hhh)

				#vr1=int(hhh[:-1])
				#vr2=int(hhh[-1:])
				#h.append(vr1)
				#h.append(vr2)
				ctr4 = ctr4 + 1

			update_matrix_save(h)
			return matrix_info_reload(request)
			#return render(request, "test5.html", {'A':h})

		shift = request.POST.get("shift")
		request.session["matrix_shift"] = shift
		position = request.POST.get("position")
		request.session["position"] = position
		return matrix_info_reload(request)
	else:
		form = toggletest_Form
	args ={}
	args.update(csrf(request))
	args['form'] = form
	
	tmp4 = map(None,tmp,k,kk,clr)
	#tmp4 = zip(tmp,jc)	
	#return render(request, "test22.html", {'tjobs':a})
	#return render(request, "test67.html", {'List':tmp,'List2':tmp4,'List3':jc})	
	return render(request, "matrix_info_display.html", {'List':tmp4,'B':job_ctr,'A':a,'C':c,'Jobs':jmp,'tjobs':tjobs,'D':col_jobs,'args':args})


def update_matrix_save(tmp):
	db, cur =db_open()
	for i in tmp:
		i_var = int(i[:-1])
		i_val = int(i[-1:])
		sql = ('update tkb_employee_matrix SET Level = "%s" WHERE Id="%s"' % (i_val,i_var))
		cur.execute(sql)
		db.commit()
	db.close()	
	return
	
	
# Read in index value and change the Matrix variable accordingly for that indexed row
def matrix_update(request, index):
	db, cur =db_open()
	
	
	sql = "SELECT Level,Rotation FROM tkb_employee_matrix where Id='%s'" %(index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	level = int(tmp2[0])
	rotation = int(tmp2[1])

	
	#return render(request, "test22.html",{'level':level})
	
	
	new_level = 0
	
	if level == 0:
		new_level = 1
	if level == 1:
		new_level = 2
	if level == 2:
		new_level = 0
		rotation = 0
	if level == 3:
		new_level = 0
	
	level = new_level

	mql = ('update tkb_employee_matrix SET Level="%s", Rotation="%s" WHERE Id="%s"' % (level,rotation,index))
	cur.execute(mql)
	db.commit()
	
	db.close()
	
	return render(request, "matrix_display_refresh.html")
	
def fix_shift(request):
	db, cur = db_set(request)
	index = 0
	x = "Cont A Nights CSD 2"
	y = "CNC"
	mql = ('update tkb_employee_matrix SET position="%s" WHERE Id>"%s"' % (y,index))
	cur.execute(mql)
	db.commit()
	db.close()
	return render(request, "matrix_display_refresh.html")
	
def job_info_enter(request):

	try:
		request.session["description"]
		request.session["job_name"]
		request.session["position"]
		
	except:
		request.session["description"] = ""
		request.session["job_name"] = ""
		request.session["position"] = ""


	if request.POST:

		request.session["description"] = request.POST.get("description")
		request.session["job_name"] = request.POST.get("job_name")
		request.session["position"] = request.POST.get("position")
	
		return job_info_update(request)
		
	else:
		form = job_info_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'job_info_enter_form.html',{'args':args})	
	
def job_info_update(request):	
    
	description = request.session["description"]
	job_name = request.session["job_name"]
	position = request.session["position"]

	db, cur = db_set(request) 	
	cur.execute('''INSERT INTO tkb_jobs(Description,Job_Name,Position) VALUES(%s,%s,%s)''', (description,job_name,position))
	db.commit()
	db.close()
	
	job_info_update_matrix(description,job_name,position)

	return job_info_display(request)
	#return render(request,'done_test.html')

def job_info_update_status(request,index):
	info_index = index
	db, cur = db_set(request)
	sql = "SELECT Job_Name, Description FROM tkb_jobs WHERE Id ='%s'" %(info_index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	job = tmp2[0]
	desc = tmp2[1]
	request.session["job_old"] = job
	request.session["description_old"] = desc
	#return render (request,'test8.html')
	
	#aql = "SELECT * FROM tkb_jobs WHERE Job_Name ='%s'" %(job)
	#cur.execute(aql)
	#ump = cur.fetchall()
	#ump2 = ump[0]
	
	#request.session["job_old"] = job
	#request.session["description"] = ump2[1]
	
	
	if request.POST:

		request.session["description"] = request.POST.get("description")
		request.session["job"] = request.POST.get("job")

	
		return job_info_update_change(request)
		#return render(request,'test8.html')
	else:
		form = job_info_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	#return render(request,'job_info_update_form.html',{'ump2':ump2,'args':args})
	return render(request,'job_info_update_form.html',{'args':args})

def job_delete_test(request):
	return render(request,'test88.html')
	
def job_info_update_change(request):	
    
	job = request.session["job"]
	job_old = request.session["job_old"]
	description = request.session["description"]
	description_old = request.session["description_old"]
	position = request.session["position"]

	db, cur = db_set(request) 	
	cur.execute("UPDATE tkb_jobs SET Job_Name = '%s', Description = '%s' WHERE Job_Name = '%s' and Description = '%s'"% (job, description, job_old, description_old))
	db.commit()
	cur.execute("UPDATE tkb_employee_matrix SET Job_Name = '%s', Description = '%s' WHERE Job_Name = '%s' and Description = '%s'"% (job, description, job_old, description_old))
	db.commit()	
	db.close()
		
	matrix_job_order(position)
	return matrix_info_reload(request)

def job_info_delete(request):	
	
	job = request.session["job_old"]
	position = request.session["position"]
	
	db, cur = db_set(request)
	
	dql = ('DELETE FROM tkb_employee_matrix WHERE Job_Name = "%s"' % (job))
	cur.execute(dql)
	db.commit()
	eql = ('DELETE FROM tkb_jobs WHERE Job_Name = "%s"' % (job))
	cur.execute(eql)
	db.commit()	
	
	db.close()
	
	matrix_job_order(position)
	
	return matrix_info_reload(request)
	
def employee_manual_enter(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_employee_batch""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_batch LIKE tkb_employee""")
	#cursor.execute('''INSERT vacation_backup Select * From vacation''')

	db.commit()
	db.close()
	return render(request,'done_test_A.html')

def emp_info_enter_manual(request):

	try:
		request.session["employee"]
		request.session["clock"]
		request.session["shift"]
		request.session["position"]
		
	except:
		request.session["employee"] = ""
		request.session["clock"] = 0
		request.session["shift"]= ""
		request.session["position"]= ""

	if request.POST:

		request.session["employee"] = request.POST.get("employee")
		request.session["clock"] = request.POST.get("clock")
		request.session["shift"] = request.POST.get("shift")
		request.session["position"] = request.POST.get("position")
		#return render(request,"test99_1.html",{'test':tmp2})
		return emp_info_update_batch(request)
		
	else:
		form = emp_info_form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	#return render(request,'emp_info_enter_form.html',{'args':args})
	
	#rlist = emp_list_display()
	#request.session["login_tech"] = "none"
	return render(request,'emp_info_enter_form.html', {'args':args})


def emp_info_update_batch(request):
	employee = request.session["employee"]
	clock = request.session["clock"]
	position = request.session["position"]
	shift = request.session["shift"]
	
	db, cur = db_set(request)
	cur.execute('''INSERT INTO tkb_employee_batch(Employee, clock, position, shift) VALUES(%s,%s,%s,%s)''', (employee,clock,position,shift))
	db.commit()
	return render(request,'done_test_B.html')
	
	
def emp_info_group_update(request):

	request.session["clock"] = 0
	request.session["batch"] = 1
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_employee_batch" 
	cur.execute(sql)
	tmp = cur.fetchall()

	for i in tmp:

		employee = i[1]
		clock = request.session["clock"]
		shift = i[4]
		position = i[3]

		cur.execute('''INSERT INTO tkb_employee(Employee, clock, position, shift) VALUES(%s,%s,%s,%s)''', (employee,clock,position,shift))
		db.commit()
		
		db.close()
		db, cur = db_set(request)
		
		tql = "SELECT * FROM tkb_jobs WHERE Position = '%s'" %(position)
		cur.execute(tql)
		smp = cur.fetchall()
		
		
		A = 'tkb_jobs'
		a = smp
		B = 'position'
		b = position
		#return render(request,'testA.html',{'A':A,'a':a,'B':B,'b':b})

		level = 0
		
		for j in smp:
			machine = j[5]
			description = j[1]
			cur.execute('''INSERT INTO tkb_employee_matrix(Employee,Description,Job_Name,Level,Shift,Position) VALUES(%s,%s,%s,%s,%s,%s)''', [employee,description,machine,level,shift,position])
			db.commit()
			A = 'Employee'
			a = employee  
			B = 'Description'
			b = description
			C = 'Job'
			c = machine 
			D = 'Shift'
			d = shift
			E = 'Position'
			e = position 
			
			#return render(request,'testA.html',{'A':A,'B':B,'C':C,'D':D,'E':E,'a':a,'b':b,'c':c,'d':d,'e':e})
			

		# matrix_job_order
		cql = "SELECT COUNT(*) FROM tkb_jobs WHERE Position = '%s'"%(position)
		cur.execute(cql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		job_ctr = tmp3[0]
	
		sql = "SELECT * FROM tkb_employee_matrix WHERE Position = '%s' ORDER BY %s %s , %s %s, %s %s" %(position,'Employee', 'ASC','Description','ASC','Job_Name','ASC')
		cur.execute(sql)
		xmp = cur.fetchall()
		ctr = 1
	
		for i in xmp:
		
			p_id = i[0]
			mql = ('update tkb_employee_matrix SET Job="%s" WHERE Id="%s"' % (ctr,p_id))
			cur.execute(mql)
			db.commit()
			ctr = ctr + 1
			if ctr > job_ctr:
				ctr = 1

	db.close()
	return render(request,'testtest.html',{'list':list})

def matrix_backup(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_employee_backup""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_backup LIKE tkb_employee""")
	cursor.execute('''INSERT tkb_employee_backup Select * From tkb_employee''')
	db.commit()
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_employee_matrix_backup""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_matrix_backup LIKE tkb_employee_matrix""")
	cursor.execute('''INSERT tkb_employee_matrix_backup Select * From tkb_employee_matrix''')
	db.commit()
	db.close()
	return render(request,'done_test.html')
	
def rot_fix(request):

	a = 1
	b = 'Production'
	c = 'Aft CSD 2'
	#db, cur = db_set(request)  
	
	#cur.execute("UPDATE tkb_employee_matrix SET Rotation = '%s' WHERE Position = '%s' and Shift = '%s'"% (a,b,c))

	#db.commit()
	#db.close()
	return render(request,'done_test.html')
	
	
