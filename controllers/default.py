# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import datetime
def index():
    rows1 = db(db.table1.Category=="Reference Books").select(orderby=db.table1.Publication_Date)
    rows2=db(db.table1.Category=="Normal Books").select(orderby=db.table1.Publication_Date)
    rows3=db(db.table1.Category=="Journals").select(orderby=db.table1.Publication_Date)
    rows4=db(db.table1.Category=="Magazines").select(orderby=db.table1.Publication_Date)
    if auth.user:
        response.flash="Welcome "+auth.user.first_name+", Happy to see you!"
    else:
        response.flash="Welcome Guest!"
    return locals()
@auth.requires_membership('managers')
def update():
    form=SQLFORM.factory(
                         Field('Book_Number',requires=IS_IN_DB(db,db.table1.book_number)),
                         Field('Roll_Number','integer',requires=IS_NOT_EMPTY()),
                         ).process()
    form['_class']="cls"
    if form.accepted:
        a=form.vars.Book_Number
        b=form.vars.Roll_Number
        c=datetime.datetime.now().date()
        var1=db((db.table1.book_number==a)).select()
        var2=db(db.auth_user.Roll_Number==b).select()
        var3=db((db.tableb.book_number==a)&(db.tableb.Rollno==b)).select()
        end=c+datetime.timedelta(7)
        if(len(var1)==1 and len(var2)==1):
            name=var2[0].first_name+" "+var2[0].last_name
            if(len(var3)==0):
                email1=var2[0].email
                phone1=var2[0].Phone_no
                numleft=var1[0].num_of_copies_left
                db(db.tableb.insert(book_name=var1[0].book_name,book_number=a,book_issued_to=name,Rollno=b,email=email1,Phone_No=phone1,Date_of_Issue=c,Due_Date=end,Status="Taken"))
                content=name+". Your entry for borrowing the book "+var1[0].book_name+" with number "+a+" has been successfully entered into records. Your Due date is "+str(end)+". \nCheers,\n Library portal Team.\n"
                mail.send([email1],subject="Book Borrowal Operation Complete",message=content)
                var1[0].update_record(num_of_copies_left=numleft-1)
                response.flash="Successfully Added the entry"
            else:
                response.flash="Such entry already exists"
        else:
            response.flash="Invalid details"
    return dict(form=form)
def otherreq():
    if auth.has_membership('user') or auth.has_membership('Faculty'):
        form=SQLFORM.factory(Field('Book_Number')).process()
        form['_class']="cls1"
        if (form.accepted):k=db(~(db.tableb.email==auth.user.email)&(db.tableb.book_number==form.vars.Book_Number)).select(orderby=db.tableb.book_name.lower())
    else:
        response.flash="Insufficient Privillages"
        form=""
    return locals()
def view():
    num=request.args(0,cast=int)
    name="Author Name"
    item=db(db.table1.book_number==num).select().first()
    var=item.Author_Name.split(',')
    if(len(var)>1):name="Authors Names"
    if item.Category=="Magazines" or item.Category=="Journals":name="Publisher Name"
    return dict(item=item,name=name)
def user():
    if (auth.user and request.url.split('/')[-1]=="login"):redirect(URL('default','index'))
    return dict(form=auth())
@auth.requires_membership('managers')
def extend():
    form=SQLFORM.factory(Field('Borrowal_Id',requires=IS_IN_DB(db,db.tableb.id)),
                         ).process()
    form['_class']="cls1"
    if(form.accepted):
        var1=form.vars.Borrowal_Id
        var=db((db.tableb.id==var1)&(db.tableb.Status=="Taken")).select()
        if(len(var)==1):
            var2=db(db.tableb.id==var1).select().first()
            p=var[0].Due_Date
            x=p+datetime.timedelta(2)
            var2.update_record(Due_Date=x)
            name=var[0].book_issued_to
            response.flash="Successfully Extended the borrowal with  id "+str(var1)+" by two days"
            content=name+". Your entry Due Date for the book "+var[0].book_name+" has been successfully Extended by two days. Your new Due date is "+str(x)+".\n Cheers,\n Library portal Team.\n"
            mail.send([var[0].email],subject="Book Borrowal Operation Complete",message=content)
        else:
            response.flash="Invalid Details"
            
    return locals()
@auth.requires_membership('managers')
def submit():
    form=SQLFORM.factory(Field('Borrowal_Id','integer')).process()
    form['_class']="cls2"
    if(form.accepted):
        a=form.vars.Borrowal_Id
        var=db(db.tableb.id==a).select()
        if(len(var)!=1):
            response.flash="Invalid Id"
        else:
            db(db.tableb.id==a).delete()
            response.flash="Successfully deleted the entry"
            name1=var[0].book_issued_to
            var1=db(db.table1.book_number==int(var[0].book_number)).select().first()
            num=int(var1.num_of_copies_left)
            numn=num+1
            var1.update_record(num_of_copies_left=numn)
            content=name1+".\nYour submission of rented book "+var[0].book_name+" has been recorded successfully.Your entry from borrowal id has been deleted.\nCheers,\n Library Portal Team.\n"
            mail.send([var[0].email],subject="Book Submission Operation Complete",message=content)
    return locals()
