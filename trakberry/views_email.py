from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from time import strftime
from datetime import datetime
import MySQLdb
import smtplib


def e_test(request):
	return render(request, "email_downtime.html")
	
	



	
  
	

  
  
