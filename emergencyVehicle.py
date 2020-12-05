import sqlite3

# connect to the database file(emergencydb.db) to store the data
conn1 = sqlite3.connect('emergencdb.db')
cur1 = conn1.cursor()  # create the object

# creating the tables
cur1.execute(
    '''CREATE TABLE IF NOT EXISTS EmergencyVehicles(Id integer PRIMARY KEY, VehicleType integer, Zipcode integer)''')
cur1.execute(
    '''CREATE TABLE IF NOT EXISTS OutTable(Id integer PRIMARY KEY, VehicleType integer, Zipcode integer,
    Zipcode2 integer , dist integer)''')
cur1.execute('''CREATE TABLE IF NOT EXISTS Distance(Zipcode1 integer ,Zipcode2 integer, dist integer)''')


class staticvariable:
    temp = 0


def RequestEV(r1, zipc1):       # this method is used for the requesting vehicle
    cur1.execute(
        'SELECT * FROM EmergencyVehicles WHERE EmergencyVehicles.VehicleType=? AND EmergencyVehicles.Zipcode=?',
        (r1, zipc1,))
    l1 = cur1.fetchall()
    zipc2 = zipc1
    try:
        id1 = 0
        id1 = l1[0][0]
        if id1 == 0:
            raise IndexError
        cur1.execute('SELECT * FROM EmergencyVehicles WHERE Id=?', (id1,))
        l2 = cur1.fetchall()

        if zipc2 == staticvariable.temp:
            cur1.execute('INSERT INTO OutTable(Id,VehicleType,Zipcode) VALUES(?,?,?)', (l2[0][0], l2[0][1], l2[0][2]))

        if zipc2 != staticvariable.temp:
            cur1.execute('SELECT * FROM Distance WHERE Zipcode1=?', (zipc2,))
            l6 = cur1.fetchall()
            cur1.execute('INSERT INTO OutTable VALUES(?,?,?,?,?)', (l2[0][0], l2[0][1], l2[0][2], l6[0][1], l6[0][2]))
        cur1.execute('DELETE FROM Distance WHERE Zipcode1=? and Zipcode2=?', (staticvariable.temp, zipc2,))
        cur1.execute('DELETE FROM Distance WHERE Zipcode1=? and Zipcode2=?', (zipc2, staticvariable.temp,))
        cur1.execute('SELECT * FROM OutTable ')
        l5 = cur1.fetchall()

        cur1.execute('DELETE FROM EmergencyVehicles WHERE Id=?', (id1,))      # deleting the vehicle from the emergencyvehicle table
        conn1.commit()
        return l2[0][0]
    except IndexError:
        cur1.execute('SELECT dist from Distance where Zipcode1=?', (staticvariable.temp,))
        l2 = cur1.fetchall()
        if len(l2) == 0:
            return 0
        zipc2 = NearByZipc(staticvariable.temp)   # calling the near by zipcode function

        res = RequestEV(r1, zipc2)
        return res

# to Show the details of the vehicle based on the id(n)

def DisplayVehicle(n):
    cur1.execute('select * from OutTable where id=? ', (n,))
    return cur1.fetchall()

