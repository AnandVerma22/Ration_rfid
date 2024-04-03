from tkinter import INSERT
import mysql.connector
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import datetime
from django.core.files.storage import FileSystemStorage

#Create database connection function
def getdb():
    mydb = mysql.connector.connect( host="localhost",user="root", passwd="",database="ration_db")
    return mydb


def vindex(request):

    sel = "select * from feedback_tb where f_status = 'Show'" 
    # connection create object
    mydb = getdb()
    mycursor = mydb.cursor()
    #query execute
    mycursor.execute(sel)
    myrecord = mycursor.fetchall()

    return render(request,'vindex.html',{'myrecord':myrecord});

def vcontact(request):
    if request.POST:
        f_status = 'Hide'
        vname = request.POST.get("vname")
        vmail = request.POST.get("vmail")
        vphone = request.POST.get("vphone")
        vmessage = request.POST.get("vmessage")
        f_cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ins = "INSERT INTO `feedback_tb` (`f_name`, `f_contact`, `f_msg`, `f_mail`, `f_status`, `f_cdate`) VALUES ('"+str(vname)+"','"+str(vphone)+"','"+str(vmessage)+"','"+str(vmail)+"','"+str(f_status)+"','"+str(f_cdate)+"')"
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(ins)
        mydb.commit()
        return redirect('vcontact')
    return render(request,'vcontact.html',{});

def vabout(request):
    return render(request,'vabout.html',{});

def vrfid(request):
    return render(request,'vrfid.html',{});

def vsignin(request):
   try:
      msg =""
      if request.POST:
         #variable Decleration
         vcontact = request.POST.get("vcontact")
         vpass = request.POST.get("vpass")
        
         sel = "select * from vendor_tb where v_contact = '"+str(vcontact)+"' and v_password ='"+str(vpass)+"' and v_status = 'Active'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         if(len(myresult)==0):
            msg = " Invalid Contact Or Password. "
         else:
            #session created
            request.session["v_contact"] =  vcontact
            request.session["vimg"] =  myresult[0][3]
            request.session["v_id"] =  myresult[0][0]
            return redirect("vindex")

      return render(request,'vsignin.html',{'msg':msg});

   except NameError:
      print("internal error")
   except:
      print('Error returned')


def vcenter(request):
    
    sel = "select * from vendor_tb where v_status = 'Active'" 
    # connection create object
    mydb = getdb()
    mycursor = mydb.cursor()
    #query execute
    mycursor.execute(sel)
    myrecord = mycursor.fetchall()

    return render(request,'vcenter.html',{'myrecord':myrecord});
def vsignout(request):
    try: 
        request.session["vcontact"] =  None
        request.session["v_id"] =  None
        request.session["vimg"] =  None

        return redirect("vsignin") 

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def vprofile(request):
    if request.POST:
        #variable Decleration
         vname = request.POST.get("vname")
        
         
         if  request.POST.get("vfile") != "":
            vimage = request.FILES["vfile"]
            img = FileSystemStorage()
            fimg = img.save(vimage.name,vimage)
         else:
            fimg = request.POST.get("old_img")

         vsname = request.POST.get("vshopname")
         vpassword = request.POST.get("vpass")
        
         cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         vid = request.session["v_id"]
         
         up = "UPDATE `vendor_tb` SET `v_name`='"+str(vname)+"',`v_image`='"+str(fimg)+"',`v_shopname`='"+str(vsname)+"',`v_password`='"+str(vpassword)+"',`v_udate`='"+str(cdate)+"' WHERE v_id='"+str(vid)+"'"
         # print(ins)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         return redirect('vprofile')
        
    else:

        vid = request.session["v_id"]

        sel = "select * from vendor_tb where v_id = '"+str(vid)+"'" 
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel)
        myrecord = mycursor.fetchall()

    return render(request,'vprofile.html',{'myrecord':myrecord});

