# -*- coding: utf-8 -*-

import datetime

from dateutil import parser


def index():
    """
    Render index page of the library app
    :return: data to be displayed in `index` page
    """
    categories = ['Reference Books', 'Normal Books', 'Journals', 'Magazines']
    results = {}

    for category in categories:
        db_results = db(db.table1.Category == category).select(
            orderby=db.table1.Publication_Date)
        if db_results:
            results[category] = db_results

    return locals()


@auth.requires_membership('managers')
def update():
    """
    Handle updating operations on a book borrow record
    :return: form for requesting a borrow
    """
    form = SQLFORM.factory(
        Field('Book_Number', requires=IS_IN_DB(db, db.table1.book_number)),
        Field('Roll_Number', 'integer', requires=IS_NOT_EMPTY()),
    ).process()
    form['_class'] = "cls"
    if form.accepted:
        a = form.vars.Book_Number
        b = form.vars.Roll_Number
        c = datetime.datetime.now().date()
        var1 = db((db.table1.book_number == a)).select()
        var2 = db(db.auth_user.Roll_Number == b).select()
        var3 = db((db.tableb.book_number == a) & (db.tableb.Rollno == b)).select()
        end = c + datetime.timedelta(7)
        if len(var1) >= 1 or len(var2) >= 1:
            response.flash = 'Invalid details'
        elif len(var3) != 0:
            response.flash = 'Such entry already exists'
        else:
            var2 = var2[0]
            var1 = var1[0]
            name = var2.first_name + ' ' + var2.last_name
            email1 = var2.email
            phone1 = var2.Phone_no
            num_left = var1.num_of_copies_left
            db(db.tableb.insert(book_name=var1.book_name, book_number=a,
                                book_issued_to=name, Rollno=b, email=email1,
                                Phone_No=phone1, Date_of_Issue=c, Due_Date=end,
                                Status='Taken'))
            content = ('%s. Your entry for borrowing the book titled %s with'
                       'number %s has been successfully entered into records.'
                       'Your Due date is %s.'
                       '\nCheers,\n Library portal team.\n' % (
                           name, var1.book_name, a, str(end)))
            mail.send([email1], subject='Book Borrow Operation Complete',
                      message=content)
            var1[0].update_record(num_of_copies_left=num_left - 1)
            response.flash = 'Successfully Added the entry'

    return dict(form=form)


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def other_req():
    """
    Display list of borrowals for given the book number
    """
    form = SQLFORM.factory(Field('Book_Number')).process()
    form['_class'] = 'cls1'
    if form.accepted:
        records = db(~(db.tableb.email == auth.user.email) & (
                db.tableb.book_number == form.vars.Book_Number)).select(
            orderby=db.tableb.book_name.lower())
    return locals()


def view():
    """
    Display information about an item in library
    """
    num = request.args(0, cast=int)
    name = 'Author Name'
    item = db(db.table1.book_number == num).select().first()
    var = item.Author_Name.split(',')
    if len(var) > 1:
        name = 'Authors Names'
    if item.Category == 'Magazines' or item.Category == 'Journals':
        name = 'Publisher Name'
    return dict(item=item, name=name)


def user():
    if auth.user and request.url.split('/')[-1] == "login":
        redirect(URL('default', 'index'))
    return dict(form=auth())


@auth.requires_membership('managers')
def extend():
    """
    Extend due date for a particular borrowal record
    """
    form = SQLFORM.factory(Field('Borrowal_Id', requires=IS_IN_DB(db, db.tableb.id)),
                           ).process()
    form['_class'] = "cls1"
    if form.accepted:
        var1 = form.vars.Borrowal_Id
        var = db((db.tableb.id == var1) & (db.tableb.Status == "Taken")).select()
        if len(var) == 1:
            var2 = db(db.tableb.id == var1).select().first()
            p = var[0].Due_Date
            x = p + datetime.timedelta(2)
            var2.update_record(Due_Date=x)
            name = var[0].book_issued_to
            response.flash = 'Successfully Extended the borrowal with id %s ' \
                             'by two days' % str(var1)
            content = (
                    '%s,\nYour entry Due Date for the book %s has been'
                    'successfully Extended by two days. Your new Due date is'
                    '%s.\n Cheers,\n Library portal team.\n' % (
                        name, var[0].book_name, str(x)))
            mail.send([var[0].email], subject='Due date extension Complete',
                      message=content)
        else:
            response.flash = 'Invalid Details'

    return locals()


