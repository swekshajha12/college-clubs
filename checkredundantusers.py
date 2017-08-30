from databaseconnection import connections
c,conn=connections()

def check(data):
	eml=data[1]
	if eml:
		c.execute("select email from user where email=:eml",{"eml":eml})
		x=c.fetchall()
		if len(x)>0:
			return 0
		del x
	if data[2]:
			
		uname=data[2]
		c.execute("select username from user where username=:uname",{"uname":uname})
		x=c.fetchall()
		if len(x)>0:
			return 0
		
	return 1
def insert(data):
	if check(data)==1:
		c.execute('insert into user values(?,?,?,?)',data)
		conn.commit()
		conn.close()
		return 1
	return 0			
#data=['aa','j.@gmail.com','abc','sdkd']
#print(insert(data))
