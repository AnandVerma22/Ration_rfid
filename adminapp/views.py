from tkinter import INSERT
import mysql.connector
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import datetime
from django.core.files.storage import FileSystemStorage

# Create your views here.
#Create database connection function
def getdb():
    mydb = mysql.connector.connect( host="localhost",user="root", passwd="",database="ration_db")
    return mydb
    
# Create your views here.
def index(request):
   sel = "select count(m_id) from member_tb" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel)
   memberrecord = mycursor.fetchall()

   sel1 = "select count(v_id) from vendor_tb" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel1)
   vrecord = mycursor.fetchall()

   sel2 = "select count(subm_id) from submember_tb" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel2)
   subrecord = mycursor.fetchall()

   sel3 = "select count(f_id) from feedback_tb where f_status='Show'" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel3)
   sfrecord = mycursor.fetchall()

   sel4 = "select count(f_id) from feedback_tb where f_status='Hide'" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel4)
   hfrecord = mycursor.fetchall()

   sel5 = "select count(c_id) from category_tb" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel5)
   crecord = mycursor.fetchall()

   sel6 = "select count(r_id) from ration_tb where r_status='Collected'" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel6)
   curecord = mycursor.fetchall()

   sel7 = "select count(r_id) from ration_tb where r_status='Not collected'" 
   # connection create object
   mydb = getdb()
   mycursor = mydb.cursor()
   #query execute
   mycursor.execute(sel7)
   nurecord = mycursor.fetchall()

   alldata={
      "memberrecord": memberrecord,
      "subrecord": subrecord,
      "vrecord": vrecord,
      "sfrecord": sfrecord,
      "hfrecord": hfrecord,
      "crecord":crecord,
      "curecord":curecord,
      "nurecord":nurecord
   }
   return render(request,'index.html',alldata);

