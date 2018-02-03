from gluon.tools import Service
service = Service(globals())

@service.xmlrpc
def add(a,b): return a+b

@service.xmlrpc
def sub(a,b): return a-b

@service.xmlrpc
def string(data):
	out=data['email_id']+data['password']
	return out

def call(): return service()