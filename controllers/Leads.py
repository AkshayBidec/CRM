
from datetime import datetime
from gluon.tools import Service
from xmlrpc.server import SimpleXMLRPCServer
service = Service(globals())
import _pickle as cPickle
from dateutil import relativedelta
import calendar

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

		# IS_IN_SET({1:"Reference"},zero="Type of contact")
		lList={}		# a dict to store the options of the leads status
		lListValues=db(db.crm_lead_status_master).select(db.crm_lead_status_master.lead_status,db.crm_lead_status_master.id).as_dict(key='id')
		# for lListValue in lListValues:
		# 	lList[str(lListValue.id)]= lListValue.lead_status
		
		for key in sorted(lListValues.keys()):
			lList[str(key)]=lListValues[key]['lead_status']


		field_names['lead_status'][1]="IS_IN_SET("+str(lList)+",zero='Lead Status')"

		del field_names['field']
		return dict(field_names)
		# return locals()

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

		# IS_IN_SET({1:"Reference"},zero="Type of contact")
		lList={}		# a dict to store the options of the leads status
		lListValues=db(db.crm_lead_status_master).select(db.crm_lead_status_master.lead_status,db.crm_lead_status_master.id).as_dict(key='id')
		# for lListValue in lListValues:
		# 	lList[str(lListValue.id)]= lListValue.lead_status
		
		for key in sorted(lListValues.keys()):
			lList[str(key)]=lListValues[key]['lead_status']


		field_names['lead_status'][1]="IS_IN_SET("+str(lList)+",zero='Lead Status')"

		del field_names['field']
		return dict(field_names)
		# return locals()
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def edit_leads(data):
	
	# only for the testing 
	# data={'data':{
	# 	'session_id': 39,		# get and add
	# 	'lead_key_id': '23',
	# 	'user_id': 2,				
	# 	'company_id':25,	
	# 	'lead_status_id':1,					
	# 	'lead_status':2,
	# 	'lead_source':'Reference',
	# 	'lead_owner':'user',
	# 	'application_of_treated_water':"",
	# 	'volume_per_day':'',
	# 	'description':''
	# 	}}

	done=0
	lReturnDict={'lKeyId':0,'msg':''}
	
	# have to enter the data into the key table first
	try:
		db(db.crm_lead_field_key.id== data['data']['lead_key_id']).update(
				db_update_time=lambda:datetime.now(),
				db_updated_by=data['data']['user_id']

			)
		# # lReturnDict['lKeyId']=int(lKeyId)
		pass
	except Exception as e:
		lReturnDict['msg']='error in editing leads key (%s)' %e
		return lReturnDict
	else:
		
		try:
			rows=db(db.crm_lead_field.field_name != None).select()
			for row in rows:
				if row.is_active== True:
					db((db.crm_lead_field_value.lead_key_id==data['data']['lead_key_id'])&
						(db.crm_lead_field_value.field_id == row.id)).update(
						field_value=data['data'][row.field_name] ,  # to insert the data take the respective data from the dictionary
						db_update_time=lambda:datetime.now(),
						db_updated_by=data['data']['user_id']
						)
				pass

		except Exception as e:
			lReturnDict['msg']=  'error in editing leads values (%s) ' %e
			return lReturnDict

		else:
			try:
				lCurrentStatus=db(db.crm_lead_status.lead_key_id==data['data']['lead_key_id'])(db.crm_lead_status.is_active== True).select(db.crm_lead_status.ALL,limitby=[0,1])
				
				# if there is a change in the leads status reflet it in the status table
				if len(lCurrentStatus)>0:
					if lCurrentStatus[0].lead_status_master_id != data['data']['lead_status']:  # if there is a change
						
						# desable the last lead first
						db((db.crm_lead_status.lead_key_id==data['data']['lead_key_id'])&(db.crm_lead_status.is_active== True)).update(is_active=False)
						
						# add the new status to the status table also
						db.crm_lead_status.insert(
							session_id=data['data']['session_id'],
							company_id=data['data']['company_id'],
							lead_key_id=data['data']['lead_key_id'],
							lead_status_master_id=data['data']['lead_status'],
							db_entry_time=lambda:datetime.now(),
							db_entered_by=data['data']['user_id']
							)

				
			except Exception as e:
				lReturnDict['msg']='error in adding the status details %s' %e
				return lReturnDict
			
			else:
				done=1 

	if done==1:
		lReturnDict['msg']=' leads done '
	
	return lReturnDict


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_leads(company_id):	# limit is a dict 
	# lLimit={}
	# lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	# lLimit['countFrom']=0		# no of the row to start from 
	# lLimit['order']='~db.crm_lead_field_key.id' 	# the name of field to order on, string will be evaluated in the api
	
	try:
		
		keys=db((db.crm_lead_field_key.is_active == True) & (db.crm_lead_field_key.company_id == company_id)).select(db.crm_lead_field_key.id,orderby=~db.crm_lead_field_key.id)
		data={}
		
		for  i in range (0,len(keys)):
			
			lead_data = db((db.crm_lead_field_key.id == db.crm_lead_field_value.lead_key_id) & (db.crm_lead_field_value.field_id == db.crm_lead_field.id) & (db.crm_lead_field_value.is_active == True) & (db.crm_lead_field_value.company_id == company_id) & (db.crm_lead_field_key.id == keys[i].id)).select(db.crm_lead_field.field_name, db.crm_lead_field_value.field_value).as_dict(key='crm_lead_field.field_name')
			
			contact_data = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id) & (db.crm_contact_field_value.field_id == db.crm_contact_field.id) & (db.crm_lead_field_key.id == keys[i].id) & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.company_id == company_id)).select(db.crm_contact_field.field_name, db.crm_contact_field_value.field_value).as_dict(key='crm_contact_field.field_name')
			company_data = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field_value.is_active == True) & (db.crm_lead_field_key.id == keys[i].id) & (db.crm_company_field_value.company_id == company_id)).select(db.crm_company_field.field_name, db.crm_company_field_value.field_value).as_dict(key='crm_company_field.field_name')
			lead_status = db((db.crm_lead_status.lead_key_id == keys[i].id) & (db.crm_lead_status.is_active == True) & (db.crm_lead_status.lead_status_master_id == db.crm_lead_status_master.id)).select(db.crm_lead_status.lead_key_id,db.crm_lead_status_master.lead_status, orderby=~db.crm_lead_status.db_entry_time,limitby=(0,1)).as_dict(key='crm_lead_status.lead_key_id')
		
			data[str(i)]={
				'Company': 'NA' if not company_data else company_data['company_name']['crm_company_field_value']['field_value'],
				'Name':str(contact_data['first_name']['crm_contact_field_value']['field_value'])+' '+str(contact_data['last_name']['crm_contact_field_value']['field_value']),
				'Email':str(contact_data['email_id']['crm_contact_field_value']['field_value']),
				'Phone':'NA' if not company_data else str(company_data['phone_no']['crm_company_field_value']['field_value']),
				'Lead Source':lead_data['lead_source']['crm_lead_field_value']['field_value'],
				'Description':lead_data['description']['crm_lead_field_value']['field_value'],
				'Status':'NA' if not lead_status else lead_status[keys[i].id]['crm_lead_status_master']['lead_status'],
				'lead_key_id':keys[i].id
			}
			# data[str(i)]=lead_data
			pass

	except Exception as e:
		return 'Exception Raised : '+e
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
		
		try:
			rows=db(db.crm_lead_field.field_name != None).select()
			for row in rows:
				if row.is_active== True:		
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
			lReturnDict['msg']=  'error in adding leads data (%s) ' %e
			return lReturnDict

		else:
			# have to update the status also
			try:
				lStatusId=db.crm_lead_status.insert(
				session_id=data['data']['session_id'],
				company_id=data['data']['company_id'],
				lead_key_id=lKeyId,
				lead_status_master_id=data['data']['lead_status'],				#db(db.crm_lead_status_master.lead_status=='Initiated').select()[0].id,
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['data']['user_id']
				)

			except Exception as e:
				return 'error in add the leads status as  %s '%e
			else:
				if len(data['data']['description'])>0:
					# the user have a description than add it to the notes as a update to that lead
					try:
						db.crm_lead_updates.insert(
							session_id=data['data']['session_id'],
							company_id=data['data']['company_id'],
							lead_key_id=lKeyId,
							lead_status_id=lStatusId,
							update_head='notes',
							update_data=data['data']['description'],
							db_entry_time=lambda:datetime.now(),
							db_entered_by=data['data']['user_id']
							)

					except Exception as e:
						return 'error in adding the leads update data %s' %e
					else:
						done=1 
				else:
					done=1

	if done==1:
		lReturnDict['msg']=' leads done '
		return lReturnDict

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def fetch_lead_basic_details(lRequestData):
	
	# ={}
	# lRequestData={
	# 	'lead_key_id':22,
	# 	'user_id': 2,
	# 	'company_id':25,
	# 	'update_head': "notes"
	# }


	data = {}
	data['lead_details'] = db((db.crm_lead_field_key.id == db.crm_lead_field_value.lead_key_id) & (db.crm_lead_field_value.field_id == db.crm_lead_field.id) & (db.crm_lead_field_value.is_active == True) & (db.crm_lead_field_value.company_id == lRequestData['company_id']) & (db.crm_lead_field_key.id == lRequestData['lead_key_id'])).select(db.crm_lead_field.field_name, db.crm_lead_field_value.field_value).as_list()
	data['contact_details'] = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id) & (db.crm_contact_field_value.field_id == db.crm_contact_field.id) & (db.crm_lead_field_key.id == lRequestData['lead_key_id']) & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.company_id == lRequestData['company_id'])).select(db.crm_contact_field.field_name, db.crm_contact_field_value.field_value).as_list()
	data['company_details'] = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field_value.is_active == True) & (db.crm_lead_field_key.id == lRequestData['lead_key_id']) & (db.crm_company_field_value.company_id == lRequestData['company_id'])).select(db.crm_company_field.field_name, db.crm_company_field_value.field_value).as_list()
	


	data['lead_details'][1]['crm_lead_field_value']['field_value']=db(db.crm_lead_status_master.id==int(data['lead_details'][1]['crm_lead_field_value']['field_value'])).select(db.crm_lead_status_master.lead_status)[0].lead_status
	# make a basic default dictionary for the contact donot have the comapny details
	if len(data['company_details'])<=0:
		data['company_details']=[
		{'crm_company_field'	:	{'field_name'	:	'company_name'},
		'crm_company_field_value'	:	{'field_value'	:	'- Company Name -'}
		},
		
		{'crm_company_field'	:	{'field_name'	:	'type_of_industry'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'website'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},


		{'crm_company_field'	:	{'field_name'	:	'phone_no'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'fax_no'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'street'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'state'},
		'crm_company_field_value'	:{	'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'city'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'
		}},

		{'crm_company_field'	:	{'field_name'	:	'pincode'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},

		{'crm_company_field'	:	{'field_name'	:	'country'},
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		}
		]
	test=data['company_details'][0]

	return data
	pass

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def fetch_lead_update_details(lRequestData):
	
	# # following data is only for the testing
	# ={
	# 'request_type': 'get',		# get and add
	# 'lead_key_id': '16',
	# 'user_id': 2,				##############
	# 'company_id':25,		##############
	# 'update_head': 'notes',
	# 'update_data': 'hiiiiii53642795632987',
	# 'lead_status_id':1,					#request.vars.status_id,
	# 'session_id':0		##############
	# #'lead_update_id':request.vars.lead_update_id
	# }
	# get the data rewuired from the db
	try:
		i=0
		lData={}
		rows = db((db.crm_lead_updates.update_head == lRequestData['update_head']) & (db.crm_lead_updates.lead_status_id == db.crm_lead_status_master.id) & (db.crm_lead_updates.lead_key_id == lRequestData['lead_key_id']) & (db.crm_lead_updates.is_active == True) & (db.crm_lead_updates.company_id == lRequestData['company_id'])
			).select(
			db.crm_lead_updates.company_id, 
			db.crm_lead_updates.lead_key_id, 
			db.crm_lead_updates.lead_status_id, 
			db.crm_lead_updates.update_head, 
			db.crm_lead_updates.update_data, 
			db.crm_lead_updates.update_file, 
			db.crm_lead_updates.update_file_name, 
			db.crm_lead_updates.file_version, 
			db.crm_lead_updates.db_entry_time,
			db.crm_lead_updates.db_entered_by, 
			orderby=~db.crm_lead_updates.db_entry_time
			).as_list()	
	except Exception as e:
		return e

	else:
		for row in rows:
			lData[str(i)]=row
			time=datetime.now()
			lDuration=relativedelta.relativedelta(time, lData[str(i)]['db_entry_time'])
			if lDuration.years==0:
				if lDuration.months==0:
					if lDuration.days==0:
						if lDuration.hours==0:
							if lDuration.minutes==0:
								lData[str(i)]['db_entry_time']=str(lDuration.seconds)+" sec  ago"
							else:
								lData[str(i)]['db_entry_time']=str(lDuration.minutes)+" minutes  ago"
								
						else:
							lData[str(i)]['db_entry_time']=str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
					else:
						lData[str(i)]['db_entry_time']=str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
				else:
					lData[str(i)]['db_entry_time']=str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
			else:
				lData[str(i)]['db_entry_time']=str(lDuration.years)+" years "+str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"


			# lData[str(i)]['db_entry_time']=str(lDuration.months)+"M "+str(lDuration.days)+"D "+str(lDuration.hours)+"h "+str(lDuration.minutes)+"m "+str(lDuration.seconds)+"s **"
			i+=1

	return lData

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_lead_update_details(lRequestData):
	# have to add the data into the lead update table
	try:		
		db.crm_lead_updates.insert(
			session_id=lRequestData['session_id'],
			company_id=lRequestData['company_id'],
			lead_key_id=lRequestData['lead_key_id'],
			lead_status_id=lRequestData['lead_status_id'],
			update_head=lRequestData['update_head'],
			update_data=lRequestData['update_data'],
			db_entry_time=lambda:datetime.now(),
			db_entered_by=lRequestData['user_id']
			)

	except Exception as e:
		return e

	else:
		i=0
		lData={}
		rows = db((db.crm_lead_updates.update_head == lRequestData['update_head']) & (db.crm_lead_updates.lead_status_id == db.crm_lead_status_master.id) & (db.crm_lead_updates.lead_key_id == lRequestData['lead_key_id']) & (db.crm_lead_updates.is_active == True) & (db.crm_lead_updates.company_id == lRequestData['company_id'])).select(db.crm_lead_updates.company_id, db.crm_lead_updates.lead_key_id, db.crm_lead_updates.lead_status_id, db.crm_lead_updates.update_head, db.crm_lead_updates.update_data, db.crm_lead_updates.db_entry_time,db.crm_lead_updates.db_entered_by, orderby=~db.crm_lead_updates.db_entry_time).as_list()

		for row in rows:
			lData[str(i)]=row
			time=datetime.now()
			lDuration=relativedelta.relativedelta(time, lData[str(i)]['db_entry_time'])
			if lDuration.years==0:
				if lDuration.months==0:
					if lDuration.days==0:
						if lDuration.hours==0:
							if lDuration.minutes==0:
								lData[str(i)]['db_entry_time']=str(lDuration.seconds)+" sec  ago"
							else:
								lData[str(i)]['db_entry_time']=str(lDuration.minutes)+" minutes  ago"
								
						else:
							lData[str(i)]['db_entry_time']=str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
					else:
						lData[str(i)]['db_entry_time']=str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
				else:
					lData[str(i)]['db_entry_time']=str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
			else:
				lData[str(i)]['db_entry_time']=str(lDuration.years)+" years "+str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"


			# lData[str(i)]['db_entry_time']=str(lDuration.months)+"M "+str(lDuration.days)+"D "+str(lDuration.hours)+"h "+str(lDuration.minutes)+"m "+str(lDuration.seconds)+"s **"
			i+=1
	

	return lData

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def download(): return response.download(request,db)

def upload():

	session_data= request.vars

	pi_diagram_upload = FORM(
		INPUT(_name='description',_type='text'),
		INPUT(_name='update_file',_type='file'),
		INPUT(_name='version',_type='string')
		)
	done=0
	e=''
	t="type"
	if pi_diagram_upload.accepts(request.vars,formname='pi_diagram_upload'):
		if type(pi_diagram_upload.vars.update_file) != bytes:
			try:
				lStorageFile = db.crm_lead_updates.update_file.store(pi_diagram_upload.vars.update_file.file, pi_diagram_upload.vars.update_file.filename)
				db.crm_lead_updates.insert(
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							lead_status_id=session_data['lead_status_id'],
							update_head='pi_diagram',
							update_data=pi_diagram_upload.vars.description,
							update_file_name= pi_diagram_upload.vars.update_file.filename,
							update_file= lStorageFile,
							file_version=pi_diagram_upload.vars.version or 0,
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id']
							)
			except Exception as e:
				return e

			else:
				done=1
		else:
			try:
				db.crm_lead_updates.insert(
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							lead_status_id=session_data['lead_status_id'],
							update_head='pi_diagram',
							update_data=pi_diagram_upload.vars.description,
							update_file_name='No file attached',
							update_file= 'NA',
							file_version=pi_diagram_upload.vars.version or 0,
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id']
							)
			except Exception as e:
				return e
			else:
				done=1
	data=[]
	lRequestData={
	'request_type': 'get',		# get and add
	'lead_key_id': session_data['lead_key_id'],
	'user_id': session_data['user_id'],				##############
	'company_id':session_data['company_id'],		##############
	'update_head': 'pi_diagram',
	'update_data': '',
	'lead_status_id':session_data['lead_status_id'],					#request.vars.status_id,
	'session_id':session_data['session_id']		##############
	}
	data=fetch_lead_update_details(lRequestData)
	return dict(data=data)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
# def edit_lead_update_details(lRequestData):
	
	# 	# have to add the data into the lead update table
	# 	try:		
	# 		db(db.crm_lead_updates.id==lRequestData['lead_update_id'])(b.crm_lead_updates.company_id==lRequestData['company_id']).update(
	# 			update_data=lRequestData['update_data'],
	# 			db_update_time=lambda:datetime.now(),
	# 			db_updated_by=lRequestData['user_id']
	# 			)
	# 	except Exception as e:
	# 		return e

	# 	else:
	# 		rows = db((db.crm_lead_updates.update_head == lRequestData['update_head']) & (db.crm_lead_updates.lead_status_id == db.crm_lead_status_master.id) & (db.crm_lead_updates.lead_key_id == lRequestData['lead_key_id']) & (db.crm_lead_updates.is_active == True) & (db.crm_lead_updates.company_id == lRequestData['company_id'])).select(db.crm_lead_updates.company_id, db.crm_lead_updates.lead_key_id, db.crm_lead_updates.lead_status_id, db.crm_lead_updates.update_head, db.crm_lead_updates.update_data, db.crm_lead_updates.db_entry_time, orderby=~db.crm_lead_updates.db_entry_time).as_list()
			
	# 		i=0
	# 		lData={}
	# 		for row in rows:
	# 			lData[str(i)]=row
	# 			lData[str(i)]['db_entry_time']=lData[str(i)]['db_entry_time'].strftime("%Y-%m-%d  %H:%M:%S")
	# 			i+=1

	# 	return lData
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def fetch_lead_status_details():
	

	lRequestData={
	'request_type': 'get',		# get and add
	'lead_key_id': '16',
	'user_id': 2,				##############
	'company_id':25,		##############
	'update_head': 'notes',
	'update_data': 'yes',
	'lead_status_id':1,					#request.vars.status_id,
	'session_id':0,		##############
	'respose':1
	}
	lData={}
	rows = db((db.crm_lead_status.lead_key_id==lRequestData['lead_key_id'])&
			(db.crm_lead_status.company_id==lRequestData['company_id'])&
			(db.crm_lead_status.lead_status_master_id==db.crm_lead_status_master.id)
				).select(
				db.crm_lead_status.lead_status_master_id,
				db.crm_lead_status_master.lead_status,
				db.crm_lead_status.db_entry_time,
				db.crm_lead_status.db_entered_by,
				).as_list()
	
	i=0
	for row in rows:
		lData[str(i)]=row
		time=datetime.now()
		lDuration=relativedelta.relativedelta(time, lData[str(i)]['crm_lead_status']['db_entry_time'])
		# if the duration is less than a week
		if lDuration.days<=7:
			day=calendar.day_name[lData[str(i)]['crm_lead_status']['db_entry_time'].weekday()]
			lData[str(i)]['crm_lead_status']['db_entry_time']=str(day)+str(lData[str(i)]['crm_lead_status']['db_entry_time'].strftime(",  %H:%M:%S"))
		
		else:
			lData[str(i)]['crm_lead_status']['db_entry_time']=lData[str(i)]['crm_lead_status']['db_entry_time'].strftime("%Y-%m-%d,  %H:%M:%S")
		
		i+=1
	

	return lData
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_lead_status_details(lRequestData):
	
	if lRequestData['response']==0:		# in this we only wish to add the data not to get the list of the data
		try:
			# have to enter the data
			db.crm_lead_status.insert(
						session_id=lRequestData['session_id'],
						company_id=lRequestData['company_id'],
						lead_key_id=lRequestData['lead_key_id'],
						lead_status_master_id=lRequestData['lead_status_master_id'],
						db_entry_time=lambda:datetime.now(),
						db_entered_by=lRequestData['user_id']
						)

		except Exception as e:
			return e
		else:
			
			return 'data entered'


	elif lRequestData['response']== 1:
		try:
			# have to enter the data
			db.crm_lead_status.insert(
						session_id=lRequestData['session_id'],
						company_id=lRequestData['company_id'],
						lead_key_id=lRequestData['lead_key_id'],
						lead_status_master_id=lRequestData['lead_status_master_id'],
						db_entry_time=lambda:datetime.now(),
						db_entered_by=lRequestData['user_id']
						)

		except Exception as e:
			return e
		else:
			rows = db((db.crm_lead_status.lead_key_id==lRequestData['lead_key_id'])
					(db.crm_lead_status.company_id==lRequestData['company_id'])
					(db.crm_lead_status.lead_status_master_id==db.crm_lead_status_master.id)
						).select(
						db.crm_lead_status.lead_status_master_id,
						db.crm_lead_status_master.lead_status,
						db.crm_lead_status.db_entry_time,
						db.crm_lead_status.db_entered_by,
						).as_list()
			
			i=0
			for row in rows:
				lData[str(i)]=row
				time=datetime.now()
				lDuration=relativedelta.relativedelta(time, lData[str(i)]['crm_lead_status']['db_entry_time'])
				# if the duration is less than a week
				if lDuration.days<=7:
					day=calendar.day_name[lData[str(i)]['crm_lead_status']['db_entry_time'].weekday()]
					lData[str(i)]['crm_lead_status']['db_entry_time']=str(day)+str(lData[str(i)]['crm_lead_status']['db_entry_time'].strftime(",  %H:%M:%S"))
				
				else:
					lData[str(i)]['crm_lead_status']['db_entry_time']=lData[str(i)]['crm_lead_status']['db_entry_time'].strftime("%Y-%m-%d,  %H:%M:%S")
				
				i+=1
	


			return lData
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def delete_leads():
	return dict()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def call(): return service() 


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def autocomplete():
	if not request.vars.data: return ''

