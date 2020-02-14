from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5,vacation_set_current6
from trakberry.views_vacation import vacation_1
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
import decimal
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set, db_set
from views_mod1 import kiosk_lastpart_find
from datetime import datetime
import json

def barcode_initial_10R(request):

  request.session["barcode_skid"] = 1
  request.session["barcode_part_number"] = '9341'

  request.session["route_1"] = 'barcode_input_10R'
  return direction(request)

def barcode_input_10R(request):

    part = request.session["barcode_part"]
    pn = request.session["barcode_part_number"]

    if request.POST:
        bc1 = request.POST.get("barcode")
        request.session["barcode"] = bc1
        request.session["barcode_part_number"] = bc1[-4:]

        request.session["route_1"] = 'barcode_check_10R'
        return direction(request)
    else:
		form = kiosk_dispForm1()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    if pn == 'GM 9341':
      return render(request,"kiosk/barcode_input_10R_GM.html",{'args':args})
    elif pn == 'FORD 9341':
      return render(request,"kiosk/barcode_input_10R_FORD.html",{'args':args})
    return render(request,"kiosk/barcode_input_10R.html",{'args':args})

def barcode_check_10R(request):
    bar1 = request.session["barcode"]
    bar1=str(bar1)
    stamp = time.time()
    part = request.session["barcode_part"]
    h = len(bar1)
    if len(bar1) == 16:
      request.session["barcode_part_number"] ='GM 9341'
      request.session["bar1"] = bar1
      request.session["barcode_part"] = part
      return render(request,"barcode_ok_10R_GM.html")
    elif len(bar1) == 29:
      request.session["barcode_part_number"] ='FORD 9341'
      request.session["bar1"] = bar1
      request.session["barcode_part"] = part
      return render(request,"barcode_ok_10R_FORD.html")
    request.session["barcode_part_number"] ='UNKNOWN'
    return render(request,"barcode_warning_10R.html")


def barcode_initial(request):
  db_set(request)
  db, cur = db_set(request)
  sql = "SELECT max(scrap) FROM barcode"
  cur.execute(sql)
  tmp2 = cur.fetchall()
  tmp3 = tmp2[0]
  max_stamp = tmp3[0]

  sql = "SELECT * from barcode where scrap = '%s'" %(tmp3[0])
  cur.execute(sql)
  tmp2 = cur.fetchall()
  request.session["barcode1"] = tmp2[0][2]
  skid = tmp2[0][3] 
  part = tmp2[0][4]
  request.session["barcode_skid"] = skid
  request.session["barcode_part"] = part 

  request.session["route_1"] = 'barcode_input'
  return direction(request)


def barcode_input(request):
    db, cur = db_set(request)
    # the above call makes the below call unnecessary now.  
    #request.session["local_toggle"]="/trakberry"
  
    part = request.session["barcode_part"]
    # db, cur = db_set(request)
    sql = "SELECT * FROM barcode"
    cur.execute(sql)
    tmp2 = cur.fetchall()


    if request.POST:
        bc1 = request.POST.get("barcode")
        request.session["barcode"] = bc1
        request.session["barcode_part_number"] = bc1[-4:]
        request.session["barcode_part_short"] = bc1[-2:]
        request.session["route_1"] = 'barcode_check'
        return direction(request)
    else:
		form = kiosk_dispForm1()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,"kiosk/barcode_input.html",{'args':args})

def barcode_reset(request):
  b = 0
  a = '0'
  db, cur = db_set(request)

  sql = "SELECT max(scrap) FROM barcode"
  cur.execute(sql)
  tmp2 = cur.fetchall()
  tmp3 = tmp2[0]
  max_stamp = tmp3[0]
  max_stamp = max_stamp + 1

  skid = 1
  cur.execute('''INSERT INTO barcode(asset_num,scrap,skid,part) VALUES(%s,%s,%s,%s)''', (a,max_stamp,skid,b))
  db.commit()
  request.session["barcode_part"] = 0
  request.session["route_1"] = 'barcode_input'
  return direction(request)

def barcode_search(request):
    if request.POST:
        bc = request.POST.get("barcode")
        request.session["barcode"] = bc
        request.session["route_1"] = 'barcode_search_check'
        return direction(request)
    else:
		form = kiosk_dispForm1()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,"kiosk/barcode_search.html",{'args':args})

def barcode_search_check(request):
    bar1 = request.session["barcode"]
    bar1=str(bar1)
    stamp = time.time()
    part = request.session["barcode_part"]
    h = len(bar1)

    bar2 = bar1[-4:]
    len_bar1 = len(bar1)
    bar3 = bar1[:(len_bar1 - 4)]

    db, cur = db_set(request)
    # mql = "SELECT * FROM barcode WHERE asset_num = '%s'" %(bar1)
    # cur.execute(mql)
    # tmp2 = cur.fetchall()
    mql = "SELECT * FROM barcode WHERE left(asset_num,length(asset_num)-4) = '%s'" %(bar3)
    cur.execute(mql)
    tmp2 = cur.fetchall()
    
    try:
      tmp3=tmp2[0]
      tmp4=tmp3[0]
      timestamp = tmp3[2]
      dd = vacation_1(stamp)
      d = vacation_1(timestamp)
      request.session["alert_time"] = d
      request.session["now_time"] = dd
      request.session["diff_time"] = int(stamp - timestamp)
      return render(request,"barcode_search_found.html")

    except:
      dummy = 5
    return render(request,"barcode_search_clear.html")

