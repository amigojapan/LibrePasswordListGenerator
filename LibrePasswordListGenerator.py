import Tkinter as tk
import Tkconstants, tkFileDialog, tkMessageBox
import string
import random
import json
import sys
import os
from  hashpass import *

root = tk.Tk()
root.title("LibrePasswordListGenerator")

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
class public_globals():
	FileNameWidget=None
	RecalculatePasswordsButton=None
	MasterPasswordWidget=None
	MasterPasswordString="unset"
	PasswordLength=12
	FileName="default_sites_list.json"
	gridarray = []
	Symbols='!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
class PasswordRow():
	PasswordWidget=None
	SiteWidget=None
	DeleteButton=None
	SaltWidget=None
	PasswordLengthWidget=None
	SymbolsWidget=None
		
def callback_delete_password_ok(index):
	public_globals.gridarray[index].PasswordWidget.destroy()
	public_globals.gridarray[index].SiteWidget.destroy()
	public_globals.gridarray[index].DeleteButton.destroy()
	public_globals.gridarray[index].SaltWidget.destroy()
	public_globals.gridarray[index].PasswordLengthWidget.destroy()
	public_globals.gridarray[index].SymbolsWidget.destroy()
	del public_globals.gridarray[index]
		
def reclaclulate_password_callback():
	for row in public_globals.gridarray:
		row.PasswordWidget.delete(0, tk.END)
		SiteString = row.SiteWidget.get()
		SaltString = row.SaltWidget.get()
		PasswordLengthString = row.PasswordLengthWidget.get()
		SymbolsString = row.SymbolsWidget.get()
		public_globals.MasterPasswordString = public_globals.MasterPasswordWidget.get()
		outhash=hash_my_password(SiteString+public_globals.MasterPasswordString,SaltString+public_globals.MasterPasswordString,SymbolsString,False)
		if int(PasswordLengthString)>32:
			tkMessageBox.showinfo("Error!", "Error: password cannot be longer than 32 characters long, defaulting to " + str(public_globals.PasswordLength))
			row.PasswordLengthWidget.delete(0, tk.END)
			row.PasswordLengthWidget.insert(0, public_globals.PasswordLength)
			PasswordLengthString=public_globals.PasswordLength
		row.PasswordWidget.insert(0, outhash[:int(PasswordLengthString)])
	public_globals.RecalculatePasswordsButton.configure(bg = "light grey")
	
def prompt_recalculate_password():
	public_globals.RecalculatePasswordsButton.configure(bg = "red")

def add_row(site,salt,passlen,symbols):
	row = PasswordRow()
	row.PasswordWidget = tk.Entry(root)
	row_index=len(public_globals.gridarray)
	SiteString = tk.StringVar()
	row.SiteWidget = tk.Entry(root, textvariable=SiteString)
	row.SiteWidget.insert(0, site)
	SaltString = tk.StringVar()
	row.SaltWidget = tk.Entry(root, textvariable=SaltString)	
	row.SaltWidget.insert(0, salt)
	PasswordLengthString = tk.StringVar()
	row.PasswordLengthWidget = tk.Entry(root, textvariable=PasswordLengthString)	
	row.PasswordLengthWidget.insert(0, passlen)
	SymbolsString = tk.StringVar()
	row.SymbolsWidget = tk.Entry(root, textvariable=SymbolsString)	
	row.SymbolsWidget.insert(0, symbols)
	row.DeleteButton = tk.Button(root, text="Delete", command=lambda:callback_delete_password_ok(row_index))
	row.PasswordWidget.grid(row=2+len(public_globals.gridarray)+1,			column=0)
	row.SiteWidget.grid(row=2+len(public_globals.gridarray)+1,				column=1)
	row.SaltWidget.grid(row=2+len(public_globals.gridarray)+1,				column=2)
	row.PasswordLengthWidget.grid(row=2+len(public_globals.gridarray)+1,	column=3)
	row.SymbolsWidget.grid(row=2+len(public_globals.gridarray)+1,			column=4)
	row.DeleteButton.grid(row=2+len(public_globals.gridarray)+1,			column=5) 
	public_globals.gridarray.append(row)
	
	
	
	SiteString.trace("w", lambda name, index, mode,SiteString=SiteString: prompt_recalculate_password())
	SaltString.trace("w", lambda name, index, mode,SaltString=SaltString: prompt_recalculate_password())
	PasswordLengthString.trace("w", lambda name, index, mode,PasswordLengthString=PasswordLengthString: prompt_recalculate_password())
	SymbolsString.trace("w", lambda name, index, mode,SymbolsString=SymbolsString: prompt_recalculate_password())
	
def callback_add_password_ok():
	add_row("http://","enter salt", public_globals.PasswordLength, public_globals.Symbols)
	public_globals.RecalculatePasswordsButton.configure(bg = "red")
	
def callback_save():
	l=[]
	for w in public_globals.gridarray:
		SaveRow=Object()
		SaveRow.SiteString=w.SiteWidget.get()
		SaveRow.SaltString=w.SaltWidget.get()
		SaveRow.PasswordLengthString=w.PasswordLengthWidget.get()
		SaveRow.SymbolsString=w.SymbolsWidget.get()
		#print(SaveRow.to_JSON())
		#aw_input()
		l.append(SaveRow.to_JSON())
	json_values = {
		'sites': l
	}
	print(json.dumps(json_values))
	json_string=json.dumps(json_values)
	#print dir(public_globals.FileNameWidget)
	public_globals.FileName=public_globals.FileNameWidget.get()
	
	result = tkMessageBox.askquestion("Save sites list", "Are You Sure you want to save the file " + public_globals.FileName + " and overwrite it?", icon='warning')
	if result == 'yes':
		print "Saving..."
		file_ = open(public_globals.FileName, 'w')
		file_.write(json_string)
		file_.close()
	else:
		print "I'm Not Saving Yet.."	
	
