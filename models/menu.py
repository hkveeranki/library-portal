response.logo = A(B('HMlibrary'), XML('&trade;&nbsp;'),
                  _class="brand", _href="/")
response.title = 'Library portal'
response.subtitle = 'Institute library management portal'

# read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Hemanth Kumar And Murali Krishna'
response.meta.description = 'Welcome to the world of books'
response.meta.keywords = 'Library-portal,hector'
response.meta.generator = 'Web2py Web Framework'

# your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
# this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Store'), False, URL('default', 'index'), []),
]
if auth.has_membership('managers'):
    response.menu += [
        (SPAN('Update details', _class='highlighted'), False, URL('default', 'index'), [
            (T('Update Information'), False, URL('default', 'update')),
            (T('Change Password'), False, URL('default', 'user/change_password')),
            (T('Update Dues'), False, URL('default', 'update_fines')),
            (T('Paid Due'), False, URL('default', 'record_payment')),
            (T('Extend Duedate'), False, URL('default', 'extend')),
            (T('Delete a borrowal record'), False, URL('default', 'submit')),
        ]
         )
        , (SPAN('View', _class='highlighted'), False, URL('default', 'index'), [
            (T('Pending Purchase Requests'), False, URL('default', 'manage_requests')),
            (T('Pending Due Books'), False, URL('default', 'pend_due')),
            (T('Manage Books'), False, URL('default', 'admin_login')),
        ])]

if auth.has_membership('user') or auth.has_membership('Faculty'):
    response.menu += [
        (SPAN('Options', _class='higlighted'), False, URL('default', 'index'), [
            (T('Search'), False, URL('default', 'search')),
            (T('My requests'), False, URL('default', 'my_requests')),
            (T('Change reservations'), False, URL('default', 'change_reservations')),
            (T('Request a book'), False, URL('default', 'book_request')),
            (T('Reserve a book'), False, URL('default', 'reserve')),
            (T('Books taken'), False, URL('default', 'display')),
            (T('Others borrowals'), False, URL('default', 'other_req')),
            (T('Change password'), False, URL('default', 'user/change_password')),

        ])]
if 'auth' in locals():
    auth.wikimenu()
