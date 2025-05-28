from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="agri_rental"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    email1=""
    mess=""


    
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        page = request.form['page']
        if page=="login":
            username1 = request.form['uname']
            password1 = request.form['pass']
            
            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s and pass=%s",(username1,password1))
            myresult = mycursor.fetchone()[0]
            print(myresult)
            if myresult>0:
                session['username'] = username1
                
                return redirect(url_for('userhome')) 
            else:
                msg="no"

        elif page=="reg":
            name = request.form['name']
            address = request.form['address']
            district = request.form['district']
            mobile = request.form['mobile']
            email = request.form['email']
            uname = request.form['uname']
            pass1 = request.form['pass']

            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s || email=%s",(uname,email))
            cnt = mycursor.fetchone()[0]
            if cnt==0:
                mycursor.execute("SELECT max(id)+1 FROM ar_user")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO ar_user(id,name,address,district,mobile,email,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,name,address,district,mobile,email,uname,pass1)
                mycursor.execute(sql, val)
                mydb.commit()
                msg="success"
            else:
                msg="fail"

        elif page=="forgot":
            email2 = request.form['email2']
            mobile2 = request.form['mobile2']
            newpass = request.form['newpass']
            cpass = request.form['cpass']

            mycursor.execute("SELECT count(*) FROM ar_user where email=%s && mobile=%s",(email2,mobile2))
            cnt = mycursor.fetchone()[0]
            if cnt>0:
                email1=email2

                mycursor.execute("SELECT * FROM ar_user where email=%s",(email2,))
                dd = mycursor.fetchone()
                name=dd[1]
                rn=randint(1000,9999)
                code=str(rn)
                mess="Dear "+name+",Forgot Password Verification Code:"+code
            
                mycursor.execute("update ar_user set pass=%s where email=%s",(newpass,email2))
                mydb.commit()
                msg="change"
            else:
                msg="wrong"
                
            
            
        

    return render_template('index.html',msg=msg,act=act,mess=mess,email1=email1)

@app.route('/login_pro',methods=['POST','GET'])
def login_pro():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            
            return redirect(url_for('pro_home')) 
        else:
            msg="Invalid Username or Password! or not approved"
            
        

    return render_template('login_pro.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/forgot',methods=['POST','GET'])
def forgot():
    cnt=0
    act=""
    msg=""
    mess=""
    email=""
    uid=""

    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        newpass = request.form['newpass']
        cpass = request.form['cpass']

        mycursor.execute("SELECT count(*) FROM ar_user where email=%s && mobile=%s",(email,mobile))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            
            mycursor.execute("SELECT * FROM ar_user where email=%s",(email,))
            dd = mycursor.fetchone()
            uid=str(dd[0])
            name=dd[1]
            rn=randint(1000,9999)
            code=str(rn)
            mess="Dear "+name+",Forgot Password Verification Code:"+code
        
            mycursor.execute("update ar_user set pass=%s,otp=%s where email=%s",(newpass,code,email))
            mydb.commit()
            msg="change"
        else:
            msg="wrong"
            
        

    return render_template('forgot.html',msg=msg,act=act,mess=mess,email=email,uid=uid)


@app.route('/verify',methods=['POST','GET'])
def verify():
    msg=""
    mess=""
    email=""
    uid=request.args.get("uid")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where id=%s",(uid,))
    dd = mycursor.fetchone()
    code=dd[8]
    
    
    if request.method == 'POST':
        otp = request.form['otp']

        if otp==code:
            msg="change"
        else:
            msg="wrong"
        

    return render_template('verify.html',msg=msg)

@app.route('/forgot_pro',methods=['POST','GET'])
def forgot_pro():
    cnt=0
    act=""
    msg=""
    mess=""
    email=""
    uid=""

    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        newpass = request.form['newpass']
        cpass = request.form['cpass']

        mycursor.execute("SELECT count(*) FROM ar_provider where email=%s && mobile=%s",(email,mobile))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            
            mycursor.execute("SELECT * FROM ar_provider where email=%s",(email,))
            dd = mycursor.fetchone()
            uid=str(dd[0])
            name=dd[1]
            rn=randint(1000,9999)
            code=str(rn)
            mess="Dear "+name+",Forgot Password Verification Code:"+code
        
            mycursor.execute("update ar_provider set pass=%s,otp=%s where email=%s",(newpass,code,email))
            mydb.commit()
            msg="change"
        else:
            msg="wrong"
            
        

    return render_template('forgot_pro.html',msg=msg,act=act,mess=mess,email=email,uid=uid)