@auth.requires_membership('managers')
def submit():
    """
    Handle return of a borrowed book
    """
    form = SQLFORM.factory(Field('Borrowal_Id', 'integer')).process()
    form['_class'] = 'cls2'
    if form.accepted:
        a = form.vars.Borrowal_Id
        var = db(db.tableb.id == a).select()
        if len(var) != 1:
            response.flash = 'Invalid Id'
        else:
            db(db.tableb.id == a).delete()
            response.flash = 'Successfully deleted the entry'
            name1 = var[0].book_issued_to
            var1 = db(db.table1.book_number == int(var[0].book_number)).select().first()
            num = int(var1.num_of_copies_left)
            numn = num + 1
            var1.update_record(num_of_copies_left=numn)
            content = ('%s,\nYour submission of rented book %s has been recorded'
                       'successfully.\nCheers,\nLibrary portal team.\n ' % (
                           name1, var[0].book_name))
            mail.send([var[0].email], subject='Book Submission Operation Complete',
                      message=content)
    return locals()


@auth.requires_membership('managers')
def pend_due():
    """
    Return pending due records from the database
    """
    records = db(db.tableb).select()
    return locals()


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def reserve():
    """
    Handle book reservation operation
    """
    form = SQLFORM.factory(
        Field('Book_Number', requires=IS_IN_DB(
            db((db.table1.Category != 'Journals') & (db.table1.Category != 'Magazines')),
            db.table1.book_number, '%(book_name)s', zero=T('Choose a book')),
              required=True),
        Field('Reservation_Date', 'date', required=True)).process()

    form['_class'] = "cls"
    if form.accepted:
        book_number = form.vars.Book_Number
        requested_date = parser.parse(form.vars.Reservation_Date).date()
        book_record = db(db.table1.book_number == book_number).select().first()
        category = book_record.Category
        user_name = auth.user.first_name + " " + auth.user.last_name
        num_left = int(book_record.num_of_copies_left)

        if category == 'Reference Books' and not auth.has_membership('Faculty'):
            response.flash = 'Reference books can be borrowed by faculty only'
            return locals()

        if num_left < 1:
            response.flash = 'Requested book is not available at given time.' \
                             'You can come back later'
            return locals()

        if requested_date < datetime.datetime.now().date():
            response.flash = 'Requested date is in the past'
            return locals()

        borrow_record = db((db.tableb.book_number == book_number) & (
                db.tableb.email == auth.user.email)).select()
        if len(borrow_record) != 0:
            response.flash = "You have already taken or reserved this book."
            return locals()

        due_date = requested_date + datetime.timedelta(7)
        db(db.tableb.insert(book_issued_to=user_name, book_number=book_number,
                            book_name=book_record.book_name,
                            Rollno=auth.user.Roll_Number,
                            email=auth.user.email,
                            Phone_No=auth.user.Phone_no,
                            Date_of_Issue=requested_date,
                            Due_Date=due_date,
                            Status="Reserved"))
        book_record.update_record(num_of_copies_left=num_left - 1)
        content = ('%s,\nYour reservation for the book %s is successful.'
                   'You can collect it on %s. Your due date is %s.\n'
                   'Cheers,\nLibrary portal team.\n'
                   % (
                       user_name, book_record.book_name, str(requested_date),
                       str(due_date)))
        mail.send([auth.user.email], subject="Reservation Complete",
                  message=content)
    return locals()


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def my_requests():
    """
    Return book requests user has already made
    """
    records = db(db.requests.email == auth.user.email).select()
    return locals()


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def book_request():
    """
    Handle a book request operation
    """
    form = SQLFORM.factory(
        Field('Book_Name', requires=IS_NOT_EMPTY(), required=True),
        Field('Author_Name', requires=IS_NOT_EMPTY(), required=True)).process()
    form['_class'] = 'cls'

    if form.accepted:
        book_name = form.vars.Book_Name.lower()
        author_name = form.vars.Author_Name.lower()
        book_data = db((db.table1.book_name.lower() == book_name) & (
                db.table1.Author_Name.lower() == author_name)).select()
        request_records = db(
            (db.requests.bookname.lower() == book_name) & (
                    db.requests.Author_Name.lower() == author_name)).select()
        if len(request_records) == 0 and len(book_data) == 0:
            response.flash = 'Form Accepted'
            message = ('Your request for the book %s has been recorded.'
                       'It will be considered in the next purchase' % book_name)
            db(db.requests.insert(bookname=form.vars.Book_Name,
                                  Author_Name=form.vars.Author_Name,
                                  email=auth.user.email, Status='Not Seen'))
        elif len(request_records) != 0:
            response.flash = 'The book has already been requested'
        elif len(book_data) != 0:
            response.flash = 'Book already exists in the library'
    return locals()


