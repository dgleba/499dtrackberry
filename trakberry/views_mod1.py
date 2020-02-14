from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_routes import direction
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current6, vacation_set_current5



# Module to Check if we need to send downtime report out
# via email.   This goes out through the Tech App refreshing	

def find_current_date():
	current_date = dt.datetime.today().strftime("%Y-%m-%d")
	return current_date

def table_copy(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_temp LIKE tkb_employee""")

	db.commit()
	db.close()
	return render(request,'done_test.html')
						  

def time_output():
	tm = int(time.time())
	time.sleep(1.4)
	return tm

def kiosk_lastpart_find(asset):
	try:
		ml = 4
		db, cur = db_open()
		a1sql = "SELECT MAX(id)  FROM sc_production1 WHERE asset_num = '%s' and length(partno) > '%d'" %(asset,ml) 
		cur.execute(a1sql)
		tp3 = cur.fetchall()
		tp4 = tp3[0]
		tp5 = tp4[0]
		a2sql = "Select partno From sc_production1 WHERE id = '%d'" %(tp5)
		cur.execute(a2sql)
		tp3 = cur.fetchall()
		tp4 = tp3[0]
		part = tp4[0]
		db.close()
	except:
		part = ""

	# part = ""  # Use this if you want to test default part to blank



	return part

# Generic Templay kickout for mtemp (headers) and mgmt_table_call which calls the sql required matching headers count
def mgmt_display(request):
	
	#request.session["mgmt_table_call"] = "SELECT id,asset_num,machine,partno,actual_produced,down_time,comments,pdate,shift,shift_hours_length,target FROM sc_production1"
	
	s2 = ""
	date_check = ['' for y in range(0)]
	ctr_var = 1
	request.session["date_check"] = 0
	for a in request.session["table_variables"]:

		if ctr_var == 1:
			id_name = a
		s2 = s2 + a + ','
		if a == 'pdate':
			date_check.append(1)
		else:
			date_check.append(0)
		ctr_var = ctr_var + 1
	request.session['ctr_var'] = ctr_var    #Assign the session variable to number of columns there are.  Use this on template to span
	request.session["date_check"] = date_check
	s2 = s2[:-1]
#	try:
	min_id = request.session["starting_id"]
	direction_id = int(request.session['direction_id'])
	cctr = int(request.session['ctr'])

#	except:
#		db, cur = db_set(request)
#		s3 = 'SELECT MAX('+id_name+') FROM '+request.session["mgmt_table_name"]
#		cur.execute(s3)
#		tmp3_1 = cur.fetchall()
#		tmp3_2=tmp3_1[0]
#		min_id = tmp3_2[0]
#		min_id = min_id + 1
#		db.close()
#		direction_id = 1
#	min_id = 456638
	x5 = '1507'
	x6 = x5
	x7 = x5
	x8 = x5
	x9 = x5
	x10 = x5
	x11 = x5
	xx5='i'
	zz = ['' for y in range(0)]
	z = ['' for y in range(0)]

	z.append(xx5)
	z.append(xx5)
	z.append(xx5)
	z.append(xx5)
	z.append(xx5)
	z.append(xx5)
	z.append(xx5)	
	zz.append(x5)
	zz.append(x6)
	zz.append(x7)
	zz.append(x8)
	zz.append(x9)
	zz.append(x10)
	zz.append(x11)

#	s2 = s2 + id_name + ') FROM '+ request.session["mgmt_table_name"] + " ORDER BY "+id_name+" DESC limit 20"
	# Template that will include filtering in every column
	if direction_id == 1:
		s1 = ("""SELECT xx1 FROM xx2 where xx3<%s ORDER BY xx4 DESC limit 20""")%(min_id)
		# s1 = ("""SELECT xx1 FROM xx2 where xx3<%s AND w10=%s OR w11=%s OR w12=%s OR w13=%s OR w14=%s OR w15=%s OR w16=%s ORDER BY xx4 DESC limit 20""")%(min_id,zz[0],zz[1],zz[2],zz[3],zz[4],zz[5],zz[6])
	else:
		# uu = request.session["eee"]
		s1 = ("""SELECT xx1 FROM xx2 where xx3>%s ORDER BY xx4 ASC limit 20""")%(min_id)
		# s1 = ("""SELECT xx1 FROM xx2 where xx3>%s AND w10=%s OR w11=%s OR w12=%s OR w13=%s OR w14=%s OR w15=%s OR w16=%s ORDER BY xx4 ASC limit 20""")%(min_id,zz[0],zz[1],zz[2],zz[3],zz[4],zz[5],zz[6])


	# This part is a test part
	# s1 = ("""SELECT xx1 FROM xx2 where xx3<%s xxy ORDER BY xx4 DESC limit 20""")%(min_id)
	

	index = s1.find('xx1')
	s1 = s1[:index] + s2 + s1[index+3:]
	index = s1.find('xx2')
	s1 = s1[:index] + request.session["mgmt_table_name"] + s1[index+3:]
	index = s1.find('xx3')
	s1 = s1[:index] + id_name + s1[index+3:]
	index = s1.find('xx4')
	s1 = s1[:index] + id_name + s1[index+3:]


# Uncomment below block to put filtering trial back in play
	# for a in range(1,8):
	# 	b = a + 9
	# 	a_var = 'w' + str(b)
	# 	index = s1.find(a_var)
	# 	s1 = s1[:index] + z[(a-1)] + s1[index+3:]




	# index = s1.find('z02')
	# s1 = s1[:index] + z[1] + s1[index+3:]
	# index = s1.find('z03')
	# s1 = s1[:index] + z[2] + s1[index+3:]


	# first test 
	# index = s1.find('xx5')
	# s1 = s1[:index-4] + s1[index+6:]
	# index = s1.find('xx5v')
	# s1 = s1[:index-1] + s1[index+4:]


	# jj = request.session["dlkjlk"]
#	Below Error check for end of or start of table.  Refresh to start if it is.
	# return render(request,'kiosk/kiosk_test2.html', {'tmp':s1})


	try:
		db, cur = db_set(request)
		cur.execute(s1)
		tmp = cur.fetchall()
		tmp1=tmp[0]
		db.close()
	except:
		request.session["route_1"] = request.session["mgmt_production_call"]
		return direction(request)


	cctr = int(request.session['ctr'])
	# return render(request,'kiosk/kiosk_test2.html', {'tmp':tmp})


	# set min_id to the last id on the page

	# this point needs to re establish the Min and Max id value for ones displayed
	#need to work on the below code

	if direction_id == 0:
		tmp = tmp[::-1]

	for b in tmp:
		tmp1=b[0]
		if tmp1>min_id:
			min_id = tmp1

	last_id = min_id
	for b in tmp:
		tmp1=b[0]
		if tmp1<last_id:
			last_id = tmp1

#	if cctr == 8:
	# jjj = request.session['biker']
	request.session['ending_id'] = last_id
	request.session['starting_id'] = min_id
	
	return render(request,'mgmt_display.html', {'tmp':tmp})

def mgmt_display_next(request):
	
	request.session['direction_id'] = 1
 	request.session['starting_id'] = request.session['ending_id']

	return mgmt_display(request)

def mgmt_display_prev(request):
	request.session['direction_id'] = 0
	return mgmt_display(request)

def mgmt_display_edit(request,index):
	# request.session["table_headers"]  ==>  The name displayed on page 
	# request.session["table_variables"] ==> The name in the DB 
	p = ['' for y in range(0)]
	v = ['' for y in range(0)]
	datecheck = ['' for y in range(0)]
	a1 = ['' for y in range(0)]

	# call in to tmp the row to edit
	update_list = ''
	ctr = 0
	tmp_index = index
	db, cur = db_set(request) 
	sq1 = request.session["mgmt_table_call"] + "  where id = '%s'" %(tmp_index)
	cur.execute(sq1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	ptr = 1
	for x in tmp2:
		if type(x) is dt.date:
			y = vacation_set_current6(x)
			datecheck.append(1)
			v.append(y)
		else:
			datecheck.append(0)
			v.append(x)
		p.append(ptr)
		ptr = ptr + 1
		

	tmp3 = zip(p,v,datecheck)
	
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'mgmt_production_hourly'
				return direction(request)
		except:
			dummy = 1
#		return render(request,'kiosk/kiosk_test2.html',{'tmp':ddd})
		for i in tmp3:
			pst = str(i[0])
			b1 = request.POST.get(pst)
			b1=str(b1)
			c1 = '"' + b1 + '"'
			a1.append(c1)
		# Brilliant recursive algorithm to update known table with known variables
		tb1 = request.session["mgmt_table_name"]
		i1 = index
		db, cur = db_set(request)       # Open DB
		for x in request.session["table_variables"]:  # column names
			#  x ==>  name of column
			#  a1[ctr] ==> value of column
			col1 = x
			v1 = a1[ctr]
			v2 = v[ctr]
			if ctr == 0 :
				id1 = x
			if ctr > 0:
				zql = ("""update xx1 SET xx2=%s where xx3=%s"""%(v1,i1))
				index = zql.find('xx1')
				zql = zql[:index] + tb1 + zql[index+3:]
				index = zql.find('xx2')
				zql = zql[:index] + col1 + zql[index+3:]
				index = zql.find('xx3')
				zql = zql[:index] + id1 + zql[index+3:]
				cur.execute(zql)   # Execute SQL
				db.commit()
			ctr = ctr + 1
		db.close()
		return mgmt_display(request)
		request.session["route_1"] = request.session["mgmt_production_call"]
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request,'mgmt_display_edit.html', {'tmp':tmp3})	

def mgmt_display_insert(request,index):
	# request.session["table_headers"]  ==>  The name displayed on page 
	# request.session["table_variables"] ==> The name in the DB 
	p = ['' for y in range(0)]
	v = ['' for y in range(0)]
	datecheck = ['' for y in range(0)]
	a1 = ['' for y in range(0)]

	# call in to tmp the row to edit
	update_list = ''
	ctr = 0
	tmp_index = index
	db, cur = db_set(request) 
	sq1 = request.session["mgmt_table_call"] + "  where id = '%s'" %(tmp_index)
	cur.execute(sq1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	ptr = 1
	for x in tmp2:
		if type(x) is dt.date:
			y = vacation_set_current6(x)
			datecheck.append(1)
			v.append(y)
		else:
			datecheck.append(0)
			v.append(x)
		p.append(ptr)
		ptr = ptr + 1
		

	tmp3 = zip(p,v,datecheck)
	
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'mgmt_production_hourly'
				return direction(request)
		except:
			dummy = 1
#		return render(request,'kiosk/kiosk_test2.html',{'tmp':ddd})
		for i in tmp3:
			pst = str(i[0])
			b1 = request.POST.get(pst)
			b1=str(b1)
			c1 = '"' + b1 + '"'
			a1.append(c1)
		# Brilliant recursive algorithm to update known table with known variables
		tb1 = request.session["mgmt_table_name"]
		i1 = index
		db, cur = db_set(request)       # Open DB
		for x in request.session["table_variables"]:  # column names
			#  x ==>  name of column
			#  a1[ctr] ==> value of column
			col1 = x
			v1 = a1[ctr]
			v2 = v[ctr]
			if ctr == 0 :
				id1 = x
			if ctr > 0:
				
				s1 = ("""SELECT xx1 FROM xx2 where xx3<%s ORDER BY xx4 DESC limit 20""")%(min_id)

				zql = ("""INSERT INTO xx1(xx2) VALUES(xx3)""",(xx4))
				
				cur.execute('''INSERT INTO tkb_kiosk(Clock,Job1,Job2,Job3,Job4,Job5,Job6,TimeStamp_In,TimeStamp_Out) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (kiosk_clock,kiosk_job1,kiosk_job2,kiosk_job3,kiosk_job4,kiosk_job5,kiosk_job6,TimeStamp,TimeOut))
				db.commit()
				db.close()

				zql = ("""update xx1 SET xx2=%s where xx3=%s"""%(v1,i1))
				index = zql.find('xx1')
				zql = zql[:index] + tb1 + zql[index+3:]
				index = zql.find('xx2')
				zql = zql[:index] + col1 + zql[index+3:]
				index = zql.find('xx3')
				zql = zql[:index] + id1 + zql[index+3:]
				cur.execute(zql)   # Execute SQL
				db.commit()
			ctr = ctr + 1
		db.close()
		return mgmt_display(request)
		request.session["route_1"] = request.session["mgmt_production_call"]
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request,'mgmt_display_edit.html', {'tmp':tmp3})	

def kiosk_email_initial(request):
  	# Below will test for a variable and if it doesn't exist then make the column with a value assigned
  	db, cursor = db_set(request)
	x = 5
 	try:
  		sql = "SELECT low_production FROM sc_production1 where id = '%d'" % (x)
  		cursor.execute(sql)
 		tmp = cursor.fetchall()
  	except:
		cursor.execute("Alter Table sc_production1 ADD low_production INT Default 0")
    	db.commit()
	try:
		sql = "SELECT manual_sent FROM sc_production1 where id = '%d'" % (x)
		cursor.execute(sql)
		tmp = cursor.fetchall()
	except:
		cursor.execute("Alter Table sc_production1 ADD manual_sent INT Default 1")
    	db.commit()
  # cursor.execute("Alter Table sc_production DROP Column low_production")  # Drop a Column
  # db.commit()
  # # cursor.execute("Alter Table tkb_test1 ADD Third Char(30) DEFAULT NULL")  # Add a Column
  # cursor.execute("Alter Table tkb_test1 ADD Third Boolean Default 0")
  # db.commit()
  	# db.close()
  	return db, cursor



