from Forcaster import *

'''
SUPPORTED LOCATIONS
Kingston, Spanish Town, Portmore, Morant Bay, Port Antonio, Port Maria, Ocho Rios, Falmouth, 
Montego Bay, Negril, Savanna-la-mar, Santa Cruz, Mandeville, May Pen
'''

def main():

	location = WeatherForcast("Kingston")

	#Get and display the forcast for location above
	location.getForcast()
	location.displayForcast()

	if location.willHaveRainTomorrow():
		Email_Subject = "Schedule Change"
		#Sent to all employees not from IT staff
		location.sendEmail(Email_Subject, True)
		# #Sent to all employees from IT staff
		location.sendEmail(Email_Subject, True, "IT Staff")
	else:
		Email_Subject = "Schedule Remains"
		location.sendEmail(Email_Subject)

if __name__ == '__main__':
	main()
