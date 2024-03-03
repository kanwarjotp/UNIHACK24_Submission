import sqlite3

def createDatabase():
  con = sqlite3.connect("inventory.db")

  cur = con.cursor()

  cur.execute('''CREATE TABLE INVENTORY(
                  id integer primary key autoincrement not null,
                  itemdesc text not null,
                  coltags text not null,
                  httplink text not null,
                  imglink text not null
              )''')
  
  con.close()


def insertData(itemDesc, col, httpl, imgl):
  with sqlite3.connect("inventroy.db") as conxn:
    execStr = '''INSERT INTO INVENTORY ( itemdesc, coltags, httplink, imglink)
                              VALUES('{}', '{}', '{}', '{}')'''.format(itemDesc, coltag, httpl, imgl)

    cur.execute(execStr)
    conxn.commit()
    


def extractData(coltags):
  '''this function extracts the data entries from the inventory whose color matches the coltags value'''
  with sqlite3.connect("inventroy.db") as conxn:
    execStr = '''SELECT * FROM INVENTORY WHERE coltags = '{}' '''.format(coltags)

    res = cur.execute(execStr)
    return res.fetchall()
  