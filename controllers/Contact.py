
from datetime import datetime
from gluon.tools import Service
service = Service(globals())
import _pickle as cPickle
from xmlrpc.server import SimpleXMLRPCServer
#import xmlrpc.client as xmlrpclib

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def string(data):
	out=data['email_id']+data['password']
	return out
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# function to get the field names to show the form
@service.xmlrpc
def contact_add_ff():
		field_names={'field':'value'}
		rows = db(db.crm_contact_field.is_active==True).select()
		lList=[]
		for row in rows:

			lList=[row.field_widget_attributes,row.field_requires_attributes] 		# make a list of required details for the field

			field_names.update({row.field_name:lList})

		del field_names['field']
		return dict(field_names)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_contact(lLimit):	# limit is a dict 

	try:
		# get the key values according to the request
		keys=db(db.crm_contact_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
		
		# select the field and there respective values according to the request, using the inner join
		contact= db(db.crm_contact_field_value.field_id==db.crm_contact_field.id)(db.crm_contact_field_value.contact_id<=keys[0].id)(db.crm_contact_field_value.contact_id>=keys[-1].id).select(db.crm_contact_field_value.contact_id,db.crm_contact_field_value.field_value,db.crm_contact_field.field_name,orderby=~db.crm_contact_field_value.contact_id|db.crm_contact_field.id).as_dict()
		
	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return cPickle.dumps(contact)
	

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_contact(data):
	done=0
	# have to enter the data into the key table first
	try:
		lKeyId=db.crm_contact_field_key.insert(
				user_id=data['user_id'] ,
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['user_id'],
				session_id=data['session_id']
			)
	except Exception as e:
		return 'error in adding contact key (%s)' %e
	else:
		rows=db(db.crm_contact_field.field_name != None).select()
		for row in rows:
			if row.is_active== True:
				try:
					db.crm_contact_field_value.insert(
						field_id=row.id ,
						contact_id=lKeyId ,
						field_value=data[row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_entry_time=lambda:datetime.now(),
						db_entered_by=data['user_id'],
						company_id=data['company_id'],
						session_id=data['session_id']
						)
					pass
				except Exception as e:
					return 'error in adding contact (%s) ' %e

				else:
					done=1

	if done==1:
		return("contact added")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_contact_list(lCompanyName):
	data = '%'+lCompanyName+'%'
	lCompanyList = {}
	rows = db((db.crm_contact_field.id == db.crm_contact_field_value.field_id) & (db.crm_contact_field.field_name == 'company_name') & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.field_value.like(data,case_sensitive=False))).select(db.crm_contact_field_value.field_value,db.crm_contact_field_value.contact_id)
	for row in rows:
		lCompanyList[str(row.contact_id)] = row.field_value
		pass
	return lCompanyList
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_company_details(lCompanyId):
	lCompanyDetails = {}
	rows = db((db.crm_contact_field.id == db.crm_contact_field_value.field_id) & (db.crm_contact_field_value.contact_id == lCompanyId)).select(db.crm_contact_field.field_name,db.crm_contact_field_value.field_value)
	for row in rows:
		lCompanyDetails[row.crm_contact_field.field_name] = row.crm_contact_field_value.field_value
		pass
	return lCompanyDetails
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def call(): return service() 


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def autocomplete():
	if not request.vars.data: return ''
