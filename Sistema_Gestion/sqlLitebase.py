import sqlite3 as sql

def createDB():
  conn = sql.connect("parking.db")
  conn.commit()
  conn.close()
  
def createTable():
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  cursor.execute(
    """CREATE TABLE realtime (
      car_type integer,
      placa text,
      model text,
      parknum integer,
      owner text,
      zone text,
      hll integer,
      mll integer,
      date text,
      check_out integer
    )"""
  )
  conn.commit()
  conn.close()
  
def createTable2():
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  cursor.execute(
    """CREATE TABLE historical (
      car_type integer,
      placa text,
      model text,
      parknum integer,
      owner text,
      zone text,
      hll integer,
      mll,
      hs integer,
      ms integer,
      date text,
      totaltime integer,
      check_out integer
    )"""
  )
  conn.commit()
  conn.close()
  
def insertrow(car_type, placa, model, parknum, owner, zone, hll, mll, date, check_out):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"INSERT INTO realtime Values ({car_type}, '{placa}', '{model}', {parknum}, '{owner}', '{zone}', {hll}, {mll}, '{date}', {check_out})"
  cursor.execute(instruction)
  conn.commit()
  conn.close()

def insertrow2(car_type, placa, model, parknum, owner, zone, hll, mll, hs, ms, date, totaltime, check_out):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"INSERT INTO historical Values ({car_type}, '{placa}', '{model}', {parknum}, '{owner}', '{zone}', {hll}, {mll}, {hs}, {ms},'{date}', {totaltime},{check_out})"
  cursor.execute(instruction)
  conn.commit()
  conn.close()
  
def readRows():
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"SELECT  * FROM realtime"
  cursor.execute(instruction)
  data = cursor.fetchall()
  conn.commit()
  conn.close()
  print(data)
  
def insertRows(parkinglist):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"INSERT INTO realtime Values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
  cursor.executemany(instruction, parkinglist)
  conn.commit()
  conn.close()
  
def readOrdered(field):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"SELECT  * FROM realtime ORDER BY {field}"
  cursor.execute(instruction)
  data = cursor.fetchall()
  conn.commit()
  conn.close()
  print(data)

def search(placa):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"SELECT  * FROM realtime WHERE placa like '{placa}'"
  cursor.execute(instruction)
  data = cursor.fetchall()
  conn.commit()
  conn.close()
  return data

def search2(placa):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"SELECT  * FROM historical WHERE placa like '{placa}'"
  cursor.execute(instruction)
  data = cursor.fetchall()
  conn.commit()
  conn.close()
  return data
  
def deleterow(plate):
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"DELETE FROM realtime WHERE placa like '{plate}'"
  cursor.execute(instruction)
  conn.commit()
  conn.close()

def depurate():
  conn = sql.connect("parking.db")
  cursor = conn.cursor()
  instruction = f"DELETE FROM historical WHERE check_out = 1"
  cursor.execute(instruction)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  #createDB()
  #createTable2()
  #depurate()
  pass
  