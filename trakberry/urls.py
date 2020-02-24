"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

from views2 import main_login, main_login_form, main, main_logout, switch_local, switch_net, main_test_init, main_login_password_lost_form
from views_machinery import machinery
from views_testing import test_display, form_robot_machine_enter, display_robot_machine, machine_list_display, toggletest, test668,create_table_1,test_datalist
from views_tech import tech, job_call, job_close, tech_logout, job_pass, tech_history, tech_history2, tech_recent, tech_recent2, tech_map, tech_tech_call, reset_call_route,tech_email_test,tech_message, modal_test
from views_tech import tech_message_close,tech_message_reply1, tech_report_email, email_hour_check,tech_name_update
#from views_tech import hour_check
from views_transfer import transfer

from mod_simulate import sim
from mod_tracking import edit_part, select_date, select_day, select_datetime, graph_gf6, graph_gf6_report
from mod_test import test_mode
from views_global_mods import test_machine_rate
from views_vacation import vacation_temp, vacation_backup, vacation_purge, vacation_purge_delete, vacation_rebuild,vacation_restore, message_create
from views_admin import retrieve
from views_db import db_select
from views_test import place_test, email_test_1, email_test_2
from views_mod1 import table_copy

# *******************************************  Testing Views *******************************************************************************************
from views_email import e_test
from views import fix_time
from views_test import test_list, toggle_1, layer_test, layer_entry, layer_transfer_temp, layer_choice_init, layer_choice, layer_select, layer_audit_check_reset
from views_test import layer_retrieve,sup_mess, test_scrap1
from views_test_email import email1, done_email_1
from views_testing import clear_login
from views_test import create_scrap_table, test_scrap_production
from test_test import table_mod1
from view_test1 import kiosk_name,update_column
# ***********************************************************************************************************************************************************


# *******************************************  Main Views *******************************************************************************************
from views import display, db_write, create_table, test, details_session, details_track, reports, test_time, scheduler, inventory, display2, fade_in, fade2
from views import create_test_table, alter_table_name, done, new, graph, graph2, graph3, graph749, graph748, graph750, graph677, ttip,graph_close, display_time, graph_close_snap
from views import graph677_snap, graph748_snap, graph749_snap, graph750_snap, display_initialize, test44, tech_reset,testB
from views2 import main_password_update
from views3 import excel_test,manpower_update
# ***********************************************************************************************************************************************************


# *******************************************  Supervisor Section ********************************************************************************************
from views_supervisor import supervisor_display, supervisor_tech_call,supervisor_elec_call,supervisor_maint_call,sup_message_close
from views_supervisor import vacation_display_jump, supervisor_edit, sup_close, employee_vac_enter, vacation_display
from views_supervisor import vacation_display_increment, vacation_display_decrement, vacation_edit, vacation_delete, sup_message_reply1,sup_message_reply0
from views_supervisor import employee_vac_enter_init, employee_vac_enter_init2, vacation_month_fix, vacation_display_initial, resetcheck,sup_message
from views_supervisor import check_email_problem
# ***********************************************************************************************************************************************************


# *******************************************  Employee Section ********************************************************************************************
from views_employee import create_matrix, emp_training_enter, emp_info_enter, emp_info_display, emp_matrix_initialize, create_jobs,emp_info_update_status
from views_employee import job_info_display, job_info_enter,matrix_info_init, matrix_update, fix_shift,matrix_info_display,matrix_info_reload,matrix_backup,rot_fix
from views_employee import job_info_update_status, job_info_delete, matrix_job_test, emp_matrix_delete, emp_matrix_rotation_fix, employee_manual_enter, emp_info_group_update
from views_employee import emp_info_absent, emp_info_enter_manual
from views_scheduler import current_schedule, set_rotation, rotation_info_display, rotation_update, schedule_set, schedule_set2, schedule_init,schedule_finalize
from views_scheduler import schedule_set2b,schedule_set3,schedule_reset_data,schedule_redisplay1, schedule_rotation_start