def managecategory(request):
   try:
      if request.POST:
         #variable Decleration
         cname = request.POST.get("cname")
         cquantity = request.POST.get("cquantity")
         cprice = request.POST.get("cprice")
         cstatus = request.POST.get("cstatus")
         cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         ins = "INSERT INTO `category_tb`(`c_name`, `c_quantity`, `c_price`, `c_status`, `c_createdate`, `c_update`) VALUES ('"+str(cname)+"','"+str(cquantity)+"','"+str(cprice)+"','"+str(cstatus)+"','"+(cdate)+"','"+(cdate)+"')"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(ins)
         mydb.commit()
         return redirect('category')
      elif request.GET.get("cat_del") != None:

         cat_del = request.GET.get("cat_del")
         dl = "DELETE FROM `category_tb` where c_id ='"+str(cat_del)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('category')
      else:
         sel = "select * from category_tb" 
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'category.html',{'record':myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned') 

def managecategory_edit(request):
   try:
      if request.POST:
         #variable Decleration
         cname = request.POST.get("cname")
         cquantity = request.POST.get("cquantity")
         cprice = request.POST.get("cprice")
         cstatus = request.POST.get("cstatus")
         cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         cat_edt = request.GET.get("cat_edt")
         up = "UPDATE `category_tb` SET `c_name`='"+str(cname)+"',`c_quantity`='"+str(cquantity)+"',`c_price`='"+str(cprice)+"',`c_status`='"+str(cstatus)+"',`c_update`='"+(cdate)+"' WHERE c_id='"+str(cat_edt)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         return redirect('category')

      elif request.GET.get("cat_edt") != None:
         cat_edt = request.GET.get("cat_edt")
         sel = "select * from category_tb where c_id = '"+str(cat_edt)+"' "
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'category_edit.html',{'record':myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')  

def managelogin(request):
   try:
      msg =""
      if request.POST:
         #variable Decleration
         username = request.POST.get("username")
         password = request.POST.get("password")
        
         sel = "select * from login_tb where l_username = '"+str(username)+"' and l_password ='"+str(password)+"' "
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         if(len(myresult)==0):
            msg = " Invalid Username Or Password. "
         else:
            #session created
            request.session["name"] =  username
            request.session["img"] =  myresult[0][3]
            request.session["time"] =  str(myresult[0][4])
            return redirect("index")

      return render(request,'login.html',{'msg':msg});

   except NameError:
      print("internal error")
   except:
      print('Error returned')
def logoutmanage(request):
    try:
        #variable decleration
        uname = request.session["name"]
        cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        ins = "update login_tb set l_lastseen = '"+cdate+"' where l_username = '"+uname+"'"
           
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(ins)
        mydb.commit()
        
        request.session["name"] =  None
        request.session["img"] =  None
        request.session["time"] =  None
        return redirect("login") 

    except NameError:
        print("internal error")
    except:
        print('Error returned')  
def managefeedback(request):
   try:
      if request.GET.get("f_del") != None:
         f_del = request.GET.get("f_del")
         dl = "DELETE FROM `feedback_tb` where f_id ='"+str(f_del)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('feedback')

      elif request.GET.get("f_id") != None:

         f_id = request.GET.get("f_id")
         f_status = request.GET.get("f_status")

         if f_status == 'Hide':
            f_status = 'Show'
         else:
            f_status = 'Hide'
   

         dl = "update `feedback_tb` set f_status = '"+f_status+"' where f_id ='"+str(f_id)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('feedback')   
      else:
         sel = "select * from feedback_tb order by f_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'feedback.html',{'record':myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def managevendor(request):
   try:
      msg = ""
      if request.POST:
         #variable Decleration
         vname = request.POST.get("vname")
         vcontact = request.POST.get("vcontact")
         if  request.POST.get("vimage") != "":
            vimage = request.FILES["vimage"]
            img = FileSystemStorage()
            fimg = img.save(vimage.name,vimage)
         else:
            fimg = request.POST.get("old_img")

         vsname = request.POST.get("vsname")
         vpassword = request.POST.get("vpassword")
         vstatus = request.POST.get("vstatus")
         cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         
         chk = "select * from vendor_tb where v_contact = '"+str(vcontact)+"'";
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(chk)
         chkresult = mycursor.fetchall()
         
         if len(chkresult) > 0:
            msg = "Already User Register..!";
            return render(request,'vendor.html',{'msg':msg});
         else:
           
            ins = "INSERT INTO `vendor_tb`(`v_name`, `v_contact`, `v_image`, `v_shopname`, `v_password`, `v_status`, `v_cdata`, `v_udate`) VALUES ('"+str(vname)+"','"+str(vcontact)+"','"+str(fimg)+"','"+str(vsname)+"','"+str(vpassword)+"','"+str(vstatus)+"','"+(cdate)+"','"+(cdate)+"')"
            # print(ins)
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(ins)
            mydb.commit()
            return redirect('vendor')

      elif request.GET.get("ven_del") != None:
         ven_del = request.GET.get("ven_del")
         dl = "DELETE FROM `vendor_tb` where v_id ='"+str(ven_del)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('vendor')
      else:
         sel = "select * from vendor_tb order by v_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         alldata = {
            'record':myresult,
            'msg' : msg,
            }
      return render(request,'vendor.html',alldata);
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def managevendor_edit(request):
   try:
      if request.POST:
         #variable Decleration
         vname = request.POST.get("vname")
         vcontact = request.POST.get("vcontact")
         
         if  request.POST.get("vimage") != "":
            vimage = request.FILES["vimage"]
            img = FileSystemStorage()
            fimg = img.save(vimage.name,vimage)
         else:
            fimg = request.POST.get("old_img")

         vsname = request.POST.get("vsname")
         vpassword = request.POST.get("vpassword")
         vstatus = request.POST.get("vstatus")
         cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         ved_edt = request.GET.get("ven_edt")
         
         up = "UPDATE `vendor_tb` SET `v_name`='"+str(vname)+"',`v_contact`='"+str(vcontact)+"',`v_image`='"+str(fimg)+"',`v_shopname`='"+str(vsname)+"',`v_password`='"+str(vpassword)+"',`v_status`='"+str(vstatus)+"',`v_udate`='"+str(cdate)+"' WHERE v_id='"+str(ved_edt)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         return redirect('vendor')

      elif request.GET.get("ven_edt") != None:
         ven_edt = request.GET.get("ven_edt")
         sel = "select * from vendor_tb where v_id = '"+str(ven_edt)+"' "
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'vendor_edit.html',{'record':myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def managemember(request):
   try:
      if request.GET.get("m_del") != None:

         m_del = request.GET.get("m_del")
         dl = "DELETE FROM `member_tb` where m_id ='"+str(m_del)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         
         dl1 = "DELETE FROM `submember_tb` where subm_m_id ='"+str(m_del)+"'"
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl1)
         mydb.commit()
         return redirect('member')
         
      elif request.GET.get("m_id") != None:

         m_id = request.GET.get("m_id")
         m_status = request.GET.get("m_status")

         if m_status == 'Deactive':
            m_status = 'Active'
         else:
            m_status = 'Deactive'


         dl1 = "update `member_tb` set m_status = '"+m_status+"' where m_id ='"+str(m_id)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl1)
         mydb.commit()
         
         dl2 = "update `submember_tb` set subm_status = '"+m_status+"' where subm_m_id ='"+str(m_id)+"' and subm_type = 'Main'"
         
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl2)
         mydb.commit()
         
         
         return redirect('member')

      else:
         sel = "select * from member_tb,vendor_tb where member_tb.m_v_id=vendor_tb.v_id order by m_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'member.html',{'record': myresult});

   except NameError:
        print("internal error")
   except:
        print('Error returned')

