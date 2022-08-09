import sqlite3
con = sqlite3.connect('sql_app.db')
cur = con.cursor()

def createtable(name_table):
	cur.execute('''CREATE TABLE {}(ft_ent_identifier text, published text, reactions text, sentiments text, comments_shares text)'''.format(name_table))
	

def savedata(data,name_table):
	
	list_of_tuple=[]
	n=len(data['published'])
	for i in range(n):
		list_of_tuple.append((data['ft ent identifier'][i],data['published'][i],data['reactions'][i],data['comments_shares'][i][0][0],data['comments_shares'][i][1][0]))
	cur.executemany('INSERT INTO {} VALUES(?, ?, ?, ?, ?)'.format(name_table), list_of_tuple)
	print(list_of_tuple)
	con.commit()
	
#for row in con.execute("select * from stocks"):
    #print(row)


#def selectdata(name_table):
	#for row in con.execute("select rowid, name, ingredients from recipe where name match 'pie'"):
    
	#return
