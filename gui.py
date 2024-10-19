import customtkinter as ctk
import os
import tkinter as tk
from tkinter import ttk
from windowCapture import Windowcapture
from main import MainProgram

class gui:
    # Create the main window and variables
   
    def __init__(self, fov:int = 100, mouse_time = 0.5, mouse_algo = 'simple'):
        #root window
        self.root = tk.Tk()
        self.root.title("Start Selection")
        self.root.geometry("500x500")
        self.main = None


        #variables for screencapture
        self.wc = Windowcapture()
        self.window = None
        self.model_weight = None
        self.model_cfg = None

        #variables for frame manipulation and 
        self.fov:int = fov 

        #variables for mouse movement
        self.mouse_time = mouse_time
        self.mouse_algo =mouse_algo 

        #variables for Traning
        self.frame_capture_interval = None
        self.no_of_frames = None
        self.model_name = None





    #Functions to list models (helper for comboboxes 2)
    def list_directories(self,path):
        # List to store directories
        directories = []
        
        # Iterate over the items in the specified path
        for item in os.listdir(path):
            # Create full path
            full_path = os.path.join(path, item)
            # Check if it's a directory
            if os.path.isdir(full_path):
                directories.append(item)  # Append the directory name

        return directories

    #Function to assign values from comboboxes
    #Landing page when program is first run
    def create_home_window(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Start Selection")
        self.root.geometry("500x500")
        print(f'self.model_weight {self.model_weight} self.model_cfg {self.model_cfg} self.fov {self.fov} self.mouse_time {self.mouse_time} self.mouse_algo {self.mouse_algo}')


        def on_select(event):
            if event.widget == dropdown1:
                window = dropdown1.get()
                self.wc.setwindow(window)
            elif event.widget == dropdown2:
                model = dropdown2.get()
                model_weight = './models/' + model+'/'+model + '.weights'
                if os.path.exists(model_weight):
                    self.model_weight = model_weight
                model_cfg = './models/'+model+'/' + model + '.cfg'
                if os.path.exists(model_cfg):
                    self.model_cfg = model_cfg
        def on_submit():
            if (self.model_weight == None) or (self.model_cfg == None):
                print("Submit failed")
                pass

            main = MainProgram(self.wc,weight_path=self.model_weight,config_path=self.model_cfg,fov = self.fov, mouse_time = self.mouse_time, mouse_algo = self.mouse_algo)
            main.run()
        def on_new_model():
            print("New model")
            pass
   


        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(5, weight=1)


        # Create a style for the Combobox
        style = ttk.Style()
        style.configure("Rounded.TCombobox", borderwidth=1, relief="flat")

        # Create the Combobox for program selection
        option1 = self.wc.getwindow()
        label = tk.Label(self.root, text="Select the program to capture:")
        label.grid(row=0, column=0,sticky="w", padx=15, pady=1)
        dropdown1 = ttk.Combobox(self.root, values=option1, style="Rounded.TCombobox")
        dropdown1.grid(row=1, column=0,sticky="ew", padx=15, pady=1)
        dropdown1.bind("<<ComboboxSelected>>", on_select)  # Bind the selection event

        # Create the Combobox for model selection
        option2 = self.list_directories("./models")
        label2 = tk.Label(self.root, text="Select the model to run:")
        label2.grid(row=2, column=0,sticky="ws", padx=15, pady=1)
        dropdown2 = ttk.Combobox(self.root, values=option2, style="Rounded.TCombobox")
        dropdown2.grid(row=3, column=0,sticky="ews", padx=15, pady=1)
        dropdown2.bind("<<ComboboxSelected>>", on_select)  # Bind the selection event

        # Create a  Text widget for explanations
        text = tk.Text(self.root, height=15, width=50)
        text.grid(row=4, column=0,sticky="ew", padx=15, pady=10)
        text.insert(tk.END,f"Note:\n • The selected Program should not be under any other running program.\n\n • Larger models run generally run slower by a small margin (noticable when gaming)\n\n ")
        # Button to start the program
        button = tk.Button(self.root, text="      Start     ", command=on_submit)
        button.grid(row=5, column=0,sticky="es", padx=15, pady=10)

        #Button to cutomize the mouse
        button2 = tk.Button(self.root, text="Customize", command=self.customize)
        button2.grid(row=5, column=0,sticky="ews", padx=150, pady=10)

        #Button to create a new model
        button3 = tk.Button(self.root, text="New model", command=self.newmodel)
        button3.grid(row=5, column=0,sticky="ws", padx=15, pady=10)

    def newmodel(self):
        self.root.destroy()
        self.root= tk.Tk()
        self.root.title("Train new model")
        self.root.geometry("650x700")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(7, weight=1)
        
        def slider_mouse(value):
                label_mouse.config(text=f"Current Value: {value} ms")
                self.mouse_time= int(value)
        def slider(value):
                label.config(text=f"Current Value: {value} %")
                self.fov= int(value)
        def option(event):
            self.mouse_algo = dropdown.get()
        
        def write():
            self.create_home_window()
        def on_select(event):
            if event.widget == dropdown1:
                window = dropdown1.get()
                self.wc.setwindow(window)
        
        # Create a label to display the slider value
        option1 = self.wc.getwindow()
        label = tk.Label(self.root, text="Select the program to capture:")
        label.grid(row=0, column=0,sticky="w", padx=15, pady=1)
        dropdown1 = ttk.Combobox(self.root, values=option1, style="Rounded.TCombobox")
        dropdown1.grid(row=1, column=0,sticky="ew", padx=15, pady=1)
        dropdown1.bind("<<ComboboxSelected>>", on_select)  # Bind the selection event



 
        # Create a label to display the slider value
        label_mouse = tk.Label(self.root, text="Frame capture interval" )
        label_mouse1 = tk.Label(self.root, text=f"Current Value:{self.mouse_time} ms")
        label_mouse1.grid(row=2, column=0,sticky="e", padx=10, pady=10)
        label_mouse.grid(row=2, column=0,sticky="w", padx=10, pady=10)
        # Create a slider (Scale widget)
        slider2 = tk.Scale(self.root, from_=1, to=50, orient='horizontal', command=slider_mouse)
        slider2.grid(row=3, column=0,sticky='ew', padx=10, pady=10)
        slider2.set(self.mouse_time)


        label_entry = tk.Label(self.root,text="Enter number of frames to capture:")
        label_entry.grid(row=4, column=0,sticky="w", padx=10, pady=10)
        entry = tk.Entry(self.root)
        entry.grid(row=5, column=0, sticky="we", padx=10, pady=10)
        self.no_of_frames = entry

        label_test = tk.Label(self.root,text="Enter the name of the model:")
        label_test.grid(row=6, column=0,sticky="w", padx=10, pady=10)
        text_box = tk.Text(self.root, height=10, width=40)
        text_box.grid(row=7, column=0,sticky="ew", padx=10, pady=10)    



        # Create a  Text widget for explanations
        text = tk.Text(self.root, height=13, width=50)
        text.grid(row=8, column=0,sticky="ew", padx=15, pady=10)
        text.insert(tk.END,f"README: \nKeep the capture interval such that there is a good balance between new enviroment and and less repetations\nFor the model to be good at detecting try having at leat 500 training images (you only need to train once)\nThe traning images will be stored in training/name/images \nAnnotated images should be stored in the same directory with the name annotated \nUse a external software such as  Labelbox to do the annotation process \nExport the annotated images for yolo model ")

        # Button to start the program
        button = tk.Button(self.root, text=" Start capturing ", command=write)
        button.grid(row=9, column=0,sticky="es", padx=15, pady=10)

        button2 = tk.Button(self.root, text="Train a annotated traning set ", command=self.customize)
        button2.grid(row=9, column=0,sticky="ews", padx=150, pady=10)

        #Button to create a new model
        button3 = tk.Button(self.root, text="   Back    ", command=self.create_home_window)
        button3.grid(row=9, column=0,sticky="ws", padx=15, pady=10)

        # Start the main event loop
        self.root.mainloop()


        

    #Landing page when customize button is clicked
    def customize(self):
        self.root.destroy()
        self.root= tk.Tk()
        self.root.title("modify running parameters")
        self.root.geometry("500x500")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(7, weight=1)
        # def show_value(value):
        #     # Update the label with the current slider value
        #     label.config(text=f"Current Value: {value}")
        # def set_fov(value):
        #     # Update the label with the current slider value
        #     label.config(text=f"Current Value: {value}")
        
        def slider_mouse(value):
                label_mouse.config(text=f"Current Value: {value} ms")
                self.mouse_time= int(value)
        def slider(value):
                label.config(text=f"Current Value: {value} %")
                self.fov= int(value)
        def option(event):
            self.mouse_algo = dropdown.get()
        
        def write():
            self.create_home_window()



        # Create a label to display the slider value
        label = tk.Label(self.root, text="FOV in dimention percent" )
        label.grid(row=1, column=0,sticky="w", padx=10, pady=10)
        label = tk.Label(self.root, text=f"Current Value: {self.fov} %")
        label.grid(row=1, column=0, padx=10, pady=10)
        # Create a slider (Scale widget)
        slider = tk.Scale(self.root, from_=20, to=100, orient='horizontal', command=slider)
        slider.grid(row=2, column=0,sticky='ew', padx=10, pady=10)
        slider.set(self.fov)

 
        # Create a label to display the slider value
        label_mouse = tk.Label(self.root, text="Mouse snap speed" )
        label_mouse.grid(row=3, column=0,sticky="w", padx=10, pady=10)
        label_mouse = tk.Label(self.root, text=f"Current Value:{self.mouse_time} ms")
        label_mouse.grid(row=3, column=0, padx=10, pady=10)
        # Create a slider (Scale widget)
        slider2 = tk.Scale(self.root, from_=10, to=1000, orient='horizontal', command=slider_mouse)
        slider2.grid(row=4, column=0,sticky='ew', padx=10, pady=10)
        slider2.set(self.mouse_time)


        # Create the Combobox for mouse algorithm selection
        option2 = ["Simple","Complex"]
        label_mouse_algo = tk.Label(self.root, text="Select mouse movement algorithm:")
        label_mouse_algo.grid(row=5, column=0,sticky="ws", padx=15, pady=1)
        dropdown = ttk.Combobox(self.root, values=option2, style="Rounded.TCombobox")
        dropdown.grid(row=6, column=0,sticky="ews", padx=15, pady=1)
        dropdown.bind("<<ComboboxSelected>>", option)  # Bind the selection event



        # Create a  Text widget for explanations
        text = tk.Text(self.root, height=30, width=50)
        text.grid(row=7, column=0,sticky="ew", padx=15, pady=10)
        text.insert(tk.END,f"Parameters:\n\n•FOV: (Set to {self.fov}%) is the size of the frame on which the object recognition is performed\n\n•Mouse snap speed: (Set to {self.mouse_time} ms) time before the mouse snaps to the object (very high can be flaged by certain....) \n•Mouse movement algorithm: (Set to {self.mouse_algo}) the mouse movemnt more complex better slight performance impact")

        # Button to start the program
        button = tk.Button(self.root, text="    Save    ", command=write)
        button.grid(row=8, column=0,sticky="es", padx=15, pady=10)


        #Button to create a new model
        button3 = tk.Button(self.root, text="   Back    ", command=self.create_home_window)
        button3.grid(row=8, column=0,sticky="ws", padx=15, pady=10)

        # Start the main event loop
        self.root.mainloop()





    def run(self):
        self.create_home_window()
        self.root.mainloop()



gui().run()