def managememberverify(request):
   try:
      if request.POST:
         m_vfy = request.GET.get("m_vfy")
         m_status = request.POST.get("m_status")
         rfid_code = request.POST.get("rfid_code")
         m_udate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         
         up = "update `member_tb` set m_status = '"+str(m_status)+"',rfid_code = '"+str(rfid_code)+"',m_udate = '"+str(m_udate)+"'  where m_id ='"+str(m_vfy)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         up1 = "update `submember_tb` set subm_status = '"+str(m_status)+"',subm_udate = '"+str(m_udate)+"'  where subm_m_id ='"+str(m_vfy)+"' and subm_type = 'Main' "
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up1)
         mydb.commit()
         return redirect('member')
         

      elif request.GET.get("m_vfy") !=None:
         m_id = request.GET.get("m_vfy")
         sel = "select * from member_tb,vendor_tb where member_tb.m_v_id= vendor_tb.v_id and member_tb.m_id='"+str(m_id)+"'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'member_verify.html',{'record':myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def managesubmember(request):
   try:
      if request.POST:
         m_name = request.POST.get("m_name")

         sel = "select * from submember_tb,member_tb,vendor_tb where submember_tb. subm_m_id = '"+str(m_name)+"' and submember_tb.subm_m_id=member_tb.m_id and member_tb.m_v_id=vendor_tb.v_id order by subm_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()

         sel1 = "select * from member_tb order by m_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel1)
         memberresult = mycursor.fetchall()

         alldata = {
            'record': myresult,
            'memberresult' : memberresult
         }
         return render(request,'submember.html',alldata);

      elif request.GET.get("s_del") !=None:

         s_del=request.GET.get("s_del")
         #delete code
         dlt = "DELETE FROM submember_tb Where subm_id='"+str(s_del)+"'" 
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dlt)
         mydb.commit()
         return redirect('submember')

      elif request.GET.get("subm_id") != None:

         subm_id = request.GET.get("subm_id")
         subm_status = request.GET.get("subm_status")

         if subm_status == 'Deactive':
            subm_status = 'Active'
         else:
            subm_status = 'Deactive'


         dl = "update `submember_tb` set subm_status = '"+subm_status+"' where subm_id ='"+str(subm_id)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('submember') 

      else:
         sel1 = "select * from member_tb order by m_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel1)
         memberresult = mycursor.fetchall()
         return render(request,'submember.html',{'memberresult': memberresult});

   except NameError:
        print("internal error")
   except:
        print('Error returned')   

