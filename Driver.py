from Forcaster import *

def main():

	#Kingston
	kingston = WeatherForcast("Kingston")

	#Get and display the forcast for kingston
	kingston.getForcast()
	kingston.displayForcast()

	if kingston.willHaveRainTomorrow():
		Email_Subject = "Schedule Change"
		#Sent to all employees not from IT staff
		kingston.sendEmail(Email_Subject, True)
		# #Sent to all employees from IT staff
		kingston.sendEmail(Email_Subject, True, "IT Staff")
	else:
		Email_Subject = "Schedule Remains"
		kingston.sendEmail(Email_Subject)


	#Execution for Montegobay
	mobay = WeatherForcast("Montego Bay")
	mobay.getForcast()
	mobay.displayForcast()

	if mobay.willHaveRainTomorrow():
		Email_Subject = "Schedule Change"
		mobay.sendEmail(Email_Subject, True, "IT Guy")
	else:
		Email_Subject = "Schedule Remains"
		mobay.sendEmail(Email_Subject)

if __name__ == '__main__':
	main()