@auth.requires_membership('managers')
def penddue():
    k=db(db.tableb).select()
    return locals()
def newreserv():
    if auth.has_membership('user') or auth.has_membership('Faculty'):
        form1=SQLFORM.factory(
                       Field('Book_Number',requires=IS_IN_DB(db,db.table1.book_number)),
                       Field('Reservation_Date','date')
                       ).process()
        content=" "
        form1['_class']="cls"
        if(form1.accepted):
            var=form1.vars.Book_Number
            now1=form1.vars.Reservation_Date
            end=now1+datetime.timedelta(7)
            var2=auth.user.Roll_Number
            var1=db(db.table1.book_number==var).select()
            var2=db(db.table1.book_number==var).select().first()
            var3=db((db.tableb.book_number==var)&(db.tableb.email==auth.user.email)).select()
            l=var1[0].Category
            name1=auth.user.first_name+" "+auth.user.last_name
            p=(now1>datetime.datetime.now().date())
            s=True
            numleft=int(var1[0].num_of_copies_left)
            if(l=="Reference Books"):
               if auth.has_membership('Faculty'):s=True
               else :s=False
            if(l=="Journals" or l=="Magazines"):s=False
            if(len(var3)==0):
                if( numleft>1and p==True): 
                    if (s==True):
                        db(db.tableb.insert(book_issued_to=name1,book_number=var,book_name=var1[0].book_name,Rollno=auth.user.Roll_Number,email=auth.user.email,Phone_No=auth.user.Phone_no,Date_of_Issue=now1,Due_Date=end,Status="Reserved"))

                    
                        var2.update_record(num_of_copies_left=numleft-1)
                        content=name1+". Your reservation for the book "+var1[0].book_name+" with number "+str(var)+" is successfull. You can take your book on reservation date "+str(now1)+".Your due date is "+str(end)+".\n Cheers,\nLibrary portal Team.\n"
                        mail.send([auth.user.email],subject="Reservation Complete",message=content)
                        response.flash="Reservation Successfull.Email Sent"
                    else:
                        response.flash="Sorry You dont have permission to borrow that book."
                else:
                    response.flash="Sorry Requested book is not available at given time.You can come back later.Sorry for the inconvinence caused."
            else:
                response.flash="Sorry You have already taken or Reserved that book."
    else:
        response.flash="Sorry Insufficient privillages."
        form1=""
    return locals()
def myreq():
    if auth.has_membership('user') or auth.has_membership('Faculty'):
        form=SQLFORM.factory(
                        Field('Book_Name',requires=IS_NOT_EMPTY()),
                        Field('Author_Name',requires=IS_NOT_EMPTY())
                        ).process()
        form['_class']="cls"
        if(form.accepted):
            var3=form.vars.Book_Name
            var4=form.vars.Author_Name
            var1=db((db.table1.book_name.lower()==var3.lower()) &(db.table1.Author_Name.lower()==var4.lower())).select()
            var=db((db.requests.bookname.lower()==form.vars.Book_Name.lower()) & (db.requests.Author_Name.lower()==form.vars.Author_Name.lower())).select()
            if(len(var)==0 and len(var1)==0):
                      response.flash="Form Accepted"
                      message="Your request for the book "+var3+" has been processed We will comeback to you as Soon as possible"
                      db(db.requests.insert(bookname=form.vars.Book_Name,Author_Name=form.vars.Author_Name,email=auth.user.email,Status="Not Seen"))
            elif(len(var)!=0): 
                       response.flash="Such Query already exists"
            elif(len(var1)!=0):
                       response.flash="Such Book already exists"
        k = db(db.requests.email==auth.user.email).select()
    else:
        response.flash="Insufficient Privillages."
        k=""
        form=""
    return dict(k=k,form=form)
@auth.requires_membership('managers')
def pendreq():
    form=SQLFORM.grid(db.requests.Status=="Not Seen")
    rows1=db(db.requests.Status=="To be Purchased").select()
    rows2=db(db.requests.Status=="Declined").select()
    return locals()
@auth.requires_membership('managers')
def adminlogin():
        grid=SQLFORM.smartgrid(db.table1)
        return dict(grid=grid)
def display():
    if auth.has_membership('user') or auth.has_membership('Faculty'):
        k = db((db.tableb.email==auth.user.email)&(db.tableb.Status=="Taken")).select()
    else:
        response.flash="No sufficient privillages"
        k=""
    return locals()
def login():
    return locals()