def vcard_holder(request):
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
         return redirect('vcard_holder')

      else:
         vid = request.session["v_id"]

         sel = "select * from member_tb where m_v_id = '"+str(vid)+"' order by m_id desc"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'vcard_holder.html',{'record': myresult});

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def vmember_edit(request):
    try:
      if request.POST:
         m_edt = request.GET.get("m_edt")
         mname = request.POST.get("m_name")
         mcontact = request.POST.get("m_contact")
         maddress = request.POST.get("maddress")

         if  request.POST.get("vfile1") != "":
            vimage1 = request.FILES["vfile1"]
            img = FileSystemStorage()
            fimg1 = img.save(vimage1.name,vimage1)
         else:
            fimg1 = request.POST.get("old_img1")
            

         if  request.POST.get("vfile2") != "":
            vimage2 = request.FILES["vfile2"]
            img = FileSystemStorage()
            fimg2 = img.save(vimage2.name,vimage2)
         else:
            fimg2 = request.POST.get("old_img2")

         udate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         up = "UPDATE `member_tb` SET `m_name`='"+str(mname)+"',`m_contact`='"+str(mcontact)+"',`m_address`='"+str(maddress)+"',`m_aadharcard`='"+str(fimg1)+"',`m_inc_c`='"+str(fimg2)+"',`m_udate`='"+udate+"' WHERE m_id = '"+str(m_edt)+"' "
        #  print(up)
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(up)
         mydb.commit()
         sup = " UPDATE `submember_tb` SET `subm_name`='"+str(mname)+"',`subm_contact`='"+str(mcontact)+"',`subm_aadharcard`='"+str(fimg1)+"',`subm_udate`='"+udate+"' WHERE subm_m_id = '"+str(m_edt)+"' "
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sup)
         mydb.commit()
         return redirect('vcard_holder')

      elif request.GET.get("m_edt") !=None:
         m_id = request.GET.get("m_edt")
         sel = "select * from member_tb,vendor_tb where member_tb.m_v_id= vendor_tb.v_id and member_tb.m_id='"+str(m_id)+"'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'vmember_edit.html',{'myresult':myresult});
    except NameError:
      print("internal error")
    except:
      print('Error returned')

def vmember(request):
    try:
        msg = ""
        if request.POST:
          mname = request.POST.get("mname")
          mcontact = request.POST.get("mcontact")
          maddress = request.POST.get("maddress")

          maadharcard = request.FILES["maadharcard"]
          img = FileSystemStorage()
          addimg = img.save(maadharcard.name,maadharcard)
          
          m_inc_c= request.FILES["m_inc_c"]
          img = FileSystemStorage()
          incimg = img.save(m_inc_c.name,m_inc_c)
          vid = request.session["v_id"]

          mpass = "12345"
          mstatus = 'Deactive'
          rfid = 0
          srel = 'Self'
          stype = 'Main'
          cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          
          chk = "select * from member_tb where m_contact = '"+str(mcontact)+"'";
          # connection create object
          mydb = getdb()
          mycursor = mydb.cursor()
          #query execute
          mycursor.execute(chk)
          chkresult = mycursor.fetchall()
          
          if len(chkresult) > 0:
              msg = "Already Member Register..!";
              return render(request,'vmember.html',{'msg':msg});
          else:
              ins = "INSERT INTO `member_tb`(`m_v_id`,`m_name`, `m_contact`, `m_address`, `m_aadharcard`, `m_inc_c`, `m_password`, `rfid_code`, `m_status`, `m_cdata`, `m_udate`) VALUES('"+str(vid)+"','"+str(mname)+"','"+str(mcontact)+"','"+str(maddress)+"','"+str(addimg)+"','"+str(incimg)+"','"+str(mpass)+"','"+str(rfid)+"','"+str(mstatus)+"','"+cdate+"','"+cdate+"')"
              #print(ins)
              mydb = getdb()
              mycursor = mydb.cursor()
              #query execute
              mycursor.execute(ins)
              mydb.commit()
              
              lastid = mycursor.lastrowid
              #print(lastid)


              sins = "INSERT INTO `submember_tb`(`subm_m_id`, `subm_name`, `subm_contact`, `subm_aadharcard`, `subm_type`, `subm_relation`, `subm_status`, `subm_cdate`, `subm_udate`) VALUES ('"+str(lastid)+"','"+str(mname)+"','"+str(mcontact)+"','"+str(addimg)+"','"+str(stype)+"','"+str(srel)+"','"+str(mstatus)+"','"+cdate+"','"+cdate+"')"
              mydb = getdb()
              mycursor = mydb.cursor()
              #query execute
              mycursor.execute(sins)
              mydb.commit()
              return redirect('vcard_holder')


        else:
            return render(request,'vmember.html',{'msg':msg});    
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def vsubmember(request):
    try:
        if request.GET.get("m_del") != None:

            m_del = request.GET.get("m_del")
            
            dl = "DELETE FROM `submember_tb` where subm_id ='"+str(m_del)+"'"
            # print(ins)
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(dl)
            mydb.commit()
            return redirect('vsubmember')
        else:
            vid = request.session["v_id"]

            sel = "select * from submember_tb, member_tb  where m_v_id = '"+str(vid)+"' and member_tb.m_id = submember_tb.subm_m_id order by subm_id desc"
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(sel)
            myresult = mycursor.fetchall()
            return render(request,'vsubmember.html',{'record': myresult});

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def vsubmember_edit(request):
    try:
      if request.POST:
         m_edt = request.GET.get("m_edt")
         mname = request.POST.get("m_name")
         mcontact = request.POST.get("m_contact")
         subm_relation = request.POST.get("s_relation")  
         if  request.POST.get("vfile1") != "":
            vimage1 = request.FILES["vfile1"]
            img = FileSystemStorage()
            fimg1 = img.save(vimage1.name,vimage1)
         else:
            fimg1 = request.POST.get("old_img1")

         udate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         sup = " UPDATE `submember_tb` SET `subm_name`='"+str(mname)+"',`subm_contact`='"+str(mcontact)+"',`subm_aadharcard`='"+str(fimg1)+"',`subm_udate`='"+udate+"', `subm_relation` = '"+str(subm_relation)+"'  WHERE subm_id = '"+str(m_edt)+"' "
        #  print(sup)
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sup)
         mydb.commit()
         return redirect('vsubmember')

      elif request.GET.get("m_edt") !=None:
         m_id = request.GET.get("m_edt")
         sel = "select * from submember_tb where subm_id='"+str(m_id)+"'"
         # connection create object
         mydb = getdb()
         mycursor = mydb.cursor()
         #query execute
         mycursor.execute(sel)
         myresult = mycursor.fetchall()
         return render(request,'vsubmember_edit.html',{'myresult':myresult});
    except NameError:
      print("internal error")
    except:
      print('Error returned')