def managesubmemberedit(request):
   try:
      if request.POST:
         subm_verify = request.GET.get("sub_edt") 
         submstatus = request.POST.get("subm_status")
         submtype = request.POST.get("submtype")
         #rfid = request.POST.get("rfid")
         mdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         up = "UPDATE submember_tb SET  `subm_status`= '"+str(submstatus)+"', `subm_udate`= '"+str(mdate)+"', `subm_type`= '"+str(submtype)+"' Where subm_id='"+str(subm_verify)+"'"
         #print(up)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         return redirect('submember')

      elif request.GET.get("sub_edt") !=None:
         subm_id = request.GET.get("sub_edt")

         sel = "select * from member_tb,submember_tb Where submember_tb.subm_m_id = member_tb.m_id and submember_tb.subm_id='"+str(subm_id)+"'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()

         return render(request,'submember_edit.html',{'record': myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def managerationview(request):
   try:
      if request.GET.get("r_del") !=None:
         m_del = request.GET.get("r_del")
         dl = "DELETE FROM `ration_tb` where r_id ='"+str(m_del)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('ration_view')

      elif request.GET.get("subm_id") != None:

         subm_id = request.GET.get("subm_id")
         subm_status = request.GET.get("subm_status")

         if subm_status == 'Not collected':
            subm_status = 'Collected'
         else:
            subm_status = 'Not collected'


         dl = "update `ration_tb` set r_status = '"+subm_status+"' where r_id ='"+str(subm_id)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(dl)
         mydb.commit()
         return redirect('ration_view')
      else:
         sel = "select * from ration_tb,vendor_tb,member_tb,submember_tb,category_tb Where ration_tb.v_id = vendor_tb.v_id and ration_tb.c_id = category_tb.c_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.m_id = member_tb.m_id order by ration_tb.r_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'ration_view.html',{'record': myresult});
   except NameError:
      print("internal error")
   except:
      print('Error returned')

def manageuser_ration(request):
   if request.POST:
      sdate = request.POST.get("sdate")
      edate = request.POST.get("edate")
      status = request.POST.get("status")
      sel = "select * from ration_tb,vendor_tb,member_tb,submember_tb,category_tb Where ration_tb.v_id = vendor_tb.v_id and ration_tb.c_id = category_tb.c_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.m_id = member_tb.m_id and DATE(ration_tb.r_cdate) BETWEEN '"+sdate+"' AND '"+edate+"' and ration_tb.r_status='"+str(status)+"' order by ration_tb.r_id desc"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'user_ration.html',{'record': myresult});
   return render(request,'user_ration.html',{});

def managevendor_ration(request):
   if request.POST:
      v_id = request.POST.get("v_id")
      vstatus = request.POST.get("vstatus")
      sel = "select * from ration_tb,vendor_tb,member_tb,submember_tb,category_tb Where ration_tb.v_id = vendor_tb.v_id and ration_tb.c_id = category_tb.c_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.m_id = member_tb.m_id and ration_tb.v_id='"+str(v_id)+"' and ration_tb.r_status='"+str(vstatus)+"' order by ration_tb.r_id desc"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()

      sel1 = "select * from vendor_tb order by v_id desc"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel1)
      vresult = mycursor.fetchall()

      alldata = {
            'record': myresult,
            'vresult' : vresult
         }

      return render(request,'vendor_ration.html',alldata);
   else:
      sel1 = "select * from vendor_tb order by v_id desc"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel1)
      vresult = mycursor.fetchall()
      return render(request,'vendor_ration.html',{'vresult': vresult});
def managemember_report(request):
   if request.POST:
      sdate = request.POST.get("sdate")
      edate = request.POST.get("edate")
      sel = "select * from member_tb,vendor_tb where member_tb.m_v_id=vendor_tb.v_id and DATE(member_tb.m_cdata) BETWEEN '"+sdate+"' AND '"+edate+"'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'member_report.html',{'record': myresult});
   return render(request,'member_report.html',{});
