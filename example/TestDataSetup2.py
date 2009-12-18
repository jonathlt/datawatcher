import pyodbc

connstring = 'Driver={Microsoft Access Driver (*.mdb)};Dbq=Example.mdb;Uid=Admin;Pwd=;'

connsrc = pyodbc.connect(connstring)
cursor = connsrc.cursor()
  
sSQL = 'DELETE FROM [Logos_Test] WHERE ID < 4'
print sSQL
cursor.execute(sSQL)

sSQL = 'UPDATE [Logos_Test] SET HTML = \'HTML Updated\',Link = NULL ,Additional_Text = \' & > - \' & CHR(13) & CHR(10) WHERE ID > 17'
print sSQL
cursor.execute(sSQL)

sSQL = 'INSERT INTO Logos_Test (ID, HTML, Link, Additional_Text) SELECT 29, HTML, Link, Additional_Text FROM Logos WHERE ID = 19'
print sSQL
cursor.execute(sSQL)

cursor.close()
connsrc.commit()
connsrc.close()
