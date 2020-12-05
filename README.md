Instructions:-

My project is on Emergency vehicles. I built this project using the sqlite3 and tkinter modules which comes with python, no need to install separately. First download three files (emergencyVehicle, emergency_tkinter, emergencdb) and save in same folder. Then open and run the emergency_tkinter to see the output of the code. 
Used modules.
•	Import Sqlite3
•	Import tkinter

About the Code:-

	This code is for those in the service, such as security, firefighters, and other emergency responders. In the database file, the data entry person enters the data on the emergency vehicles and their locations. These emergency services will access the file in the time of emergency and can request the services according to the requirement and availability. If the vehicle is not available in their location, it will show the nearest available vehicle in the table. It will also allocate the vehicle from the other location if the vehicle is unavailable in their location.
This code also has the retune confirmation module which only present in the apps available at the vehicle controllers who notify the return of the vehicle and ready for the next service. For the demo, I added this functionality in this code.
	Emergencdb file is the database file, where all the information about the vehicles is saved in this file. when you’re running the code for the first time, the database file will be empty. We have to provide the data to the database file to store and use for the code. If you download the file you can get the data that I saved in the file and can use to allocate the vehicle. 
	In the emergencyVechicle, I build the self-function to support the emergency_tkinter file. In emergency_tkinter all the GUI is arranged and with the help of the emergencyVechicle functions it provide the output. 

Description:-

	 This code as the functionalities like requesting the vehicles, adding new vehicles, adding the zip codes, deleting the vehicles, changing the status of the out vehicles to in vehicles. With the help of these functionalities, we can manipulate the data according to the availability and requirement of the vehicle and assign them to the service. 
	In the requesting vehicle function, we request the vehicle with the type of vehicle required and zip code as the vehicle location. According to the availability, it will assign the vehicle. If there is no vehicle available in the location it will assign the vehicle from the nearest location. If there is no vehicle available, then it says “No vehicle available, try again later”. 
	Adding the vehicle function, in this function, we can add the vehicle, type of vehicle, location of the vehicle to the database. Similarly, adding the zip code function also works the same. It will take zip code 1, zip code 2, and the distance between them and store the data in the database.
	Delete vehicle function, with this function we can delete the vehicle from the database. With the return vehicle function, it will change the status of the vehicle from out table to the vehicle available table.
	With the help of these functionalities, we can assign the vehicles to the service according to the requirement and availability. 