@auth.requires_membership('managers')
def manage_requests():
    """
    Display book requests to the managers
    """
    form = SQLFORM.grid(db.requests.Status == "Not Seen")
    rows1 = db(db.requests.Status == "To be Purchased").select()
    rows2 = db(db.requests.Status == "Declined").select()
    return locals()


@auth.requires_membership('managers')
def admin_login():
    """
    Handle updates to books in library
    """
    grid = SQLFORM.smartgrid(db.table1)
    return dict(grid=grid)


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def display():
    """
    Display books taken by users
    """
    records = db(
        (db.tableb.email == auth.user.email) & (db.tableb.Status == "Taken")).select()
    return locals()


def login():
    return locals()


@auth.requires(auth.has_membership(auth.id_group('user')) or auth.has_membership(
    auth.id_group('Faculty')))
def change_reservations():
    """
    Handle cancelling of reservations
    """
    form = SQLFORM.factory(
        Field('Reservation_Id',
              requires=IS_IN_DB(
                  db((db.tableb.email == auth.user.email)
                     & (db.tableb.Status == "Reserved")),
                  db.tableb.id,
                  zero=T('Choose one')))
    ).process()
    form['_class'] = "cls4"
    if form.accepted:
        reservation_id = form.vars.Reservation_Id
        reservation_record = db((db.tableb.id == reservation_id)).select().first()
        name1 = auth.user.first_name + " " + auth.user.last_name
        book_number = reservation_record.book_number
        book_record = db(db.table1.book_number == book_number).select().first()
        num = int(book_record.num_of_copies_left) + 1
        book_record.update_record(num_of_copies_left=num)
        reservation_record.delete_record()
        content = (
                '%s,\nYour reservation for the book %s has been cancelled\n'
                'Cheers,\nLibrary portal team.\n' % (name1, book_record.book_name))
        mail.send([auth.user.email], subject="Reservation cancellation successful",
                  message=content)
    grid = db((db.tableb.email == auth.user.email) & (
            db.tableb.Status == "Reserved")).select()
    to_return = {'grid': grid, 'form': None}
    if len(grid) != 0:
        to_return['form'] = form
    return to_return


def call():
    return service()


