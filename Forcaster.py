from Database import *
import smtplib, os
from texttable import Texttable

class WeatherForcast:

	#Class Variable
	DayCount = 0

	#Class Contructure
	def __init__(self, city):
		self.city = city
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
			#If City is Kingston
			if self.city == "Kingston":
				#Where to go to get forcast
				link = "http://jamaica.weatherproof.fi/glenroy/weather/jaweather.php?place=Kingston"
			#If City is Montego Bay
			elif self.city == "Montego Bay":
				link = "http://jamaica.weatherproof.fi/glenroy/weather/jaweather.php?place=Montego+Bay"
			else:
				#If City is not Kingston or Montego Bay raies an exception error
				raise Exception("Invalid City!")

			#If the database has data
			if(self.db.dataExist(self.city) > 0):
				#Remove all data related to a particular city
				self.db.clearDatabase(self.city)

			#Get foracast details from link
			Table = WeatherForcast.getdata(link)
			
			for days in Table:
				#Parsing data from link
				days = days.text.split(' ')
				DayTime = days[0]+' '+days[1]+' PM'
				Temp = days[3].split("\xa0")[0]+"°C"
				Rainfall = days[3].split("C")[1]
				Pressure = days[4].split("mm")[1]+"mb"
				WindSpeed = days[6]+"kts"
				WindDirection = days[7].split("kts")[1]
				#Add the parsed data to the database
				self.db.dataEntry(DayTime, Temp, Rainfall, Pressure, WindSpeed, WindDirection, self.city, self.DayCount)
				#Updates the class variable
				self.update(1)
		except Exception as err:
			#Print out err if any
			print(err)

	@classmethod
	def getdata(self, link):
		data = []
		#Goes to link
		url = requests.get(link)
		#Gets the page source of the url
		html = BeautifulSoup(url.content,"html.parser")
		#Get the rows from the table
		odd=html.find_all("tr",{"class":"odd"})
		even=html.find_all("tr",{"class":"even"})

		for i in odd:
			n = i.text.split(' ')
			data.append(n[0])
		for i in even:
			n = i.text.split(' ')
			data.append(n[0])
		
		#Get length of the rows and determine if its a even table or odd table
		if len(data) % 2 == 0:
			Table = even
			self.update(1)
		elif len(data) % 2 == 1:
			Table = odd

		return Table

	#Display forcast for a particular city 	
	def displayForcast(self):
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
			text_table.add_rows([['DayTime', 'Temperature', 'Rainfall', 'Pressure', 'Wind Speed', 'Wind Direction'], [day[0], day[1],  str(rain), day[3], str(wind), day[5]]])
		print("=========================== Forcast For " + self.city + " ===========================")
		print(text_table.draw()+'\n')

	#Checks if it will rain today in a particular city
	def willHaveRainToday(self):
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

	#Checks if it will rain tomorrow in a particular city
	def willHaveRainTomorrow(self):
		rainval = self.db.getTomorrowRainValue(self.city)
		if float(rainval) > 0.0:
			return True
		else:
			return False

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
				print("No Emails Found!")
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

				print("\n\nSending Email...")
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
					#For each in email in the emails list
					header = 'To:' + email + '\n' + 'From: '+ gmail_user + '\n' + 'Subject: '+emailtitle +'\n'
					print("Sending Email to "+email)
					msg = header + '\n' + contents
					#Send email 'Sender Email, Reciever Email, Contents of Email'
					smtpserver.sendmail(gmail_user, email, msg)
				print("Emails Sent!")
				#Close the server connection
				smtpserver.close()
		except Exception as err:
			print(err)
			print("Error in sending Emails")

	#Convert wind speed from knots and to text value
	@staticmethod
	def windSpeedToText(kts):
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

	#Convert rain rates from metre per second to text value
	@staticmethod
	def rainRateToText(rainRate):
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
