import tkinter as tk
from tkinter import font as tkfont
import emergencyVehicle   # importing the self build module


# this the main class that drives next steps
class EmergencyVehicleAPP(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

# This space is used for all the tkinter frames used in this emergency GUI App
        self.frames = {}
        for F in (StartPage, NewVehicle, RequestVehicle, AddZip, DeleteVehicle, ReturnVehicle, ShowVehicle):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

# this method is used for raise the frames to top of the app
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# this is the home page for the application and in this class we created buttons and labels required for the homepage

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Emergency Vehicle response service\n", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        request_button = tk.Button(self, text="Request Emergency Vehicle", bg='powder blue', activebackground='#00ff00',
                                   height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("RequestVehicle"))
        request_button.pack()

        vehicle_add_button = tk.Button(self, text="Add New Vehicle", bg='powder blue', activebackground='#00ff00',
                                       height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("NewVehicle"))
        vehicle_add_button.pack()

        zipcode_button = tk.Button(self, text="Add Zipcode Information", bg='powder blue', activebackground='#00ff00',
                                   height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("AddZip"))
        zipcode_button.pack()

        delete_button = tk.Button(self, text="Delete Emergency Vehicle", bg='powder blue', activebackground='#00ff00',
                                  height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("DeleteVehicle"))
        delete_button.pack()

        return_button = tk.Button(self, text="Return Vehicle", bg='powder blue', activebackground='#00ff00',
                                  height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("ReturnVehicle"))
        return_button.pack()

        show_button = tk.Button(self, text="Show Vehicles", bg='powder blue', activebackground='#00ff00',
                                height=1, width=20, padx=10, pady=10, command=lambda: controller.show_frame("ShowVehicle"))
        show_button.pack()

        close_button = tk.Button(self, text="Close", bg='red', activebackground='#00ff00',
                                 padx=10, pady=10, command=self.quit)
        close_button.pack()


# this is the newvehicle page for the application and in this class we created buttons, labels and check box as required

