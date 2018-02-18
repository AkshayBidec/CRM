
from datetime import datetime
from gluon.tools import Service
service = Service(globals())
import _pickle as cPickle
from xmlrpc.server import SimpleXMLRPCServer
#import xmlrpc.client as xmlrpclib

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
def contact_edit_ff(contact_key_id):

		# contact_key_id=32
		
		field_names={'field':'value'}
	
		rows = db(db.crm_contact_field_value.field_id == db.crm_contact_field.id)(db.crm_contact_field_value.contact_key_id== contact_key_id).select(
			db.crm_contact_field_value.field_value,
			db.crm_contact_field.field_widget_attributes,
			db.crm_contact_field.field_requires_attributes,
			db.crm_contact_field.field_name
			)
		
		lList=[]
		for row in rows:

			lList=[row.crm_contact_field.field_widget_attributes,row.crm_contact_field.field_requires_attributes,row.crm_contact_field_value.field_value] 		# make a list of required details for the field

			field_names.update({row.crm_contact_field.field_name:lList})

		del field_names['field']

		# uncomment it if the company key id is needed and use that accordingly
		
		company_key_id=db(db.crm_contact_field_key.id==contact_key_id).select()[0].company_key_id
		
		lData={"field_names":field_names,
			"company_key_id":company_key_id}

		return lData

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def edit_contact(data):
	
	done=0
	
	lReturnDict={'lKeyId':0,'msg':''}
	# have to enter the data into the key table first
	
	try:
		db(db.crm_contact_field_key.id==data['data']['contact_key_id']).update(
				company_key_id=data['data']['company_key_id'],
				db_update_time=lambda:datetime.now(),
				db_updated_by=data['data']['user_id'],
			)
		
	except Exception as e:
		lReturnDict['msg']='error in adding contact key (%s)' %e
		return lReturnDict	
	
	else:
		rows=db(db.crm_contact_field.field_name != None).select()
		for row in rows:
			if row.is_active== True:
				try:
					db(db.crm_contact_field_value.field_id==row.id)(db.crm_contact_field_value.contact_key_id==data['data']['contact_key_id']).update(
						field_value=data['data'][row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_update_time=lambda:datetime.now(),
						db_updated_by=data['data']['user_id']
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
def get_contact(lLimit):	# limit is a dict 

	# # following data is for the testing only
	# lLimit={}
	# lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	# lLimit['countFrom']=0		# no of the row to start from 
	# lLimit['order']='~db.crm_contact_field_key.id' 	# the name of field to order on, string will be evaluated in the api

	try:
		keys=db(db.crm_contact_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
		i=0
		data={}
		for  i in range (0,len(keys)):

			company_data= db(db.crm_contact_field_key.id== keys[i].id).select(
				db.crm_contact_field_key.id,
				db.crm_company_field_value.field_value,
				left=db.crm_company_field_value.on(db.crm_company_field_value.company_key_id == keys[i].company_key_id)
				).as_list()

			
			contact_data=db(db.crm_contact_field_value.contact_key_id== keys[i].id).select(
					db.crm_contact_field_value.field_value,
					db.crm_contact_field_value.contact_key_id
					).as_list()
			
			# data[str(i)]=company_data
			data[str(i)]={
				'Company':company_data[0]['crm_company_field_value']['field_value'],
				'Name':str(contact_data[0]['field_value'])+' '+str(contact_data[1]['field_value']),
				'Email':str(contact_data[6]['field_value']),
				'Phone':str(contact_data[5]['field_value']),
				'Type Of Contact':contact_data[4]['field_value'],
				'Designation':contact_data[2]['field_value'],
				'Department':contact_data[3]['field_value']
			}

	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return dict(data)

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