def managesubmember_report(request):
   if request.POST:
      sdate = request.POST.get("sdate")
      edate = request.POST.get("edate")
      sel = "select * from submember_tb,member_tb,vendor_tb where submember_tb.subm_m_id=member_tb.m_id and member_tb.m_v_id=vendor_tb.v_id and DATE(submember_tb.subm_cdate) BETWEEN '"+sdate+"' AND '"+edate+"'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'submember_report.html',{'record': myresult});
   return render(request,'submember_report.html',{});
def managevendor_report(request):
   if request.POST:
      sdate = request.POST.get("sdate")
      edate = request.POST.get("edate")
      sel = "select * from vendor_tb where DATE(vendor_tb.v_cdata) BETWEEN '"+sdate+"' AND '"+edate+"'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'vendor_report.html',{'record': myresult});
   return render(request,'vendor_report.html',{});

def manageration(request):
   msg = ""
   if request.POST:
      v_id = request.POST.get("v_id")
      m_id = 0
      c_id = 0
      c_quantity = 0
      c_price = 0
      r_status = 'Not collected'
      s_id = 0
      mdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      r_months = datetime.datetime.now().strftime("%m-%Y")
      

      chk = "select r_months from ration_tb where r_months = '"+str(r_months)+"' and v_id = '"+str(v_id)+"'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(chk)
      chkdata = mycursor.fetchall()
      if len(chkdata) > 0:
         sel1 = "select * from vendor_tb where v_status = 'Active'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel1)
         vresult = mycursor.fetchall()
         msg = "Already Generated Ration For this Month."
         alldata = {
            'vresult': vresult,
            'msg' : msg
         }
         return render(request,'generate_ration.html',alldata);

      else:
         sel1 = "select * from category_tb where c_status='Active'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel1)
         cresult = mycursor.fetchall()
         #print(len(cresult))
         if len(cresult) > 0:
            for catdata in cresult:
               c_id = catdata[0]
               c_quantity = catdata[2]
               c_price = catdata[3]
               sel = "select * from vendor_tb,member_tb,submember_tb where vendor_tb.v_id = member_tb.m_v_id and member_tb.m_id = submember_tb.subm_m_id and vendor_tb.v_id = '"+str(v_id)+"' and member_tb.m_status = 'Active' and submember_tb.subm_status = 'Active'" 
               mydb = getdb()
               mycursor = mydb.cursor()
               #query execute
               mycursor.execute(sel)
               myresult = mycursor.fetchall()
               for ration in myresult:
                  s_id  = ration[21]
                  m_id = ration[9]
                  r_total = c_quantity * c_price
                  ins = "INSERT INTO `ration_tb` (`v_id`, `c_id`, `s_id`, `m_id`, `r_price`, `r_quantity`, `r_total`, `r_status`, `r_cdate`, `r_udate`,`r_months`) VALUES ('"+str(v_id)+"','"+str(c_id)+"','"+str(s_id)+"','"+str(m_id)+"','"+str(c_price)+"','"+str(c_quantity)+"','"+str(r_total)+"','"+str(r_status)+"','"+mdate+"','"+mdate+"','"+str(r_months)+"')"
                  mydb = getdb()
                  mycursor = mydb.cursor()
                  #query execute
                  mycursor.execute(ins)
                  mydb.commit()
            return redirect('ration_view')
         
      sel2 = "select * from vendor_tb where v_status='Active'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel2)
      vresult = mycursor.fetchall()
      return render(request,'generate_ration.html',{'vresult': vresult});

   else:
      sel1 = "select * from vendor_tb where v_status = 'Active'"
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel1)
      vresult = mycursor.fetchall()
      alldata = {
         'vresult': vresult,
         'msg' : msg
      }
      return render(request,'generate_ration.html',alldata);
