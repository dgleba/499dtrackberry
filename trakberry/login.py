# **** Log in ****
def login(request):
    if request.POST:
        form = Members_Login_Form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            db = form.cleaned_data['DB']
            pwd = form.cleaned_data['password']
            #form.save()
            if Members.objects.filter(DB = db).filter(user = user).filter(password = pwd).count()<>1:
                return render(request,'/dashboard_fail.html')
            else:
                m = Members.objects.get(user = user, DB = db)
                if m.type == 'admin':
                    tp = "Administrator"
                else:
                    tp = 'User'
                if user == 'kodi':
                    request.session["active_type"] = "Guest"
                    request.session["active_user"] = user
                    request.session["active_admin"] = "Guest"
                    
                    
                    return render(request,'dashboard_main_kodi.html')
					
		else:	
		    request.session["active_type"] = tp
		    request.session["active_user"] = user
		    request.session["active_db"] = db
		    request.session["active_admin"] = "Administrator"
		    a, w = members_features_list(db)
                
		    return render(request,'dashboard_main.html',{'A':a, 'W':w})
    else:
        form = Members_Login_Form()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,'login.html', args)
