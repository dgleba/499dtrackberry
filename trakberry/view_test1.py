from django.shortcuts import render_to_response
#from math import trunc
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from trakberry.forms import login_Form
from django.http import HttpResponse
from views_db import db_open, db_set
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from smtplib import SMTP
import MySQLdb

import uuid

def kiosk_name(request):
    if request.POST:
        kiosk_id = request.POST.get("kiosk_id")
        request.session["kiosk_id"] = kiosk_id
        return render(request,'done_test8.html')
    else:
        form = login_Form()
    args = {}
    args.update(csrf(request))
    args['form'] = login_Form
    return render(request,'kiosk_id.html', args)	

def update_column(request):
    db, cur = db_set(request)
    old_value = "OP30"
    new_value = "PP30"
    part1 = "50-9341"
    cql = ('update sc_production1 SET machine = "%s" WHERE machine ="%s"  and partno = "%s"' % (old_value,new_value,part1))
    cur.execute(cql)
    db.commit()
    db.close()
    return render(request,'done_test8.html')