def reserve():
    if auth.has_membership('user') or auth.has_membership('Faculty'):
        grid=db((db.tableb.email==auth.user.email )&(db.tableb.Status=="Reserved")).select()
        form=SQLFORM.factory(
                        Field('Reservation_Id',requires=IS_IN_DB(db,db.tableb.id))
                        ).process()
        form['_class']="cls4"
        if(form.accepted):
            var=form.vars.Reservation_Id
            var1=db((db.tableb.id==var)&(db.tableb.Status=="Reserved")&(db.tableb.email==auth.user.email)).select()
            name1=auth.user.first_name+" "+auth.user.last_name
            if(len(var1)==1):
                p=var1[0].book_number
                s=db(db.table1.book_number==p).select()
                num=int(s[0].num_of_copies_left)+1
                row=db(db.table1.book_number==p).select().first()
                row.update_record(num_of_copies_left=num)
                db(db.tableb.id==var).delete()
                grid=db((db.tableb.email==auth.user.email )&(db.tableb.Status=="Reserved")).select()
                response.flash="Successfully cancelled your reservation for the book "+s[0].book_name+"."
                content=name1+". Your reservation for the book "+s[0].book_name+" is successfully cancelled.\n Cheers"
                mail.send([auth.user.email],subject="Reservation Cancellation Successfull",message=content)
            else:
                response.flash="Sorry That Borrowal Id doesnt belong to yourself !."
    else:
        form=""
        grid=""
        response.flash="Insufficient privillages."
    return dict(form=form,grid=grid)
def call():
    return service()
@auth.requires_membership('managers')
def updatedues():
    amount=10
    now=datetime.datetime.now().date()
    rows=db(db.tableb.Due_Date<now).select()
    var=db(db.tableb.Due_Date==now+datetime.timedelta(4)).select()
    var1=db(db.tableb.Due_Date==now+datetime.timedelta(1)).select()
    lis=[]
    lis1=[]
    lis2=[]
    for item in rows:
        p=db(db.auth_user.Roll_Number==item.Rollno).select().first()
        ap=int(p.Fines_due)
        p.update_record(Fines_due=ap+amount)
        lis.append(p)
        name1=p.first_name+" "+p.last_name
        content=name1+". Your Borrowal for the book \""+item.book_name+"\" has resulted an extra due fine of Rs "+str(amount)+". Please Return the book soon. For more details log onto Library Portal.\nCheers,\nLibrary Portal Team.\n"
        sub="Due fine for book borrowal."
        mail.send([p.email],subject=sub,message=content)
    for j in var:
        p=db(db.auth_user.Roll_Number==j.Rollno).select().first()
        lis1.append(p)
        name1=p.first_name+" "+p.last_name
        content=name1+". Your Borrowal for the book \""+j.book_name+"\" has a due date 4 days from today.Please Return the book on the due date. For more details log onto Library Portal.\nCheers,\nLibrary Portal Team.\n"
        sub="Due date for the book you have borrowed"
        mail.send([p.email],subject=sub,message=content)
    for i in var1:
        p=db(db.auth_user.Roll_Number==i.Rollno).select().first()
        lis2.append(p)
        name1=p.first_name+" "+p.last_name
        content=name1+". Your Borrowal for the book \""+i.book_name+"\" has a due date on tomorrow.Please Return the book Tomorrow to avoid Fine due and also avoid inconvinience for others.Else request a extension for Due date.For more details log onto Library Portal.\nCheers,\nLibrary Portal Team.\n"
        sub="Due date for the book you have borrowed"
        mail.send([p.email],subject=sub,message=content)
    return dict(lis=lis,lis1=lis1,lis2=lis2)
@auth.requires_membership('managers')
def paiddue():
    form=SQLFORM.factory(Field('Roll_Number','integer',requires=IS_NOT_EMPTY()),
                         Field('Paid_Amount','integer',requires=IS_NOT_EMPTY())
                         ).process()
    mess=""
    form['_class']="cls3"
    if(form.accepted):
        a=int(form.vars.Roll_Number)
        b=int(form.vars.Paid_Amount)
        var=db(db.auth_user.Roll_Number==a).select()
        if(b<=0):response.flash="Amount should be positive"
        elif(len(var)!=1):response.flash="Sorry Roll Number is invalid"
        else:
            name1=var[0].first_name+" "+var[0].last_name
            due=int(var[0].Fines_due)
            bal=due-b
            if(bal<0):bal=0
            var[0].update_record(Fines_due=bal)
            response.flash="Successfully Changed Due."
            mess="The Balance due for the user "+name1+" is Rs "+str(bal)+"."
            sub="Payment for the due fine successful."
            content=name1+",\nYour Payment for Fine Due is successfull. Your Current due fine balance is "+str(bal)+".\nCheers,\n Library Portal Team.\n"
            mail.send([var[0].email],subject=sub,message=content)
    return locals()
@auth.requires_login()
def search():
     form,rows=crud.search(db.table1,chkall=True,flash="Search is Successful",fields=['book_name','book_number','Publication_Date','num_of_copies_bought','num_of_copies_left','Author_Name'])
     form['_class']="cls1"
     return locals()
def download():
    return response.download(request, db)
@auth.requires_login() 
def api():
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
