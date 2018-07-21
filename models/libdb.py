db.define_table('table1',
                Field('book_name','string',requires=IS_NOT_EMPTY()),
                Field('book_number','integer',unique=True),
                Field('Publication_Date','date'),
                Field('num_of_copies_bought','integer'),
                Field('num_of_copies_left','integer'),
                Field('Author_Name','string'),
                Field('image','upload',readable=False),
                Field('image_file','blob',readable=False),
                Field('Category',requires=IS_IN_SET(['Reference Books','Normal Books','Magazines','Journals'])),
                )
db.define_table('tableb',
                Field('book_name','string'),
                Field('book_number','integer',readable=False,writable=False),
                Field('book_issued_to','string',requires=IS_NOT_EMPTY(),readable=False,writable=False),
                Field('Rollno','integer','reference auth_user',requires=IS_IN_DB(db,db.auth_user.Roll_Number)),
                Field('email','string',requires=IS_EMAIL(),readable=False,writable=False),
                Field('Phone_No','integer',requires=IS_MATCH('\d{10}'),readable=False,writable=False),
                Field('Date_of_Issue','date'),
                Field('Due_Date','date',readable=False,writable=False),
                Field('Status',requires=IS_IN_SET(['Reserved','Taken'])),
                )
db.tableb.book_number.requires=IS_IN_DB(db,db.table1.book_number)
db.define_table('requests',
               Field('bookname','string',requires=IS_NOT_EMPTY()),
               Field('Author_Name','string',requires=IS_NOT_EMPTY()),
               Field('email',readable=False,writable=False),
               Field('Status',requires=IS_IN_SET(['Not Seen','To be Purchased','Declined']),writable=True)
               )
db.requests.bookname.requires=IS_NOT_IN_DB(db,db.table1.book_name)
