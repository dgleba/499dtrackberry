from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from time import strftime

from views_db import db_open, db_set
from datetime import datetime
import MySQLdb
import time

def fup(x):
	return x[2]

def gup(x):
	return x[5]
	
def nup(x):
	return x[4]

def tup(x):
	global tst
	tst.append(str(x[5]))
	
def eup(x):
		global a,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11
		a.append(str(x[0]))
		a1.append(str(x[1]))
		a2.append(str(x[2]))
		a3.append(str(x[3]))
		a4.append(str(x[4]))
		a5.append(str(x[5]))
		a6.append(str(x[6]))
		a7.append(str(x[7]))
		a8.append(str(x[8]))
		a9.append(str(x[9]))
		a10.append(str(x[10]))
		a11.append(str(x[11]))
		

	
def transfer(request):

  global a,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11
  
  a = []
  a1 = []
  a2 = []
  a3 = []
  a4 = []
  a5 = []
  a6 = []
  a7 = []
  a8 = []
  a9 = []
  a10 = []
  a11 = []


  u = 1447837118

  db, cursor = db_set(request)

  sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
  cursor.execute(sql)
  tmp = cursor.fetchall()

  
  [eup(x) for x in tmp]
  
  list = zip(a,a1,a2,a3)

  return render(request,"transfer.html",{'list':list})

