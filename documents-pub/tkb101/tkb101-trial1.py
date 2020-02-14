#!/usr/bin/python

import RPi.GPIO as GPIO
import MySQLdb as mdb
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Assign GPIO number for both buttons 
button = 14
s_button = 15

Machine_Num = "662"


# Initialize buttons
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(s_button, GPIO.IN, GPIO.PUD_UP)

#Open Database connection
con = mdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdbtest');

#Set start variables 
vr = 0
st_time=int(time.time())

#Begin Loop
while vr <1:
    #Do if 1st button is depressed
    if GPIO.input(button) == 0:
        fi_time = int(time.time())
        if (fi_time - st_time)<3:
            print("TOO SOON")
        else:
	    print("writing to MySQL")
	    print(fi_time)
	    with con:
		cur = con.cursor()
		cur.execute('''INSERT INTO Trial_1(Machine, UTime) VALUES(%s, %s)''', (Machine_Num,fi_time))	
          
        st_time = fi_time
        time.sleep(0.09)

    #Break Loop if 2nd button is hit
    if GPIO.input(s_button) == 0:
        vr = 1
 
GPIO.cleanup()






    