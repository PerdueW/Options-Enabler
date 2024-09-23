#!/usr/bin/python

from Tkinter import *
import Tkinter, tkFileDialog
from tkFileDialog import askopenfilename, asksaveasfilename
import Tkinter as tk
import tkFont
import ttk as ttk 
import os
import os.path
import tkMessageBox
import re
import sys
import hashlib


sizex = 650
sizey = 500
posx  = 0
posy  = 0

oWsizex = 350
oWsizey = 150
oWposx  = 0
oWposy  = 0

features = {}
md5 = hashlib.md5()

class OptionEnabler:
    def populateMacs(self):
        macs = []
        macfilePath = askopenfilename()
        if macfilePath == "":
            tkMessageBox.showinfo("Missing MACs File selection", "Please select a file with MACs.")
            pass
        else:
            with open(macfilePath) as macFile:
                for mac in macFile:
                    mac = mac.strip()
                    mac = mac.lower()                   
                    lenMac = len(mac)
                    if len(mac) == 12:
                        mac = ":".join(mac[i:i+2] for i in range(0, len(mac), 2))
                    else:
                        mac = mac
                    if "00:d0:5f" in mac[:8]:
                        mac = str(mac).lower()
                        mac = mac.strip()               
                        macs.append(mac)
                    else:
                        pass
                macs = str(macs).strip('[]')
                macs = macs.replace("'", "")
                self.macEntry.insert(0, macs)
            
    def populateFeatures(self):
        PATH = 'OptionsList.txt'        
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            featurefile = open('OptionsList.txt')
            for line in featurefile:                
                line = line.strip()
                feature = line.split('=', 1)[0]
                displayName = line.split('=', 1)[1]
                features[feature] = displayName            
                self.featureList.insert(0, displayName)                            
        else:
            self.featureList.insert(0, "'OptionList' file not found!")
            
    def createOptionsUgrade(self):  
        macs = []
        features = []  
        inputMacs = self.macEntry.get()      
        if not self.macEntry.get():
            tkMessageBox.showinfo("Missing MACs", "Please enter a MAC or MACs to continue")
            return
        else:
            inputMacs = inputMacs.split()
            for mac in inputMacs:
                mac = mac.strip()
                mac = mac.replace(",", "")
                lenMac = len(mac)
                if len(mac) == 12:
                    mac = ":".join(mac[i:i+2] for i in range(0, len(mac), 2))
                    macs.append(mac) 
                else:
                    macs.append(mac) 

        selectedFeatures = map(int, self.featureList.curselection())
        if not selectedFeatures:
            tkMessageBox.showinfo("Missing Feature(s)", "Please select a Feature or Features to continue")
            return
        else:
            for selfeature in selectedFeatures:
                feature = self.featureList.get(selfeature)
                featurefile = open('OptionsList.txt')
                for line in featurefile:
                    line = line.strip()
                    displayName = line.rsplit('=', 1)[1]
                    if feature == displayName:
                        feature = line.rsplit('=', 1)[0]
                        features.append(feature)        

        PATH = asksaveasfilename(initialfile='options.upgrade')
        if PATH == "":
            PATH = "options.upgrade"
        else:
            PATH = PATH
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            override = tkMessageBox.askyesno("File Overrride", PATH + " file detected. Do you wish to overrride?")   
            if override == True:
                file = open(PATH, 'w') 
                for mac in macs:
                    mac = mac.upper()
                    file.write("[" + mac + "]" + '\n')
                    for feature in features:                        
                        print mac
                        data = feature + mac + "valcom"
                        data = str(data)
                        encodedFeature = hashlib.md5(data).hexdigest()
                        file.write(feature + "=" + encodedFeature + '\n')
                    file.write('\n') 
            elif override == False:   
                return
        else:
            file = open(PATH, 'w') 
            for mac in macs:
                mac = mac.upper()
                file.write("[" + mac + "]" + '\n')
                for feature in features:                    
                    print mac
                    data = feature + mac + "valcom"
                    data = str(data)
                    encodedFeature = hashlib.md5(data).hexdigest()
                    file.write(feature + "=" + encodedFeature + '\n')
                file.write('\n') 
                  
        self.macEntry.delete(0, END)                   
        self.featureList.selection_clear(0, END)    
                           
    def __init__(self, master):
        self.helv10  = tkFont.Font(family="Helvetica", size=10)
        self.helv10b = tkFont.Font(family="Helvetica", size=10, weight="bold")
        self.helv11  = tkFont.Font(family="Helvetica", size=11)
        self.helv11b = tkFont.Font(family="Helvetica", size=11, weight="bold")
        self.helv12  = tkFont.Font(family="Helvetica", size=12)
        self.helv12b = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.helv13  = tkFont.Font(family="Helvetica", size=13)
        self.helv13b = tkFont.Font(family="Helvetica", size=13, weight="bold") 
    
        self.master = master
        self.master.title("Valcom Option Enabler")
        
        self.emptyLabel1 = tk.Label(root, textvariable="")
        self.emptyLabel1.grid(row=0, columnspan=5)
        
        self.macLabel = tk.Label(root, text="MAC(s):", font=self.helv12b, width=9, anchor='w')
        self.macLabel.grid(row=1, column=0, padx=3, pady=1, sticky='n')
        
        self.macEntry = tk.Entry(root, width=62, font=self.helv11)
        self.macEntry.grid(row=1, column=1, columnspan=3)
        self.macEntry.focus_force()  
        
        self.emptyLabel2 = tk.Label(root, textvariable="")
        self.emptyLabel2.grid(row=2, column=0, sticky='w')
        
        self.addmacBtn = tk.Button(root, text="Add MAC(s)", command=self.populateMacs, width=8, height=1, font=self.helv10)
        self.addmacBtn.grid(row=2, column=1, sticky='w')
        
        self.featureLabel = tk.Label(root, text = "Feature(s):", font=self.helv12b, width=9, anchor='w')
        self.featureLabel.grid(row=3, column=0, padx=3, sticky='n')   
        
        self.featureList = tk.Listbox(root, yscrollcommand="", selectmode='extended', height=20, width=62, background='#bbbbbb')
        self.featureList.grid(row=3, column=1, rowspan=4, columnspan=3)
        
        self.emptyLabel3 = tk.Label(root, textvariable="")
        self.emptyLabel3.grid(row=8, column=0)
        
        self.exitBtn = tk.Button(root, text = "Exit", command=close_window, width=8, font=self.helv12b)
        self.exitBtn.grid(row=9, column=0, sticky='e')
        
        self.emptyLabel4 = tk.Label(root, textvariable="", width=8)
        self.emptyLabel4.grid(row=9, column=1)
        
        self.emptyLabel5 = tk.Label(root, textvariable="", width=8)
        self.emptyLabel5.grid(row=9, column=2)
        
        self.createfileBtn = tk.Button(root, text="Create File", command=self.createOptionsUgrade, width=8, font=self.helv12b)
        self.createfileBtn.grid(row=9, column=3, sticky='e')
        
        self.populateFeatures()

               
def close_window():   
    root.destroy()
       
root = tk.Tk()
OptionEnabler = OptionEnabler(root)
root.wm_geometry("%dx%d+%d+%d" % (sizex,sizey,posx,posy)) # sets the size of the main window
root.resizable(width=False, height=False) # disables the ability to resize the window
root.update_idletasks()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
x = w/2 - size[0]/2
y = h/2 - size[1]/2
root.geometry("%dx%d+%d+%d" % (size + (x, y)))
root.configure()
root.mainloop()

