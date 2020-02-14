from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
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

def manpower_layout(request):

	db, cur = db_set(request)
	TimeOut = -1
	part = '50-9341'
	sql = "SELECT DISTINCT asset_num FROM sc_production1 WHERE partno = '%s'" %(part)
	cur.execute(sql)
	tmp = cur.fetchall()
	return render(request, "kiosk/kiosk_test.html",{'tmp':tmp})