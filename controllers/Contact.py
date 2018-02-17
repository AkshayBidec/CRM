
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
		contacts= db(db.crm_contact_field_value.field_id==db.crm_contact_field.id)(db.crm_contact_field_value.contact_key_id<=keys[0].id)(db.crm_contact_field_value.contact_key_id>=keys[-1].id).select(db.crm_contact_field_value.contact_key_id,db.crm_contact_field_value.field_value,db.crm_contact_field.field_name,orderby=~db.crm_contact_field_value.contact_key_id|db.crm_contact_field.id)
		
		lContactDict={}
		i=0
		for contact in contacts:
			i+=1
			lContactDict[str(i)]=[str(contact.crm_contact_field_value.contact_key_id),str(contact.crm_contact_field.field_name),str(contact.crm_contact_field_value.field_value)]


	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return lContactDict

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_contact(data):
	
	done=0
	
	lReturnDict={'lKeyId':0,'msg':''}
	# have to enter the data into the key table first
	
	try:
		lKeyId=db.crm_contact_field_key.insert(
				company_key_id=data['data']['company_key_id'],
				user_id=data['data']['user_id'] ,
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['data']['user_id'],
				session_id=data['data']['session_id']
			)
	
		lReturnDict['lKeyId']=int(lKeyId)
	
	except Exception as e:
		lReturnDict['msg']='error in adding contact key (%s)' %e
		return lReturnDict	
	
	else:
		rows=db(db.crm_contact_field.field_name != None).select()
		for row in rows:
			if row.is_active== True:
				try:
					db.crm_contact_field_value.insert(
						field_id=row.id ,
						contact_key_id=lKeyId ,
						field_value=data['data'][row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_entry_time=lambda:datetime.now(),
						db_entered_by=data['data']['user_id'],
						company_id=data['data']['company_id'],
						session_id=data['data']['session_id']
						)
					pass
				except Exception as e:
					lReturnDict['msg']='error in adding contact data (%s)' %e
					return lReturnDict	
				else:
					done=1

	if done==1:
		lReturnDict['msg']=' contact done '
	return lReturnDict	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_contact_company_key_id(data):
	done=0
	
	lReturnDict={'lKeyId':0,'msg':''}
	# have to enter the data into the key table first
	
	try:
		db(db.crm_contact_field_key.id==data['data']['contact_key_id']).update(
				company_key_id=data['data']['company_key_id'],
				db_updated_by=data['data']['user_id'] ,
				db_update_time=lambda:datetime.now()
			)
		
	except Exception as e:
		lReturnDict['msg']='error in adding contact key (%s)' %e
		return lReturnDict	

	else:
		done=1


	if done==1:
		lReturnDict['msg']=' contact updated '
	return lReturnDict	

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@service.xmlrpc
def add_contact_company(data):
	db(db.crm_contact_field_key.id ==data[contact_key_id]).update(
			company_key_id=data[company_key_id]
		)
	return 'done'

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_company_list(lCompanyName,lSessionCompanyId):
	data = '%'+lCompanyName+'%'
	lCompanyList = {}
	rows = db((db.crm_company_field.id == db.crm_company_field_value.field_id) & (db.crm_company_field.field_name == 'company_name') & (db.crm_company_field_value.is_active == True) & (db.crm_company_field_value.company_id == lSessionCompanyId) & (db.crm_company_field_value.field_value.like(data,case_sensitive=False))).select(db.crm_company_field_value.field_value,db.crm_company_field_value.company_key_id)
	for row in rows:
		lCompanyList[str(row.company_key_id)] = row.field_value
		pass
	return lCompanyList
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_company_details(lCompanyId):
	lCompanyDetails = {}
	rows = db((db.crm_company_field.id == db.crm_company_field_value.field_id) & (db.crm_company_field_value.company_key_id == lCompanyId)).select(db.crm_company_field.field_name,db.crm_company_field_value.field_value)
	for row in rows:
		lCompanyDetails[row.crm_company_field.field_name] = row.crm_company_field_value.field_value
		pass
	return lCompanyDetails
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_company_contact_list(lFirstName,lCompanyKeyId,lSessionCompanyId):

	data = '%'+lFirstName+'%'
	rows = db((db.crm_contact_field.id == db.crm_contact_field_value.field_id) & (db.crm_contact_field_key.id == db.crm_contact_field_value.contact_key_id) & (db.crm_contact_field.field_name == 'first_name') & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.company_id == lSessionCompanyId) & (db.crm_contact_field_key.company_key_id == lCompanyKeyId) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field.field_name == 'company_name') & (db.crm_contact_field_value.field_value.like(data,case_sensitive=False))).select(db.crm_contact_field_value.field_value,db.crm_contact_field_value.contact_key_id,db.crm_contact_field_key.company_key_id,db.crm_company_field_value.field_value).as_list()
	#d=rows[0]['crm_contact_field_key']['company_key_id']
	return rows
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_contact_list(lFirstName,lSessionCompanyId):

	data = '%'+lFirstName+'%'
	rows = db((db.crm_contact_field.id == db.crm_contact_field_value.field_id) & (db.crm_contact_field_key.id == db.crm_contact_field_value.contact_key_id) & (db.crm_contact_field.field_name == 'first_name') & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.company_id == lSessionCompanyId) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field.field_name == 'company_name') & (db.crm_contact_field_value.field_value.like(data,case_sensitive=False))).select(db.crm_contact_field_value.field_value,db.crm_contact_field_value.contact_key_id,db.crm_contact_field_key.company_key_id,db.crm_company_field_value.field_value).as_list()
	#d=rows[0]['crm_contact_field_key']['company_key_id']
	return rows
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def ajax_contact_details(lContactId):
	lContactDetails = {}
	rows = db((db.crm_contact_field.id == db.crm_contact_field_value.field_id) & (db.crm_contact_field_value.contact_key_id == lContactId)).select(db.crm_contact_field.field_name,db.crm_contact_field_value.field_value)
	for row in rows:
		lContactDetails[row.crm_contact_field.field_name] = row.crm_contact_field_value.field_value
		pass
	return lContactDetails
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def call(): return service() 


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def autocomplete():
	if not request.vars.data: return ''
