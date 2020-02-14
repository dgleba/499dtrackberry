from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP
from django.core.context_processors import csrf
from datetime import datetime, date
from views_db import db_open, db_set


def direction(request):

	return render(request, "kiosk/route.html")


