from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_routes import direction
from views_mod1 import kiosk_lastpart_find, kiosk_email_initial, find_current_date
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current7, vacation_set_current6, vacation_set_current5
import smtplib
from smtplib import SMTP

def hrly_display(request):   # This will return a tuple with hourly prod summary on last hour for each p_cell
    
    hourly = ['' for x in range(0)]
    hourly_var = ['' for x in range(0)]
    ert = ['' for x in range(0)]
    xx = ['' for x in range(0)]
    hourly_all = ['' for x in range(0)]

    red_block = '#ff0000'
    green_block = '#62c12e'
    yellow_block = '#faff2b'
    grey_block = '#a5a4a4'
    hhh = 3
    

    email_hour_check2(request)



    current_first, shift1, shift2, shift3, hour_curr  = vacation_set_current7()
    db, cur = db_set(request)  
    s1 = "SELECT p_cell FROM sc_prod_hr_target"  # Set the p_cell value we'll use to iterate through for each cell
    cur.execute(s1)
    tmp = cur.fetchall()
    p_cell = tmp[0]
    row_ctr = 1
    for i in tmp:
        c1 = 0
        c2 = 0
        pc = i[0]
        try:
                aql = "SELECT MAX(id) FROM sc_prod_hour where p_cell = '%s'" %(pc) # Set the max_id to get p_cell latest entry
                cur.execute(aql)
                tmp3 = cur.fetchall()
                tmp4 = tmp3[0]
                max_id = tmp4[0]
                
        except:
                route = 'Filed'
        try:
                bql = "Select * From sc_prod_hour where id = '%s'" %(max_id) # Get latest entry for p_cell
                cur.execute(bql)
                tmp3 = cur.fetchall()
                tmp4 = tmp3[0]
                ert.append(tmp4)
                c1 = int((float(tmp4[8])/float(tmp4[7]))*100)  # Calculate the % for Hourly
                c2 = int((float(tmp4[10])/float(tmp4[9]))*100) # Calculate the % for Shift Total
                if c1 > 84:        # Below determins d1 and d2 to signify colour  red, yellow, green
                        d1 = green_block
                elif c1 > 69:
                        d1 = yellow_block
                else:
                        d1 = red_block
                if c2 > 84:
                        d2 = green_block
                elif c2 > 69:
                        d2 = yellow_block
                else:
                        d2 = red_block
                ctr = 0
                s1 = 1
                s2 = 2
                s3 = 0
                s4 = 4
                d11 = 99
                hourly_var.append(str(tmp4[4]))
                if int(tmp4[6]) != (hour_curr-1):
                        d1 = grey_block 
                        c1 = '---'
                if (str(tmp4[4])) != str(current_first):
                        d2 = grey_block
                        d1 = grey_block
                        c1 = '---'
                        c2 = '---'
                elif (tmp4[5]) != shift1:
                        if (tmp4[5]) != shift2:
                                if (tmp4[5]) != shift3:
                                        d2 = grey_block
                                        d1 = grey_block
                                        c1 = '---'
                                        c2 = '---'

                new_line = row_ctr % hhh # uses Mod of hhh to determine how many on a line.   hhh is the number on a line

                #yyt = vacation_set_current6(tmp[4])

                # new code
                lst = list(tmp4)
                d3 = d2 + ' 60%,' + d1 + ' 40%' # combines the two colors together to d3 format 
                lst.extend((c2,d2,c1,d1,d3,new_line,tmp[4]))
                mst=tuple(lst)
                xx.append(mst)
                row_ctr = row_ctr + 1

        except:
                dummy = 1

    db.close()

    current_first, shift1, shift2, shift3, hour_curr  = vacation_set_current7()
    request.session["variableA"] = current_first
    request.session["variableB"] = shift1
    request.session["variableC"] = shift2
    request.session["variableD"] = hourly_var
    request.session["variableE"] = hour_curr

    # This is where you return the value 'hourly' which has all the data needed in tuple form
    return render(request,'production/hrly_display.html', {'tmpp':xx})	


def butter(request):
    email_hour_check2(request)
    return render(request,'done_test.html')

