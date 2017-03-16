import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup

class Database:

	#Class Contructure
	def __init__(self, database_name):
		self.today = datetime.date.today()
		self.database_name = database_name
		self.connection = sqlite3.connect(database_name)
		self.cursor = self.connection.cursor()

	#Insert forcast data into the the database
	def dataEntry(self, DayTime, Temp, Rainfall, Humidity, WindSpeed, WindDirection, city, nextday):
	    try:
	    	if(nextday == 0):
	    		nextday = self.today
	    	else:
	    		nextday = datetime.datetime.now() + datetime.timedelta(days=nextday)
	    	self.cursor.execute("INSERT INTO WeatherInfo (DateAdded, Date, DayTime, Temp, Rainfall, Humidity, WindSpeed, WindDirection, City) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.today, str(nextday).split(' ')[0], DayTime, Temp, Rainfall, Humidity, WindSpeed, WindDirection, city))
	    	self.connection.commit()
	    except Exception as error:
	    	print("ERROR: "+str(error))

	#Select all rows the database and return its contents
	def getForcast(self, city):
		self.cursor.execute('SELECT DayTime, Temp, Rainfall, Humidity, WindSpeed, WindDirection FROM WeatherInfo WHERE DateAdded = ? AND City = ?',(self.today, city, ))
		data = self.cursor.fetchall()
		return data

	#Checks if rows are in the database and return how much rows exists
	def dataExist(self, city):
		self.cursor.execute('SELECT City FROM WeatherInfo WHERE DateAdded = ? AND City = ?',(self.today, city, ))
		data = self.cursor.fetchall()
		return len(data)

	#Returns tomorrow's weather conditions
	def getTomorrowRainValue(self, city):
		tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
		self.cursor.execute('SELECT Rainfall FROM WeatherInfo WHERE City = ? and Date = ?',(city, str(tomorrow).split(' ')[0]))
		result = self.cursor.fetchone()
		return result[0]

	#Returns today's weather conditions
	def getTodayRainValue(self, city):
		self.cursor.execute('SELECT Rainfall FROM WeatherInfo WHERE City = ? and Date = ?',(city, self.today))
		result = self.cursor.fetchone()
		return result[0]

	#Delete data from the database where the is city is one specified 
	def clearDatabase(self, city):
		old_db = Database("Database.sqlite")
		self.cursor.execute('DELETE FROM WeatherInfo WHERE City = ?',(city, ))
		self.connection.commit()
		old_db.closeDatabase()
		new_db = Database("Database.sqlite")

	#Return all the email addresses of employees who are not apart of the IT staff
	def getEmployeeEmailAddresses(self, City):
		emails = []
		self.cursor.execute('SELECT Email FROM Employee WHERE Role IS NOT ? AND City = ?',("IT", City, ))
		data = self.cursor.fetchall()
		for email in data:
			emails.append(email[0])
		return emails

	#Return all the email address of employees who are apart of the IT Staff
	def getITEmailAddresses(self, City):
		emails = []
		self.cursor.execute('SELECT Email FROM Employee WHERE Role IS ? AND City = ?',("IT", City, ))
		data = self.cursor.fetchall()
		for email in data:
			emails.append(email[0])
		return emails

	#Close the database connection
	def closeDatabase(self):
		self.cursor.close()
		self.connection.close()
