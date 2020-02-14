from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date, mgmt_display, mgmt_display_edit
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5,vacation_set_current6
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set
from datetime import datetime 

# *********************************************************************************************************
# MAIN Production View
# This is the main Administrator View to tackle things like cycle times, view production etc.
# *********************************************************************************************************

def mgmt(request):
	return render(request, "mgmt.html")

# Reset the password so it logs out
def mgmt_logout(request):
	request.session["mgmt_login_password"] = " "
	return render(request, "mgmt.html")

def mgmt_login_form(request):	

#	if request.POST:
	if 'button1' in request.POST:


		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")

		if len(login_name) < 5:
			login_password = 'wrong'

		request.session["mgmt_login_name"] = login_name
		request.session["mgmt_login_password"] = login_password
	
		return mgmt(request)
		
	elif 'button2' in request.POST:
		
		return render(request,'login/reroute_lost_password.html')

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'mgmt_login_form.html', args)	

def mgmt_production_hourly(request):
	table_headers = ["ID","Cell","Operator","Date","Shift","Hour","Target","Actual","Shift Target","Shift Actual","DT Code","DT Mins","DT Reason","Created"]
	table_variables = ["id","p_cell","initial","p_date","p_shift","p_hour","hourly_target","hourly_actual","shift_target","shift_actual","downtime_code","downtime_mins","downtime_reason","created_at"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM sc_prod_hour"
	request.session["mgmt_table_name"] = 'sc_prod_hour'
	request.session["mgmt_table_title"] = 'Hourly Production'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_production_hourly_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_production_hourly'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)

def mgmt_production(request):
	table_headers = ["ID","Asset","Job","Part","Amount","DTime","Clock","Date","Shift","Runtime","Target"]
	table_variables = ["id","asset_num","machine","partno","actual_produced","down_time","comments","pdate","shift","shift_hours_length","target"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM sc_production1"
	request.session["mgmt_table_name"] = 'sc_production1'
	request.session["mgmt_table_title"] = 'Production Entries'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_display_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_production'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)

def mgmt_cycletime(request):
	table_headers = ["ID","Asset","Part","Cycletime","Job"]
	table_variables = ["Id","asset","part","cycletime","machine"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM tkb_cycletime"
	request.session["mgmt_table_name"] = 'tkb_cycletime'
	request.session["mgmt_table_title"] = 'Cycle Times'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_display_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_cycletime'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)






def mgmt_production_hourly_edit(request, index):
	tmp_index = index
	#request.session["index"] = index
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM sc_prod_hour where id = '%s'" %(tmp_index)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		tmp="No"	


# ***********************************************************************************************************************************
	request.session["mgmt_hourly_cell"] = tmp2[1]
	request.session["mgmt_hourly_initials"] = tmp2[2]
	request.session["mgmt_hourly_shift"] = tmp2[5]
	ddate = tmp2[4]
	ddd = vacation_set_current6(ddate)
	request.session["mgmt_hourly_date"] = vacation_set_current6(ddate)
	request.session["mgmt_hourly_hour"] = tmp2[6]
	request.session["mgmt_hourly_actual"] = tmp2[8]
	request.session["mgmt_hourly_dtcode"] = tmp2[11]
	request.session["mgmt_hourly_dtmins"] = tmp2[12]
	request.session["mgmt_hourly_dtreason"] = " "
	request.session["mgmt_hourly_dtreason"] = tmp2[13]

	


	try:
		if len(request.session["mgmt_hourly_dtreason"]) < 2:
			request.session["mgmt_hourly_dtreason"] = "-"
	except:
		request.session["mgmt_hourly_dtreason"] = "-"


	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'mgmt_production_hourly'
				return direction(request)
		except:
			dummy = 1

#		return render(request,'kiosk/kiosk_test2.html',{'tmp':ddd})
		mgmt_hourly_date = request.POST.get("mgmt_hourly_date")
		mgmt_hourly_cell = request.POST.get("mgmt_hourly_cell")
		mgmt_hourly_initials = request.POST.get("mgmt_hourly_initials")
		mgmt_hourly_shift = request.POST.get("mgmt_hourly_shift")
		mgmt_hourly_hour = request.POST.get("mgmt_hourly_hour")
		mgmt_hourly_actual = request.POST.get("mgmt_hourly_actual")
		mgmt_hourly_dtcode = request.POST.get("mgmt_hourly_dtcode")
		mgmt_hourly_dtmins = request.POST.get("mgmt_hourly_dtmins")
		mgmt_hourly_dtreason = request.POST.get("mgmt_hourly_reason")


		try:
			cql = ('update sc_prod_hour SET p_cell = "%s",initial="%s",hourly_actual="%s", p_date="%s", p_shift="%s" WHERE id ="%s"' % (mgmt_hourly_cell,mgmt_hourly_initials,mgmt_hourly_actual,mgmt_hourly_date,mgmt_hourly_shift,tmp_index))
			cur.execute(cql)
			db.commit()
		except:
			dummy = 1
			
		db.close()
		request.session["route_1"] = 'mgmt_production_hourly'
		return direction(request)
		#return render(request,'kiosk/kiosk_test2.html',{'tmp':tmp2})

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  

#	db, cur = db_set(request)
#	s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
#	cur.execute(s1)
#	tmp = cur.fetchall()
#	tmp2 = tmp[0]
#	tmp3 = tmp2[0]

	return render(request, "production/mgmt_production_hourly_edit.html",{'args':args,'tmp':tmp2,'ddate':ddd})

# ***********************************************************************************************************************************


