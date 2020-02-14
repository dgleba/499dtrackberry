#******************************************************************************************************************
#***************  MODULE 1 CONTAINING REPEATED ALGORITHMS  ********************************************************
#******************************************************************************************************************

from mysite.myapp.models import main, temp1

# *****************************************************************************************************************
#****  Used to formulate the Job Training Matrix  *****************************************************************
def matrix_set(D):
    job = main.objects.order_by('name').filter(tpe='column').filter(db=D).values('name').distinct()
    emj = main.objects.order_by('name', 'entry').filter(tpe='row').filter(db=D).values('name','entry').distinct()
    emp = main.objects.filter(tpe='row').filter(db=D).order_by('name').values('name').distinct()
    b='2'
    a='X'
    d='Z'
    nmme=[]
    mach=[]
    lname=[]
    lmach=[]
    res=[]
    for i in emp:
        nmme.append(i['name'])
    for j in job:
        mach.append(j['name'])
    for k in emj:
        lname.append(k['name'])
        lmach.append(k['entry'])

    for i in range(len(nmme)):
        res.append(nmme[i])
        for j in range(len(mach)):
            c = 'false'
            for k in range(len(lname)):
                if (lname[k] == nmme[i]) and (lmach[k] == mach[j]):
                    g='X'
                    res.append(g)
                    c = 'true'
            if c == 'false':
                g='Z'
                res.append(g)
        g='2'
        res.append(g)

    return job, emj, emp, res, a, b, d, mach