# show the type of the vehicle in the table which are avaliable or allocted
def showVehicles(type_check):
    data_complete = []
    if type_check == "entire":                                          # display table of emergency vehicles
        cur1.execute("""SELECT ID, VehicleType, 
                    CASE WHEN VehicleType = 1 THEN "AMBULANCE"
                    WHEN VehicleType = 2 THEN "FIRETRUCK"
                    ELSE "POLICE CAR"
                    END AS Vehicle_Type,
                    ZIPCODE
                    FROM EmergencyVehicles""")
        data_complete = cur1.fetchall()
        data_complete.insert(0, ("ID", "Type", "TypeName", "Zipcode"))

    elif type_check == "zip":                                           # display table of zipcodes
        cur1.execute("""SELECT ZIPCODE1, ZIPCODE2, DIST, " " AS DUMMY
                    FROM Distance""")
        data_complete = cur1.fetchall()
        data_complete.insert(0, ("ZIPCODE1", "ZIPCODE2", "DISTANCE", " "))

    elif type_check == "out":                                           # display table of out vehicles
        cur1.execute("""SELECT ID, VehicleType, 
                    CASE WHEN VehicleType = 1 THEN "AMBULANCE"
                    WHEN VehicleType = 2 THEN "FIRETRUCK"
                    ELSE "POLICE CAR"
                    END AS Vehicle_Type,
                    ZIPCODE
                    FROM Outtable""")
        data_complete = cur1.fetchall()
        data_complete.insert(0, ("ID", "Type", "TypeName", "Zipcode"))

    return data_complete


# changing the statues of out to in to make it available for the service

def return_vehicle(id):
    cur1.execute("select count(*) as cnt from outtable where id=? ", (id,))
    if cur1.fetchall()[0][0] == 0:
        return f"No vehicles with the {id} available to return\n"
    else:
        cur1.execute('insert into emergencyvehicles SELECT id, vehicletype, zipcode from outtable where id=? ', (id,))
        cur1.execute('delete from outtable where id=? ', (id,))
        conn1.commit()
        return f"Vehicle with the {id} returned\n"


# deleting the vehicles which are unwanted or not in service

def delete_vehicle(id):
    cur1.execute("select count(*) as cnt from emergencyvehicles where id=? ", (id,))
    if cur1.fetchall()[0][0] == 0:
        return "No vehicles with the ID available \n"
    else:
        cur1.execute('delete from emergencyvehicles where id=? ', (id,))
        cur1.execute('delete from outtable where id=? ', (id,))
        conn1.commit()
        return f"Vehicle {id} is deleted"

 # checking the nearest zip code

def NearByZipc(zip1):
    try:
        cur1.execute('SELECT dist from Distance where Zipcode1=?', (staticvariable.temp,))
        l2 = cur1.fetchall()
        if len(l2) == 0:
            return 0
        cur1.execute('SELECT Zipcode2 FROM Distance WHERE Distance.Zipcode1=?', (zip1,))
        l1 = cur1.fetchall()

        return l1[0][0]
    except IndexError:
        return 0


# adding the vehicles for the service in the table

def add_emergencyvehicles(id_v, type_v, zipcode):
    cur1.execute('insert into EmergencyVehicles values(?,?,?)', (id_v, type_v, zipcode))
    cur1.execute('DELETE FROM OutTable WHERE Id=? and VehicleType=? and Zipcode=?', (id_v, type_v, zipcode))
    conn1.commit()

# this def is used for calling the request vehicle action from emergency tkinter
def request_emergency_vehicle(type_v, zipcode):
    staticvariable.temp = zipcode
    cur1.execute('SELECT * FROM OutTable ')
    l5 = cur1.fetchall()
    length_before = len(l5)

    res = RequestEV(type_v, zipcode)      # calling the reuestEV function for allocating a vehicle or nearest vehicle

    cur1.execute('SELECT * FROM OutTable ')
    l3 = cur1.fetchall()
    length_after = len(l3)
    conn1.commit()

    if length_before == length_after:
        return 'no vehicle found, please try later!'
    else:
        return DisplayVehicle(res)  # calling the displayvehicle function to display vehicle details as a output

# adding the zipcodes with the distance
def add_zipcode(zip1, zip2, distance):
    cur1.execute('insert into Distance values(?,?,?)', (zip1, zip2, distance))
    cur1.execute('insert into Distance values(?,?,?)', (zip2, zip1, distance))
    conn1.commit()

<<<<<<< HEAD
    return "Added Zipcodes"      # show as the comment when successfully executed this program
=======
    return "Added Zipcodes"      # showes as the comment
>>>>>>> 4ecc2011c0f052454bdc7fa6edf31c1478e59871
