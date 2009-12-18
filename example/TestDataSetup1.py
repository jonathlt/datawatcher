import pyodbc

connstring = 'Driver={Microsoft Access Driver (*.mdb)};Dbq=Example.mdb;Uid=Admin;Pwd=;'

connsrc = pyodbc.connect(connstring)
cursor = connsrc.cursor()
  
sSQL = 'DROP TABLE [Logos_Test]'
print 'DROPPING Logos_Test'
cursor.execute(sSQL)

sSQL = 'CREATE TABLE [Logos_Test] ( ID NUMBER, HTML TEXT, Link TEXT, Additional_Text TEXT)'
print 'CREATING new Logos_Test'
cursor.execute(sSQL)

sSQL = 'INSERT INTO Logos_Test (ID, HTML, Link, Additional_Text) SELECT ID, HTML, Link, Additional_Text FROM Logos'
print 'INSERTING data from Logos_Test'
cursor.execute(sSQL)

cursor.close()
connsrc.commit()
connsrc.close()