@auth.requires_membership('managers')
def update_fines():
    """
    Update fines for users based on due date
    Also remind users with due date as tomorrow
    """
    fine = 10
    now = datetime.datetime.now().date()
    rows = db(db.tableb.Due_Date < now).select()
    fined_users_count = len(rows)
    fined_message = '%d users have been fined today' % fined_users_count \
        if fined_users_count != 0 else 'No outstanding dues'
    fined_users = ([], fined_message, fined_users_count)
    subject = 'Fine for book borrowal.'
    for item in rows:
        user_record = db(db.auth_user.Roll_Number == item.Rollno).select().first()
        amount = fine * (now - item.Due_Date).days
        user_record.update_record(Fines_due=amount)
        fined_users[0].append(user_record)
        user_name = ' '.join([user_record.first_name, user_record.last_name])
        content = ('%s,\n'
                   'Your borrowal for the book %s has a total of Rs %s fine. '
                   'Return the book and pay the fine to avoid extra fines. '
                   'For more details, log onto library portal.\n'
                   'Cheers,\n'
                   'Library portal team\n' % (user_name, item.book_name, str(amount)))
        mail.send([user_record.email], subject=subject, message=content)

    var1 = db(db.tableb.Due_Date == now + datetime.timedelta(1)).select()
    reminded_users_count = len(var1)
    reminded_message = '%d users having due on tomorrow have been reminded' % (
        reminded_users_count) if reminded_users_count != 0 \
        else 'No users have due date on tomorrow'
    reminded_users = ([], reminded_message, reminded_users_count)
    subject = 'Reminder for book due date'
    for item in var1:
        user_record = db(db.auth_user.Roll_Number == item.Rollno).select().first()
        reminded_users[0].append(user_record)
        user_name = user_record.first_name + " " + user_record.last_name
        content = ('%s,\n'
                   'Your borrowal for the book %s has due date on tomorrow. '
                   'Return the book tomorrow or request for a due date extension.'
                   ' For more details, log onto library portal.\n'
                   'Cheers,\n'
                   'Library portal team.\n' % (user_name, item.book_name))
        mail.send([user_record.email], subject=subject, message=content)

    data = dict(fined_users=fined_users, reminded_users=reminded_users)

    return dict(data=data)


@auth.requires_membership('managers')
def record_payment():
    """
    Record a fine payment and delete fine data from users
    """
    form = SQLFORM.factory(Field('Roll_Number', 'integer', requires=IS_NOT_EMPTY()),
                           Field('Paid_Amount', 'integer', requires=IS_NOT_EMPTY())
                           ).process()
    message = ""
    form['_class'] = "cls3"
    if form.accepted:
        roll_number = int(form.vars.Roll_Number)
        amount_paid = int(form.vars.Paid_Amount)
        user_record = db(db.auth_user.Roll_Number == roll_number).select()
        if amount_paid <= 0:
            response.flash = 'Amount should be positive'
        elif len(user_record) != 1:
            response.flash = 'Invalid roll number'
        else:
            user_record = user_record[0]
            user_name = ' '.join([user_record.first_name, user_record.last_name])
            due = int(user_record.Fines_due)
            balance = max(0, due - amount_paid)
            user_record.update_record(Fines_due=balance)
            response.flash = 'Payment recorded successfully.'
            message = 'The Balance due for the user %s is Rs %s' % (
                user_name, str(balance))
            subject = 'Payment for the due fine successful.'
            content = ('%s,\n'
                       'Your payment of %s amount towards fine is successful. '
                       'Remaining fine due balance is %s.\n'
                       'Cheers,\n'
                       'Library portal team\n' % (user_name, amount_paid, balance))
            mail.send([user_record.email], subject=subject, message=content)
    return locals()


@auth.requires_login()
def search():
    """
    Handle search operation
    """
    form, rows = crud.search(db.table1, chkall=True, fields=['book_name',
                                                             'book_number',
                                                             'Publication_Date',
                                                             'num_of_copies_bought',
                                                             'num_of_copies_left',
                                                             'Author_Name'])
    form['_class'] = "cls1"
    return locals()


def download():
    return response.download(request, db)


@auth.requires_login()
def api():
    import gluon.contrib.hypermedia
    rules = {
        '<tablename>': {'GET': {}, 'POST': {}, 'PUT': {}, 'DELETE': {}},
    }
    return gluon.contrib.hypermedia.Collection(db).process(request, response, rules)