@app.route('/verify_pro',methods=['POST','GET'])
def verify_pro():
    msg=""
    mess=""
    email=""
    uid=request.args.get("uid")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where id=%s",(uid,))
    dd = mycursor.fetchone()
    code=dd[12]
    
    
    if request.method == 'POST':
        otp = request.form['otp']

        if otp==code:
            msg="change"
        else:
            msg="wrong"
        

    return render_template('verify_pro.html',msg=msg)
        

@app.route('/reg_pro', methods=['GET', 'POST'])
def reg_pro():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        district=request.form['district']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        account=request.form['account']
        gpay=request.form['gpay']

        

        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ar_provider")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ar_provider(id,name,address,district,mobile,email,uname,pass,create_date,account,gpay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,district,mobile,email,uname,pass1,rdate,account,gpay)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('reg_pro.html', msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    email=""
    mess=""
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ar_provider")
    data = mycursor.fetchall()

    if act=="ok":
        pid=request.args.get("pid")
        mycursor.execute("update ar_provider set status=1 where id=%s",(pid,))
        mydb.commit()
        msg="success"
    
    
    return render_template('admin.html',msg=msg,data=data,act=act)


@app.route('/pro_home', methods=['GET', 'POST'])
def pro_home():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('pro_home.html',data=data,act=act)


@app.route('/pro_add', methods=['GET', 'POST'])
def pro_add():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        vehicle=request.form['vehicle']
        vno=request.form['vno']
        details=request.form['details']
        cost1=request.form['cost1']
        cost2=request.form['cost2']
        file= request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM ar_vehicle")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        if file:
            fname1 = file.filename
            fname = secure_filename(fname1)
            photo="P"+str(maxid)+fname
            file.save(os.path.join("static/upload/", photo))
                
        sql = "INSERT INTO ar_vehicle(id,uname,vehicle,vno,details,cost1,cost2,photo,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,vehicle,vno,details,cost1,cost2,photo,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        

        
    return render_template('pro_add.html',msg=msg,data=data,act=act)

@app.route('/pro_vehicle', methods=['GET', 'POST'])
def pro_vehicle():
    msg=""
    act=""
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('pro_vehicle.html',msg=msg,data=data,act=act,data2=data2)

@app.route('/pro_request', methods=['GET', 'POST'])
def pro_request():
    msg=""
    vid=request.args.get("vid")
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    print(uname)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid, ))
    vdata = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status<=1",(uname, vid))
    cnt3 = mycursor.fetchone()[0]

    if cnt3>0:
        st="1"
        mycursor.execute("SELECT * FROM ar_booking b, ar_user a where b.uname=a.uname && b.provider=%s && b.vid=%s && b.status<=1",(uname, vid))
        data2 = mycursor.fetchall()
        
       
    if act=="ok":
        bid=request.args.get("bid")
        mycursor.execute("update ar_booking set status=1 where id=%s", (bid,))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=1 where id=%s", (vid,))
        mydb.commit()
        msg="ok"
        
    return render_template('pro_request.html',msg=msg,data=data,act=act,data2=data2,vdata=vdata,st=st,vid=vid)

#KNN for Agri Vehicle Search
def Knn_vehicle():
    df = pd.read_csv("static/dataset/agri_vehicles.csv")

    # Select and preprocess features
    features = ['Horsepower', 'Price', 'Year']  # + encoded categorical features
    X = df[features]

    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # KNN model
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn.fit(X_scaled)

    # query
    query = [[50, 700000, 2023]]
    query_scaled = scaler.transform(query)

    # Find similar vehicles
    distances, indices = knn.kneighbors(query_scaled)

    # Display results
    similar_vehicles = df.iloc[indices[0]]
    print(similar_vehicles)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    df = pd.read_csv("static/dataset/agri_vehicles.csv")
    
    if request.method=='POST':
        search=request.form['search']
        hp=search
        price=search
        year=search
        '''query = [[hp, price, year]]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        query_scaled = scaler.transform(query)
        distances, indices = knn.kneighbors(query_scaled)
        results = df.iloc[indices[0]].to_dict(orient='records')'''
        st="1"

        gs='%'+search+'%'

        uu=[]
        mycursor.execute("SELECT * FROM ar_provider where name like %s || address like %s || district like %s",(gs,gs,gs))
        dd2 = mycursor.fetchall()
        for ds2 in dd2:
            uu.append(ds2[6])

        
        if len(uu)>0:
            for u1 in uu:
                mycursor.execute("SELECT * FROM ar_vehicle where uname=%s && status=0",(u1,))
                dd3 = mycursor.fetchall()
                for ds3 in dd3:
                    data2.append(ds3)
                
                
        else:
            mycursor.execute("SELECT * FROM ar_vehicle where (uname like %s || vehicle like %s || vno like %s || details like %s) && status=0",(gs,gs,gs,gs))
            data2 = mycursor.fetchall()
        

    if st=="":
        mycursor.execute("SELECT * FROM ar_vehicle where status=0 order by rand() limit 0,10")
        data2 = mycursor.fetchall()
    
    return render_template('userhome.html',data=data,act=act,data2=data2)


