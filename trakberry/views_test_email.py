from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set

from datetime import datetime
import MySQLdb
import time
from django.core.context_processors import csrf


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def email1(request):

	return render(request, "email_test_A.html")

def done_email_1(request):

	return render(request, "done_test.html")



