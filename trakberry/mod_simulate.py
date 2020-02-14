from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import entry
import MySQLdb
import time
from django.core.context_processors import csrf

# Updated June 3,2015

# Module to simulate Machine Inputs for M/C  677 , 748 , 749 , 750

# Module to Take entry simulate Pi 
# Eventually this module will link create and enter data into MySQL from button presses to simulate machine operation
# so we can run the view on another terminal to test.
def sim(request):

	machine = "none"
	qty = ""
	current = 0

	
	if request.POST:
		if '749button' in request.POST:
			machine = '749'
			current = int(time.time())
			qty = 1
		if '750button' in request.POST:
			machine = '750'
			current = int(time.time())
			qty = 1
		if '748button' in request.POST:
			machine = '748'
			current = int(time.time())
			qty = 1
		if '677button' in request.POST:
			machine = '677'
			current = int(time.time())
			qty = 1
			
		db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
		cur = db.cursor()
		sql = "SELECT MAX(pcount) FROM tkb_prodtrak where machine = '%s'" %(machine)
		cur.execute(sql)	  
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		pcount = tmp2[0]	
		db.commit()
		db.close()	
		pcount = pcount + qty
		simulate(machine,current,qty,pcount)	
		return render(request,'re.html')
		
	else:
		form = entry()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'simulator.html', args)

# Submodule to write selected machine to database	
def simulate(machine,current,qty,pcount):
  p = 101
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cur = db.cursor()
  sql =( 'insert into tkb_prodtrak(pi_id,machine,time,qty,pcount) values("%d","%s","%d","%d","%d")' % (p,machine,current,qty,pcount) )
  cur.execute(sql)
  db.commit()
  db.close()
  
  return 
	
	