def barcode_verify(request):
    if request.POST:
        bc = request.POST.get("barcode")
        request.session["barcode"] = bc
        request.session["route_1"] = 'barcode_verify_check'
        return direction(request)
    else:
		form = kiosk_dispForm1()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,"kiosk/barcode_verify.html",{'args':args})

def barcode_verify_check(request):
    bar1 = request.session["barcode"]
    bar1=str(bar1)
    stamp = time.time()
    part = request.session["barcode_part"]
    h = len(bar1)

    bar2 = bar1[-4:]
    len_bar1 = len(bar1)
    bar3 = bar1[:(len_bar1 - 4)]

    db, cur = db_set(request)
    mql = "SELECT * FROM barcode WHERE left(asset_num,length(asset_num)-4) = '%s'" %(bar3)
    cur.execute(mql)
    tmp2 = cur.fetchall()



    try:
      tmp3=tmp2[0]
      tmp4=tmp3[0]
      timestamp = tmp3[2]
      request.session["barcode"] = tmp3[1]

      tmp3=tmp2[1]
      tmp4=tmp3[0]
      timestamp2 = tmp3[2]
      request.session["barcode2"] = tmp3[1]


      dd = vacation_1(stamp)
      d = vacation_1(timestamp)
      d2 = vacation_1(timestamp2)

      request.session["alert_time"] = d
      request.session["alert_time2"] = d2
      request.session["now_time"] = dd
      request.session["diff_time"] = int(stamp - timestamp)
      request.session["diff_time2"] = int(stamp - timestamp2)


      return render(request,"barcode_verify_found2.html")
    
    except:

      try:
        tmp3=tmp2[0]
        tmp4=tmp3[0]
        timestamp = tmp3[2]
        dd = vacation_1(stamp)
        d = vacation_1(timestamp)
        request.session["alert_time"] = d
        request.session["now_time"] = dd
        request.session["diff_time"] = int(stamp - timestamp)
        return render(request,"barcode_verify_found1.html")

      except:
        dummy = 5

    return render(request,"barcode_verify_clear.html")


def barcode_check(request):
    bar1 = request.session["barcode"]
    bar1=str(bar1)
    stamp = time.time()
    part = request.session["barcode_part"]
    h = len(bar1)
    if len(bar1) >24:
      return render(request,"barcode_warning.html")
    if len(bar1) <22:
      if len(bar1) != 16:
        return render(request,"barcode_warning.html")
  

    db, cur = db_set(request)
    if len(bar1) == 16:
      request.session["barcode_part_number"] = '9341'
 #   try:
    
    bar2 = bar1[-4:]
    len_bar1 = len(bar1)
    bar3 = bar1[:(len_bar1 - 4)]
    

    # mql = "SELECT * FROM barcode WHERE asset_num = '%s'" %(bar1)
    mql = "SELECT * FROM barcode WHERE left(asset_num,length(asset_num)-4) = '%s'" %(bar3)
    cur.execute(mql)
    tmp2 = cur.fetchall()

    # kk = request.session["bbummy"]

    
    try:
     tmp3=tmp2[0]
     tmp4=tmp3[0]
     timestamp = tmp3[2]
     dd = vacation_1(stamp)
     d = vacation_1(timestamp)
     request.session["alert_time"] = d
     request.session["now_time"] = dd
     request.session["diff_time"] = int(stamp - timestamp)
     return render(request,"barcode_alert.html")

    except:
      dummy = 1

    part = part + 1
    skid = 1
    cur.execute('''INSERT INTO barcode(asset_num,scrap,skid,part) VALUES(%s,%s,%s,%s)''', (bar1,stamp,skid,part))
    db.commit()
    
    request.session["bar1"] = bar1
    
    request.session["barcode_part"] = part

    db.close()

    part_num = request.session["barcode_part_number"]
    part_short = request.session["barcode_part_short"]

    if part_short == "BB":
      part_num == "5214"
      request.session["barcode_part_number"] = "5214"
    if part_short == "CB":
      part_num == "3214"
      request.session["barcode_part_number"] = "3214"
    if part_num == "5214" and part == 280:
      return render(request,"barcode_complete.html")
    if part_num == "3214" and part == 280:
      return render(request,"barcode_complete.html")

    if part_num == "5401" and part == 144:
      return render(request,"barcode_complete.html")
    if part_num == "3214" and part == 280:
      return render(request,"barcode_complete.html")
    if part_num == "5214" and part == 280:
      return render(request,"barcode_complete.html")
    if part_num == "8670" and part == 40:
      return render(request,"barcode_complete.html")
    if part_num == "5404" and part == 120:
      return render(request,"barcode_complete.html")
    if part_num == "9341" and part == 112:
      
      return render(request,"barcode_complete.html")


    return render(request,"barcode_ok.html")
    
    request.session["route_1"] = 'barcode_input'
    return direction(request)

    