# ***********************************************************************************************************************************************************

# *******************************************  Maintenance App Section ********************************************************************************************
from views_maintenance import maint, maint_call, maint_pass, maint_close, maint_logout, maint_job_history, maint_map, maint_call_call
# ***********************************************************************************************************************************************************

# *******************************************  Inventory Section ********************************************************************************************
from views_inventory import push_button, inventory_type_entry, inventory_entry, inventory_fix

# ***********************************************************************************************************************************************************

# *******************************************  Kiosk Section ********************************************************************************************
from views_kiosk import kiosk,kiosk_job,kiosk_job_assign, kiosk_job_leave,kiosk_error_badjobnumber,kiosk_error_badclocknumber,kiosk_error_assigned_clocknumber
from views_kiosk import kiosk_production, kiosk_production_entry,flex_test,manual_production_entry,manual_production_entry2
from views_kiosk import entry_recent, manual_cycletime_table, tenr_fix2, tenr_fix3,kiosk_hourly_entry,kiosk_initial_9HP,kiosk_initial_6L_Output
from views_kiosk import kiosk_initial_GF9,kiosk_initial_6L_IN,kiosk_initial_AB1V, kiosk_sub_menu, kiosk_manual, kiosk_kiosk


# ***********************************************************************************************************************************************************
# *******************************************  Manpower Section ********************************************************************************************
from views_kiosk import manpower_layout, tenr_fix,kiosk_menu,ab1v_manpower,tenr1,trilobe,tenr2, error_hourly_duplicate
from views_kiosk import set_test1, kiosk_fix55, kiosk_fix44

# ***********************************************************************************************************************************************************

# ***********************************************************************************************************************************************************
# *******************************************  Management Section ********************************************************************************************
from views_production import mgmt,mgmt_login_form,mgmt_logout,mgmt_production_hourly,mgmt_production_hourly_edit, mgmt_production, mgmt_display_edit, mgmt_cycletime

from views4 import ios_test, IsDone, NotDone, target_fix1, medium_production, multidrop, scantest, target_fix1
from views4 import target_fix_5401, target_fix_5404, target_fix_5399, target_fix_5214, target_fix_3214
from views_mod1 import mgmt_display_next,mgmt_display_prev

from views_mod2 import hrly_display, butter
from views_barcode import barcode_check, barcode_input, barcode_initial, barcode_reset, barcode_search, barcode_search_check, barcode_verify, barcode_verify_check
from views_barcode import barcode_check_10R,barcode_input_10R,barcode_initial_10R



