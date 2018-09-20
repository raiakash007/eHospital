from django.db import connection
from django.db import models

cursor = connection.cursor()

# Create your models here.
def patientregModel(pname, pmob, padd, pemail, ppass, uploaded_file_url):
    cursor.execute("INSERT INTO patient_profile(name,mobile,address,email,password,image)VALUES('%s','%s','%s','%s','%s','%s')" % (pname, pmob, padd, pemail, ppass, uploaded_file_url))
    rid = cursor.lastrowid
    connection.close()
    return rid

def checkUserExists(p_email):
    sql = ("select *from patient_profile where email='%s'" % (p_email))
    cursor.execute(sql)
    rows_effected = cursor.rowcount
    return rows_effected
    connection.close()
    
def checkDoctor(email):
    sql = ("select *from doctor_profile where email='%s'" % (email))
    cursor.execute(sql)
    rows_effected = cursor.rowcount
    return rows_effected
    connection.close()
    
def docregModel(d_name, d_con, d_spcl, address, email, password, uploaded_file_url):
    cursor.execute("INSERT INTO doctor_profile(name,contact,specialization,address,email,password,image)VALUES('%s','%s','%s','%s','%s','%s','%s')" % (d_name, d_con, d_spcl, address, email, password, uploaded_file_url))
    rid = cursor.lastrowid
    connection.close()
    return rid

def hospitalregModel(hname, hadd, hemail, hpass, hsecurity, hans):
    cursor.execute("INSERT INTO hospital_profile(name,address,email,password,security_ques,answer)VALUES('%s','%s','%s','%s','%s','%s')" % (hname, hadd, hemail, hpass, hsecurity, hans))
    rid = cursor.lastrowid
    connection.close()
    return rid

def p_checkuserModel(email, pass_word):
    cursor.execute("SELECT * FROM patient_profile WHERE email='%s' AND password='%s'" % (email, pass_word))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

def h_checkuserModel(email, pass_word):
    cursor.execute("SELECT * FROM hospital_profile WHERE email='%s' AND password='%s'" % (email, pass_word))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

def pf_checkuserModel(email):
    cursor.execute("SELECT * FROM patient_profile WHERE email='%s'" % (email))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

def p_updatepassModel(p_password, email):
    cursor.execute("update patient_profile set password='%s' where email='%s'" % (p_password, email))
    connection.close()

def hospital_listModel():
    cursor.execute("SELECT * FROM hospital_profile")
    hlist = cursor.fetchall()
    connection.close()
    return hlist

def doc_listModel():
    cursor.execute("SELECT * FROM doctor_profile")
    dlist = dictfetchall(cursor)
    connection.close()
    return dlist

def appointmentModel(d_name, date, time, reason, description, username):
    cursor.execute("INSERT INTO appointments(doctor_id,date,appt_time,reason,description,patient_id,status)VALUES('%s','%s','%s','%s','%s','%s','%s')" % (d_name, date, time, reason, description, username, 'Open'))
    rid = cursor.lastrowid
    connection.close()
    return rid

def getAppointmentDetailsModel(username):
    cursor.execute("SELECT doctor_profile.name,doctor_profile.specialization,appointments.* FROM doctor_profile INNER JOIN appointments ON doctor_profile.id=appointments.doctor_id where appointments.status='Open' and appointments.patient_id='%s'" % (username))
    dlist = dictfetchall(cursor)
    connection.close()
    return dlist

def getAllAppointmentDetailsModel(username):
    cursor.execute("SELECT doctor_profile.name,doctor_profile.specialization,appointments.* FROM doctor_profile INNER JOIN appointments ON doctor_profile.id=appointments.doctor_id where appointments.patient_id='%s'" % (username))
    dlist = dictfetchall(cursor)
    connection.close()
    return dlist

def df_checkuserModel(name):
    cursor.execute("SELECT * FROM doctor_profile WHERE name='%s'" % (name))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

def d_updatepassModel(contact, name):
    cursor.execute("update doctor_profile set contact='%s' where name='%s'" % (contact, name))
    connection.close()

def d_checkuserModel(name, contact):
    cursor.execute("SELECT * FROM doctor_profile WHERE name='%s' AND contact='%s'" % (name, contact))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

def getPatientDetailModel(user):
    cursor.execute("SELECT * FROM patient_profile where email='%s'" % (user))
    dlist = dictfetchone(cursor)
    connection.close()
    return dlist

def checkAppt(d_name, date, patient_id):
    cursor.execute("SELECT * FROM appointments WHERE doctor_id='%s' AND date='%s' and patient_id='%s'" % (d_name, date, patient_id))
    rowcount = cursor.rowcount
    connection.close()
    return rowcount

#used to convert cursor object to dictionary with key value so that in django template you can show values from database table by column name
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def dictfetchone(cursor):
    seq = cursor.fetchone()
    if seq == None:
        return seq
    result = {}
    colnum = 0
    for column in cursor.description:
        result[column[0]] = seq[colnum]
        colnum += 1
    return result