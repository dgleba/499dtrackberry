from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import inventory_entry_Form, inventory_count_Form
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_email import e_test
from views_supervisor import supervisor_tech_call
from trakberry.views_testing import part_list_display, cust_list_display
import MySQLdb
import time
import datetime
from django.core.context_processors import csrf
import smtplib
from smtplib import SMTP
from django.template.loader import render_to_string  #To render html content to string
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import shutil
import os

def push_button(request):
	pathX = r'/home/file/import1/Inventory'
	#pathX = r'C:/Hello/HelloWorld'  
	print os.path.dirname(pathX) 
	
	shutil.copy2('test.txt', '/importedxls/test.txt') # complete target filename given
	return render(request, "push_button.html")
	

def inventory_type_entry(request):	

	if request.POST:
        			
		part = request.POST.get("inventory_part")
		storage = request.POST.get("inventory_storage")
		customer = request.POST.get("inventory_customer")
		qty = request.POST.get("inventory_qty")
		
		request.session['inventory_part'] = part
		request.session['inventory_storage'] = storage
		request.session['inventory_customer'] = customer
		request.session['inventory_qty'] = qty


		db, cur = db_set(request)
		
		try:
			sql2 = "SELECT * from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s' and Customer = '%s'" % (part, storage,customer)
			cur.execute(sql2)
			tmp = cur.fetchall()
			tmp2 = tmp[0]

			return render(request,'done_inventory_fixed.html')
		except:
			cur.execute('''INSERT INTO tkb_inventory_fixed(Part,Storage,Customer,Quantity) VALUES(%s,%s,%s,%s)''', (part,storage,customer,qty))
			db.commit()
			return render(request,'done_inventory_fixed.html')
			
		#cur.execute('''INSERT INTO tkb_audits(Type,Part,Op,Department,Description) VALUES(%s,%s,%s,%s,%s)''', (dept,part,op,pl,desc))
		#db.commit()
		db.close()
		
		return render(request,'temp_inventory.html')
		
	else:
		form = inventory_entry_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'entry_fixed.html', {'args':args})


def inventory_fix(request):
	db, cur = db_set(request)
	sql = "SELECT * from tkb_inventory_fixed" 
	cur.execute(sql)
	tmp = cur.fetchall()
	
	for i in tmp:
		if i[2] != "Green" and i[2] != "Blue" and i[2] != "Cart":
			iid = i[0]
			h = "Final"
			sql2 = ('update tkb_inventory_fixed SET Storage="%s" WHERE Id ="%s"' % (h, iid))
			cur.execute(sql2)
			db.commit()
	return render(request,'done_test.html')

def inventory_entry1(request):
	tmp = part_list_display()
	
def inventory_entry(request):	
	tmp = part_list_display()
	c_tmp = cust_list_display()
	if request.POST:
		u = 3
		customer = ''
		T = int(time.time())
		part = request.POST.get("Part")
		op = request.POST.get("Op")
		final = request.POST.get("Final")
		customer = request.POST.get("Customer")
		blue = request.POST.get("Blue")
		green = request.POST.get("Green")
		cart = request.POST.get("Cart")
		wire = request.POST.get("Wire")
		quantity = request.POST.get("Quantity")
		try:
			final = int(final)
		except:
			final = 0
		try:	
			blue = int(blue)
		except:
			blue = 0
		try:
			green = int(green)
		except:
			green = 0
		try:
			cart = int(cart)
		except:
			cart = 0	
		try:
			wire = int(wire)
		except:
			wire = 0		
		try:
			q = int(quantity)
		except:
			q = 0
			
		# Update Inventory
		db, cur = db_set(request)
		
		
		if final > 0:
			storage = "Final"
			sql1 = "SELECT Quantity from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s' and Customer ='%s'" % (part, storage, customer)
			cur.execute(sql1)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			ht = int(tmp2[0])
			q = q + (final * ht)

		if blue > 0:
			storage = "blue"
			sql2 = "SELECT Quantity from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s'" % (part, storage)
			cur.execute(sql2)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			ht = int(tmp2[0])
			q = q + (blue * ht)
			
		if green > 0:
			storage = "green"
			sql3 = "SELECT Quantity from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s'" % (part, storage)
			cur.execute(sql3)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			ht = int(tmp2[0])
			q = q + (green * ht)
		
		if cart > 0:
			storage = "cart"
			sql4 = "SELECT Quantity from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s'" % (part, storage)
			cur.execute(sql4)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			ht = int(tmp2[0])
			q = q + (cart * ht)	
		
		if wire > 0:
			storage = "wire"
			sql4 = "SELECT Quantity from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s'" % (part, storage)
			cur.execute(sql4)
			tmp = cur.fetchall()
			tmp2 = tmp[0]
			ht = int(tmp2[0])
			q = q + (wire * ht)	
			
			
		cur.execute('''INSERT INTO tkb_inventory_ops(Timestamp,Part,Customer,Op,Final,Blue,Green,Cart,Wire,Quantity,Count_Update) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (T,part,customer,op,final,blue,green,cart,wire,q,u))
		db.commit()
		db.close()
		return render(request,'done_inventory_entry.html')
	
	else:
		form = inventory_count_Form()
		
	
	
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	#return render(request, "test992.html", {'X':tmp})
	aa = 1
	bb = 0
	return render(request,'inventory_count_form.html', {'List':tmp,'LList':c_tmp,'aa':aa,'bb':bb,'args':args})
	

	
	
		

