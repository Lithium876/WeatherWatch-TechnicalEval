from Database import *
import smtplib, os, sys
from texttable import Texttable

BASE_URL = "http://jamaica.weatherproof.fi/glenroy/weather/jaweather.php?place="

class WeatherForcast:

	#Class Variable
	DayCount = 0

	#Class Contructure
	def __init__(self, city):
		self.city = city
		WeatherForcast.DayCount=0
		self.db = Database("Database.sqlite")

	#Class Destructure
	def __del__(self):
		self.db.closeDatabase()

	#Update Class Variable
	@classmethod
	def update(WeatherForcast, value):
	    WeatherForcast.DayCount += value

	#Gets Weather Forcast For a City
	def getForcast(self):
		try:
			if self.city in open('supported areas.txt').read():
				location = self.city.title().replace(" ","+")
				link = BASE_URL+location
			else:
				#If City is not supported raies an exception error
				raise Exception(self.city+" is an invalid or unsupported city!")

			#If the database has data
			if(self.db.dataExist(self.city) > 0):
				#Remove all data related to a particular city
				self.db.clearDatabase(self.city)

			#Get foracast details from link
			Table = WeatherForcast.getdata(link)
			
			for days in Table:
				#Parsing data from link
				days = days.split(' ')
				DayTime = days[0]+' '+days[1]+' PM'
				Temp = days[3].split("\xa0")[0]+"°C"
				Rainfall = days[3].split("C")[1]
				Pressure = days[4].split("mm")[1]+"mb"
				WindSpeed = days[6]+"m/s"
				WindDirection = days[7].split("m/s")[1]
				#Add the parsed data to the database
				self.db.dataEntry(DayTime, Temp, Rainfall, Pressure, WindSpeed, WindDirection, self.city, self.DayCount)
				#Updates the class variable
				self.update(1)
		except Exception as err:
			#Print out err if any
			print("Get Forcast Error: "+str(err))
			sys.exit()

	@classmethod
	def getdata(self, link):
		forecast = []
		raw_data = []
		passed = 0
		x=0
		y=6
		try:
			#Get the data from the link
			url = requests.get(link)
			#Gets the page source of the url
			html = BeautifulSoup(url.content,"html.parser")
			#Get the rows from the table
			Table=html.find_all("td",{"":""})
			#Parsing the data from the source
			for i in Table:
				if passed == 0:
					if len(i.text.split()) == 3 and i.text.split()[2] == 'pm':
						raw_data.append(i.text)
						passed += 6
				else:
					raw_data.append(i.text)
					passed -=1

			#Formatting the parsed data
			for n in range(0,5):
				parsed_str = ''.join(map(str,raw_data[x:y]))
				if len(parsed_str) == 0:
					pass
				else:
					forecast.append(parsed_str)
				x+=7
				y+=7

			if len(forecast)<5:
				self.update(1)

			return forecast
		except Exception as err: 
			print("Get Data Error: "+str(err))

	#Display forcast for a particular city 	
	def displayForcast(self):
		data = []
		try:
			#Get the city forcast from the database
			forcast = self.db.getForcast(self.city)
			#Create a table display instant of the Texttable class
			text_table = Texttable()
			for day in forcast:
				#Convert the windspeed from knots to Text
				wind = WeatherForcast.windSpeedToText(day[4].split('m/s')[0])
				#Convert the rain rate from meters per second to text
				rain = WeatherForcast.rainRateToText(day[2])
			#Display data from database in a tabular format
				# text_table.add_rows([['DayTime', 'Temperature', 'Rainfall', 'Pressure', 'Wind Speed', 'Wind Direction'], [day[0], day[1],  str(rain), day[3], str(wind), day[5]]])
				data.append(day[0])
				data.append(day[1])  
				data.append(str(rain))
				data.append(day[3])
				data.append(str(wind))
				data.append(day[5])
			return data
			# print("=========================== Forcast For " + self.city + " ===========================")
			# print(text_table.draw()+'\n')
		except Exception as err:
			print("Display Forcast Error: "+ str(err))

	#Checks if it will rain today in a particular city
	def willHaveRainToday(self):
		try:
			#Get the rain rate values from the database
			rainval = self.db.getTodayRainValue(self.city)
			#Check if the value recieved is greater than 0.0
			if float(rainval) > 0.0:
				#If the rain rate value is greater than 0.0 
				#It means it will rain today so return ture
				return True
			else:
				#Else it will not rain so return false
				return False
		except Exception as err:
			print("Will have rain today Error: "+str(err))

	#Checks if it will rain tomorrow in a particular city
	def willHaveRainTomorrow(self):
		try:
			rainval = self.db.getTomorrowRainValue(self.city)
			if float(rainval) > 0.0:
				return True
			else:
				return False
		except Exception as err:
			print("Will have rain tomorrow Error: "+str(err))
			
	#Send email to employees of a particular city
	def sendEmail(self, emailtitle, willrain=None, role=None):
		try:
			"""
			If a role variable is not passed to the function,
			get all employee email addresses from the database
			whose role is not 'IT'
			"""
			if role == None:
				emails = self.db.getEmployeeEmailAddresses(self.city)
			else:
				"""
				If the role variable is passed to the function (sendEmail),
				get all employee email addresses from the database 
				whose role is 'IT'
				"""
				emails = self.db.getITEmailAddresses(self.city)
	
			if emails == []:
				#If no email addresses were return from the database
				return "No Emails Found!"
			else:
				#If it will not rain, open the 'NoRainEmail.txt' file
				if willrain == None:
					with open("NoRainEmail.txt",'r') as message:
						#Read the contents of the file into the variable 'contents'
						contents = message.read()
					message.close()
				#If it will rain and a role variable is passed to the function 
				#(sendEmail), open 'ITStaffEmail.txt' file
				elif willrain != None and role != None:
					with open("ITStaffEmail.txt",'r') as message:
						contents = message.read()
					message.close()
				else:
					#If it will rain, open the 'RainEmail.txt' file
					with open("RainEmail.txt",'r') as message:
						contents = message.read()
					message.close()

				#Sender email address
				gmail_user = 'lomarlilly0712@gmail.com' 
				#Sender password address
				gmail_pwd = 'p@$$w0rd'
				#Send the email via our own SMTP server.
				smtpserver = smtplib.SMTP("smtp.gmail.com",587)
				#Test server connection
				smtpserver.ehlo()
				smtpserver.starttls()
				smtpserver.ehlo
				#Log into the server
				smtpserver.login(gmail_user, gmail_pwd)
				for email in emails:
					sent = []
					#For each in email in the emails list
					header = 'To:' + email + '\n' + 'From: '+ gmail_user + '\n' + 'Subject: '+emailtitle +'\n'
					sent.append(email)
					msg = header + '\n' + contents
					#Send email 'Sender Email, Reciever Email, Contents of Email'
					smtpserver.sendmail(gmail_user, email, msg)
				return "Emails Sent Successfully"
				#Close the server connection
				smtpserver.close()
		except Exception as err:
			return "Error: "+str(err)

	#Convert wind speed from knots and to text value
	@staticmethod
	def windSpeedToText(kts):
		try:
			knots = str(kts).split('kts')[0]
			knots = int(knots)
			if knots >= 1 and knots <= 3:
				return "Light Air"
			elif knots >= 4 and knots <= 6:
				return "Light Breeze"
			elif knots >= 7 and knots <= 10:
				return "Gentle Breeze"
			elif knots >= 11 and knots <= 16:
				return "Moderate Breeze"
			elif knots >= 17 and knots <= 21:
				return "Fresh Breeze"
			elif knots >= 22 and knots <= 27:
				return "Strong Breeze"
			elif knots >= 28 and knots <= 33:
				return "Near Gale"
			elif knots >= 34 and knots <= 40:
				return "Gale"
			elif knots >= 48 and knots <= 55:
				return "Storm"
			elif knots >= 56 and knots <= 63:
				return "Violent Storm"
			elif knots >= 56 and knots <= 63:
				return "Hurricane"
		except Exception as err:
			print("Wind Speed to text Error: "+str(err))

	#Convert rain rates from metre per second to text value
	@staticmethod
	def rainRateToText(rainRate):
		try:
			rainRate = float(rainRate)
			if rainRate == 0.0:
				return "No Rain"
			elif rainRate > 0.0 and rainRate <= 0.2:
				return "Very Light Rain"
			elif rainRate > 0.2 and rainRate <= 1:
				return "Light Rain"
			elif rainRate > 1 and rainRate <= 4:
				return "Moderate Rain"
			elif rainRate > 4 and rainRate <= 16:
				return "Heavy Rain"
			elif rainRate > 16 and rainRate <= 50:
				return "Very Heavy Rain"
			elif rainRate > 50:
				return "Extreme Rain"
		except Exception as err:
			print("Rain rate to text: "+str(err))
