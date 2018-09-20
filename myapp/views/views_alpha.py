from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.model.models_alpha import *

# Create your views here.
@csrf_exempt
def preg(request):
    return render(request, 'patientReg.html')

@csrf_exempt
def dreg(request):
    return render(request, 'addDoctor.html')

@csrf_exempt
def hreg(request):
    return render(request, 'addHospital.html')

@csrf_exempt
def patientlog(request):
    return render(request, 'patientLogin.html')

@csrf_exempt
def hospitalog(request):
    return render(request, 'hospitalLogin.html')

@csrf_exempt
def doctorlog(request):
    return render(request, 'doctorLogin.html')

@csrf_exempt
def forgotpass(request):
    return render(request, 'forgotpass.html')

@csrf_exempt
def hforgotpass(request):
    return render(request, 'h_forgotpass.html')

@csrf_exempt
def dforgotpass(request):
    return render(request, 'd_forgotpass.html')

@csrf_exempt
def patient_dashboard(request):
    return render(request, 'patientDashboard.html')

@csrf_exempt
def patientreg(request):
    if request.method == "POST":        
        p_name = request.POST["pname"]
        p_mob = request.POST["pmob"]
        p_add = request.POST["padd"]
        p_email = request.POST["pemail"]
        p_pass = request.POST["pass"]
        
        checkUser = checkUserExists(p_email)
        
        if checkUser > 0:
            return render(request, 'patientReg.html', {"error":"Patient record already exists"})
        else:
            myfile = request.FILES['pimg']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            
            rid = patientregModel(p_name, p_mob, p_add, p_email, p_pass, uploaded_file_url)
            #return HttpResponse(rid)
            return render(request, 'patientReg.html', {"message":"Patient registered successfully"})
    
@csrf_exempt
def docreg(request):
    if request.method == "POST":
        
        d_name = request.POST["dname"]
        d_con = request.POST["dcon"]
        d_spcl = request.POST["dspcl"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]
        
        checkDoctor1 = checkDoctor(email)
        
        if checkDoctor1 > 0:
            return render(request, 'addDoctor.html', {"error":"Record already exists"})
        else:
            myfile = request.FILES['dimg']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            
            docregModel(d_name, d_con, d_spcl, address, email, password, uploaded_file_url)
            
            return render(request, 'addDoctor.html', {"message":"Record created successfully"})

@csrf_exempt
def hospitalreg(request):
    if request.method == "POST":
        h_name = request.POST["hname"]
        h_add = request.POST["hadd"]
        h_email = request.POST["hemail"]
        h_pass = request.POST["hpass"]
        h_sec = request.POST["hsecurity"]
        h_ans = request.POST["hans"]
        rid = hospitalregModel(h_name, h_add, h_email, h_pass, h_sec, h_ans)
        return HttpResponse(rid)
    
@csrf_exempt
def patientlogin(request):
    user = request.POST["username"]
    password = request.POST["pas"]
    
    checkuserExist = p_checkuserModel(user, password)

    if checkuserExist >= 1:
        
        getPatientDetails = getPatientDetailModel(user)
                
        request.session['patient_user_name'] = user
        request.session['patient_id'] = getPatientDetails["id"]
        
        return HttpResponseRedirect('/p_dashboard/')
    else:
        return render(request, 'patientLogin.html', {"error":"User does not exist"})

@csrf_exempt
def p_dashboard(request):
    userName = request.session['patient_user_name']
    patient_id = request.session['patient_id']

    if 'patient_user_name' in request.session:
        
        return render(request, 'patientDashboard.html', {"appt_list":getAppointmentDetailsModel(patient_id)})
    else:
        return HttpResponseRedirect('/patientlog/')
    
@csrf_exempt
def patientlogout(request):
    del request.session['patient_user_name']
    return HttpResponseRedirect('/patientlog/')

@csrf_exempt
def hospitalogin(request):
    user = request.POST["username"]
    password = request.POST["pas"]
    checkuserExist = h_checkuserModel(user, password)

    if checkuserExist >= 1:
        request.session['user_name'] = user
        return HttpResponseRedirect('/h_dashboard/')
    else:
        return render(request, 'hospitalLogin.html', {"message":"User does not exist"})

