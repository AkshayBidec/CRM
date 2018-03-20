
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
# fucntion to get the form field for the filter 
def leads_filter_field():
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

		field_names={'field':'value'}
		rows = db(db.crm_lead_field.is_active==True )(db.crm_lead_field.filter_flag==True).select()
		lList=[]
		for row in rows:
			lList=[row.field_widget_attributes,row.field_requires_attributes]
			field_names.update({row.field_name:lList})

		lDict={}		# a dict to store the options of the leads status
		lListValues=db(db.crm_lead_status_master).select(db.crm_lead_status_master.lead_status,db.crm_lead_status_master.id).as_dict(key='id')
		
		# make the dictionary of the lead status and its id as the key
		for key in sorted(lListValues.keys()):
			lDict[str(key)]=lListValues[key]['lead_status']
		# replace the dummy dictionary with the oreginal one for the proper representation
		field_names['lead_status'][1]="IS_IN_SET("+str(lDict)+",zero='Lead Status')"
		del field_names['field']

		lFinalFilterFields['Lead']=field_names

		return dict(lFinalFilterFields)
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
							activity='Status Updated',
							session_id=data['data']['session_id'],
							company_id=data['data']['company_id'],
							lead_key_id=data['data']['lead_key_id'],
							lead_status_master_id=data['data']['lead_status'],
							db_entry_time=lambda:datetime.now(),
							db_entered_by=data['data']['user_id'],
							db_entered_by_name=lRequestData['name']
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
	data_flag=0
	try:
		
		keys=db((db.crm_lead_field_key.is_active == True) & (db.crm_lead_field_key.company_id == company_id)).select(db.crm_lead_field_key.id,orderby=~db.crm_lead_field_key.id)
		data={}
		
		for  i in range (0,len(keys)):
			
			lead_data = db((db.crm_lead_field_key.id == db.crm_lead_field_value.lead_key_id) & (db.crm_lead_field_value.field_id == db.crm_lead_field.id) & (db.crm_lead_field_value.is_active == True) & (db.crm_lead_field_value.company_id == company_id) & (db.crm_lead_field_key.id == keys[i].id)).select(db.crm_lead_field.field_name, db.crm_lead_field_value.field_value).as_dict(key='crm_lead_field.field_name')
			
			contact_data = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id) & (db.crm_contact_field_value.field_id == db.crm_contact_field.id) & (db.crm_lead_field_key.id == keys[i].id) & (db.crm_contact_field_value.is_active == True) & (db.crm_contact_field_value.company_id == company_id)).select(db.crm_contact_field.field_name, db.crm_contact_field_value.field_value).as_dict(key='crm_contact_field.field_name')
			company_data = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field_value.is_active == True) & (db.crm_lead_field_key.id == keys[i].id) & (db.crm_company_field_value.company_id == company_id)).select(db.crm_company_field.field_name, db.crm_company_field_value.field_value).as_dict(key='crm_company_field.field_name')
			lead_status = db(
				(db.crm_lead_status.lead_key_id == keys[i].id) & 
				(db.crm_lead_status.is_active == True) & 
				(db.crm_lead_status.lead_status_master_id == db.crm_lead_status_master.id)
				).select(
				db.crm_lead_status.lead_key_id,
				db.crm_lead_status_master.lead_status, 
				orderby=~db.crm_lead_status.db_entry_time,limitby=(0,1)
				).as_dict(key='crm_lead_status.lead_key_id')
		
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
			data_flag=1
			pass
		lFilterField=leads_filter_field()
		if len(data)==0:
			data['0']={
				'Company': '',
				'Name':'',
				'Email':'',
				'Phone':'',
				'Lead Source':'',
				'Description':'',
				'Status':'',
				'lead_key_id':''
			}
			data_flag=0



	except Exception as e:
		return 'Exception Raised : '+e
	else:
		return dict(data=data,filter_field=lFilterField,data_flag=data_flag)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def get_leads_with_filter(lFilterData):	# limit is a dict 
	

	# ={'company_id':25,
	# 	'lFilterOutput':{
	# 	'Company': [],
	# 	 'Contact': [], 
	# 	 'Lead': ['lead_owner.contains("super user")']
	# 	 } }
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
		lFilterField=leads_filter_field()
		data={}
		lContactIdList=[]
		lCompanyIdList=[]
		lLeadIdList=[]
		
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

				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				if len(lFilterData['lFilterOutput']['Lead'])>0: # have lead data
					lList=lFilterData['lFilterOutput']['Lead']
					lFirstFlag=0

					for lCondition in lList:
						if lFirstFlag==0:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
									(db.crm_lead_field_key.is_active == True) & 
									(db.crm_lead_field_key.company_id == lFilterData['company_id'])
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

							lFirstFlag=1
							pass
						elif lFirstFlag==1:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_value.lead_key_id.belongs(lLeadIdList))
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

							pass
				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				else:	# no leads data
					lLeadIdList=[]
					rows=db((db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
							(db.crm_lead_field_key.is_active == True) & 
							(db.crm_lead_field_key.company_id == lFilterData['company_id'])
							).select(
							db.crm_lead_field_key.id
							)
					for row in rows:
						lLeadIdList.append(row.id)
					pass
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


				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				if len(lFilterData['lFilterOutput']['Lead'])>0: # have the leads data
					lList=lFilterData['lFilterOutput']['Lead']
					lFirstFlag=0

					for lCondition in lList:
						if lFirstFlag==0:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
									(db.crm_lead_field_key.is_active == True) & 
									(db.crm_lead_field_key.company_id == lFilterData['company_id'])
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

							lFirstFlag=1
							pass
						elif lFirstFlag==1:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_value.lead_key_id.belongs(lLeadIdList))
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

					pass
				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				else:		# no leads data
					lLeadIdList=[]
					rows=db((db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
							(db.crm_lead_field_key.is_active == True) & 
							(db.crm_lead_field_key.company_id == lFilterData['company_id'])
							).select(
							db.crm_lead_field_key.id
							)
					for row in rows:
						lLeadIdList.append(row.id)
					
					pass
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

				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				if len(lFilterData['lFilterOutput']['Lead'])>0: # have lead data
					lList=lFilterData['lFilterOutput']['Lead']
					lFirstFlag=0

					for lCondition in lList:
						if lFirstFlag==0:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
									(db.crm_lead_field_key.is_active == True) & 
									(db.crm_lead_field_key.company_id == lFilterData['company_id'])
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

							lFirstFlag=1
							pass
						elif lFirstFlag==1:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_value.lead_key_id.belongs(lLeadIdList))
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)
					pass
				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				else:	# no leads data
					lLeadIdList=[]
					rows=db((db.crm_lead_field_key.contact_key_id.belongs(lContactIdList))&
							(db.crm_lead_field_key.is_active == True) & 
							(db.crm_lead_field_key.company_id == lFilterData['company_id'])
							).select(
							db.crm_lead_field_key.id
							)
					for row in rows:
						lLeadIdList.append(row.id)
					pass
				pass
			#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
			else: 		# no contact data
				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
				if len(lFilterData['lFilterOutput']['Lead'])>0:		# have the leads data
					lList=lFilterData['lFilterOutput']['Lead']
					lFirstFlag=0

					for lCondition in lList:
						if lFirstFlag==0:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_key.is_active == True) & 
									(db.crm_lead_field_key.company_id == lFilterData['company_id'])
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

							lFirstFlag=1
							pass
						elif lFirstFlag==1:
							rows=db(
									(db.crm_lead_field.id==db.crm_lead_field_value.field_id)&
									(db.crm_lead_field_key.id==db.crm_lead_field_value.lead_key_id)&
									(db.crm_lead_field.field_name == lCondition.split('.')[0]) &
									(eval('db.crm_lead_field_value.field_value.'+lCondition.split('.')[1]))&
									(db.crm_lead_field_value.lead_key_id.belongs(lLeadIdList))
									).select(
									db.crm_lead_field_value.lead_key_id
									)
							lLeadIdList=[]
							for row in rows:
								lLeadIdList.append(row.lead_key_id)

					pass
				#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞	
				else:		# no leads data
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

			pass

		# END #
		#∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞	
		i=0

		for  key in sorted(lLeadIdList):
			
			lead_data = db(
				(db.crm_lead_field_key.id == db.crm_lead_field_value.lead_key_id) & 
				(db.crm_lead_field_value.field_id == db.crm_lead_field.id) & 
				(db.crm_lead_field_value.is_active == True) & 
				(db.crm_lead_field_value.company_id == lFilterData['company_id']) & 
				(db.crm_lead_field_key.id == key)
				).select(
				db.crm_lead_field.field_name, 
				db.crm_lead_field_value.field_value
				).as_dict(key='crm_lead_field.field_name')
			
			contact_data = db(
				(db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id) & 
				(db.crm_contact_field_value.field_id == db.crm_contact_field.id) & 
				(db.crm_lead_field_key.id == key) & 
				(db.crm_contact_field_value.is_active == True) & 
				(db.crm_contact_field_value.company_id == lFilterData['company_id'])
				).select(
				db.crm_contact_field.field_name, 
				db.crm_contact_field_value.field_value
				).as_dict(key='crm_contact_field.field_name')

			company_data = db((db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id) & (db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & (db.crm_company_field_value.field_id == db.crm_company_field.id) & (db.crm_company_field_value.is_active == True) & (db.crm_lead_field_key.id == key) & (db.crm_company_field_value.company_id == lFilterData['company_id'])).select(db.crm_company_field.field_name, db.crm_company_field_value.field_value).as_dict(key='crm_company_field.field_name')
			
			lead_status = db((db.crm_lead_status.lead_key_id == key) & (db.crm_lead_status.is_active == True) & (db.crm_lead_status.lead_status_master_id == db.crm_lead_status_master.id)).select(db.crm_lead_status.lead_key_id,db.crm_lead_status_master.lead_status, orderby=~db.crm_lead_status.db_entry_time,limitby=(0,1)).as_dict(key='crm_lead_status.lead_key_id')
		
			data[str(i)]={
				'Company': 'NA' if not company_data else company_data['company_name']['crm_company_field_value']['field_value'],
				'Name':str(contact_data['first_name']['crm_contact_field_value']['field_value'])+' '+str(contact_data['last_name']['crm_contact_field_value']['field_value']),
				'Email':str(contact_data['email_id']['crm_contact_field_value']['field_value']),
				'Phone':'NA' if not company_data else str(company_data['phone_no']['crm_company_field_value']['field_value']),
				'Lead Source':lead_data['lead_source']['crm_lead_field_value']['field_value'],
				'Description':lead_data['description']['crm_lead_field_value']['field_value'],
				'Status':'NA' if not lead_status else lead_status[key]['crm_lead_status_master']['lead_status'],
				'lead_key_id':str(key)
			}
			# enter the extra requested data
			for key in lFieldList:
				data[str(i)][key]=eval(lFieldList[key])
				pass
			i+=1
			data_flag=1			
			pass
		
		if len(data)==0:
			data['0']={
				'Company': '',
				'Name':'',
				'Email':'',
				'Phone':'',
				'Lead Source':'',
				'Description':'',
				'Status':'',
				'lead_key_id':''
			}
			data_flag=0


		return dict(filter_field=lFilterField,data=data,data_flag=data_flag)

	except Exception as e:
		return 'Exception Raised : '+str(e)
	# else:
		# return locals()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def lead_delete(lead_key_id):
	try:
		db(db.crm_lead_field_key.id== lead_key_id)(db.crm_company_field_key.is_active==True).update(
			is_active=False)
	except Exception as e:
		return str(e)
	else:
		try:
			db(db.crm_lead_field_value.lead_key_id == lead_key_id)(db.crm_lead_field_value.is_active==True).update(
				is_active=False)
		except Exception as e:
			return str(e)
		else:
			return 'done'

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
				activity='Lead Created',
				session_id=data['data']['session_id'],
				company_id=data['data']['company_id'],
				lead_key_id=lKeyId,
				lead_status_master_id=data['data']['lead_status'],				
				db_entry_time=lambda:datetime.now(),
				db_entered_by=data['data']['user_id'],
				db_entered_by_name=lRequestData['name']
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
	# 	'lead_key_id':50,
	# 	'user_id': 2,
	# 	'company_id':25,
	# 	'update_head': "notes"
	# }


	data = {}
	data['lead_details'] = db(
		(db.crm_lead_field_key.id == db.crm_lead_field_value.lead_key_id) & 
		(db.crm_lead_field_value.field_id == db.crm_lead_field.id) & 
		(db.crm_lead_field_value.is_active == True) & 
		(db.crm_lead_field_value.company_id == lRequestData['company_id']) & 
		(db.crm_lead_field_key.id == lRequestData['lead_key_id'])
		).select(
		db.crm_lead_field.field_name, 
		db.crm_lead_field_value.field_value).as_list()

	data['contact_details'] = db(
		(db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id) & 
		(db.crm_contact_field_value.field_id == db.crm_contact_field.id) & 
		(db.crm_lead_field_key.id == lRequestData['lead_key_id']) & 
		(db.crm_contact_field_value.is_active == True) & 
		(db.crm_contact_field_value.company_id == lRequestData['company_id'])
		).select(
		db.crm_contact_field_value.contact_key_id,
		db.crm_contact_field.field_name, 
		db.crm_contact_field_value.field_value).as_list()

	data['company_details'] = db(
		(db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id) & 
		(db.crm_contact_field_key.company_key_id == db.crm_company_field_value.company_key_id) & 
		(db.crm_company_field_value.field_id == db.crm_company_field.id) & 
		(db.crm_company_field_value.is_active == True) & 
		(db.crm_lead_field_key.id == lRequestData['lead_key_id']) & 
		(db.crm_company_field_value.company_id == lRequestData['company_id'])
		).select(
		db.crm_company_field.field_name, 
		db.crm_company_field_value.company_key_id,
		db.crm_company_field_value.field_value).as_list()
	
	data['lead_details'][1]['crm_lead_field_value']['field_value']=db(
		(db.crm_lead_status.lead_key_id==lRequestData['lead_key_id'])& 
		(db.crm_lead_status.is_active==True)
		).select(db.crm_lead_status.lead_status_master_id)[0].lead_status_master_id
	lead_status=db(db.crm_lead_status_master.id==int(data['lead_details'][1]['crm_lead_field_value']['field_value'])
		).select(db.crm_lead_status_master.lead_status)
	data['lead_details'][1]['crm_lead_field_value']['field_value']=lead_status[0].lead_status+'.'+str(data['lead_details'][1]['crm_lead_field_value']['field_value'])
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
	# 'lead_key_id': '49',
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
			db.crm_lead_updates.head_id, 
			db.crm_lead_updates.title, 
			db.crm_lead_updates.update_file_name, 
			db.crm_lead_updates.head_version, 
			db.crm_lead_updates.db_entry_time,
			db.crm_lead_updates.db_entered_by_name, 
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

def download(): return response.download(request,db)

def get_versions():
	return locals()
def water_test_form():
	lFields=[]
	rows = db(db.crm_water_test_field.is_active==True).select()
	for row in rows:
		if row.field_widget_attributes:
			widget=eval(row.field_widget_attributes)
		else:
			widget=eval('SQLFORM.widgets.string.widget') 		# a default value for a field if the widget not given
		if row.field_requires_attributes:
			requires=eval(row.field_requires_attributes)
		else:
			requires=[] 		# it is a list and can be empty		
		lFields.append(Field('f_'+str(row.id),widget=widget, requires=requires))

	form =SQLFORM.factory(*lFields)
	return form

def upload():

	session_data= request.vars
	# session_data={'lead_key_id' : '2' ,
	# 		 'user_id' : '2' ,
	# 		 'company_id' :'25' , 
	# 		 'session_id':'50' , 'lead_status_id' : '1','update_head':'p_&_i_digrams'}
	
	# lWaterTestForm=water_test_form()
	fields=[]
	lWaterTestField=db(db.crm_water_test_field.is_active==True).select()
	for row in lWaterTestField:
		fields.append(eval('INPUT(_name="f_'+str(row.id)+'",_type="string")'))
		pass
	water_form=FORM(*fields)

	upload_form = FORM(
		INPUT(_name='description',_type='text'),
		INPUT(_name='update_file',_type='file'),
		INPUT(_name='version',_type='string'),
		INPUT(_name='head_id',_type='string'),
		INPUT(_name='title',_type='string')
		)
	done=0
	e=''
	if upload_form.accepts(request.vars,formname='upload_form'):
		if type(upload_form.vars.update_file) != bytes:
			try:
				lStorageFile = db.crm_lead_updates.update_file.store(upload_form.vars.update_file.file, upload_form.vars.update_file.filename)
				db.crm_lead_updates.insert(
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							lead_status_id=session_data['lead_status_id'],
							update_head=session_data['update_head'],
							update_data=upload_form.vars.description,
							title=upload_form.vars.title,
							head_id=upload_form.vars.head_id,
							update_file_name= upload_form.vars.update_file.filename,
							update_file= lStorageFile,
							head_version=upload_form.vars.version or 0,
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id'],
							db_entered_by_name=session_data['user_name']
							)
			except Exception as e:
				return e

			else:
				# have to update the status also
				try:
					db((db.crm_lead_status.lead_key_id==session_data['lead_key_id'])&
						(db.crm_lead_status.is_active==True)).update(is_active=False)
					db.crm_lead_status.insert(
							activity=session_data['update_head'].title().replace('_',' ')+' added',
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							current_stage='1',
							lead_status_master_id=session_data['lead_status_id'],
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id'],
							db_entered_by_name=session_data['user_name']
							)
					pass
				except Exception as e:
					return 'error in adding the lead status' + str(e)
					pass
				else:
					done=1
		else:
			try:
				db.crm_lead_updates.insert(
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							lead_status_id=session_data['lead_status_id'],
							update_head=session_data['update_head'],
							update_data=str(upload_form.vars.description)+' *No file included * ',
							title=upload_form.vars.title,
							head_id=upload_form.vars.head_id,
							update_file_name='No file attached',
							update_file= 'NA',
							head_version=upload_form.vars.version or 0,
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id'],
							db_entered_by_name=session_data['user_name']
							)
			except Exception as e:
				return e
			else:
				# have to update the status also
				try:
					db((db.crm_lead_status.lead_key_id==session_data['lead_key_id'])&
						(db.crm_lead_status.is_active==True)).update(is_active=False)
					db.crm_lead_status.insert(
							activity=session_data['update_head'].title().replace('_',' ')+' added',
							session_id=session_data['session_id'],
							company_id=session_data['company_id'],
							lead_key_id=session_data['lead_key_id'],
							current_stage='1',
							lead_status_master_id=session_data['lead_status_id'],
							db_entry_time=lambda:datetime.now(),
							db_entered_by=session_data['user_id'],
							db_entered_by_name=session_data['user_name']
							)
					pass
				except Exception as e:
					return 'error in adding the lead status' + str(e)
					pass
				else:
					done=1
	
	if water_form.accepts(request.vars,formname='water_test'):
		
		# add the leads status update and than take that key to store the water test
		try:
			Id=db.crm_lead_updates.insert(
						session_id=session_data['session_id'],
						company_id=session_data['company_id'],
						lead_key_id=session_data['lead_key_id'],
						lead_status_id=session_data['lead_status_id'],
						update_head=session_data['update_head'],
						update_data='Water Test data added',
						title='Water Test Data',
						head_id='1',
						update_file_name='No file attached',
						update_file= 'NA',
						head_version='0',
						db_entry_time=lambda:datetime.now(),
						db_entered_by=session_data['user_id'],
						db_entered_by_name=session_data['user_name']
						)
		except Exception as e:
			return e
		else:
			# have to update the status also
			try:
				db((db.crm_lead_status.lead_key_id==session_data['lead_key_id'])&
					(db.crm_lead_status.is_active==True)).update(is_active=False)
				db.crm_lead_status.insert(
						activity=session_data['update_head'].title().replace('_',' ')+' added',
						session_id=session_data['session_id'],
						company_id=session_data['company_id'],
						lead_key_id=session_data['lead_key_id'],
						current_stage='1',
						lead_status_master_id=session_data['lead_status_id'],
						db_entry_time=lambda:datetime.now(),
						db_entered_by=session_data['user_id'],
						db_entered_by_name=session_data['user_name']
						)
				pass
			except Exception as e:
				return 'error in adding the lead status' + str(e)
				pass
			else:
				for row in lWaterTestField:
					db.crm_water_test_value.insert(
						field_id=row.id,
						key_id=session_data['lead_key_id'],
						key_reference='crm_lead_field_key',
						update_key=Id,
						update_referece='crm_lead_updates',
						test_title=row.field_name,
						test_value=eval('water_form.vars.f_'+str(row.id)),
						company_id=session_data['company_id'],
						session_id=session_data['session_id'],
						db_entry_time=lambda:datetime.now(),
						db_entered_by=session_data['user_id'],
					)
				done=1
	

		

	data=[]
	lRequestData={
	'request_type': 'get',		# get and add
	'lead_key_id': session_data['lead_key_id'],
	'user_id': session_data['user_id'],				##############
	'company_id':session_data['company_id'],		##############
	'update_head': session_data['update_head'],
	'update_data': '',
	'lead_status_id':session_data['lead_status_id'],					
	'session_id':session_data['session_id']		##############
	}
	data=fetch_lead_update_details(lRequestData)
	# return dict(data=data)

	return locals()


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def fetch_lead_status_details(lRequestData):
	
	# ={
	# 'request_type': 'get',		# get and add
	# 'lead_key_id': '49',
	# 'user_id': 2,				##############
	# 'company_id':25,		##############
	# 'update_head': '',
	# 'update_data': 'yes',
	# 'lead_status_id':1,					#request.vars.status_id,
	# 'session_id':0,		##############
	# 'respose':1
	# }

	lData={}
	
	i=0
	lData={}
	rows = db((db.crm_lead_status.lead_key_id==lRequestData['lead_key_id'])&
		(db.crm_lead_status.company_id==lRequestData['company_id'])&
		(db.crm_lead_status.lead_status_master_id==db.crm_lead_status_master.id)
			).select(
			db.crm_lead_status.lead_status_master_id,
			db.crm_lead_status_master.progress,
			db.crm_lead_status_master.lead_status,
			db.crm_lead_status.activity,
			db.crm_lead_status.db_entry_time,
			db.crm_lead_status.db_entered_by,
			db.crm_lead_status.db_entered_by_name,
			).as_list()

	for row in rows:
		lData[str(i)]=row
		time=datetime.now()
		lDuration=relativedelta.relativedelta(time, lData[str(i)]['crm_lead_status']['db_entry_time'])
		if lDuration.years==0:
			if lDuration.months==0:
				if lDuration.days==0:
					if lDuration.hours==0:
						if lDuration.minutes==0:
							lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.seconds)+" sec  ago"
						else:
							lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.minutes)+" minutes  ago"
							
					else:
						lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
				else:
					lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
			else:
				lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
		else:
			lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.years)+" years "+str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"

		i+=1
	
	

	return lData
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@service.xmlrpc
def add_lead_status_details(lRequestData):
	# data={
	# 	'request_type': 'add',		# get and add
	# 	'lead_key_id': 50,
	# 	'user_id': 2,				##############
	# 	'company_id':25,		##############
	# 	'session_id':2,		##############
	# 	'response':'0',
	# 	'activity':'Lead Converted',
	# 	'lead_status_master_id':11,
	# 	'current_stage':3,
	# 	'db_entered_by':2,
	# 	'db_entered_by_name':'test user'
	# 	}
	# ={}
	# lRequestData['data']=data
	d=0
	if lRequestData['data']['response']==0:		# in this we only wish to add the data not to get the list of the data
		try:

			# have to enter the data
			db((db.crm_lead_status.lead_key_id == lRequestData['data']['lead_key_id'])&
				(db.crm_lead_status.is_active == True)
				).update(is_active=False)

			db.crm_lead_status.insert(
				activity=lRequestData['data']['activity'],
				session_id=lRequestData['data']['session_id'],
				company_id=lRequestData['data']['company_id'],
				lead_key_id=lRequestData['data']['lead_key_id'],
				lead_status_master_id=lRequestData['data']['lead_status_master_id'],
				current_stage=lRequestData['data']['current_stage'],
				db_entry_time=lambda:datetime.now(),
				db_entered_by=lRequestData['data']['user_id'],
				db_entered_by_name=lRequestData['data']['db_entered_by_name']
						)

		except Exception as e:
			return e
		else:
			d=1
			
	return locals()


	# elif lRequestData['response'] == 1:
	# 	try:
	# 		# have to enter the data
	# 		db.crm_lead_status.insert(
	# 					activity='Status Updated',
	# 					session_id=lRequestData['session_id'],
	# 					company_id=lRequestData['company_id'],
	# 					lead_key_id=lRequestData['lead_key_id'],
	# 					lead_status_master_id=lRequestData['lead_status_master_id'],
	# 					db_entry_time=lambda:datetime.now(),
	# 					db_entered_by=lRequestData['user_id'],
	# 					db_entered_by_name=lRequestData['name']
	# 					)

	# 	except Exception as e:
	# 		return e
	# 	else:
	# 		lData={}
	
	# 		i=0
	# 		lData={}
	# 		rows = db((db.crm_lead_status.lead_key_id==lRequestData['lead_key_id'])&
	# 			(db.crm_lead_status.company_id==lRequestData['company_id'])&
	# 			(db.crm_lead_status.lead_status_master_id==db.crm_lead_status_master.id)
	# 				).select(
	# 				db.crm_lead_status.lead_status_master_id,
	# 				db.crm_lead_status_master.progress,
	# 				db.crm_lead_status_master.lead_status,
	# 				db.crm_lead_status.activity,
	# 				db.crm_lead_status.db_entry_time,
	# 				db.crm_lead_status.db_entered_by,
	# 				db.crm_lead_status.db_entered_by_name,
	# 				).as_list()

	# 		for row in rows:
	# 			lData[str(i)]=row
	# 			time=datetime.now()
	# 			lDuration=relativedelta.relativedelta(time, lData[str(i)]['crm_lead_status']['db_entry_time'])
	# 			if lDuration.years==0:
	# 				if lDuration.months==0:
	# 					if lDuration.days==0:
	# 						if lDuration.hours==0:
	# 							if lDuration.minutes==0:
	# 								lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.seconds)+" sec  ago"
	# 							else:
	# 								lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.minutes)+" minutes  ago"
									
	# 						else:
	# 							lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
	# 					else:
	# 						lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
	# 				else:
	# 					lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"
	# 			else:
	# 				lData[str(i)]['crm_lead_status']['db_entry_time']=str(lDuration.years)+" years "+str(lDuration.months)+" months "+str(lDuration.days)+" days "+str(lDuration.hours)+" hours "+str(lDuration.minutes)+" minutes  ago"

	# 			i+=1


	# 		return lData
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def lead_status():
	session_data= request.vars
	# form_data={}
	form = FORM(
		INPUT(_name='field_name',_type='string'),
		INPUT(_name='lead_status_master_id',_type='string'),
		INPUT(_name='lead_key_id',_type='string'),
		INPUT(_name='lead_status_stage_value',_type='string'),
		)
	if form.accepts(request.vars,formname='status_form'):
		db((db.crm_lead_status.lead_key_id == form.vars.lead_key_id )&
			(db.crm_lead_status.is_active == True)
			).update(is_active=False)
		db.crm_lead_status.insert(
			activity='Status update at '+ str(form.vars.field_name),
			session_id=session_data['session_id'],
			company_id=session_data['company_id'],
			lead_key_id=form.vars.lead_key_id,
			lead_status_master_id=form.vars.lead_status_master_id,
			current_stage=form.vars.lead_status_stage_value,
			db_entry_time=lambda:datetime.now(),
			db_entered_by=session_data['user_id'],
			db_entered_by_name=session_data['user_name']
			)
		# form_data=form.vars
		pass
	lRequestData={
	'request_type': 'get',		# get and add
	'lead_key_id': session_data['lead_key_id'],
	'user_id': 2,				##############
	'company_id':25,		##############
	'update_head': '',
	'update_data': 'yes',
	'lead_status_id':session_data['lead_status_id'],					#request.vars.status_id,
	'session_id':0,		##############
	'respose':1
	}
	data=fetch_lead_status_details(lRequestData)
	lStatusData={}
	rows= db(db.crm_lead_status_master).select()
	for row in rows:
		lStatus=db((db.crm_lead_status.lead_status_master_id==row.id)&
			(db.crm_lead_status.lead_key_id== session_data['lead_key_id'])
			).select(db.crm_lead_status.current_stage,orderby=~db.crm_lead_status.db_entry_time,limitby=[0,1])
		if len(lStatus)>0:
			lStatusData[str(row.lead_status)]=[lStatus[0].current_stage if lStatus[0].current_stage !=None else 0,row.id]
		else:
			lStatusData[str(row.lead_status)]=[0,row.id]

		pass
	return locals()
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def delete_leads():
	return dict()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def call(): return service() 


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def autocomplete():
	if not request.vars.data: return ''

