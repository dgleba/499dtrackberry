from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
import MySQLdb
import time



def machinery(request):
  

  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
  
	date = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
   
  # Select prodrptdb db 
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	# Retrieve information from Database and put 2 columns in array {list}
	# then send array to Template machinery.html
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	sqlA = "SELECT * FROM pr_downtime1 ORDER BY called4helptime DESC LIMIT 100" 
	
	sqlB = "SELECT machinenum, COUNT(*) FROM pr_downtime1 GROUP BY machinenum ORDER BY COUNT(*) DESC"
	

	
	cursor.execute(sqlA)
	tmp = cursor.fetchall()

	cursor.execute(sqlB)
	smp = cursor.fetchall()
	smp2 = smp[0]
	mach_cnt = smp2[0]
	a=1
	for i in range(0,100):
		
		tmp2 =(tmp[i]) 
		#machine[i]=(tmp2[0])
		
		machine.append(tmp2[0])
		date.append(tmp2[2])
		count.append(a)
	list = zip(machine,date,count)
	
	db.close()
  
  # call up 'display.html' template and transfer appropriate variables.  
	return render(request,"machinery.html",{'L':list,'M':smp})

