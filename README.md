## Library portal
The main purpose of this application is to provide user-
friendly Library Portal for an institute which can be used to digitalise
the records of the books in the library, books taken by
the users,faculty etc

Features Implemented
--------------------

What an user can do?
--------------------

#### Details of books in library

On clicking the store option on the menu bar takes the user to all the
books available in the library.Clicking on the book name takes the user
to the details of the books as shown in the picture.

#### Search across the library

The user can Search the required book by using the search by clilcking
the search option in the options located in the menubar. The user can
search using the name of the book, author of the book,etc.

#### Book reservation

The user has the facility to reserve a book for a particular date so
that he can take the book on the reserved day.This can be done by using
the ’Reserved book’ in the options of the menubar.

#### Cancellation of reservation

The user can see his reservations in the ’My Reservations’ of the
options in the menubar. The user can cancel his reservation for a book
by giving his Borrowal Id from the available reservations shown in the
the users reservations. Both the options are provided here so as to
reduce redirection.

#### Viewing Details of Borrowal/Reservation/Fine due

The user can view the details of his Borrowed books , reserved books and
the fine amount so that the user can pay the fine if any.

#### Others Borrowals

The user can also view others Borrowal’s for the required book by giving
the Book Number.This can be done by using the Others Borrowal available
in the options of the menubar.

#### Request a purchase

The user can request the Librarian to buy the new books by giving the
details of the book such as name an the author of the book.This will be
viewed by the admin and necessaru action would take place.The user can
also the status of the requested books by using the my requests in the
menubar.

What an Admin(Librarian) can do?
--------------------------------

#### Extension of a due date for Borrowal

The due date for a book can be extended for a particular person when the
person comes manually for the extension.This is done by entering the
Borrowal id for the borrowed book. Note:- It gets extended by two days.

#### Manage books in Library

The Librarian can add bood to the database,edit the details of the
books. He can mange the number of copies. He can delete thso books and
Increase or decrease the number of copies.

#### View Purchase Requests and take action

Librarian can view the requests for buying books can take decision for
buying the book.

#### View Book Borrowals and Reservations

The Librarian can view all the records of the books that have been given
to the users and the books that have been reserved by the user.

#### Dealing with due fines and Sending automatic mails

The email is automatically sent on viewing the update dues in the
’update details ’ of the menu .

#### Update paid fines and Submissions

The fines are Updated when the user comes manually to the Librarian to
pay the fine. The paid amount and the UID of the user is entered and the
paid amount is deducted form the fine amount of user.

#### Update Book Borrowals

This is done when the user manually takes a book from the library.The
Librarian enters the book Number and the UID of the user and the book.

Schema of tables and groups and memberships
------------------------------------------

#### Books table

This contains the details of the books in the library i.e. Name of book,
Name of author,Total Books of the library,No of books in the library
etc.

#### Borrowals table

This contains the details of the borrowed books and the reserved books
with due dates ans the reserved dates , the user’s UID etc.

#### Requests table

This contains the details of the requests for buying new books and after
the admin views the status is also stored in the table.

Groups and Memberships
----------------------

There are three Groups in the database.They are Managers,Users,Faculty.

#### Managers

Manager is the Librarian.

#### Users

Users are the students.

#### Faculty

Faculty are same as users but they have special permissions for
borrowing and reserving Reference Books.

Further Scope of Developement
-----------------------------

Grouping of Books
-----------------

Books can be grouped into many more topics such as Novels,Science
Fiction etc.

Automate Tasks
--------------

Using scheduler the mails can be sent automatically, updation of dues
without the initiation of the Librarian.

Adding Online Journals and New Arrivals
---------------------------------------

Online Journals,E-books can be added and a page about New Arrivals Which
can be done by using the added date of Book.

Styling
-------

Including Jquery functions,css,ajax makes the website more responsive
and beautiful.
