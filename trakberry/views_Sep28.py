from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from time import strftime

from datetime import datetime
import MySQLdb
import time

def fup(x):
	return x[2]

def gup(x):
	return x[5]
	
def eup(x):
		global st, nt
		nt.append(str(x[4]))
		st.append(str(x[5]))
		
def mup(x):
		global dt
		dt.append(str(x[7]))
	
	
def test2(request):

  try:
	request.session["details_gf6op30"]
  except:
	request.session["details_gf6op30"] = 0
  try:
	request.session["details_track"]
  except:
	request.session["details_track"] = 0	
	
  t=int(time.time())
  rate = float(7)
  machine_list = ['677','748','749','750']
  tm = time.localtime(t)
  count =[0,0,0,0]
  down_time = [0,0,0,0]
  diff_time = [0,0,0,0]
  part = [0,0,0,0]
  diff = [0,0,0,0]
  projection = [0,0,0,0]
  hrate = [0,0,0,0]
  cycle = [0,0,0,0]
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  total = 0
  global st, pt_ctr,nt, pt, dt
  
  # Determine initial Shift Start value based on current time
  # Initialize shift_start as -1 to represent 11pm so all 24hr numbers calculate properly
  shift_start = -1
  if tm[3]<23 and tm[3]>=15:
	shift_start = 15
  elif tm[3]<15 and tm[3]>=7:
	shift_start = 7
  cur_hour = tm[3]
  if cur_hour == 23:
	cur_hour = -1
  
  # Shift Start EPOCH TIME designation  
  # Set u to the epoch time for the beginning of the shift of current day.  Either 23, 7 or 15	
  u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])
  u = u - 28800
  # Select prodrptdb db 
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
  cursor.execute(sql)
  tmp = cursor.fetchall()

  rate = 0.00790
  # find totals of each non zero part for each machine
  for y in range(0, 4):
	st = []
	nt = []
	pt = []
	dt = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = 0
		cycle[y] = 0
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	# calculate projected shift target
	t = int(time.time())
	time_ran = t - int(u)
	rate = (count[y]/float(time_ran))
	projection[y] = round(rate * 28800,0)
	hrate[y] = round(rate *3600,2)
	
	total = total + count[y]	
	red[y]=900
	yellow[y]=180
	
	
  #list = zip(machine_list,count,diff_time,diff,down_time,part,projection,hrate)	
		
  #return render(request,"test2.html",{'List':list})
  #request.session["details_gf6op30"] = 1
  return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'Cycle':cycle, 'Hrate':hrate, 'Downtime':down_time, 'Projection':projection, 'Part':part})

  	
  