def getDays(date1,date2):
    from datetime import datetime

    sd=date1.split("-")
    sd1=int(sd[0])
    sd2=int(sd[1])
    sd3=int(sd[2])

    ed=date2.split("-")
    ed1=int(ed[0])
    ed2=int(ed[1])
    ed3=int(ed[2])

    date1 = datetime(sd1, sd2, sd3)  # Start date
    date2 = datetime(ed1, ed2, ed3)    # End date
    difference = date2 - date1
    num_days = difference.days
    return num_days


@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    act=""
    uname=""
    name=""
    mess=""
    mobile=""
    st=""
    amt=0
    vdata=[]
    vid=request.args.get("vid")
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid,))
    dd = mycursor.fetchone()
    pro=dd[1]
    cost1=dd[5]
    cost2=dd[6]
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(pro,))
    pdata = mycursor.fetchone()
    provider=pdata[6]
    name=pdata[1]
    mobile=str(pdata[4])

    now = datetime.datetime.now()
    rdate=now.strftime("%Y-%m-%d")
    rtime=now.strftime("%H-%M-%S")
    rt=rtime.split("-")
    rh=int(rt[0])
    tm=0
    dm=0

    if request.method=='POST':
        
        time_type=request.form['time_type']
        if time_type=="1":
            sdate1=request.form['sdate1']
            shour=request.form['shour']
            ehour=request.form['ehour']

            sh=int(shour)
            eh=int(ehour)
            
            ndt=getDays(rdate,sdate1)
            st=""
            
            if ndt>=0:
                print("s")
    
                
                if rdate==sdate1:
                    if sh>rh:

                        mycursor.execute("SELECT count(*) FROM ar_booking where sdate=%s && vid=%s",(sdate1,vid))
                        cn = mycursor.fetchone()[0]
                        if cn>0:
                            mycursor.execute("SELECT * FROM ar_booking where sdate=%s && vid=%s",(sdate1,vid))
                            rw = mycursor.fetchall()
                            for rw1 in rw:
                                if rw1[16]>=sh and rw1[17]<=eh:
                                    tm+=1

                        if tm==0:
                            st="1"
                            print("h")
                        else:
                            msg="wrong3"

                        
                    else:
                        msg="wrong2"
                else:
                    st="1"
                    print("h")
                
                
            else:
                msg="wrong"

            if st=="1":
                mycursor.execute("SELECT max(id)+1 FROM ar_booking")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1

                tot_hour=eh-sh
                amt=cost1*tot_hour
                sql = "INSERT INTO ar_booking(id,uname,provider,vid,duration,time_type,req_date,status,amount,pay_st,sdate,shour,ehour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,uname,provider,vid,tot_hour,time_type,rdate,'0',amt,'0',sdate1,sh,eh)
                mycursor.execute(sql, val)
                mydb.commit()
                mess="Vehicle ID: "+str(vid)+" book by "+uname
                msg="success"

                

        elif time_type=="2":
            sdate=request.form['sdate']
            edate=request.form['edate']

            ndt=getDays(rdate,sdate)
            ndt2=getDays(rdate,edate)

            

            if ndt>=0 and ndt2>=0:
                tot=getDays(sdate,edate)
                tot_days=tot+1

                mycursor.execute("SELECT count(*) FROM ar_booking where status=0 && vid=%s",(vid,))
                cn = mycursor.fetchone()[0]
                if cn>0:
                    mycursor.execute("SELECT * FROM ar_booking where status=0 && vid=%s",(vid,))
                    rw = mycursor.fetchall()
                    for rw1 in rw:

                        ndtt1=getDays(rdate,rw1[14])
                        ndtt2=getDays(rdate,rw1[15])

                        ndtt3=getDays(rdate,sdate)
                        ndtt4=getDays(rdate,edate)
                        
                        if ndtt3==ndtt1:
                            dm+=1
                        if ndtt3==ndtt2:
                            dm+=1
                        if ndtt4==ndtt1:
                            dm+=1
                        if ndtt4==ndtt2:
                            dm+=1

                        if ndtt3>ndtt1 and ndtt3<ndtt2:
                            dm+=1
                        if ndtt4>ndtt1 and ndtt4<ndtt2:
                            dm+=1

                        
                if dm==0:
                    mycursor.execute("SELECT max(id)+1 FROM ar_booking")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1

                    
                    amt=cost2*tot_days
                    sql = "INSERT INTO ar_booking(id,uname,provider,vid,duration,time_type,req_date,status,amount,pay_st,sdate,edate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (maxid,uname,provider,vid,tot_days,time_type,rdate,'0',amt,'0',sdate,edate)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    mess="Vehicle ID: "+str(vid)+" book by "+uname
                    msg="success"
                else:
                    msg="wrong3"
            else:
                msg="wrong"
                
            
        

        '''mycursor.execute("SELECT max(id)+1 FROM ar_booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        tt=int(duration)
        if time_type=="1":
            
            amt=cost1*tt
        else:
            amt=cost2*tt
        
        sql = "INSERT INTO ar_booking(id,uname,provider,vid,duration,time_type,req_date,status,amount,pay_st) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,provider,vid,duration,time_type,req_date,'0',amt,'0')
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"'''
        
    mycursor.execute("SELECT * FROM ar_booking where vid=%s",(vid,))
    vdata = mycursor.fetchall()
    
    return render_template('book.html',msg=msg,data=data,act=act,pdata=pdata,vdata=vdata,mess=mess,mobile=mobile,name=name)