# ***********************************************************************************************************************************************************



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    # May 26,2015
    # Path for Test of single direct live tracking and then 
    # link to display.html template
	url(r'^$',main),

    
	url(r'^display/', main),
	url(r'^testB/', testB),
	url(r'^main_login/', main_login),
	url(r'^main_logout/', main_logout),
	url(r'^main_login_password_lost_form/', main_login_password_lost_form),
	url(r'^switch_local/', switch_local),
	url(r'^switch_net/', switch_net),
	url(r'^main_login_form/', main_login_form),
	url(r'^display1/', display),
	url(r'^display_initialize/', display_initialize),
	url(r'^display2/', display2),
	url(r'^test6/', test_display),
	url(r'^test668/', test668),
	url(r'^create/', test),
	url(r'^new/', new),
	
	url(r'^display_time/', display_time),
	
	url(r'^tmr/', test_machine_rate),
	url(r'^fix_shift/', fix_shift),
	url(r'^sup_message_close/', sup_message_close),
	
	url(r'^fade/', fade_in),
	url(r'^fade2/', fade2),
	url(r'^ttip/', ttip),
	
	url(r'^graph_gf6op/get/(?P<index>\d+)/$', graph_gf6),
	
	url(r'^graph_gf6_report/get/(?P<index>\w{0,50})/$', graph_gf6_report),
	#url(r'^graph_gf6_report/get/(?P<index>\d+)/$', graph_gf6_report),
	
	url(r'^graph/', graph),
	url(r'^graph2/', graph2),
	url(r'^graph3/', graph3),
    url(r'^db_write/', db_write),  
	url(r'^sim/', sim),	
	url(r'^test/', test),
	url(r'^sup_mess/', sup_mess),	
	url(r'^done/', done),
	url(r'^details_session/', details_session),
	url(r'^details_track/', details_track),
	url(r'^main/', main),
	url(r'^tech_reset/', tech_reset),
	url(r'^tech_email_test/', tech_email_test),
	url(r'^done_email_1/', done_email_1),
	url(r'^tech_message_close/', tech_message_close),
	url(r'^tech_message_reply1/', tech_message_reply1),
	url(r'^email_hour_check/', email_hour_check),
	url(r'^modal_test/', modal_test),	
	
	# Reports URL Patterns ***********************************
	url(r'^reports/', select_date),
	url(r'^reports_day/', select_day),
	url(r'^reports_snapshot/', select_datetime),
	# ********************************************************
	
	# Reports URL Patterns for Vacations ***********************************
	url(r'^employee_vacation_enter/', employee_vac_enter),
	url(r'^employee_vacation_enter_init2/', employee_vac_enter_init2),
	url(r'^employee_vacation_enter_init/get/(?P<index>\d+)/$', employee_vac_enter_init),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^employee_manual_enter/', employee_manual_enter),
	url(r'^emp_info_enter_manual/', emp_info_enter_manual),
	url(r'^emp_info_group_update/', emp_info_group_update),
	url(r'^matrix_backup/', matrix_backup),
	url(r'^vacation_display/', vacation_display),
	url(r'^vacation_display_jump/', vacation_display_jump),
	url(r'^vacation_display_increment/', vacation_display_increment),
	url(r'^vacation_display_decrement/', vacation_display_decrement),
	url(r'^vacation_edit/get/(?P<index>\d+)/$', vacation_edit),
	url(r'^vacation_delete/', vacation_delete),
	url(r'^vacation_display_initial/', vacation_display_initial),
	url(r'^vacation_backup/', vacation_backup),
	url(r'^message_create/', message_create),
	url(r'^vacation_rebuild/', vacation_rebuild),
	url(r'^vacation_restore/', vacation_restore),
	url(r'^vacation_purge/', vacation_purge),
	url(r'^vacation_purge_delete/', vacation_purge_delete),
	url(r'^vacation_month_fix/', vacation_month_fix),
	url(r'^resetcheck/', resetcheck),
	# ********************************************************	
	
	url(r'^machinery/', machinery),
	url(r'^test_time/', test_time),
	url(r'^scheduler/', scheduler),
	url(r'^inventory/', inventory),
	url(r'^testdb/', create_test_table),
	url(r'^edit/', edit_part),
	url(r'^create_table_1/', create_table_1),
	url(r'^test44/', test44),
	
	url(r'^graph_gf6/get/(?P<index>\w{0,50})/$', graph_gf6),
	
	url(r'^check_email_problem/', check_email_problem),

	#url(r'^graph_gf6/get/(?P<index>\d+)/$', graph_gf6),
	
	url(r'^graph749/', graph749),
	url(r'^graph748/', graph748),
	url(r'^graph750/', graph750),
	url(r'^graph677_snap/', graph677_snap),
	url(r'^graph748_snap/', graph748_snap),
	url(r'^graph749_snap/', graph749_snap),
	url(r'^graph750_snap/', graph750_snap),
	url(r'^graph677/', graph677),
	url(r'^graph_close/', graph_close),
	url(r'^graph_close_snap/', graph_close_snap),
	url(r'^test_var/', test_mode),
	url(r'^tech/', tech),
	url(r'^sup/', supervisor_display),
	url(r'^sup_down_tech/', supervisor_tech_call),
	url(r'^sup_close/', sup_close), 
	url(r'^transfer/', transfer),
	url(r'^reset_call_route/', reset_call_route),
	url(r'^sup_down_elec/', supervisor_elec_call),
	url(r'^sup_down_maint/', supervisor_maint_call),
	url(r'^sup_message_reply1/', sup_message_reply1),
	url(r'^sup_message_reply0/', sup_message_reply0),
	url(r'^sup_message/', sup_message), 
	#url(r'^sup_down_main/', supervisor_main_call),
	#url(r'^sedit/get/(?P<index>\d+)/$', supervisor_edit),
	url(r'^sedit/', supervisor_edit),
	url(r'^alter/', alter_table_name),
	url(r'^tech_logout/', tech_logout),
	url(r'^jcall/get/(?P<index>\d+)/$', job_call),
	url(r'^jclose/get/(?P<index>\d+)/$', job_close),
	url(r'^jpass/get/(?P<index>\d+)/$', job_pass),
	url(r'^tech_history/', tech_history),
	url(r'^tech_history2/', tech_history2),
	
	url(r'^tech_recent/', tech_recent),
	url(r'^tech_recent2/', tech_recent2),
	url(r'^tech_tech_call/', tech_tech_call),
    url(r'^tech_map/', tech_map),
    url(r'^tech_message/', tech_message),	
	url(r'^tech_report_email/', tech_report_email),
	url(r'^tech_name_update/', tech_name_update),
	url(r'^main_password_update/', main_password_update),
	
	# **************  Maintenance Section ***************************************
	url(r'^maint/', maint),
	url(r'^maint_map/', maint_map),
	url(r'^mcall/get/(?P<index>\d+)/$', maint_call),
	url(r'^mclose/get/(?P<index>\d+)/$', maint_close),
	url(r'^mpass/get/(?P<index>\d+)/$', maint_pass),
	url(r'^maint_logout/', maint_logout),
	url(r'^maintenance/', maint_logout),
	url(r'^maint_job_history/', maint_job_history),
	url(r'^maint_call_call/', maint_call_call),
	
	
	# **************  Employee Section ***************************************
	url(r'^create_matrix/', create_matrix),
	url(r'^create_jobs/', create_jobs),
	url(r'^emp_training_enter/', emp_training_enter),
	url(r'^emp_info_delete/get/(?P<index>\w{0,50})/$', emp_info_update_status),
	url(r'^emp_info_absent/get/(?P<index>\w{0,50})/$', emp_info_absent),
	url(r'^emp_info_enter/', emp_info_enter),
	url(r'^rot_fix/', rot_fix),
	url(r'^emp_info_display/', emp_info_display),
	url(r'^emp_matrix_delete/', emp_matrix_delete),
	url(r'^emp_matrix_initialize/', emp_matrix_initialize),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^job_info_delete/', job_info_delete),
	url(r'^job_info_display/', job_info_display),
	url(r'^job_info_enter/', job_info_enter),
	url(r'^job_info_update_status/get/(?P<index>\w{0,50})/$', job_info_update_status),
	url(r'^matrix_info_init/', matrix_info_init),
	url(r'^matrix_info_display/', matrix_info_display),
	url(r'^matrix_info_reload/', matrix_info_reload),
	url(r'^training_matrix/get/(?P<index>\d+)/$', matrix_update),
	
	url(r'^matrix_job_test/', matrix_job_test),
	url(r'^current_schedule/', current_schedule),
	url(r'^set_rotation/', set_rotation),
	url(r'^rotation_info_display/', rotation_info_display),
	url(r'^rotation_matrix/get/(?P<index>\d+)/$', rotation_update),
	                # *******  Scheduling Section   **********
	url(r'^schedule_set/', schedule_set),
	url(r'^schedule_rotation_start/', schedule_rotation_start),
	url(r'^schedule_finalize/', schedule_finalize),
	url(r'^schedule_set2b/', schedule_set2b),
	url(r'^schedule_redisplay1/', schedule_redisplay1),
	#url(r'^schedule_add_job/get/(?P<index>\w{0,50})/$', schedule_add_job),
	
	#url(r'^tech/get/complete/(?P<index>\d+)/$', complete),
	
	
	# ************************************************************************
	
	# **************  Testing Section ***************************************
	url(r'^main_test_init/', main_test_init),   
	url(r'^email_test_1/', email_test_1),
	url(r'^email_test_2/', email_test_2),
	url(r'^email1/', email1),
	url(r'^target_fix1/', target_fix1),
	url(r'^target_fix_5401/', target_fix_5401),
	url(r'^target_fix_5404/', target_fix_5404),
	url(r'^target_fix_5399/', target_fix_5399),
	url(r'^target_fix_5214/', target_fix_5214),
	url(r'^target_fix_3214/', target_fix_3214),
	url(r'^multidrop/', multidrop),
	url(r'^scantest/', scantest),

	url(r'^ios_test/', ios_test),
	url(r'^medium_production/', medium_production),
	url(r'^IsDone/', IsDone),
	url(r'^NotDone/', NotDone),
	
	url(r'^form_robot_machine_enter/', form_robot_machine_enter),
	url(r'^display_robot_machine/', display_robot_machine),
	url(r'^machine_list_display/', machine_list_display),
	url(r'^e_test/', e_test),
	url(r'^db_select/', db_select),
	url(r'^place_test/', place_test),
	url(r'^schedule_init/', schedule_init),
	url(r'^schedule_set2/', schedule_set2),
	url(r'^schedule_set3/', schedule_set3),
	url(r'^schedule_reset_data/', schedule_reset_data),
	url(r'^table_copy/', table_copy),
	# Test for correcting timestamp issues on tracking data
	url(r'^fix_time/', fix_time),
	url(r'^test_list/', test_list),
	url(r'^test_datalist/', test_datalist),
	url(r'^toggle_1/', toggle_1),
	url(r'^layer_test/', layer_test),
	url(r'^layer_entry/', layer_entry),
	url(r'^layer_transfer_temp/', layer_transfer_temp),
	
	url(r'^layer_choice/', layer_choice),
	url(r'^layer_select/', layer_select),
	url(r'^layer_audit_check_reset/', layer_audit_check_reset),
	url(r'^layer_retrieve/get/(?P<index>\d+)/$', layer_retrieve),
	url(r'^clear_login/', clear_login),
	url(r'^create_scrap_table/', create_scrap_table),
	url(r'^test_scrap_production/', test_scrap_production),
	url(r'^test_scrap1/', test_scrap1),
	url(r'^excel_test/', excel_test),
	url(r'^manpower_update/', manpower_update),
	url(r'^table_mod1/', table_mod1),
	url(r'^kiosk_name/', kiosk_name),
	url(r'^update_column/', update_column),
