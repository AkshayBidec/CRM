
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
def get_leads():	# limit is a dict 
	lLimit={}		# this dic is to get a single data or a range of data from the api

	lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	lLimit['countFrom']=0		# no of the row to start from 
	lLimit['order']='~db.crm_lead_field_key.id' 	# the name of field to order on, string will be evaluated in the api
		
	try:
		# get the key values according to the request
		keys=db(db.crm_lead_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
		
		# select the field and there respective values according to the request, using the inner join
		leads= db(db.crm_lead_field_value.field_id==db.crm_lead_field.id)(db.crm_lead_field_value.lead_key_id<=keys[0].id)(db.crm_lead_field_value.lead_key_id>=keys[-1].id).select(db.crm_lead_field_value.lead_key_id,db.crm_lead_field_value.field_value,db.crm_lead_field.field_name,orderby=~db.crm_lead_field_value.lead_key_id|db.crm_lead_field.id)
		
		lLeadsDict={}
		i=0
		for lead in leads:
			i+=1
			lLeadsDict[str(i)]=[str(lead.crm_lead_field_value.lead_key_id),str(lead.crm_lead_field.field_name),str(lead.crm_lead_field_value.field_value)]


	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return lLeadsDict

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_leads(data):
	done=0
	# have to enter the data into the key table first
	try:
		lKeyId=db.crm_lead_field_key.insert(
				contact_key_id=data['contact_key_id'],
				user_id=data['user_id'] ,
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['user_id'],
				session_id=data['session_id']
			)
	except Exception as e:
		return 'error in adding leads key (%s)' %e
	else:
		rows=db(db.crm_lead_field.field_name != None).select()
		for row in rows:
			if row.is_active== True:
				try:
					db.crm_lead_field_value.insert(
						field_id=row.id ,
						lead_key_id=lKeyId ,
						field_value=data[row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_entry_time=lambda:datetime.now(),
						db_entered_by=data['user_id'],
						company_id=data['company_id'],
						session_id=data['session_id']
						)
					pass
				except Exception as e:
					return 'error in adding leads (%s) ' %e

				else:
					done=1

	if done==1:
		return("lead added")

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

