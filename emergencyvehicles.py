import sqlite3

#connect to the database file(emergencydb.db) to store the data
conn1=sqlite3.connect('emergencdb.db')
cur1=conn1.cursor() # create the object

#creating the tables
cur1.execute('''CREATE TABLE IF NOT EXISTS EmergencyVehicles(Id integer PRIMARY KEY, VehicleType integer, Zipcode integer)''')
cur1.execute('''CREATE TABLE IF NOT EXISTS OutTable(Id integer PRIMARY KEY, VehicleType integer, Zipcode integer, Zipcode2 integer , dist integer)''')
cur1.execute('''CREATE TABLE IF NOT EXISTS Distance(Zipcode1 integer ,Zipcode2 integer, dist integer)''')

class staticvariable:
    temp=0


def RequestEV(r1,zipc1):
    cur1.execute('SELECT * FROM EmergencyVehicles WHERE EmergencyVehicles.VehicleType=? AND EmergencyVehicles.Zipcode=?',(r1,zipc1,))
    l1=cur1.fetchall()
    zipc2=zipc1
    try:
        id1=0
        id1=l1[0][0]
        if id1==0:
            raise IndexError
        cur1.execute('SELECT * FROM EmergencyVehicles WHERE Id=?',(id1,))
        l2=cur1.fetchall()
        
        if zipc2==staticvariable.temp:
            cur1.execute('INSERT INTO OutTable(Id,VehicleType,Zipcode) VALUES(?,?,?)',(l2[0][0],l2[0][1],l2[0][2]))

        if zipc2!=staticvariable.temp:
            cur1.execute('SELECT * FROM Distance WHERE Zipcode1=?',(zipc2,))
            l6=cur1.fetchall()
            cur1.execute('INSERT INTO OutTable VALUES(?,?,?,?,?)',(l2[0][0],l2[0][1],l2[0][2],l6[0][1],l6[0][2]))
        cur1.execute('DELETE FROM Distance WHERE Zipcode1=? and Zipcode2=?',(staticvariable.temp,zipc2,))
        cur1.execute('DELETE FROM Distance WHERE Zipcode1=? and Zipcode2=?',(zipc2,staticvariable.temp,))
        cur1.execute('SELECT * FROM OutTable ')
        l5=cur1.fetchall()
        
        cur1.execute('DELETE FROM EmergencyVehicles WHERE Id=?',(id1,))
        conn1.commit()
        return l2[0][0]
    except IndexError:
        cur1.execute('SELECT dist from Distance where Zipcode1=?',(staticvariable.temp,))
        l2=cur1.fetchall()
        if len(l2)==0:
            return 0
        zipc2=NearByZipc(staticvariable.temp)
        
        
        res=RequestEV(r1,zipc2)
        return res

def DisplayVehicle(n):
    cur1.execute('select * from OutTable where id=? ',(n,))
    print(cur1.fetchall())

def return_vehicle(id):
    cur1.execute("select count(*) as cnt from outtable where id=? ", (id,))
    if cur1.fetchall()[0][0] == 0:
        print("No vehicles with the ID available to return\n")
    else:
        cur1.execute('insert into emergencyvehicles SELECT id, vehicletype, zipcode from outtable where id=? ', (id,))
        cur1.execute('delete from outtable where id=? ', (id,))
        conn1.commit()

def delete_vehicle(id):
    cur1.execute("select count() as cnt from emergencyvehicles where id=? union select count() as cnt from outtable "
                 "where id=? ", (id, id,))
    if cur1.fetchall()[0][0] == 0:
        print("No vehicles with the ID available \n")
    else:
        cur1.execute('delete from emergencyvehicles where id=? ', (id,))
        cur1.execute('delete from outtable where id=? ', (id,))
        conn1.commit()

def NearByZipc(zip1):
    try:
        cur1.execute('SELECT dist from Distance where Zipcode1=?',(staticvariable.temp,))
        l2=cur1.fetchall()
        if len(l2)==0:
            return 0
        cur1.execute('SELECT Zipcode2 FROM Distance WHERE Distance.Zipcode1=?',(zip1,))
        l1=cur1.fetchall()
      
        return l1[0][0]
    except IndexError:
        return 0


res=0
switch=True
i=1
while True:
    try:
        print('\n\n-----------------------------------------------------------------\n')
        try:
                inp=int(input('Press 1 to request a emergency vehicle \nPress 2 to add emergency vehicles \nPress 3 to add new '
                              'Zipcode \nPress 4 To delete vehicle \nPress 5 To return the vehicle \nPress any number for more '
                              'options\nPress 9 to shutdown the program\nSelect your choice from above: '))
        except Exception as e:
                        print('enter correct input')
                        continue

        l1=[]
        if inp==1:

            r=int(input('what type of emergency vehicle you require?\n1: Ambulance\n2: Fire truck\n3: Police car\nEnter your requirement:'))
            zipc=int(input('enter the of requested zipcode : '))

            staticvariable.temp=zipc
            cur1.execute('SELECT * FROM OutTable ')
            l5=cur1.fetchall()
            a=len(l5)

            res=RequestEV(r,zipc)

            cur1.execute('SELECT * FROM OutTable ')
            l3=cur1.fetchall()
            b=len(l3)

            if a==b:
                print('no vehicle found, please try later!')
            else:
                DisplayVehicle(res)
            conn1.commit()
                
        if inp==2:

              n=int(input('enter number of emergency vehicles you want to add : '))
              for i in range(n):
                    x=int(input('enter id of vehicle(only numbers) %d:'%(i+1)))
                    print('what type of emergency vehicle you want to add?\n1: Ambulance\n2: Fire truck\n3: Police car')
                    y=int(input('enter vehicle type of vehicle %d :'%(i+1)))
                    z=int(input('enter zipcode of area you want to add vehicle %d:'%(i+1)))
                    cur1.execute('insert into EmergencyVehicles values(?,?,?)',(x,y,z))
                    cur1.execute('DELETE FROM OutTable WHERE Id=? and VehicleType=? and Zipcode=?',(x,y,z))
              conn1.commit()
              continue


        if inp==3:
              
              n=int(input('enter number of entries : '))
              print('Enter the values in ascending order of the distance')
              
              for i in range(n):
                    x=int(input('enter zipcode 1:'))
                    y=int(input('enter zipcode 2 :'))
                    z=int(input('enter distance :'))
                    cur1.execute('insert into Distance values(?,?,?)',(x,y,z))
                    cur1.execute('insert into Distance values(?,?,?)',(y,x,z))
              conn1.commit()
              continue

        if inp==4:

            n = int(input('Enter vehicle ID number you want to delete: '))
            delete_vehicle(n)

            continue

        if inp == 5:
            n = int(input('Enter vehicle ID number you want to return: '))
            return_vehicle(n)
            continue

        temp=0
        y=int(input('Press 1 To check the entries in all the tables \nPress 2 to Restart\nPress 9 to shutdown\nEnter your choice: : '))
        
        if y==1:
              print('Emergency vehicles:')
              cur1.execute('select * from EmergencyVehicles')
              print(cur1.fetchall())
              print('Zipcodes and their distances:')
              cur1.execute('select * from Distance')
              print(cur1.fetchall())
              print('out vehicles are :')
              cur1.execute('select * from OutTable')
              print(cur1.fetchall())
              temp=int(input('Press 1 to restart the program\nPress 9 to shutdown : '))
              

        if y==9 or temp==9:
                break

    except Exception as e:
        print('enter correct input');
        conn1.commit()
        continue

