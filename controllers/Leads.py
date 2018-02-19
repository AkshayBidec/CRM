
from datetime import datetime
from gluon.tools import Service
from xmlrpc.server import SimpleXMLRPCServer
service = Service(globals())
import _pickle as cPickle
#import xmlrpc.client as xmlrpclib

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def string(data):
	out=data['email_id']+data['password']
	return out
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# function to get the field names to show the form
@service.xmlrpc
def leads_add_ff():
		field_names={'field':'value'}
		rows = db(db.crm_lead_field.is_active==True).select()
		lList=[]
		for row in rows:

			lList=[row.field_widget_attributes,row.field_requires_attributes]

			field_names.update({row.field_name:lList})

		del field_names['field']
		return dict(field_names)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def leads_edit_ff(lead_key_id):
		# lead_key_id=16
		field_names={'field':'value'}
		rows = db(db.crm_lead_field_value.field_id == db.crm_lead_field.id)(db.crm_lead_field_value.lead_key_id == lead_key_id).select(
			db.crm_lead_field_value.field_value,
			db.crm_lead_field.field_widget_attributes,
			db.crm_lead_field.field_requires_attributes,
			db.crm_lead_field.field_name
			)
		lList=[]
		for row in rows:

			lList=[row.crm_lead_field.field_widget_attributes,row.crm_lead_field.field_requires_attributes,row.crm_lead_field_value.field_value]

			field_names.update({row.crm_lead_field.field_name:lList})

		del field_names['field']

		## uncomment the following to get the contact id also, and return the data instead of the field_name
		# contact_key_id=db(db.crm_lead_field_key.id==lead_key_id).select()[0].contact_key_id 		# take the contact key id for contact details 
		# data={"field_names":field_names,
		# 	"contact_key_id":contact_key_id}
		
		return dict(field_names)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def edit_lieds(data):
	
	done=0
	lReturnDict={'lKeyId':0,'msg':''}
	
	# have to enter the data into the key table first
	try:
		db(db.crm_lead_field_key.id== data['data']['lead_key_id']).update(
				db_update_time=lambda:datetime.now(),
				db_updated_by=data['data']['user_id']

			)
		# lReturnDict['lKeyId']=int(lKeyId)
	
	except Exception as e:
		lReturnDict['msg']='error in editing leads key (%s)' %e
		return lReturnDict
	else:
		rows=db(db.crm_lead_field.field_name != None).select()
		for row in rows:
			# if row.is_active== True:
			try:
				db((db.crm_lead_field_value.lead_key_id==data['data']['lead_key_id'])&
					(db.crm_lead_field_value.field_id == row.id)).update(
					field_value=data['data'][row.field_name] ,  # to insert the data take the respective data from the dictionary
					db_update_time=lambda:datetime.now(),
					db_updated_by=data['data']['user_id']
					)
				pass
			except Exception as e:
				lReturnDict['msg']=  'error in adding leads (%s) ' %e
				return lReturnDict

			else:
				done=1

	if done==1:
		lReturnDict['msg']=' leads done '
		return lReturnDict


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_leads(lLimit):	# limit is a dict 
	# lLimit={}
	# lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	# lLimit['countFrom']=0		# no of the row to start from 
	# lLimit['order']='~db.crm_lead_field_key.id' 	# the name of field to order on, string will be evaluated in the api
	try:
		
		keys=db(db.crm_lead_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
		i=0
		data={}
		for  i in range (0,len(keys)):

			company_data= db(db.crm_contact_field_key.id == keys[i].contact_key_id).select(
				db.crm_contact_field_key.id,
				db.crm_company_field_value.field_value,
				left=db.crm_company_field_value.on(db.crm_company_field_value.company_key_id == db.crm_contact_field_key.company_key_id)
				).as_list()

			lead_data=db(db.crm_lead_field_value.lead_key_id==keys[i].id).select(
					db.crm_lead_field_value.field_value,
					).as_list()
			
			contact_data=db(db.crm_contact_field_value.contact_key_id== keys[i].contact_key_id).select(
					db.crm_contact_field_value.field_value,
					db.crm_contact_field_value.contact_key_id
					).as_list()
		
			data[str(i)]={
				'Company':company_data[0]['crm_company_field_value']['field_value'],
				'Name':str(contact_data[0]['field_value'])+' '+str(contact_data[1]['field_value']),
				'Email':str(contact_data[6]['field_value']),
				'Phone':str(company_data[3]['crm_company_field_value']['field_value']),
				'Lead Source':lead_data[0]['field_value'],
				'Description':lead_data[5]['field_value'],
				'Status':lead_data[1]['field_value']
			}
			pass

	except Exception as e:
		return e

	else:
		return data


	

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_leads(data):
	
	done=0
	lReturnDict={'lKeyId':0,'msg':''}
	
	# have to enter the data into the key table first
	try:
		lKeyId=db.crm_lead_field_key.insert(
				contact_key_id=data['data']['contact_key_id'],
				company_id=data['data']['company_id'] ,
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['data']['user_id'],
				session_id=data['data']['session_id']
			)
		lReturnDict['lKeyId']=int(lKeyId)
	except Exception as e:
		lReturnDict['msg']='error in adding leads key (%s)' %e
		return lReturnDict
	else:
		rows=db(db.crm_lead_field.field_name != None).select()
		for row in rows:
			if row.is_active== True:
				try:
					db.crm_lead_field_value.insert(
						field_id=row.id ,
						lead_key_id=lKeyId ,
						field_value=data['data'][row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_entry_time=lambda:datetime.now(),
						db_entered_by=data['data']['user_id'],
						company_id=data['data']['company_id'],
						session_id=data['data']['session_id']
						)
					pass
				except Exception as e:
					lReturnDict['msg']=  'error in adding leads (%s) ' %e
					return lReturnDict

				else:
					done=1

	if done==1:
		lReturnDict['msg']=' leads done '
		return lReturnDict
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def update_leads():
	return dict()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def delete_leads():
	return dict()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def call(): return service() 


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def autocomplete():
	if not request.vars.data: return ''

