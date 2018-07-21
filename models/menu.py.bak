response.logo = A(B('HMLibrary'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.iiit.ac.in/")
response.title = 'Library Portal'
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Hemanth Kumar And Murali Krishna'
response.meta.description = 'Welcome to the world of books'
response.meta.keywords = 'Library-portal,hector'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Store'), False, URL('default', 'index'), []),
]
if auth.has_membership('managers'):
   response.menu+=[(SPAN('Update details', _class='highlighted'),False,URL('default','index'),[
    (T('Update Information'), False, URL('default', 'update')),
    (T('Change Password'),False,URL('default','user/change_password')),
    (T('Update Dues'),False,URL('default','updatedues')),
    (T('Paid Due'),False,URL('default','paiddue')),
    (T('Extend Duedate'),False,URL('default','extend')),
    (T('Delete a borrowal record'),False,URL('default','submit')),
]
    )
    ,(SPAN('View', _class='highlighted'),False,URL('default','index'),[
    (T('Pending Purchase Requests'),False,URL('default','pendreq')),
    (T('Pending Due Books'),False,URL('default','penddue')),
    (T('Manage Books'), False, URL('default', 'adminlogin')),
    ])]

if auth.has_membership('user') or auth.has_membership('Faculty'):
    response.menu+=[(SPAN('Options',_class='higlighted'),False,URL('default','index'),[
	((T('Search'),False,URL('default','search'))),
    (T('My Requests'),False,URL('default','myreq',)),
    (T('My Reservations'),False,URL('default','reserve')),
    (T('Reserve a book'),False,URL('default','newreserv')),
    (T('Books Taken'), False, URL('default', 'display')),
    (T('Others borrowals'),False,URL('default','otherreq')),
    (T('Change Password'),False,URL('default','user/change_password')),

])]
if "auth" in locals(): auth.wikimenu()
