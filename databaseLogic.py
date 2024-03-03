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


def insertData(itemDesc, coltag, httpl, imgl):
  with sqlite3.connect("inventory.db") as conxn:
    cur = conxn.cursor()
    execStr = '''INSERT INTO INVENTORY ( itemdesc, coltags, httplink, imglink)
                              VALUES('{}', '{}', '{}', '{}')'''.format(itemDesc, coltag, httpl, imgl)

    cur.execute(execStr)
    conxn.commit()
    


def extractData(colTags = "blue", first = False):
  
  '''this function extracts the data entries from the inventory whose color matches the coltags value'''
  with sqlite3.connect("inventory.db") as conxn:
    cur = conxn.cursor()

    if not first:
      execStr = '''SELECT * FROM INVENTORY WHERE coltags = '{}' '''.format(colTags)

      res = cur.execute(execStr)
      return res.fetchall()
    else:
      strtData = []
      for i in ["shirt", "shoes", "jacket", "trouser"]:
        execStr = '''SELECT * FROM INVENTORY WHERE itemdesc = "{}"'''.format(i)
        res = cur.execute(execStr)
        strtData.append(res.fetchone()[0]) # sends the first entry as default
      
      return strtData
  