def callback_load():
	FileName_TMP = tkFileDialog.askopenfile(mode='r')
	if not FileName_TMP==None: #filename will be None when no file is selected	
		print FileName_TMP.name
		file_ = open(FileName_TMP.name, 'r')
		input_data=file_.read()
		file_.close()
		print input_data
		#delete all the UI for the previeus entries
		for w in public_globals.gridarray:
			w.PasswordWidget.destroy()
			w.SiteWidget.destroy()
			w.DeleteButton.destroy()
			w.SaltWidget.destroy()
			w.PasswordLengthWidget.destroy()
			w.SymbolsWidget.destroy()
		public_globals.gridarray=[]
		try:
			parsed_json = json.loads(input_data)
		except: # catch *all* exceptions
			e = sys.exc_info()[0]
			tkMessageBox.showinfo("Error!", "Error: %s, if this error is value error, you are either opening an empty file or an invalid file" % e)
		SitesList = parsed_json['sites']
		for site in SitesList:
			site_obj=json.loads(site)
			add_row(site_obj['SiteString'], site_obj['SaltString'], site_obj['PasswordLengthString'], site_obj['SymbolsString'])
		reclaclulate_password_callback()
		
def create_printable_file_callback():
	outputString=""
	outputString="Master Password:"+public_globals.MasterPasswordString+"\n"
	for w in public_globals.gridarray:
		outputString=outputString+"Site:"+w.SiteWidget.get()
		outputString=outputString+"\tSalt:"+w.SaltWidget.get()
		outputString=outputString+"\tPass Length:"+w.PasswordLengthWidget.get()
		outputString=outputString+"\tSymbols:"+w.SymbolsWidget.get()
		outputString=outputString+"\n"
	file_ = open("report.txt", 'w')
	file_.write(outputString)
	file_.close()
	tkMessageBox.showinfo("Warning!", "Warning, READ CAREFULLY: we have generated the file report.txt, print it before clicking ok, after you click ok, the file will be deleted for security purposes")
	os.remove("report.txt")#delete file
	
				
def callback_master_password_ok():
	public_globals.MasterPasswordString = e.get()
	l.destroy()
	e.destroy()
	b.destroy()
	public_globals.MasterPasswordWidget = tk.Entry(root)
	public_globals.MasterPasswordWidget.insert(0, public_globals.MasterPasswordString)
	MasterPasswordLabel = tk.Label(root, text="Master Password:")
	public_globals.RecalculatePasswordsButton = tk.Button(root, text="Recalculate Passwords", command=reclaclulate_password_callback)
	CreatePrintableFile = tk.Button(root, text="Cfreate printable file", command=create_printable_file_callback)
	AddPasswordButton = tk.Button(root, text="Add Password", command=callback_add_password_ok)
	SaveButton = tk.Button(root, text="Save site lables as file", command=callback_save)
	LoadButton = tk.Button(root, text="Load site labels from file", command=callback_load)
	public_globals.FileNameWidget = tk.Entry(root)
	public_globals.FileNameWidget.insert(0, public_globals.FileName)
	FileNameLabel = tk.Label(root, text="File Name:")
	PasswordLabel = tk.Label(root, text="Password")
	SiteLabel = tk.Label(root, text="Site")
	PasswordLengthLabel = tk.Label(root, text="Password Length")	
	SaltLabel = tk.Label(root, text="Salt")	
	SymbolsLabel = tk.Label(root, text="Symbols")	
	MasterPasswordLabel.grid(row=0,column=0)
	public_globals.MasterPasswordWidget.grid(row=0,				column=1)
	public_globals.RecalculatePasswordsButton.grid(row=0,		column=3)
	CreatePrintableFile.grid(row=0,	column=4)
	AddPasswordButton.grid(row=1,                 column=0)
	SaveButton.grid(row=1,                        column=1)
	LoadButton.grid(row=1,                        column=2)
	FileNameLabel.grid(row=1,                     column=3)
	public_globals.FileNameWidget.grid(row=1,     column=4)
	PasswordLabel.grid(row=2,			column=0)
	SiteLabel.grid(row=2,				column=1)
	SaltLabel.grid(row=2,				column=2)
	PasswordLengthLabel.grid(row=2,		column=3)
	SymbolsLabel.grid(row=2,			column=4)	
e = tk.Entry(root)
l = tk.Label(root, text="Enter your master password:")
b = tk.Button(root, text="OK", command=callback_master_password_ok)
l.grid(row=0,column=0)
e.grid(row=1,column=0)
b.grid(row=2,column=0)
root.mainloop()
#TO-DO:
#(done)dump password and site list to a file so it can be printed
#(done)warn the user that he should delete the file after printing, provide a button to delete the file
#(done) it was not a mac error, it was an error on linux too fix error on mac when clicking delete: https://gist.github.com/vdamewood/6b5ad052e7ff4d0915bd654ac63ad49c probably diffeent version of tkinter