#	url(r'^hour_check/', hour_check),

	
	# ************************************************************************
	
	# **************  Kiosk Section ***************************************
	url(r'^kiosk/', kiosk),
	url(r'^set_test1/', set_test1),
	url(r'^flex_test/', flex_test),
	url(r'^kiosk_job/', kiosk_job),
	url(r'^kiosk_production/', kiosk_production),
	url(r'^kiosk_job_assign/', kiosk_job_assign),
	url(r'^kiosk_error_badjobnumber/', kiosk_error_badjobnumber),
	url(r'^kiosk_error_badclocknumber/', kiosk_error_badclocknumber),
	url(r'^kiosk_error_assigned_clocknumber/', kiosk_error_assigned_clocknumber),
	url(r'^kiosk_job_leave/', kiosk_job_leave),
	url(r'^kiosk_production_entry/', kiosk_production_entry),
	url(r'^kiosk_hourly_entry/', kiosk_hourly_entry),
	url(r'^error_hourly_duplicate/', error_hourly_duplicate),
	url(r'^kiosk_menu/', kiosk_menu),
	url(r'^kiosk_sub_menu/', kiosk_sub_menu),
	url(r'^tenr1/', tenr1),
	url(r'^kiosk_fix55/', kiosk_fix55),
	url(r'^kiosk_fix44/', kiosk_fix44),
	url(r'^kiosk_manual/', kiosk_manual),
	url(r'^kiosk_kiosk/', kiosk_kiosk),

	url(r'^tenr2/', tenr2),
	url(r'^trilobe/', trilobe),
	url(r'^kiosk_initial_9HP/', kiosk_initial_9HP),
	url(r'^kiosk_initial_6L_Output/', kiosk_initial_6L_Output),
	url(r'^kiosk_initial_6L_IN/', kiosk_initial_6L_IN),
	url(r'^kiosk_initial_GF9/', kiosk_initial_GF9),
	url(r'^kiosk_initial_AB1V/', kiosk_initial_AB1V),
	url(r'^trilobe/', trilobe),
	url(r'^manual_production_entry/', manual_production_entry),
	url(r'^manual_production_entry2/', manual_production_entry2),
	url(r'^entry_recent/', entry_recent),
	url(r'^tenr_fix/', tenr_fix),
	url(r'^tenr_fix2/', tenr_fix2),
	url(r'^tenr_fix3/', tenr_fix3),
	url(r'^manual_cycletime_table/', manual_cycletime_table),
	url(r'^ab1v_manpower/', ab1v_manpower),

	# ************************************************************************
		# **************  Manpower Section ***************************************
	url(r'^manpower_layout/', manpower_layout),

	# ************************************************************************


		# **************  Management Section ***************************************
	url(r'^mgmt/', mgmt),
	url(r'^mgmt_login_form/', mgmt_login_form),
	url(r'^mgmt_logout/', mgmt_logout),
	url(r'^mgmt_production_hourly/', mgmt_production_hourly),
	url(r'^mgmt_production/', mgmt_production),
	url(r'^mgmt_cycletime/', mgmt_cycletime),
	url(r'^mgmt_production_hourly_edit/get/(?P<index>\d+)/$', mgmt_production_hourly_edit),
	url(r'^mgmt_display_edit/get/(?P<index>\d+)/$', mgmt_display_edit),
	url(r'^mgmt_display_next/', mgmt_display_next),
	url(r'^mgmt_display_prev/', mgmt_display_prev),

	# ************************************************************************


	# Retrieve Data from ADMIN views for testing
	url(r'^retrieve/', retrieve),
	url(r'^create_table/', create_table),
	
	
	url(r'^push_button/', push_button),
	url(r'^inventory_type_entry/', inventory_type_entry),
	url(r'^inventory_entry/', inventory_entry),
	url(r'^inventory_fix/', inventory_fix),

	# **************  Mod2 Section ***************************************
	url(r'^hrly_display/', hrly_display),
    url(r'^butter/', butter),

	# *************  Barcode *********************************************
	url(r'^barcode_input/', barcode_input),
	url(r'^barcode_check/', barcode_check),
	url(r'^barcode_initial/', barcode_initial),
	url(r'^barcode_reset/', barcode_reset),
	url(r'^barcode_search/', barcode_search),
	url(r'^barcode_search_check/', barcode_search_check),
	url(r'^barcode_verify/', barcode_verify),
	url(r'^barcode_verify_check/', barcode_verify_check),
	url(r'^barcode_input_10R/', barcode_input_10R),
	url(r'^barcode_check_10R/', barcode_check_10R),
	url(r'^barcode_initial_10R/', barcode_initial_10R),

	
]
 