@csrf_exempt
def h_dashboard(request):
    userName = request.session['user_name']

    if 'user_name' in request.session:
        return render(request, 'dashboard.html', {"user_name":userName})
    else:
        return HttpResponseRedirect('/hospitalog/')

@csrf_exempt
def hospitalogout(request):
    del request.session['user_name']
    return HttpResponseRedirect('/hospitalog/')

#patient
@csrf_exempt
def p_confirm(request):
    user = request.POST["username"]
    checkuserExist = pf_checkuserModel(user)

    if checkuserExist >= 1:
        request.session['patient_user_name'] = user
        return HttpResponseRedirect('/p_editpass/')
    else:
        return render(request, 'patientLogin.html', {"error":"User does not exist"})

@csrf_exempt
def p_editpass(request):
    return render(request, 'changePass.html')

@csrf_exempt
def p_changepass(request):
    if request.method == "POST":
        p_password = request.POST["pass"]
        username = request.session['patient_user_name']
        p_updatepassModel(p_password, username)
        return render(request, 'changePass.html', {"message":"Your password has been changed successfully"})

@csrf_exempt
def appointments(request):
    doc_list = doc_listModel()
    return render(request, 'appointments.html', {"data1":doc_list})

@csrf_exempt
def bookappointment(request):
    if request.method == "POST":
        d_name = request.POST["doctorname"]
        date = request.POST["date"]
        time = request.POST["time"]
        reason = request.POST["reason"]
        description = request.POST["description"]
        username = request.session['patient_id']
        
        #check appointment
        checkAppt = checkAppt(d_name, date, patient_id)
        
        doc_list = doc_listModel()
        
        if checkAppt > 0:
            return render(request, 'appointments.html', {"data1":doc_list, "error":"Appointment on this date already exists"})
        else:
            rid = appointmentModel(d_name, date, time, reason, description, username)
            return render(request, 'appointments.html', {"data1":doc_list, "message":"Appointment created successfully"})
        
@csrf_exempt
def manage_appointment(request):
    username = request.session['patient_id']
    getAppointmentDetails = getAllAppointmentDetailsModel(username)
    return render(request, 'manage_appointment.html', {"data2":getAppointmentDetails})

@csrf_exempt
def remove_appt(request):
    username = request.session['patient_id']
    getAppointmentDetails = getAllAppointmentDetailsModel(username)
    return render(request, 'manage_appointment.html', {"data2":getAppointmentDetails})

#doctor
@csrf_exempt
def doctorlogin(request):
    user = request.POST["username"]
    password = request.POST["pas"]
    checkuserExist = d_checkuserModel(user, password)

    if checkuserExist >= 1:
        request.session['user_contact'] = user
        return HttpResponseRedirect('/d_dashboard/')
    else:
        return render(request, 'doctorLogin.html', {"message":"User does not exist"})

@csrf_exempt
def d_dashboard(request):
    userName = request.session['user_contact']

    if 'user_contact' in request.session:
        return render(request, 'doctorDashboard.html')
    else:
        return HttpResponseRedirect('/doctorlog/')

@csrf_exempt
def d_confirm(request):
    user = request.POST["username"]
    checkuserExist = df_checkuserModel(user)

    if checkuserExist >= 1:
        request.session['user_contact'] = user
        return HttpResponseRedirect('/d_editpass/')
    else:
        return render(request, 'doctorLogin.html', {"message":"User does not exist"})

@csrf_exempt
def d_editpass(request):
    user = request.session['user_contact']
    if 'user_contact' in request.session:
        return render(request, 'dchangePass.html')
    else:
        return render(request, 'dforgotpass.html', {"message":"Invalid username"})

@csrf_exempt
def d_changepass(request):
    if request.method == "POST":
        d_password = request.POST["pass"]
        username = request.session['user_contact']
        d_updatepassModel(d_password, username)
        return render(request, 'dchangePass.html', {"message":"your password has been changed successfully"})
    
def change_password(request):
    return render(request, 'pchangepass.html')

def pchangepass(request):
    if 'patient_user_name' in request.session:
        
        return render(request, 'patientDashboard.html', {"appt_list":getAppointmentDetailsModel(patient_id)})
    else:
        return HttpResponseRedirect('/patientlog/')
    userpass = request.POST["pass"]