def vsubmember_add(request):
    try:
        msg = ""
        if request.POST:
            m_id = request.POST.get("m_id")
            mname = request.POST.get("mname")
            mcontact = request.POST.get("mcontact")
            m_inc_c= request.FILES["maadharcard"]
            img = FileSystemStorage()
            incimg = img.save(m_inc_c.name,m_inc_c)
            s_rel = request.POST.get("s_rel")
            type = 'Sub'
            status = 'Deactive'
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ins = "INSERT INTO `submember_tb`( `subm_m_id`, `subm_name`, `subm_contact`, `subm_aadharcard`, `subm_type`, `subm_relation`, `subm_status`, `subm_cdate`, `subm_udate`) VALUES ('"+str(m_id)+"','"+str(mname)+"','"+str(mcontact)+"','"+str(incimg)+"','"+str(type)+"','"+str(s_rel)+"','"+str(status)+"','"+cdate+"','"+cdate+"')"    
            #print(ins)
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(ins)
            mydb.commit()
            return redirect('vsubmember')
        else:
            vid = request.session["v_id"]
            sel1 = "select * from member_tb where m_v_id = '"+str(vid)+"'"
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(sel1)
            vresult = mycursor.fetchall()

            alldata = {
                    'vresult' : vresult,
                    'msg':msg
                }
            return render(request,'vsubmember_add.html',alldata);
    except NameError:
        print("internal error")
    except:
      print('Error returned')

def vpending(request):
   if request.POST:
      
      vid = request.session["v_id"]
      
      rfid = request.POST.get("rfid")
      
      sel ="select * from ration_tb,category_tb,member_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.r_status = 'Not collected' and member_tb.m_status = 'Active'  and member_tb.rfid_code = '"+(rfid)+"' and member_tb.m_v_id = '"+str(vid)+"' GROUP by ration_tb.c_id"
    # print(sel)
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'vpending.html',{'record': myresult});
      
   return render(request,'vpending.html',{});


