
from datetime import datetime
from gluon.tools import Service
service = Service(globals())
import cPickle

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
		rows = db(db.crm_lead_field.field_name != None).select()
		for row in rows:
			field_names.update({row.field_name:''})

		del field_names['field']
		return dict(field_names)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_leads(lLimit):	# limit is a dict 

	try:
		# get the key values according to the request
		keys=db(db.crm_lead_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
		
		# select the field and there respective values according to the request, using the inner join
		leads= db(db.crm_lead_field_value.field_id==db.crm_lead_field.id)(db.crm_lead_field_value.lead_id<=keys[0].id)(db.crm_lead_field_value.lead_id>=keys[-1].id).select(db.crm_lead_field_value.lead_id,db.crm_lead_field_value.field_value,db.crm_lead_field.field_name,orderby=~db.crm_lead_field_value.lead_id|db.crm_lead_field.id).as_dict()
		
	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return cPickle.dumps(leads)
	

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_leads(data):
	done=0
	# have to enter the data into the key table alse
	try:
		lKeyId=db.crm_lead_field_key.insert(
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
						lead_id=lKeyId ,
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

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def delete_leads():
	return dict()

def test():
		# pointer=db(db.crm_lead_field_key).select(db.crm_lead_field_key.id.max()).first()[db.crm_lead_field_key.id.max()]
		# rows=db(db.crm_lead_field_key.id>=pointer-3).select(orderby=~db.crm_lead_field_key.id)
		# rows=db(db.crm_lead_field_key).select(db.crm_lead_field_key.id.max()).first()[db.crm_lead_field_key.id.max()]
		rows=db(db.crm_lead_field_key).select(db.crm_lead_field_key.id,orderby=~db.crm_lead_field_key.id,limitby=(0,10))
		data=type(rows[0].id)
		return locals()

def call(): return service() 
