# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('mysql://root:@localhost/erp_crm_db',migrate=True,migrate_enabled=configuration.get('db.migrate'),check_reserved=['all'])

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# db.define_table(
#     'crm_contact_type',
#     Field('customer_type',type='string',length=250, required=True, notnull=True),
#     Field('is_active',type='boolean',default=True, required=True, notnull=True),
#     Field('db_entry_time', type='datetime',  required=True, notnull=True),
#     Field('db_entered_by', type='integer',required=False,notnull=False),
#     Field('db_update_time', type='datetime', notnull=False),
#     Field('db_updated_by',type='integer',required=False,notnull=False),
#     Field('company_id',type='integer',required=True,notnull=True)
# )
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ COMPANY

db.define_table(
    'crm_company_field_key',
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)


db.define_table(
    'crm_company_field',
    Field('company_id',type='integer',required=True,notnull=True),
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('sequence_no',type='integer',default=0,required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_widget_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_requires_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_suggestion_attributes',type='string',length=500,required=False,notnull=False),            
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_company_field_value',
    Field('field_id',db.crm_company_field),
    Field('company_key_id',db.crm_company_field_key),
    Field('company_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True), # to represent that data is present or deleted
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CONTACT

db.define_table(
    'crm_contact_field_key',
    Field('company_key_id',type='integer',required=False,notnull=False),
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)


db.define_table(
    'crm_contact_field',
    Field('company_id',type='integer',required=True,notnull=True),
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('sequence_no',type='integer',default=0,required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_widget_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_requires_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_suggestion_attributes',type='string',length=500,required=False,notnull=False),            
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_contact_field_value',
    Field('field_id',db.crm_contact_field),
    Field('contact_key_id',db.crm_contact_field_key),
    Field('company_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True), # to represent that data is present or deleted
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LEAD
db.define_table(
    'crm_lead_status',
    Field('lead_status',type='string',length=250, required=True, notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
    Field('company_id',type='integer',required=True,notnull=True)
)

db.define_table(
    'crm_lead_field_key',
    Field('contact_key_id',db.crm_contact_field_key),
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_lead_field',
    Field('company_id',type='integer',required=True,notnull=True),
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('sequence_no',type='integer',default=0,required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_widget_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_requires_attributes',type='string',length=500,required=False,notnull=False),
    Field('field_suggestion_attributes',type='string',length=500,required=False,notnull=False),            
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_lead_field_value',
    Field('field_id',db.crm_lead_field),
    Field('lead_key_id',db.crm_lead_field_key),
    Field('company_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True), # to represent that data is present or deleted
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DEAL
db.define_table(
    'crm_deal_field_key',
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)


db.define_table(
    'crm_deal_field',
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_values',type='string',length=250,required=False,notnull=False),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
    Field('company_id',type='integer',required=True,notnull=True)
)

db.define_table(
    'crm_deal_field_value',
    Field('field_id',db.crm_deal_field),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('deal_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ EVENT
db.define_table(
    'crm_events_field_key',
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_events_field',
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_values',type='string',length=250,required=False,notnull=False),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
    Field('company_id',type='integer',required=True,notnull=True)
)

db.define_table(
    'crm_events_field_value',
    Field('field_id',db.crm_events_field),
    Field('event_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CAMPAIGN
db.define_table(
    'crm_campaign_field_key',
    Field('user_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)


db.define_table(
    'crm_campaign_field',
    Field('feature_id',type='integer', required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('form_name',type='string',length=250,required=True,notnull=True),
    Field('field_name',type='string',length=500,required=False,notnull=False),
    Field('field_values',type='string',length=250,required=False,notnull=False),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False),
    Field('company_id',type='integer',required=True,notnull=True)
)

db.define_table(
    'crm_campaign_field_value',
    Field('field_id',db.crm_campaign_field),
    Field('campaign_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('field_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False),
    Field('db_update_time', type='datetime', notnull=False),
    Field('db_updated_by',type='integer',required=False,notnull=False)
)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ AUDIT
db.define_table(
    'crm_audit_trail',
    Field('table_name',type='string',length=500,required=True,notnull=True),
    Field('audit_datetime',type='datetime',required=True,notnull=True),
    Field('user_id',type='integer',required=True,notnull=True),
    Field('company_id',type='integer',required=True,notnull=True),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('function_operation',type='string',length=500,required=True,notnull=True),
    Field('instance_key',type='string',length=500,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False)
)

db.define_table(
    'crm_audit_trail_value',
    Field('audit_trail_id',db.crm_audit_trail),
    Field('session_id',type='integer',required=True,notnull=True),
    Field('col_name',type='string',length=500,required=True,notnull=True),
    Field('old_value',type='string',length=1000,required=True,notnull=True),
    Field('new_value',type='string',length=1000,required=True,notnull=True),
    Field('is_active',type='boolean',default=True, required=True, notnull=True),
    Field('db_entry_time', type='datetime',  required=True, notnull=True),
    Field('db_entered_by', type='integer',required=False,notnull=False)
)

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
auth.enable_record_versioning(db)
