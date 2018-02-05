
from datetime import datetime
from gluon.tools import Service
service = Service(globals())

@service.xmlrpc
def string(data):
	out=data['email_id']+data['password']
	return out


@service.xmlrpc
def leads_add_ff():
	# if type==1: # for the field names
		field_names={'field':'value'}
		rows = db(db.crm_lead_field.field_name != None).select()
		for row in rows:
			field_names.update({row.field_name:''})

		del field_names['field']
		return dict(field_names)
	# elif type==0:# for the field name and there values
	# 	return
def get_leads():
	# get the selet conditions from the request.vars
	# fetch the data from the db
	# arrange the data
	# send it back to the ERP/../leads
	return dict()

@service.xmlrpc
def add_leads(data):
	done=0
	rows=db(db.crm_lead_field.field_name != None).select()
	for row in rows:
		try:
			db.crm_lead_field_value.insert(
				field_id=row.id ,
				user_id=0 ,
				field_value=data[row.field_name] ,
				db_entry_time=lambda:datetime.now()
				)
			pass
		except Exception as e:
			return 'error in adding leads (%s) ' %e

		else:
			done=1
			
	if done==1:
		return("lead added")
def update_leads():
	return dict()

def delete_leads():
	return dict()

def call(): return service() 