# Updated May 26,2015
# Module to obtain trial run information and display live data in display.html
def display(request):
  
  try:
	request.session["details_gf6op30"]
  except:
	request.session["details_gf6op30"] = 0
  try:
	request.session["details_track"]
  except:
	request.session["details_track"] = 0	
  count = [0,0,0,0]
  part = [0,0,0,0]
  diff = [0,0,0,0]
  cycle = [0,0,0,0]
  diff_time = [0,0,0,0]
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  projection = [0,0,0,0]
  hrate = [0,0,0,0]
  machine_list = [677,748,749,750]
  down_time = [0,0,0,0]
  total = 0
  # initialize current time and set 'u' to shift start time
  t=int(time.time())
  tm = time.localtime(t)
  
  # Determine initial Shift Start value based on current time
  # Initialize shift_start as -1 to represent 11pm so all 24hr numbers calculate properly
  shift_start = -1
  if tm[3]<23 and tm[3]>=15:
	shift_start = 15
  elif tm[3]<15 and tm[3]>=7:
	shift_start = 7
  cur_hour = tm[3]
  if cur_hour == 23:
	cur_hour = -1
  
  # Shift Start EPOCH TIME designation  
  # Set u to the epoch time for the beginning of the shift of current day.  Either 23, 7 or 15	
  u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])
  
   
  # Select prodrptdb db 
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  
  for i in range(0, 4):

	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	  sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND part_timestamp >= '%d'" %(machine_list[i], u)
	  cursor.execute(sqlA)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]

	  # Select Sum of downtime since shift start for machine[i] and assign to DT
	  sqlAB = "SELECT SUM(downtime) FROM tkb_prodtrak where machine = '%s' AND part_timestamp >= '%d'" %(machine_list[i], u)
	  cursor.execute(sqlAB)
	  temp = cursor.fetchall()
	  temp2 = temp[0]
	  DT = temp2[0]
	  
	  # convert respective machine downtime DT for the shift to display format and assign to 
	  # down_time variable.  Default to 0 if error from div by 0 for shift start
	  try:
		m, s = divmod(DT,60)
		h, m = divmod(m, 60)
		down_time[i]="%d:%02d:%02d" % (h,m,s)		
	  except:
		down_time[i] = "0"
			
	  # check to ensure there are entries for the shift otherwise set count to 0	  
	  if tmp2[0]<> None:
		count[i] = tmp2[0]
	  else:
		count[i] = 0
	  
	  # calculate projected shift target
	  t = int(time.time())
	  time_ran = t - int(u)
	  rate = count[i]/time_ran
	  projection[i] = round(rate * 28800,0)
	  hrate[i] = round(rate *3600,2)
	  
	  var = 1
	  # Select the highest Unix time entered as being the last entry 
	  # and assign it to 'max'
	  sqlB = "SELECT MAX(part_timestamp) FROM tkb_prodtrak where machine = '%s' AND qty = '%d'" %(machine_list[i], var)
	  cursor.execute(sqlB)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]
	  max = tmp2[0]

	  sqlAB = "SELECT MAX(part_timestamp) FROM tkb_prodtrak where machine = '%s'" %(machine_list[i])
	  cursor.execute(sqlAB)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]
	  maxx = tmp2[0]	  
	  
	  
	  sqlC = "Select(perpetual_counter) FROM tkb_prodtrak where machine = '%s' AND part_timestamp = '%d' AND qty = '%d'" %(machine_list[i], max, var) 
	  cursor.execute(sqlC)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]
	  pcount = tmp2[0]

	  sqlD = "Select(cycletime) FROM tkb_prodtrak where machine = '%s' AND perpetual_counter = '%d' AND qty = '%d'" %(machine_list[i], pcount, var) 
	  cursor.execute(sqlD)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]
	  cycle[i] = tmp2[0]	  

	  
	  sqlF = "Select(part_number) FROM tkb_prodtrak where machine = '%s' AND part_timestamp = '%d'" %(machine_list[i], maxx) 
	  cursor.execute(sqlF)
	  tmp = cursor.fetchall()
	  tmp2 = tmp[0]
	  part[i] = tmp2[0]
	  
	  # seconds from current time and last entry time.
	  # convert that to readable time and assign it to 'diff_time'
	  current = int(time.time())
	  diff[i] = current - max
	  # Failsafe should it be shift start to avoid div by 0 error
	  try:
		m, s = divmod(diff[i],60)
		h, m = divmod(m, 60)
		diff_time[i]="%d:%02d:%02d" % (h,m,s)
	  except:
		diff_time[i] = "0"
	  
	  # Set the warning times in seconds
	  yellow[i] = 180
	  red[i] = 900
	  total = total + count[i]
  
  db.close()
  
  # call up 'display.html' template and transfer appropriate variables.  
  return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'Cycle':cycle, 'Hrate':hrate, 'Downtime':down_time, 'Projection':projection, 'Part':part})
# End of Trial Run Module

def create_table(request):
  # Construct tkb_prodtrak format
  # Select prodrptdbtest db 
  
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  cursor.execute("""DROP TABLE IF EXISTS tkb_prodtrak""")
  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_prodtrak(Id INT PRIMARY KEY AUTO_INCREMENT,pi_id INT(10), machine CHAR(30), part_timestamp INT(20), qty INT(2), pcount INT(20), downtime INT(20), cycletime INT(10), status VARCHAR(25))""")
  db.commit()
  t = int(time.time())
  m1 = '750'
  m2 = '749'
  m3 = '677'
  m4 = '748'
  tb = 101
  qty = 0
  perp = 0
  db.commit()
  sqA =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m1,t,qty,perp) )
  sqB =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m2,t,qty,perp) )
  sqC =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m3,t,qty,perp) )
  sqD =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m4,t,qty,perp) )
  cursor.execute(sqA)
  cursor.execute(sqB)
  cursor.execute(sqC)
  cursor.execute(sqD)
  db.commit()
  db.close()
  return render(request,'done.html')
 
def create_test_table(request):
  # Construct tkb_test format
  # Select prodrptdbtest db 
  
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_test(Id INT PRIMARY KEY AUTO_INCREMENT,message CHAR(30),stime INT(20),ftime INT(20),ctime INT(20))""")
  db.commit()
  m1 = 'BEGIN MESSAGES'
  st = 0
  ft = 0  
  ct = 999
  db.commit()
  sqA =( 'insert into tkb_test(message,stime,ftime,ctime) values("%s","%d","%d","%d")' % (m1,st,ft,ct))
  cursor.execute(sqA)
  db.commit()
  db.close()
  return render(request,'done.html')

  # Alter a column name in a table 
