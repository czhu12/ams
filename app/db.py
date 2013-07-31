import MySQLdb as mdb
import sys

class db:

  def __init__(self):
    self.con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')
    self.cursor = con.cursor()

  def get_cursor(self):
    return self.cursor
  
  def insert(self, sql):
    try:
      self.cursor.execute(sql)
      self.con.commit()
    except:
      self.con.rollback()
      raise Exception("Insertion failed")

  def read(self, sql):
    self.cursor.execute(sql)
    return self.cursor.fetchall()