@app.route('/user_status', methods=['GET', 'POST'])
def user_status():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('user_status.html',data=data,act=act,data2=data2)

@app.route('/user_pay', methods=['GET', 'POST'])
def user_pay():
    msg=""
    act=""
    uname=""
    name=""
    name2=""
    mobile=""
    mobile2=""
    mess=""
    mess2=""
    bid=request.args.get("bid")
    vid=request.args.get("vid")
    st=""
    data2=[]
    d2=[]
    if 'username' in session:
        uname = session['username']
        
    now = datetime.datetime.now()
    pdate=now.strftime("%d-%m-%Y")

    t = time.localtime()
    ptime = time.strftime("%H:%M:%S", t)

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()
    name=data[1]
    mobile=str(data[4])

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s && b.id=%s",(uname,bid))
    data2 = mycursor.fetchone()
    amount=str(data2[18])

    mycursor.execute("SELECT * FROM ar_booking where id=%s",(bid, ))
    d1 = mycursor.fetchone()
    provider=d1[2]

    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(provider, ))
    d2 = mycursor.fetchone()
    name2=d2[1]
    mobile2=str(d2[4])
    

    if request.method=='POST':
        transid=request.form['transid']
        reviews=request.form['reviews']
        
        mycursor.execute("update ar_booking set status=2,transid=%s,pdate=%s,ptime=%s,reviews=%s where id=%s", (transid,pdate,ptime,reviews,bid))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=0 where id=%s", (vid,))
        mydb.commit()

        mess="Amount Paid: Rs. "+amount
        mess2="Rs."+amount+" Credited from "+uname
        msg="ok"
        
    
    return render_template('user_pay.html',msg=msg,data=data,act=act,data2=data2,d2=d2,mess=mess,mobile=mobile,name=name,mess2=mess2,mobile2=mobile2,name2=name2)

@app.route('/view_pro', methods=['GET', 'POST'])
def view_pro():
    msg=""
    act=""
    uname=request.args.get("uname")
    data2=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('view_pro.html',msg=msg,data=data,act=act,data2=data2,uname=uname)

@app.route('/pro_history', methods=['GET', 'POST'])
def pro_history():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.provider=%s && b.status=2 order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('pro_history.html',data=data,act=act,data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