class NewVehicle(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Vehicle Addition\n", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        id_label = tk.Label(self, text="New Vehicle ID: ")
        id_label.place(x=200, y=80, width=220, height=25)
        type_label = tk.Label(self, text="New Vehicle Type: ")
        type_label.place(x=200, y=120, width=220, height=25)
        zip_label = tk.Label(self, text="New Vehicle Zipcode: ")
        zip_label.place(x=200, y=200, width=220, height=25)
        id_entry = tk.Entry(self, bd=5)
        id_entry.place(x=400, y=80, width=220, height=25)
        zip_entry = tk.Entry(self, bd=5)
        zip_entry.place(x=400, y=200, width=220, height=25)

        id_entry.focus()
        id_entry.bind("<Return>", lambda dummy: zip_entry.focus())
        zip_entry.bind("<Return>", lambda dummy: submit_form())

        submit_button = tk.Button(self, text="Submit",
                                  command=lambda: submit_form())
        submit_button.place(x=200, y=240, width=220, height=25)
        button = tk.Button(self, text="Home page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=500, y=240, width=220, height=25)

# this def show the choice to select the type of vehicle using radio buttons

        def ShowChoice():
            print(v.get())

        types = [("Ambulance", 1), ("Fire Truck", 2), ("Police Car", 3)]
        v = tk.IntVar()
        v.set(1)  # initializing the choice, i.e. Python
        dist = 95

        for typeofvehicle, val in types:
            dist = dist + 25
            type_radio = tk.Radiobutton(self, text=typeofvehicle, padx=20, variable=v,
                                        command=ShowChoice, value=val)
            type_radio.place(x=400, y=dist)

        def submit_form():  #
            if id_entry.get().isdigit() and zip_entry.get().isdigit():
                try:
                    emergencyVehicle.add_emergencyvehicles(id_entry.get(), v.get(), zip_entry.get())  # it is calling the function from the emergencyVehicle module
                except Exception as e:
                    error_label = tk.Label(self, text="Issue with adding entries")
                    error_label.config(bg="white", fg='Red')
                error_label = tk.Label(self, text="Added Entries")
                error_label.config(bg="white", fg='Green')
                error_label.place(x=330, y=280, width=220, height=25)
                id_entry.delete(0, 'end')
                zip_entry.delete(0, 'end')
                id_entry.focus()

            else:
                error_label = tk.Label(self, text="Need only integers in Vehicle ID and Zip ")
                error_label.config(bg="white", fg='red')
                error_label.place(x=330, y=280, width=220, height=25)
                if not id_entry.get().isdigit():
                    id_entry.delete(0, 'end')
                if not zip_entry.get().isdigit():
                    zip_entry.delete(0, 'end')


# this is the requisting vehicle page for the application and in this class we created buttons, labels and check box as required

class RequestVehicle(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Please request your Vehicle", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        type_label = tk.Label(self, text="Vehicle Type: ")
        type_label.place(x=200, y=120, width=220, height=25)
        zip_label = tk.Label(self, text="Vehicle Zipcode: ")
        zip_label.place(x=200, y=200, width=220, height=25)

        zip_entry = tk.Entry(self, bd=5)
        zip_entry.place(x=400, y=200, width=220, height=25)

        zip_entry.bind("<Return>", lambda dummy: submit_form())

        submit_button = tk.Button(self, text="Submit",
                                 command=lambda: submit_form())
        submit_button.place(x=200, y=240, width=220, height=25)
        button = tk.Button(self, text="Home page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=500, y=240, width=220, height=25)

        def ShowChoice():
            print(v.get())

        types = [("Ambulance", 1), ("Fire Truck", 2), ("Police Car", 3)]
        v = tk.IntVar()
        v.set(1)  # initializing the choice
        dist = 95

#
        for typeofvehicle, val in types:  # defining the type of vehicle using radio buttons
            dist = dist + 25
            type_radio = tk.Radiobutton(self, text=typeofvehicle, padx=20, variable=v,
                                        command=ShowChoice, value=val)
            type_radio.place(x=400, y=dist, width=200, height=25)

        def submit_form():      # this method is for submit button
            global output
            output = []
            if zip_entry.get().isdigit():
                try:
                    print(f"this is the output{output}")
                    output = emergencyVehicle.request_emergency_vehicle(v.get(), zip_entry.get())  # it is calling the function from the emergencyVehicle module

                except Exception as e:
                    error_label = tk.Label(self, text="Issue with identifying vehicles")
                    error_label.config(bg="white", fg='Red')
                error_label = tk.Label(self, text=output)
                error_label.config(bg="white", fg='Green')
                error_label.place(x=330, y=280, width=220, height=25)
                zip_entry.delete(0, 'end')

            else:
                error_label = tk.Label(self, text="Need only integers in Zip ")
                error_label.config(bg="white", fg='red')
                error_label.place(x=330, y=280, width=220, height=25)
                if not zip_entry.get().isdigit():
                    zip_entry.delete(0, 'end')

# this is the add zipcode page for the application and in this class we created buttons, labels and check box as required
class AddZip(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="ADDING ZIPCODES", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        zip_label2 = tk.Label(self, text="New Zipcode1: ")
        zip_label2.place(x=200, y=120, width=220, height=25)
        zip_label = tk.Label(self, text="New Zipcode2: ")
        zip_label.place(x=200, y=160, width=220, height=25)
        zip_entry2 = tk.Entry(self, bd=5)
        zip_entry2.place(x=400, y=120, width=220, height=25)
        zip_entry2.bind("<Return>", lambda dummy: zip_entry.focus())
        zip_entry = tk.Entry(self, bd=5)
        zip_entry.place(x=400, y=160, width=220, height=25)
        zip_entry.bind("<Return>", lambda dummy: distance_entry.focus())

        distance_label = tk.Label(self, text="Enter Distance: ")
        distance_label.place(x=200, y=200, width=220, height=25)
        distance_entry = tk.Entry(self, bd=5)
        distance_entry.place(x=400, y=200, width=220, height=25)
        distance_entry.bind("<Return>", lambda: submit_form())

        submit_button = tk.Button(self, text="Submit",
                                  command=lambda: submit_form())
        submit_button.place(x=200, y=240, width=220, height=25)
        button = tk.Button(self, text="Home page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=500, y=240, width=220, height=25)

        def submit_form():      # this method is for submit button
            global output
            if zip_entry.get().isdigit() and zip_entry2.get().isdigit() and distance_entry.get().isdigit():
                try:
                    output = emergencyVehicle.add_zipcode(zip_entry2.get(), zip_entry.get(), distance_entry.get())  # it is calling the function from the emergencyVehicle module
                except Exception as e:
                    error_label = tk.Label(self, text="Issue adding zipcodes")
                    error_label.config(bg="white", fg='Red')
                error_label = tk.Label(self, text=output)
                error_label.config(bg="white", fg='Green')
                error_label.place(x=330, y=280, width=220, height=25)
                zip_entry.delete(0, 'end')
                zip_entry2.delete(0, 'end')
                distance_entry.delete(0, 'end')
                zip_entry2.focus()

            else:
                error_label = tk.Label(self, text="Need only integers in Zip and Distance")
                error_label.config(bg="white", fg='red')
                error_label.place(x=330, y=280, width=220, height=25)
                if not zip_entry.get().isdigit() and not zip_entry2.get().isdigit() and not distance_entry.get().isdigit():
                    zip_entry.delete(0, 'end')
                    zip_entry2.delete(0, 'end')
                    distance_entry.delete(0, 'end')
                    zip_entry2.focus()


# this is the Delete vehicle page for the application and in this class we created buttons, labels and check box as required
class DeleteVehicle(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="DELETING VEHICLE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        id_label = tk.Label(self, text="Vehicle ID to delete: ")
        id_label.place(x=200, y=120, width=220, height=25)
        id_entry = tk.Entry(self, bd=5)
        id_entry.place(x=400, y=120, width=220, height=25)
        id_entry.bind("<Return>", lambda dummy: submit_form())

        submit_button = tk.Button(self, text="Submit",
                                  command=lambda: submit_form())
        submit_button.place(x=200, y=240, width=220, height=25)
        button = tk.Button(self, text="Home page",
                           command=lambda:controller.show_frame("StartPage"))
        button.place(x=500, y=240, width=220, height=25)

        def submit_form():      # this method is for submit button
            global output
            if id_entry.get().isdigit():
                try:
                    output = emergencyVehicle.delete_vehicle(id_entry.get())  # it is calling the function from the emergencyVehicle module
                except Exception as e:
                    error_label = tk.Label(self, text="Issue deleting vehicles")
                    error_label.config(bg="white", fg='Red')
                error_label = tk.Label(self, text=output)
                error_label.config(bg="white", fg='Green')
                error_label.place(x=330, y=280, width=220, height=25)
                id_entry.delete(0, 'end')
                id_entry.focus()

            else:
                error_label = tk.Label(self, text="Need only integers to delete")
                error_label.config(bg="white", fg='red')
                error_label.place(x=330, y=280, width=220, height=25)
                if not id_entry.get().isdigit():
                    id_entry.delete(0, 'end')
                    id_entry.focus()


# this is the returning vehicle page for the application and in this class we created buttons, labels and check box as required

class ReturnVehicle(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="RETURNING VEHICLE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        id_label = tk.Label(self, text="Vehicle ID to return: ")
        id_label.place(x=200, y=120, width=220, height=25)
        id_entry = tk.Entry(self, bd=5)
        id_entry.place(x=400, y=120, width=220, height=25)
        id_entry.bind("<Return>", lambda dummy: submit_form())

        submit_button = tk.Button(self, text="Submit",
                                  command=lambda: submit_form())
        submit_button.place(x=200, y=240, width=220, height=25)
        button = tk.Button(self, text="Home page",
                           command=lambda:controller.show_frame("StartPage"))
        button.place(x=500, y=240, width=220, height=25)

        def submit_form():      # this method is for submit button in GUI
            global output
            if id_entry.get().isdigit():
                try:
                    output = emergencyVehicle.return_vehicle(id_entry.get())  # it is calling the function from the emergencyVehicle module
                except Exception as e:
                    error_label = tk.Label(self, text="Issue returning vehicles")
                    error_label.config(bg="white", fg='Red')
                error_label = tk.Label(self, text=output)
                error_label.config(bg="white", fg='Green')
                error_label.place(x=330, y=280, width=220, height=25)
                id_entry.delete(0, 'end')
                id_entry.focus()

            else:
                error_label = tk.Label(self, text="Need only integers to return")
                error_label.config(bg="white", fg='red')
                error_label.place(x=330, y=280, width=220, height=25)
                if not id_entry.get().isdigit():
                    id_entry.delete(0, 'end')
                    id_entry.focus()


# this is the show vehicle page for the application and in this class we created buttons, labels and check box as required

class ShowVehicle(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.submit_form("entire")

        submit_button = tk.Button(self, text="VehicleAvail", command=lambda: self.submit_form("entire"))
        submit_button.place(x=550, y=50, width=100, height=30)
        out_button = tk.Button(self, text="OutVehicles", command=lambda: self.submit_form("out"))
        out_button.place(x=550, y=80, width=100, height=30)
        submit_button = tk.Button(self, text="zipcode", command=lambda: self.submit_form("zip"))
        submit_button.place(x=550, y=110, width=100, height=30)
        button = tk.Button(self, text="Home page", command=lambda: controller.show_frame("StartPage"))
        button.place(x=550, y=160, width=100, height=30)

    max_columns = 0
    max_rows = 0

    def submit_form(self, type_check):      # this method is for submit button in the GUI

        lst_vehicles = emergencyVehicle.showVehicles(type_check)

        total_rows = len(lst_vehicles)
        total_columns = len(lst_vehicles[0])

        self.max_columns = total_columns if total_columns > self.max_columns else self.max_columns
        self.max_rows = total_rows if total_rows > self.max_rows else self.max_rows

        for i in range(self.max_rows):
            for j in range(self.max_columns):
                e = tk.Entry(self, width=11, fg='blue', font=('Arial', 8, 'bold'))
                e.grid(row=i, column=j)
                e.insert(i, " ")

        for i in range(total_rows):
            for j in range(total_columns):
                e = tk.Entry(self, width=11, fg='blue', font=('Arial', 8, 'bold'))
                e.grid(row=i, column=j)
                e.insert(i, lst_vehicles[i][j])


# it is the main body of the program

if __name__ == "__main__":
    app = EmergencyVehicleAPP()
    app.wm_geometry("780x400")
    app.title("Emergency Vehicles GUI")
    app.resizable(False, False)
    app.mainloop()