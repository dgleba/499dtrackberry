from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_test import layer_choice_init
from trakberry.forms import login_Form, login_password_update_Form
from datetime import datetime
import MySQLdb
import time
from django.core.context_processors import csrf
import smtplib
from smtplib import SMTP


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
	
	
# Call Main Login screen
def main_login(request):
	
	return render(request, "main_log.html")

def login_initial(request,login_name):
	
		request.session["shift1"] = ''
		request.session["shift2"] = ''
		request.session["shift3"] = ''
		request.session["shift4"] = ''
		request.session["shift5"] = ''
		request.session["shift6"] = ''
		request.session["shift7"] = ''
		request.session["shift8"] = ''
		request.session["shift9"] = ''
		request.session["shift10"] = ''
		request.session["shift11"] = ''
		request.session["shift12"] = ''
		request.session["shift13"] = ''
		request.session["shift14"] = ''
		
		request.session["sfilter1"] = ''
		request.session["sfilter2"] = ''
		request.session["sfilter3"] = ''
		request.session["sfilter4"] = ''
		request.session["sfilter5"] = ''
		request.session["sfilter6"] = ''
		request.session["sfilter7"] = ''
		request.session["sfilter8"] = ''
		request.session["sfilter9"] = ''
		request.session["sfilter10"] = ''
		request.session["sfilter11"] = ''
		request.session["sfilter12"] = ''
		request.session["sfilter13"] = ''
		request.session["sfilter14"] = ''
		request.session["shift_primary"] = 'Cont A Days'
		
		if login_name == 'Ken Frey':
			request.session["shift_primary"] = 'Cont A Days'
			request.session["matrix_shift"] = 'Cont A Days CSD 2'
			request.session["sfilter1"] = 'checked'
			request.session["sfilter5"] = 'checked'
			request.session["shift1"] = 'CSD2 Day'
			request.session["shift5"] = 'Cont A Days'
			
		elif login_name == 'Dave Clark':
			request.session["matrix_shift"] = 'Cont A Nights CSD 2'
			request.session["shift_primary"] = 'Cont A Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter4"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift4"] = 'Cont A Nights'
			
						
		elif login_name == 'Chris Strutton':
			request.session["matrix_shift"] = 'Cont B Nights CSD 2'
			request.session["shift_primary"] = 'Cont B Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter6"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift6"] = 'Cont B Nights'
						
		elif login_name == 'Scott McMahon':
			request.session["matrix_shift"] = 'Aft CSD 2'
			request.session["shift_primary"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'			
									
		elif login_name == 'Scott Herman':
			request.session["matrix_shift"] = 'Day CSD 2'
			request.session["shift_primary"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			request.session["sfilter5"] = 'checked'
			request.session["sfilter7"] = 'checked'
			request.session["shift1"] = 'CSD2 Day'
			request.session["shift5"] = 'Cont A Days'
			request.session["shift7"] = 'Cont B Days'
	
									
		elif login_name == 'Karl Edwards':
			request.session["matrix_shift"] = 'Mid CSD 2'
			request.session["shift_primary"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter4"] = 'checked'
			request.session["sfilter6"] = 'checked'
			request.session["shift6"] = 'Cont B Nights'
			request.session["shift4"] = 'Cont A Nights'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'			
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'		
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'				
			
		elif login_name == 'Rick Wurm':
			request.session["matrix_shift"] = 'Cont A Nights CSD 2'
			request.session["shift_primary"] = 'Cont A Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter4"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift4"] = 'Cont A Nights'

		
		elif login_name == 'Pete Murphy':
			request.session["matrix_shift"] = 'Cont B Nights CSD 2'
			request.session["shift_primary"] = 'Cont B Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter6"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift6"] = 'Cont B Nights'
			
		elif login_name == 'Don Barber':
			request.session["shift_primary"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'
			
		elif login_name == 'Kevin Baker':
			request.session["shift_primary"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'
			
		elif login_name == 'Steven Koehler':
			request.session["shift_primary"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'	
			
		elif login_name == 'Brad Sproat':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
		
		elif login_name == 'Mark Phillips':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
			
		elif login_name == 'John Seagram':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'	
		elif login_name == 'Rob Zylstra':
			request.session["shift_primary"] = 'Q.A.'
			request.session["sfilter15"] = 'checked'
			request.session["shift15"] = 'Q.A.'	
		elif login_name == 'Kevin Faubert':
			request.session["shift_primary"] = 'Furnace Setter'
			request.session["sfilter17"] = 'checked'
			request.session["shift17"] = 'Furnace Setter'	

			
		elif login_name == 'Jennifer Button':
			request.session["shift_primary"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift13"] = 'CSD1 Mid'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'		
			
		elif login_name == 'Matt Ohm':
			request.session["shift_primary"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift13"] = 'CSD1 Mid'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'
		elif login_name == 'Scott Brownlee':
			request.session["shift_primary"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift11"] = 'CSD1 Day'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'				
		elif login_name == 'Mike Clarke':
			request.session["shift_primary"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift12"] = 'CSD1 Aft'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'
			
		elif login_name == 'Kelly Crowder':
			request.session["shift_primary"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
			request.session["shift11"] = 'CSD1 Day'

				
		else:
			dummy_yy = 'meaningless'
#			request.session["shift_primary"] = 'Cont A Days'
#			request.session["sfilter1"] = 'checked'
#			request.session["shift1"] = 'CSD2 Day'	
			
		return
					
	
# Login for Main Program
def main_login_form(request):	

#	if request.POST:
	if 'button1' in request.POST:
		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")

		request.session["login_name"] = login_name
		request.session["login_password"] = login_password
		
		login_initial(request,login_name)
	
	
		return main(request)
		
	elif 'button2' in request.POST:
		
		return render(request,'login/reroute_lost_password.html')

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'main_login_form.html', args)	

# Password Forgot Form
def main_login_password_lost_form(request):	

	if request.POST:
		login_name = request.POST.get("login_name")
		request.session["login_name"] = login_name
		main_password_lost_email(request)  # Email password to proper login's email
		return render(request, "main_log.html")  # Completed sending email of password

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'login/main_login_password_lost.html', args)	
	
# Password Update

# Send login password via email
def main_password_lost_email(request):
	
	user_name = request.session["login_name"]

	# retrieve left first character of login_name only
	name_temp1 = user_name[:1]
	# retrieve last name of login name only 	
	name_temp2 = user_name.split(" ",1)[1]
	name_temp3 = name_temp1 + name_temp2 + '@stackpole.com'
	
	toaddrs = name_temp3

	
	
	#return render(request,'login/done_email_password.html', {'user_name':user_name})


	db, cur = db_set(request)
	# Create the table if it does not exist
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_users(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), active INT(2))""")
	# Check password to match name.  If no record of name then divert to except and reroute to create new password
	try:
		sql = "SELECT * FROM tkb_users where user_name = '%s'"%(user_name)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		password = tmp2[2]

	except:
		password = 'stackberry'

	password = 'Password is : ' + password

	message_subject = 'Trackberry Password for :' + request.session["login_name"]


	fromaddr = 'stackpole@stackpole.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	
	message = "From: %s\r\n" % frname + "To: %s\r\n" % toaddrs + "Subject: %s\r\n" % message_subject + "\r\n" 

	
	
	message = message + message_subject + "\r\n\r\n" + password
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	
	db.close()
	return
	
def main_password_update(request):	
	#return render(request, "test_temp2.html")
	login_name = request.session["login_name"]
	
	if request.POST:
        			
		login_password1 = request.POST.get("login_password1")
		login_password2 = request.POST.get("login_password2")
		
		if login_password1 != login_password2:
			return render(request, "reroute_main_password_updatee.html")
		request.session["login_password"] = login_password1
		
		
		
		
		login_password_update(request)
		
		
		login_initial(request,login_name)
	
		return render(request, "reroute_main.html")
		#return main(request)

	else:
		form = login_password_update_Form()
	
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_password"] = ""
	return render(request,'main_password_update_form.html', {'login_name':login_name,'args':args})

# Updates the Password of the current user
def login_password_update(request):
	login_name = request.session["login_name"]
	login_password = request.session["login_password"]
	db, cur =db_open()
	try:
		sql = "SELECT password FROM tkb_users where name = '%s'"%(login_name)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		
		tql = ('update tkb_users SET password="%s" WHERE name="%s"' % (login_password,login_name))
		cur.execute(tql)
		db.commit()
		
	except:
		cur.execute ('''INSERT INTO tkb_users(user_name,password) VALUES(%s,%s)''',(login_name,login_password))
		db.commit()

		
	return

def main_A(request):
	return main(request)


# ********************************* Main Test *****************************************
# Use a counter for testing to see how many times through main
# And delete all session variables to start fresh
def main_test_init(request):
	# Delete all session variables
	for key in request.session.keys():
		del request.session[key]
	# Assign a counter session variable
	request.session["test_counter"] = 0
	request.session["local_switch"] = 1  #Make sure it's 1 for local use
	return render(request, "reroute_test_main.html")
# ************************************************************************************


def main(request):
	# Check if it's local running or not and if not then force the path as /trakberry
	# Run switch_net to set it back to network or switch_local for local use
	try:
		if request.session["local_switch"] == 1:
			request.session["local_toggle"] = ""
		else:
			request.session["local_toggle"] = "/trakberry"
	except:
		request.session["local_toggle"] = "/trakberry"
	# ******************************************************************************
	
#	Check if login_name and login_password have been entered.

	try:
		password = request.session["login_password"]
		name = request.session["login_name"]

	except:
		password = 'no'
		name = ""
	
	#ctr = request.session["test_counter"]
	
	
	# how to delete a session variable
	#del request.session['mykey']
	
	log_pass = 0   # Make this -99 if you use password checker
	
	# Password Check Section
#	sql = "SELECT * FROM tkb_layered where Name = '%s'" %(name)
#	cursor.execute(sql)
#	tmp = cursor.fetchall()
#	tmp2 = tmp[0]
	


	#if ctr > 0:
	#	return render(request, "test_temp3.html", {'log_pass':log_pass,'name':name,'password':password})
	#request.session["test_counter"] = request.session["test_counter"] + 1
	
	# Call password check Sub Module 
	#request.session["test_counter"] = request.session["test_counter"] + .001
	
	
	# *******************************************************************************
	# Password Checker       ********************************************************
	# *******************************************************************************
	#log_pass = main_password_check(name,password,request)   # Uncomment when you want to use it
	# *******************************************************************************
	# *******************************************************************************
	
	
	#return render(request, "test_temp3.html", {'log_pass':log_pass,'name':name,'password':password})
	
	
	#if (request.session["test_counter"]) > 2:
	#	return render(request, "test_temp3.html", {'log_pass':log_pass,'name':name,'password':password})
		
		
	# below line is for testing
	#return render(request, "reroute_main_password_update.html", {'log_pass': log_pass,'name':name,'password':password})
	
	
	# Administrator Password
	if name == 'Dave Clark':
		if password == 'Jaden2008':
			log_pass = 1
	elif password == 'stackberry':
		log_pass = 1
	
	#return render(request, "test_temp3.html", {'log_pass':log_pass})

		
	# Code for checking if layered audit needs to be sent.  Make 
	if log_pass == 1:
	
		# use below line to bypass for testing
		return render(request, "main.html")
		
		
		
		
		#request.session.set_expiry(1800)
		#Check if layered audit required

		ID_1 = layered_audit_check(name)

		if ID_1 == 4:
			#return render(request,'done_test1.html')
			return layer_choice_init(request)
		# Check for Layered Audit done or not.
		layer_check = 1
		try:
			layer_check = int(request.session["layer_audit_check"])
		except:
			request.session["layer_audit_check"] = 1
		
		# Below statement determines if a layered audit message needs to occur using layer_check variable
		# Use 6 as dummy number until ready to run then use 0
		if layer_check == 0 and name == 'Dave Clark':
			return layer_choice_init(request)
		
		return render(request, "main.html")
	elif log_pass == 0:
		return main_login(request)
		return render(request, "reroute_main.html")   # reroute to login again because either no name given or wrong one
	elif log_pass == 3:
		return main_login(request)

	else: # Reroute with 2 value to change password on old one
		#return main_login(request)
		return render(request, "reroute_main_password_updatee.html")
		#return main_password_update(request)
		
		
# Reset Login_Password  and re route back to main for re login
def main_logout(request):
	
	try:
		del request.session['login_password']
		del request.session['login_name']
	except:
		request.session['login_password'] = ' '
	return main(request)

#  ******  Password Check Sub Module ***********
def main_password_check(user_name,password,request):
	db, cur = db_set(request)
	# Create the table if it does not exist
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_users(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), active INT(2))""")
	# Check password to match name.  If no record of name then divert to except and reroute to create new password
	try:
		sql = "SELECT * FROM tkb_users where user_name = '%s'"%(user_name)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		if tmp2[2] == password:
			log_pass = 1
		else:
			log_pass = 0
			
			#return render(request, "test_temp3.html", {'log_pass':log_pass,'name':user_name,'tmp':tmp,'password':password})
	# Reroute to create new password
	except:
		if user_name == "":                 # No User given so login again
			log_pass = 3
		elif password == 'stackberry':      # there is no updated password and stackberry was used so update
			log_pass = 2
		else:                               # there is no updated password but stackberry was not used
			log_pass = 3

	
	#return render(request, "test_temp.html")
	return log_pass
	
	
# Check if Layered Audit has been entered for this name and todays date
def layered_audit_check(name):

	current_date = find_current_date()
	t = int(time.time())

	db, cursor = db_set(request)  
	try:
		sql = "SELECT * FROM tkb_layered where Name = '%s'" %(name)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		ts = tmp2[6]
		
		ID_1 = tmp2[0]

	except:
		ID_1 = 4

	db.close()
		
	return ID_1
  
def switch_local(request):
	request.session["local_switch"] = 1
	request.session["local_toggle"] = ""
	return main(request)
	
def switch_net(request):
	request.session["local_switch"] = 0
	request.session["local_toggle"] = "/trakberry"
	return main(request)
	
	





