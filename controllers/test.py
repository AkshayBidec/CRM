# from gluon.tools import Service
# service = Service(globals())

# @service.xmlrpc
# def add(a,b): return a+b

# @service.xmlrpc
# def sub(a,b): return a-b

# @service.xmlrpc
# def string(data):
# 	out=data['email_id']+data['password']
# 	return out


# @service.xmlrpc
# def leads_add_ff():
# 	field_names={'field':'value'}
# 	rows = db(db.crm_lead_field.field_name != None).select()
# 	for row in rows:
# 		field_names.update({row.field_name:''})

# 	del field_names['field']
# 	return dict(field_names)


# def call(): return service() 

def test():
		field_names={'field':'value'}
		rows = db(db.crm_contact_field.is_active==True).select()
		lList=[]
		for row in rows:

			lList=[row.field_widget_attributes,row.field_requires_attributes] 		# make a list of required details for the field

			field_names.update({row.field_name:lList})

		del field_names['field']
		return dict(field_names)

def month_selector():

	if not request.vars.month: return ''

	data= '%'+request.vars.month+'%'
	selected=[]
	rows=db((db.crm_lead_field_value.field_id==1)&(db.crm_lead_field_value.field_value.like(data,case_sensitive=False))).select(db.crm_lead_field_value.field_value)
	for row in rows:
		selected.append(row.field_value)


	# months = ['January', 'February', 'March', 'April', 'May',

	#           'June', 'July', 'August', 'September' ,'October',
	# #           'November', 'December']
	# month_start = request.vars.month.capitalize()
	# selected = [m for m in months if m.startswith(month_start)]

	return DIV(*[DIV(k,
	             _onclick="jQuery('#month').val('%s')" % k,
	             _onmouseover="this.style.backgroundColor='yellow'",
	             _onmouseout="this.style.backgroundColor='white'"
	             ) for k in selected])



def test2():
	lLimit={}
	lLimit['countTo']=10		# total number of fieds required, replace it with request.vars.* to make it dynamin
	lLimit['countFrom']=0		# no of the row to start from 
	lLimit['order']='~db.crm_lead_field_key.id' 	# the name of field to order on, string will be evaluated in the api
	
	# try:
	# get the key values according to the request
	

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
	
		data[i]={
			'Company':company_data[0]['crm_company_field_value']['field_value'],
			'Name':str(contact_data[0]['field_value'])+' '+str(contact_data[1]['field_value']),
			'Email':str(contact_data[6]['field_value']),
			'Phone':str(company_data[3]['crm_company_field_value']['field_value']),
			'Lead Source':lead_data[0]['field_value'],
			'Description':lead_data[5]['field_value'],
			'Status':lead_data[1]['field_value']
		}





	

	return locals()




	# keys=db(db.crm_lead_field_key).select(orderby=eval(lLimit['order']),limitby=(lLimit['countFrom'],lLimit['countTo']))
	
	# select the field and there respective values according to the request, using the inner join
	# leads= db(db.crm_lead_field_value.field_id==db.crm_lead_field.id)(db.crm_lead_field_value.lead_key_id<=keys[0].id)(db.crm_lead_field_value.lead_key_id>=keys[-1].id).select(db.crm_lead_field_value.lead_key_id,db.crm_lead_field_value.field_value,db.crm_lead_field.field_name,orderby=~db.crm_lead_field_value.lead_key_id|db.crm_lead_field.id)
	
	# leads=db(
	# 	(db.crm_lead_field_key.contact_key_id == db.crm_contact_field_key.id)&
	# 	(db.crm_lead_field_key.contact_key_id == db.crm_contact_field_value.contact_key_id)&
	# 	(db.crm_lead_field_key.contact_key_id == db.crm_lead_field_value.id)&
	# 	(db.crm_lead_field_value.lead_key_id<=lead_field_keys[0].id)&(db.crm_lead_field_value.lead_key_id>=lead_field_keys[-1].id)&
	# 	(db.crm_contact_field_value.field_id == db.crm_contact_field.id)&
	# 	(db.crm_lead_field_value.field_id == db.crm_lead_field.id)
	# 	).select(
	# 	db.crm_lead_field_key.id,
	# 	db.crm_contact_field_key.id,
	# 	db.crm_company_field_key.id,
	# 	db.crm_contact_field_value.field_value,
	# 	db.crm_lead_field_value.field_value,
	# 	db.crm_company_field_value.field_value,
	# 	db.crm_lead_field.field_name,
	# 	db.crm_contact_field.field_name,
	# 	db.crm_company_field.field_name,

	# 	left=[db.crm_company_field_key.on(db.crm_contact_field_key.company_key_id == db.crm_company_field_key.id),
	# 		db.crm_company_field_value.on(db.crm_company_field_value.company_key_id == db.crm_company_field_key.id),
	# 		db.crm_company_field.on(db.crm_company_field.id == db.crm_company_field_value.field_id)],

	# # 	orderby=~db.crm_lead_field_value.lead_key_id
	# # 	)

	# lLeadsDict={
	# 	'Company':"",
	# 	'Name':"",
	# 	'Email':"",
	# 	'Phone':"",
	# 	'Lead Source':"",
	# 	'Description':"",
	# 	'Status':""
	# }