def alter_table_name(request):  
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  cursor.execute("""ALTER TABLE tkb_prodtrak RENAME COLUMN pcount to perpetual_counter""")
  db.commit() 
  return render(request,'done.html')
  
  
def db_write(request):
  # Select prodrptdbtest db 
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdbtest')
  cur = db.cursor()
  
  A = "TrialRun"
  B = "TestValue"

  # Below is example of inserting text into coloumns of gpio table
  #sql = '''INSERT into gpio (Machine, Date) VALUES ('Willie', 'Wonka')'''

  # Below is example of inserting variables into columns of gpio table.  (use tuple %d for integers)
  sql =( 'insert into gpio(Machine,Date) values("%s","%s")' % (A,B) )
  
  cur.execute(sql)
  db.commit()

  db.close()
  return render(request,'done.html')


def test(request):

	# Time Conversions.  Timestamp - DateTime and vica versa **********
	
	x=[]
	# takes a unix timestamp
	t = int(time.time())
	x=[0 for i in range(9)] 
	# converts timestamp to a tuple with format
	tm = time.localtime(t)
	
	# take an assigned tuple
	x[0] = 2015
	x[1] = 8
	x[2] = 8
	x[3] = 3
	x[4] = 1
	x[5] = 45
	# and convert to a unix time
	y = time.mktime(x)
	# ******************************************************************


#	dif = (tm[3]-15)*60*60
#	dif = dif + (tm[4]*60)+tm[5]
#	u=t-dif
#	tx = time.localtime(u)
	
	#call each variable in tuple as needed Ex  tm[3] = hours
	#h = request.session["s_date"]
	#xm = time.mktime(h)
	
	
	# ***Convert formated datetime '2015-09-01T15:09' and convert to timestamp and tuple
	# *** s_date is string used
	
	start_date = request.session["s_date"]
	
	temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
	#   Time Stamp
	start_stamp = int(time.mktime(temp.timetuple()))
	#   Time Tuple
	start_tuple = time.localtime(start_stamp)
	
	



	
	return render(request, "test_1.html", {'Hour': tm,'Time': t, 'Time2': y, 'Stamp':start_stamp, 'Tuple':start_tuple})

def done(request):
	request.session["test"] = 78
	return render(request, "done.html")
	
# Module to expand / retract details on Live Tracking	
def details_session(request):
	temp = int(request.session["details_gf6op30"])
	if temp == 1:
		request.session["details_gf6op30"] = 0
	else:
		request.session["details_gf6op30"] = 1
		
	return display(request)

def details_track(request):
	temp = int(request.session["details_track"])
	if temp == 1:
		request.session["details_track"] = 0
	else:
		request.session["details_track"] = 1
		
	return display(request)	
	
def main(request):

	return render(request, "main.html")
def reports(request):

	return render(request, "reports.html")	

def scheduler(request):

	return render(request, "scheduler.html")
def inventory(request):

	return render(request, "inventory.html")		


def production_report(request):

	machine_list = [677,748,749,750]
	total = [0,0,0,0]
	part = [0,0,0,0]
	
	start_date = request.session["s_date"]
	end_date = request.session["e_date"]
	
	temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
	start_stamp = int(time.mktime(temp.timetuple()))
	start_tuple = time.localtime(start_stamp)

	temp = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")
	end_stamp = int(time.mktime(temp.timetuple()))
	end_tuple = time.localtime(end_stamp)	

	db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
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

def test_time(request):

	# initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	
	#request.session["local_time"] = tm

	shift_start = -1
	if tm[3]<23 and tm[3]>=15:
		shift_start = 15
	elif tm[3]<15 and tm[3]>=7:
		shift_start = 7
	
	#request.session["shift_start"] = shift_start

	u = t - (((tm[3]-shift_start)*60*60)+(tm[4]*60)+tm[5])
	d = t - u
	#request.session["unix_time"] = u
	
	
	return render(request, "test_time.html", {'Tm': tm,'S':shift_start,'U':u,'D':d})
	
	