def vgive(request):
    msg = "" 
    if request.POST:
        
        vid =   request.session["v_id"]
        vmid = request.GET.get("vm_id")
        rfid = request.POST.get("rfid")
        vcid = request.GET.get("vc_id")
        cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
        sel1 ="select * from member_tb WHERE m_v_id = '"+str(vid)+"' and m_id = '"+str(vmid)+"' and rfid_code = '"+str(rfid)+"'"
        #print(sel)
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel1)
        mydata = mycursor.fetchall()
        
        if len(mydata) > 0:

            dl = "update `ration_tb` set r_status = 'Collected', r_udate = '"+cdate+"' where v_id ='"+str(vid)+"' and c_id = '"+str(vcid)+"' and m_id = '"+str(vmid)+"'"
            #print(dl)
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor()
            #query execute
            mycursor.execute(dl)
            mydb.commit()

            return redirect('vpending')
        else:

            msg = "Invalid RFID..!"
            return render(request,'vgive.html',{'msg' : msg});


    elif request.GET.get("vm_id") !=None:

        vid =   request.session["v_id"]
        vmid = request.GET.get("vm_id")
        vcid = request.GET.get("vc_id")
        
        sel ="select * from ration_tb,member_tb,category_tb,submember_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.r_status = 'Not collected' and ration_tb.v_id = '"+str(vid)+"' and ration_tb.c_id = '"+str(vcid)+"' and ration_tb.m_id = '"+str(vmid)+"' and submember_tb.subm_status = 'Active'"
        #print(sel)
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel)
        myresult = mycursor.fetchall()
        sel1 ="select sum(r_total) from ration_tb,member_tb,category_tb,submember_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.r_status = 'Not collected' and ration_tb.v_id = '"+str(vid)+"' and ration_tb.c_id = '"+str(vcid)+"' and ration_tb.m_id = '"+str(vmid)+"' and submember_tb.subm_status = 'Active'"
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel1)
        mytotal = mycursor.fetchall()
        alldata = {

            'record': myresult,
            'msg' : msg,
            'mytotal' : mytotal,
        }

        return render(request,'vgive.html',alldata);


def vcollected(request):
    if request.POST:
      
      vid = request.session["v_id"]
      
      rfid = request.POST.get("rfid")
      
      sel ="select * from ration_tb,category_tb,member_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.r_status = 'Collected' and member_tb.m_status = 'Active'  and member_tb.rfid_code = '"+(rfid)+"' and member_tb.m_v_id = '"+str(vid)+"' GROUP by ration_tb.c_id"
    # print(sel)
      # connection create object
      mydb = getdb()
      mycursor = mydb.cursor()
      #query execute
      mycursor.execute(sel)
      myresult = mycursor.fetchall()
      return render(request,'vcollected.html',{'record': myresult});
      
    return render(request,'vcollected.html',{});
def vfinal(request):
    if request.GET.get("vm_id") !=None:

        vid =  request.session["v_id"]
        vmid = request.GET.get("vm_id")
        vcid = request.GET.get("vc_id")
        
        sel ="select * from ration_tb,member_tb,category_tb,submember_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.r_status = 'Collected' and ration_tb.v_id = '"+str(vid)+"' and ration_tb.c_id = '"+str(vcid)+"' and ration_tb.m_id = '"+str(vmid)+"' and submember_tb.subm_status = 'Active'"
        #print(sel)
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel)
        myresult = mycursor.fetchall()
        
        sel1 ="select sum(r_total) from ration_tb,member_tb,category_tb,submember_tb WHERE ration_tb.c_id = category_tb.c_id and ration_tb.m_id = member_tb.m_id and ration_tb.s_id = submember_tb.subm_id and ration_tb.r_status = 'Collected' and ration_tb.v_id = '"+str(vid)+"' and ration_tb.c_id = '"+str(vcid)+"' and ration_tb.m_id = '"+str(vmid)+"' and submember_tb.subm_status = 'Active'"
        #print(sel)
        # connection create object
        mydb = getdb()
        mycursor = mydb.cursor()
        #query execute
        mycursor.execute(sel1)
        mytotal = mycursor.fetchall()
        
        alldata = {
            'record': myresult,
            'mytotal' : mytotal
        }
        
        return render(request,'vfinal.html',alldata);