def email_hour_check2(request):

    h1 = 7
    h2 = 15
    h3 = 23
    h4 = 17
    m1 = 15
    m2 = 30
    m3 = 45
    ch = 0
    t=int(time.time())
    tm = time.localtime(t)
    mn = tm[4]
    hour = tm[3]
    if hour == h1:
        if mn > m1 and mn < m2:
            ch = 1
    if hour == h2:
        if mn > m1 and mn < m2:
            ch = 1
    if hour == h3:
        if mn > m1 and mn < m2:
            ch = 1
    if hour == h4:
        if mn > m2 and mn < m3:
            ch = 1
    
    if ch != 1:
        return

    # Define Variables
    production_check = 2
    manual_check = 0
    manual_set = 1
    production_set = 1
    reason1 = "Missed Kiosk Entries"
    reason2 = "Low Production"
    db, cursor = db_set(request)
    # db, cursor = kiosk_email_initial(request) # This Check will ensure the new columns are in and if not will add them
    # sql = "SELECT * FROM sc_production1 where low_production = '%d'" %(production_check)
    # cursor.execute(sql)
    # tmp = cursor.fetchall()
    # tmp2 = tmp[0]
    # email_manual1(tmp,reason1)
    try:
        zql = "SELECT * FROM sc_production1 where low_production = '%d'" %(production_check)
        cursor.execute(zql)
        zmp = cursor.fetchall()
        tmp2 = zmp[0]
        email_manual1(zmp,reason2)
        zql = ('update sc_production1 SET low_production = "%d" WHERE low_production = "%d"' % (production_set, production_check))
        cursor.execute(zql)
        db.commit()
    except:
        dummy = 0
    try:
        sql = "SELECT * FROM sc_production1 where manual_sent = '%d'" %(manual_check)
        cursor.execute(sql)
        tmp = cursor.fetchall()
        tmp2 = tmp[0]
        email_manual1(tmp,reason1)
        sql = ('update sc_production1 SET manual_sent = "%d" WHERE manual_sent = "%d"' % (manual_set, manual_check))
        cursor.execute(sql)
        db.commit()
    except:
        dummy = 0

    db.close()
    return 

def email_manual1(tmp,reason):
    db, cursor = db_open()
    b = "\r\n"
    ctr = 0
    message_subject = reason
    message = ""
    #toaddrs = ["sbrownlee@stackpole.com,jmcmaster@stackpole.com","dmiller@stackpole.com","dclark@stackpole.com","sherman@stackpole.com","pmurphy@stackpole.com","ghundt@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","mclarke@stackpole.com","gharvey@stackpole.com","rstanley@stackpole.com","nkleingeltink@stackpole.com"]
    toaddrs = ["dclark@stackpole.com"]
    
    fromaddr = 'stackpole@stackpole.com'
    frname = 'Dave'
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('StackpolePMDS@gmail.com', 'stacktest6161')
    message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
    message = message + message_subject + "\r\n\r\n" + "\r\n\r\n"
    # message = message + "Name" + " || " + "Job" + " || " + "Count" + " || " + "Target" + " || " + "Date          " + " || " + "Shift" + b + b
    # message = message + " --------------------------------------------------------------------------------" + b
    # message = message + str(tmp)
    # h = 6 / 0
    for x in tmp:
        nm = (str(x[9]))
        # nm = int(nm)
        try:
            zql = "SELECT * FROM tkb_users where Clock = '%s'" %(nm)
            cursor.execute(zql)
            zmp = cursor.fetchall()
            zzmp = zmp[0]
            nm = zzmp[2]
        except:
            nm = "Clock " + str(x[9])


        a1 = "Name:"+nm
        a2 = "Job:"+str(x[1])
        a3 = "Count:"+str(x[4])
        a4 = "Target:"+str(x[13])
        a5 = "Date:"+str(x[10])
        a6 = "Shift:"+str(x[11])

        # a1 = string_make(str(x[9]),7)
        # a2 = str(x[1])
        # a3 = string_make(str(x[4]),7)
        # a4 = string_make(str(x[13]),8)
        # a5 = str(x[10])
        # a6 = str(x[11])
        # a7 = str(ctr)
        ctr = ctr + 1
        b = "\r\n"
        message = message + a1 + "  " + a2 + "  " + a3 + "  " +  a4 + "  " +  a5 + "  " +  a6  + b + b
        # message = message + x[8] + " " + x[1] + " " + x[4] + ":" + x[3] + " " + "\r\n\r\n"
        m_ctr = 4

    server.sendmail(fromaddr, toaddrs, message)
    server.quit()
    db.close()
    return

def string_make(x,n):
    while True:
        if len(x) >= n:
            break
        x = x + " "
    return x

    

