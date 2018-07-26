# -*- coding: utf-8 -*-

if not request.env.web2py_runtime_gae:
    # if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    # store sessions and tickets there
    session.connect(request, response, db=db)
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
# (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
# (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()
from gluon.tools import Crud

crud = Crud(db)
# create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user'] = [
    Field('Roll_Number', 'integer', label='UID/Roll Number'),
    Field('Phone_no', requires=IS_MATCH('\d{10}')),
    Field('Fines_due', 'integer', readable=False, writable=False, default=0)
]
auth.settings.create_user_groups = True
auth.define_tables(username=False, signature=False)
db.auth_user.Roll_Number.requires = IS_NOT_IN_DB(db, db.auth_user.Roll_Number)
# configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'zing.mylib@gmail.com'
mail.settings.login = 'zing.mylib@gmail.com:iiit123123'
# configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = None
auth.settings.everybody_group_id = int(9)
auth.settings.login_next = URL('index')

# from gluon.contrib.login_methods.janrain_account import use_janrain
# use_janrain(auth, filename='private/janrain.key')
