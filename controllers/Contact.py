
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
# fucntion to get the form field for the filter 
@service.xmlrpc
def contact_filter_field():
		lFinalFilterFields={}
		field_names={'field':'value'}
		rows = db(db.crm_company_field.is_active==True).select()
		lList=[]
		for row in rows:

			lList=[row.field_widget_attributes,row.field_requires_attributes] 		# make a list of required details for the field

			field_names.update({row.field_name:lList})

		del field_names['field']
		lFinalFilterFields['Company']=field_names

		field_names={'field':'value'}
		rows = db(db.crm_contact_field.is_active==True).select()
		lList=[]		# empty the last list
		for row in rows:

			lList=[row.field_widget_attributes,row.field_requires_attributes] 		# make a list of required details for the field

			field_names.update({row.field_name:lList})
		del field_names['field']
		lFinalFilterFields['Contact']=field_names

		return dict(lFinalFilterFields)
		# return locals()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_contact(company_id):	# limit is a dict 
	# =25
	# # following data is for the testing only
	# lLimit={}
	# lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	# lLimit['countFrom']=0		# no of the row to start from 
	# lLimit['order']='~db.crm_contact_field_key.id' 	# the name of field to order on, string will be evaluated in the api
	data_flag=0
	try:
		keys=db((db.crm_contact_field_key.is_active == True) & (db.crm_contact_field_key.company_id == company_id)).select(db.crm_contact_field_key.id,orderby=~db.crm_contact_field_key.id)
		i=0
		data={}
		for  i in range (0,len(keys)):

			contact_data = db( 
				(db.crm_contact_field_value.field_id == db.crm_contact_field.id) & 
				(db.crm_contact_field_value.contact_key_id == keys[i].id) & 
				(db.crm_contact_field_value.is_active == True) & 
				(db.crm_contact_field_value.company_id == company_id)
				).select(
				db.crm_contact_field.field_name,
				 db.crm_contact_field_value.field_value
				 ).as_dict(key='crm_contact_field.field_name')

			company_data = db((db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field_value.is_active == True) & (db.crm_contact_field_key.id == keys[i].id) & (db.crm_company_field_value.company_id == company_id)).select(db.crm_company_field.field_name, db.crm_company_field_value.field_value).as_dict(key='crm_company_field.field_name')
			
			data[str(i)]={
				'Company': 'NA' if not company_data else company_data['company_name']['crm_company_field_value']['field_value'],
				'Name':str(contact_data['first_name']['crm_contact_field_value']['field_value'])+' '+str(contact_data['last_name']['crm_contact_field_value']['field_value']),
				'Email':str(contact_data['email_id']['crm_contact_field_value']['field_value']),
				'Phone':'NA' if not company_data else str(company_data['phone_no']['crm_company_field_value']['field_value']),
				'Type of Contact':contact_data['type_of_contact']['crm_contact_field_value']['field_value'],
				'Designation':str(contact_data['designation']['crm_contact_field_value']['field_value']),
				'Department':str(contact_data['department']['crm_contact_field_value']['field_value']),
				'contact_key_id':keys[i].id
			}
			data_flag=1
		if len(data)==0:
			data['0']={
				'Company':'',
				'Name':'',
				'Email':'',
				'Phone':'',
				'Type of Contact':'',
				'Designation':'',
				'Department':'',
				'contact_key_id':''
			}
			data_flag=0
		filter_field=contact_filter_field()
	except Exception as e:
		return 'error in getting data (%s)' %e
	else:
		return dict(data=data,data_flag=data_flag,filter_field=filter_field)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_contacts_with_filter(lFilterData):	# limit is a dict 
	
	# # Data for the testing
	# ={'company_id':25,
	# 	'lFilterOutput':{'Company': ['company_name.startswith("a")'], 'Contact': []} }


	data_flag=0
	lFieldList={}
	present=['company_name','lead_status','description','lead_source','phone_no','email_id']
	for condition in lFilterData['lFilterOutput'].keys():
		for data in lFilterData['lFilterOutput'][condition]:
			if data.split('.')[0] not in present:
				name=data.split('.')[0].title()
				name=name.replace('_',' ')
				# lFieldList.append(str('"'+name+'"'+' : '+'str('+condition.lower()+'_data['+'"'+data.split('.')[0]+'"'+']["crm_'+condition.lower()+'_field_value"]["field_value"])'))
				lFieldList[name]=(str('str('+condition.lower()+'_data['+'"'+data.split('.')[0]+'"'+']["crm_'+condition.lower()+'_field_value"]["field_value"])'))
		pass


	try:
		# get the filter fields to process the data
		lFilterField=contact_filter_field()
		data={}
		lContactIdList=[]
		lCompanyIdList=[]
		
		#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
		if len(lFilterData['lFilterOutput']['Company'])>0: # have company data

			# have to select the contact id to get the contacts list for that
			lList=lFilterData['lFilterOutput']['Company']
			lFirstFlag=0

			for lCondition in lList:
				if lFirstFlag==0:

					rows=db(
							(db.crm_company_field.id==db.crm_company_field_value.field_id)&
							(db.crm_company_field.field_name == lCondition.split('.')[0]) &
							(eval('db.crm_company_field_value.field_value.'+lCondition.split('.')[1]))&
							(db.crm_company_field_key.is_active == True) & 
							(db.crm_company_field_key.company_id == lFilterData['company_id'])
							).select(
							db.crm_company_field_value.company_key_id
							)
					lCompanyIdList=[]
					for row in rows:
						lCompanyIdList.append(row.company_key_id)

					lFirstFlag=1
					pass
				elif lFirstFlag==1:
					rows=db(
							(db.crm_company_field.id==db.crm_company_field_value.field_id)&
							(db.crm_company_field.field_name == lCondition.split('.')[0]) &
							(eval('db.crm_company_field_value.field_value.'+lCondition.split('.')[1]))&
							(db.crm_company_field_value.company_key_id.belongs(lCompanyIdList))
							).select(
							db.crm_company_field_value.company_key_id
							)
					lCompanyIdList=[]
					for row in rows:
						lCompanyIdList.append(row.company_key_id)

					pass
			#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
			if len(lFilterData['lFilterOutput']['Contact'])>0:	# have contact data
				lList=lFilterData['lFilterOutput']['Contact']
				lFirstFlag=0

				for lCondition in lList:
					if lFirstFlag==0:
						rows=db(
								(db.crm_contact_field.id==db.crm_contact_field_value.field_id)&
								(db.crm_contact_field_key.id==db.crm_contact_field_value.contact_key_id)&
								(db.crm_contact_field.field_name == lCondition.split('.')[0]) &
								(eval('db.crm_contact_field_value.field_value.'+lCondition.split('.')[1]))&
								(db.crm_contact_field_key.company_key_id.belongs(lCompanyIdList))&
								(db.crm_contact_field_key.is_active == True) & 
								(db.crm_contact_field_key.company_id == lFilterData['company_id'])
								).select(
								db.crm_contact_field_value.contact_key_id
								)
						lCompanyIdList=[]
						for row in rows:
							lContactIdList.append(row.contact_key_id)

						lFirstFlag=1
						pass
					elif lFirstFlag==1:
						rows=db(
								(db.crm_contact_field.id==db.crm_contact_field_value.field_id)&
								(db.crm_contact_field_key.id==db.crm_contact_field_value.contact_key_id)&
								(db.crm_contact_field.field_name == lCondition.split('.')[0]) &
								(eval('db.crm_contact_field_value.field_value.'+lCondition.split('.')[1]))&
								(db.crm_contact_field_value.contact_key_id.belongs(lContactIdList))
								).select(
								db.crm_contact_field_value.contact_key_id
								)
						lCompanyIdList=[]
						for row in rows:
							lContactIdList.append(row.contact_key_id)
						test=lCompanyIdList
						pass
			
			#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
			else: 		# no contact data
				# in this we donot have a filter on the contact data, but we have for the company data
				lContactIdList=[]
				rows=db((db.crm_contact_field_key.company_key_id.belongs(lCompanyIdList))&
						(db.crm_contact_field_key.is_active == True) & 
						(db.crm_contact_field_key.company_id == lFilterData['company_id'])
						).select(
						db.crm_contact_field_key.id
						)
				for row in rows:
					lContactIdList.append(row.id)

				pass
			
			pass
		
		#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
		else:		# no company data

			#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
			if len(lFilterData['lFilterOutput']['Contact'])>0:	# have contact data

				lList=lFilterData['lFilterOutput']['Contact']
				lFirstFlag=0
				for lCondition in lList:
					if lFirstFlag==0:
						rows=db(
								(db.crm_contact_field.id==db.crm_contact_field_value.field_id)&
								(db.crm_contact_field_key.id==db.crm_contact_field_value.contact_key_id)&
								(db.crm_contact_field.field_name == lCondition.split('.')[0]) &
								(eval('db.crm_contact_field_value.field_value.'+lCondition.split('.')[1]))&
								(db.crm_contact_field_key.is_active == True) & 
								(db.crm_contact_field_key.company_id == lFilterData['company_id'])
								).select(
								db.crm_contact_field_value.contact_key_id
								)
						lContactIdList=[]
						for row in rows:
							lContactIdList.append(row.contact_key_id)

						lFirstFlag=1
						pass
					elif lFirstFlag==1:
						rows=db(
								(db.crm_contact_field.id==db.crm_contact_field_value.field_id)&
								(db.crm_contact_field_key.id==db.crm_contact_field_value.contact_key_id)&
								(db.crm_contact_field.field_name == lCondition.split('.')[0]) &
								(eval('db.crm_contact_field_value.field_value.'+lCondition.split('.')[1]))&
								(db.crm_contact_field_value.contact_key_id.belongs(lContactIdList))
								).select(
								db.crm_contact_field_value.contact_key_id
								)
						lCompanyIdList=[]
						for row in rows:
							lContactIdList.append(row.contact_key_id)

				
				pass
			#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
			else: 		# no contact data
				# this condition is not posible as there is no filters, but still for safety
				rows=db((db.crm_lead_field_key.is_active == True) & 
						(db.crm_lead_field_key.company_id == lFilterData['company_id'])
						).select(
						db.crm_lead_field_key.id,
						orderby=~db.crm_lead_field_key.id
						)
				lLeadIdList=[]
				for row in rows:
					lLeadIdList.append(row.lead_key_id)

			pass

		# END #
		#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞	
		i=0

		for key in sorted(lContactIdList):

			contact_data = db( 
				(db.crm_contact_field_value.field_id == db.crm_contact_field.id) & 
				(db.crm_contact_field_value.contact_key_id == key) & 
				(db.crm_contact_field_value.is_active == True) & 
				(db.crm_contact_field_value.company_id == lFilterData['company_id'])
				).select(
				db.crm_contact_field.field_name,
				 db.crm_contact_field_value.field_value
				 ).as_dict(key='crm_contact_field.field_name')

			company_data = db(
				(db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & 
				(db.crm_contact_field_key.id == key) & 
				(db.crm_company_field_value.field_id == db.crm_company_field.id) & 
				(db.crm_company_field_value.is_active == True) & 
				(db.crm_company_field_value.company_id == lFilterData['company_id'])
				).select(
				db.crm_company_field.field_name, 
				db.crm_company_field_value.field_value).as_dict(key='crm_company_field.field_name')
			
			data[str(i)]={
				'Company': 'NA' if not company_data else company_data['company_name']['crm_company_field_value']['field_value'],
				'Name':str(contact_data['first_name']['crm_contact_field_value']['field_value'])+' '+str(contact_data['last_name']['crm_contact_field_value']['field_value']),
				'Email':str(contact_data['email_id']['crm_contact_field_value']['field_value']),
				'Phone':'NA' if not company_data else str(company_data['phone_no']['crm_company_field_value']['field_value']),
				'Type of Contact':contact_data['type_of_contact']['crm_contact_field_value']['field_value'],
				'Designation':str(contact_data['designation']['crm_contact_field_value']['field_value']),
				'Department':str(contact_data['department']['crm_contact_field_value']['field_value']),
				'contact_key_id':str(key)
			}
			for key in lFieldList:
				data[str(i)][key]=eval(lFieldList[key])
				pass
			data_flag=1
			i+=1
			pass

		if len(data)==0:
			data[str(i)]={
				'Company':'',
				'Name':'',
				'Email':'',
				'Phone':'',
				'Type of Contact':'',
				'Designation':'',
				'Department':'',
				'contact_key_id':''
			}
			data_flag=0
		filter_field=contact_filter_field()

		return dict(filter_field=lFilterField,data=data,data_flag=data_flag)

	except Exception as e:
		return 'Exception Raised : '+str(e)
	# else: # not needed exactly
	# 	return locals()
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def fetch_contact_basic_details(lRequestData):
	
	# ={}
	# lRequestData={
	# 	'contact_key_id':30,
	# 	'user_id': 2,
	# 	'company_id':25,
	# 	'update_head': "notes"
	# }


	data = {}
	data['contact_details'] = db(
		(db.crm_contact_field_key.id == db.crm_contact_field_value.contact_key_id) & 
		(db.crm_contact_field_value.field_id == db.crm_contact_field.id) & 
		(db.crm_contact_field_key.id == lRequestData['contact_key_id']) & 
		(db.crm_contact_field_value.is_active == True) & 
		(db.crm_contact_field_value.company_id == lRequestData['company_id'])
		).select(
		db.crm_contact_field.field_name, 
		db.crm_contact_field_value.field_value
		).as_list()
	
	data['company_details'] = db(
		(db.crm_contact_field_key.id == lRequestData['contact_key_id'])& 
		(db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & 
		(db.crm_company_field_value.field_id == db.crm_company_field.id) & 
		(db.crm_company_field_value.is_active == True) & 
		(db.crm_company_field_value.company_id == lRequestData['company_id'])
		).select(
		db.crm_company_field.field_name, 
		db.crm_company_field_value.field_value
		).as_list()
	


	
	# contact donot have the comapny details
	# send a basic default dictionary for that
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
		'crm_company_field_value'	:	{'field_value'	:	'NA'}
		},
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
def add_contact(data):
	
	done=0
	
	lReturnDict={'lKeyId':0,'msg':''}
	# have to enter the data into the key table first
	
	try:
		lKeyId=db.crm_contact_field_key.insert(
				company_key_id=data['data']['company_key_id'],
				company_id=data['data']['company_id'] ,
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
