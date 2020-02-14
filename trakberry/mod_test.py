from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import MySQLdb
import time


# Updated July 12,2015
# Module to run test variables
def test_mode(request):
  
  request.session["var_test"] = "No Information"
  request.session["var_start"] = 0
  request.session["var_finish"] = 0
  request.session["var_cycle"] = 0
  request.session["var_dtime"] = 0
	
	

  t=int(time.time())
  tm = time.localtime(t)
  

  # Select prodrptdb db 
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  sqlA = "SELECT MAX(Id) FROM tkb_test"
  cursor.execute(sqlA)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  last_id = tmp2[0]
  
  sqlB = "SELECT message FROM tkb_test where Id = '%d'" %(last_id)
  cursor.execute(sqlB)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  msg = tmp2[0]	  
  request.session["var_test"] = msg
  
  sqlC = "SELECT stime FROM tkb_test where Id = '%d'" %(last_id)
  cursor.execute(sqlC)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  start = tmp2[0]	  
  request.session["var_start"] = start

  sqlD = "SELECT ftime FROM tkb_test where Id = '%d'" %(last_id)
  cursor.execute(sqlD)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  finish = tmp2[0]	  
  request.session["var_finish"] = finish
  
  sqlE = "SELECT ctime FROM tkb_test where Id = '%d'" %(last_id)
  cursor.execute(sqlE)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  cycle = tmp2[0]	  
  request.session["var_cycle"] = cycle
  
  sqlF = "SELECT dtime FROM tkb_test where Id = '%d'" %(last_id)
  cursor.execute(sqlF)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  dtime = tmp2[0]	  
  request.session["var_dtime"] = dtime

  
  db.close()
    
  return render(request,"test_var.html")
  
  
