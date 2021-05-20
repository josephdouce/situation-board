from tkinter import *
import tkinter as tk
from ttkthemes import themed_tk 
from tkinter import messagebox
import csv
import json

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        root.wm_title("Situation Board")
        #root.iconbitmap(default='./icon.ico')
        self.grid()
        self.main_window()


    #create main window
    def main_window(self):
        print("Making Main Window Widgets")        
        self.config = self.load_json()

        self.buttons = []
        self.labels = []
        self.entrys = []
        self.options = []
        self.colors = []
        self.headings = []
        self.tables = []
        self.last_value = []

        self.column_one = Frame(self)
        self.column_one.grid(row=0, column=0, sticky="n", padx=5)
        self.column_two = Frame(self)
        self.column_two.grid(row=0, column=1, padx=5, sticky="n")
        self.column_three = Frame(self)
        self.column_three.grid(row=0, column=2, sticky="n", padx=5)
        self.column_four = Frame(self)
        self.column_four.grid(row=0, column=3, sticky="n", padx=5)
        self.column_five = Frame(self)
        self.column_five.grid(row=0, column=4, sticky="n", padx=5)

        for i in range(len(self.config)):
            
            if self.config[i]["Column"] == "1":
                column = self.column_one
            elif self.config[i]["Column"] == "2":
                column = self.column_two
            elif self.config[i]["Column"] == "3":
                column = self.column_three
            elif self.config[i]["Column"] == "4":
                column = self.column_four
            elif self.config[i]["Column"] == "5":
                column = self.column_five
                
            self.labels.append(Label(column))
            self.labels[i]["anchor"] = "w"  
            self.buttons.append(Button(column))
            self.entrys.append(Entry(column))
            self.options.append([self.config[i]["Option 1"],self.config[i]["Option 2"],self.config[i]["Option 3"],self.config[i]["Option 4"],self.config[i]["Option 5"]])
            self.colors.append([self.config[i]["Color 1"],self.config[i]["Color 2"],self.config[i]["Color 3"],self.config[i]["Color 4"],self.config[i]["Color 5"]])
            self.tables.append(Frame(column))

            if self.config[i]["Type"] == "Heading":
                self.labels[i]["text"] = self.config[i]["Label"]
                self.labels[i]["font"] = ("bold", 16)
                self.labels[i].grid(column=0, columnspan=2, pady=5,sticky="w")
            elif self.config[i]["Type"] == "Spacer":
                self.labels[i]["text"] = "Spacer"
                self.labels[i]["fg"] = self.labels[i]["bg"]
                self.labels[i].grid(column=0, sticky="w", pady=3)
            elif self.config[i]["Type"] == "Button":
                self.labels[i]["text"] = self.config[i]["Label"]
                self.labels[i]["width"] = 15
                self.labels[i].grid(column=0, sticky="w")
                self.buttons[i]["text"] = self.config[i]["Option 1"]
                self.buttons[i]["command"] = lambda i=i: self.button_click(i)
                self.buttons[i]["width"] = 15
                if not self.colors[i][0] == "":
                    self.buttons[i]["background"] =  self.colors[i][0]
                self.buttons[i]["relief"] = "flat"
                self.buttons[i].grid(row=self.labels[i].grid_info()["row"], column=1,sticky="nesw", pady=1)
            elif self.config[i]["Type"] == "Text":
                self.labels[i]["text"] = self.config[i]["Label"]
                self.labels[i]["width"] = 15
                self.labels[i].grid(column=0, sticky="w")
                self.entrys[i] = Entry(column)
                self.entrys[i]["relief"] = "flat"
                self.entrys[i].grid(row=self.labels[i].grid_info()["row"], column=1, sticky="nesw", pady=4)
            elif self.config[i]["Type"] == "Note":
                self.entrys[i] = Text(column)
                self.entrys[i]["width"] = 30
                self.entrys[i]["relief"] = "flat"
                self.entrys[i].grid(column=0, sticky="nesw", pady=4, columnspan=2)
            elif self.config[i]["Type"] == "Table":
                self.tables[i] = Frame(column)
                for col in range(3):
                    for row in range(3):
                        button = Button(self.tables[i])
                        button["width"] = 10
                        button.grid(row=row, column=col)
                self.tables[i].grid(column=0, sticky="nesw", pady=4, columnspan=2)
            else:
                self.labels[i]["text"] = self.config[i]["Label"]
                self.labels[i]["width"] = 15
                self.labels[i].grid(column=0, sticky="w")

        menubar = Menu(self)
        menubar["relief"] = "flat"

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Preferences", command=self.preferences_window)
        editmenu.add_command(label="Edit Layout", command=self.layout_window)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about_window)
        helpmenu.add_command(label="Help", command=self.help_window)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        root.config(menu=menubar)

    def preferences_window(self):
        preferencesWindow = Toplevel(self)
        preferencesWindow.title("Preferences")

    def layout_window(self):
        keys = []
        values = []
        for i in range(len(self.config[0])):
            values.append("")
            values[i] = StringVar()
            keys.append("")
            keys[i] = StringVar()
            

        columnSelected = StringVar()
        columnSelected.set("1")
        columnChoices = [1,2,3,4,5]
        
        labelSelected = StringVar()
        labelSelected.set(self.config[0]["Label"])
        labelChoices = [""]

        optionsEnabled = {"Heading" : ["Type","Column","Label"],
                         "Spacer" : ["Type","Column"],
                         "Note" : ["Type","Column"],
                         "Text" : ["Type","Column","Label"],
                         "Button" : ["Type","Column","Label","Color 1", "Color 2","Color 3","Color 4","Color 5","Option 1", "Option 2","Option 3","Option 4","Option 5"]}

        def column_change(*args):
            print("Column Selected: ", columnSelected.get())
            #clear list of choices
            labelChoices = []
            #get new choices for slected column
            for item in self.config:
                if item["Column"] == columnSelected.get():
                    labelChoices.append(item["Label"])
            #clear choices fom menu
            self.labelOptionMenu['menu'].delete(0, 'end')
            #add new choices to menu
            i=0
            for choice in labelChoices:
                self.labelOptionMenu['menu'].add_command(
                label=choice, command=tk._setit(labelSelected, choice, label_change))

        def label_change(*args):
            print("Label Selected: ", labelSelected.get())
            for item in self.config:
                if item["Label"] == labelSelected.get():
                    i=0
                    for key in item:
                        values[i].set(item[key])
                        i+=1
            make_widgets()

        def save(*args):
            print("Saving")
            for item in self.config:
                if str(item["UID"]) == values[13].get():
                    i=0
                    for key in keys:
                        k = ""
                        k = keys[i].get()
                        v = ""
                        v = values[i].get()
                        item[k] = v
                        i+=1
                    print(item)
   
            self.save_json()
            make_widgets()
            refresh()

        def new():
            print("New")
            uid = 0
            for item in self.config:
                if int(item["UID"]) > uid:
                    uid = int(item["UID"])
            uid+=1
            self.config.append({'Type': 'Heading',
                                'Column': columnSelected.get(),
                                'Label': 'New',
                                'Option 1': '',
                                'Option 2': '',
                                'Option 3': '',
                                'Option 4': '',
                                'Option 5': '',
                                'Color 1': '',
                                'Color 2': '',
                                'Color 3': '',
                                'Color 4': '',
                                'Color 5': '',
                                'UID': uid})

            self.save_json()
            column_change()
            refresh()

        def delete():
            print("Deleting: ", str(values[2].get()))
            for i in range(len(self.config)):
                if str(self.config[i]["UID"]) == str(values[13].get()):
                    print("Deleting:", self.config[i])
                    self.config.pop(i)

            self.save_json()
            refresh()

        def move_up():
            for i in range(len(self.config)):
                if str(self.config[i]["UID"]) == str(values[13].get()):
                    if i==0:
                        print("Already at Top")
                        break
                    self.config.insert(i-1, self.config.pop(i))
                    print("Moving ", str(values[13].get()), " from ", i, " to ", i-1)
                    break

            self.save_json()
            refresh()
            
        def move_down():
            for i in range(len(self.config)):
                if str(self.config[i]["UID"]) == str(values[13].get()):
                    if i==len(self.config)-1:
                        print("Already at Bottom")
                        break
                    self.config.insert(i+1, self.config.pop(i))
                    print("Moving ", str(values[13].get()), " from ", i, " to ", i+1)                   
                    break
                
            self.save_json()
            refresh()

        def refresh():
            print("Refreshing UI")
            for widget in self.winfo_children():
                if not widget == layoutWindow:
                    widget.destroy()
            self.main_window()

        def make_widgets():
            print("Making Layout Editor Widgets")
            for widget in layoutWindow.winfo_children():
                widget.destroy()
                
            label = Label(layoutWindow)
            label["text"] = "Current Column"
            label["relief"] = "flat"
            label.grid(row=0, column=0, sticky="w")
            label = Label(layoutWindow)
            label["text"] = "Current Label"
            label["relief"] = "flat"
            label.grid(row=1, column=0, sticky="w")

            columnOptionMenu = OptionMenu(layoutWindow,columnSelected,*columnChoices,command=column_change)
            columnOptionMenu["relief"] = "flat"
            columnOptionMenu["bg"] = "lightgrey"
            columnOptionMenu.grid(row=0, column=1, sticky="nesw")
            
            self.labelOptionMenu = OptionMenu(layoutWindow,labelSelected,*labelChoices, command=label_change)
            self.labelOptionMenu["relief"] = "flat"
            self.labelOptionMenu["bg"] = "lightgrey"
            self.labelOptionMenu.grid(row=1, column=1, sticky="nesw")

            label = Frame(layoutWindow)
            label["bg"] = "grey"
            label.grid(row=2, column=0, columnspan=2, sticky="nesw", pady=1)
            
            column_change()
            
            for item in self.config:
                if item["Label"] == labelSelected.get():
                    print("Making Widgets for ", item["Label"])
                    i=0
                    for key in item:
                        label = Label(layoutWindow)
                        label["textvariable"] = keys[i]
                        label.grid(column=0, row =i+3, sticky="w")
                      
                        values[i].set(item[key])
                        keys[i].set(key)

                        if key in optionsEnabled[values[0].get()]:
                            if key == "Type":
                                entry = OptionMenu(layoutWindow, values[i], "Heading", "Spacer", "Button", "Text", "Note", command=save)
                                entry["relief"] = "flat"
                                entry["bg"] = "lightgrey"
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=1)
                            elif key == "Column":
                                entry = OptionMenu(layoutWindow, values[i], "1", "2", "3", "4", "5", command=save)
                                entry["relief"] = "flat"
                                entry["bg"] = "lightgrey"
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=1)
                            elif key in ["Color 1", "Color 2","Color 3","Color 4","Color 5"]:
                                entry = OptionMenu(layoutWindow, values[i], "red", "green", "yellow", "orange", "brown" )
                                entry["relief"] = "flat"
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=1)
                            elif key in ["Option 1", "Option 2","Option 3","Option 4","Option 5"]:
                                entry = Entry(layoutWindow)
                                entry["relief"] = "flat"
                                entry["textvariable"] = values[i]
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=4)
                            else:
                                entry = Entry(layoutWindow)
                                entry["relief"] = "flat"
                                entry["textvariable"] = values[i]
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=4)

                        else:
                                entry = Label(layoutWindow)
                                entry["relief"] = "flat"
                                entry["textvariable"] = values[i]
                                entry.grid(column=1, row = i+3, sticky="nesw", pady=3)
                        i+=1
                        
            label = Frame(layoutWindow)
            label["bg"] = "grey"
            label.grid(columnspan=2, sticky="nesw", pady=1)
         
            button = Button(layoutWindow, text="Save", command=save)
            button["relief"] = "flat"
            button["bg"] = "lightgrey"
            button.grid(column=0, sticky="nesw", pady=1, columnspan=2)

            button = Button(layoutWindow, text="New", command=new)
            button["relief"] = "flat"
            button["bg"] = "lightgrey"
            button.grid(column=0, sticky="nesw", pady=1, columnspan=2)
            
            button = Button(layoutWindow, text="Delete", command=delete)
            button["relief"] = "flat"
            button["bg"] = "lightgrey"
            button.grid(column=0, sticky="nesw", pady=1, columnspan=2)

            button = Button(layoutWindow, text="Up", command=move_up)
            button["relief"] = "flat"
            button["bg"] = "lightgrey"
            button.grid(column=0, sticky="nesw", pady=1, columnspan=2)

            button = Button(layoutWindow, text="Down", command=move_down)
            button["relief"] = "flat"
            button["bg"] = "lightgrey"
            button.grid(column=0, sticky="nesw", pady=1, columnspan=2)

        layoutWindow = Toplevel(self)
        layoutWindow.title("Layout")
        
        make_widgets()
            
    def about_window(self):
        aboutWindow = Toplevel(self)
        aboutWindow.title("About")

    def help_window(self):
        helpWindow = Toplevel(self)
        helpWindow.title("Help")

    def button_click(self, i):
        if self.buttons[i]["text"] == self.options[i][0]:
            self.buttons[i]["text"] = self.options[i][1]
            if not self.colors[i][1] == "":
                self.buttons[i]["background"] =  self.colors[i][1]
        elif self.buttons[i]["text"] == self.options[i][1]:
            if self.options[i][2] == "":
                self.buttons[i]["text"] = self.options[i][0]
                if not self.colors[i][0] == "":
                    self.buttons[i]["background"] =  self.colors[i][0]
            else:
                self.buttons[i]["text"] = self.options[i][2]
                if not self.colors[i][2] == "":
                    self.buttons[i]["background"] =  self.colors[i][2]
        elif self.buttons[i]["text"] == self.options[i][2]:
            if self.options[i][3] == "":
                self.buttons[i]["text"] = self.options[i][0]
                if not self.colors[i][0] == "":
                    self.buttons[i]["background"] =  self.colors[i][0]
            else:
                self.buttons[i]["text"] = self.options[i][3]
                if not self.colors[i][3] == "":
                    self.buttons[i]["background"] =  self.colors[i][3]
        elif self.buttons[i]["text"] == self.options[i][3]:
            if self.options[i][4] == "":
                self.buttons[i]["text"] = self.options[i][0]
                if not self.colors[i][0] == "":
                    self.buttons[i]["background"] =  self.colors[i][0]
            else:
                self.buttons[i]["text"] = self.options[i][4]
                if not self.colors[i][4] == "":
                    self.buttons[i]["background"] =  self.colors[i][4]
        elif self.buttons[i]["text"] == self.options[i][4]:
            self.buttons[i]["text"] = self.options[i][0]
            if not self.colors[i][0] == "":
                self.buttons[i]["background"] =  self.colors[i][0]
    
    def save_json(self):
        output_file = open('./config.json', 'w', encoding='utf-8')
        json.dump(self.config, output_file) 

    def load_json(self):
        with open('./config.json') as json_file:  
            data = json.load(json_file)
            return(data)
            
#launch app      
if __name__ == '__main__':
    root = themed_tk.ThemedTk()
    app = Application(master=root)
    app.mainloop()
