import Tkinter as tk
import Tkconstants, tkFileDialog, tkMessageBox
import string
import random
import json
import sys

root = tk.Tk()

MasterPassword="unset"
PasswordLength=9
FileName="default_sites_list.json"
gridaray = []
class PasswordRow():
	PasswordWidget=None
	PasswordLabel=None
	SiteWidget=None
	SiteLabel=None
	DeleteButton=None
	
def id_generator(size=PasswordLength, chars=string.ascii_uppercase + string.ascii_lowercase+string.digits +  ' !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~' ):
	return ''.join(random.choice(chars) for _ in range(size))

def callback_delete_password_ok(index):
	print index
	gridaray[index].SiteWidget.insert(0, "DELETED--")
	
def callback_add_password_ok():
	row = PasswordRow()
	row.PasswordWidget = tk.Entry(root)
	row.PasswordWidget.insert(0, id_generator())
	row.PasswordLabel = tk.Label(root, text="Password #" + str(len(gridaray)+1) + ":")
	row.SiteWidget = tk.Entry(root)
	row.SiteWidget.insert(0, "http://")
	row.SiteLabel = tk.Label(root, text="site #" + str(len(gridaray)+1) + ":")
	index=len(gridaray)
	row.DeleteButton = tk.Button(root, text="Delete", command=lambda:callback_delete_password_ok(index).pack())
	row.PasswordLabel.grid(row=1+len(gridaray)+1,  column=0)
	row.PasswordWidget.grid(row=1+len(gridaray)+1, column=1)
	row.SiteLabel.grid(row=1+len(gridaray)+1,      column=2)
	row.SiteWidget.grid(row=1+len(gridaray)+1,     column=3)
	row.DeleteButton.grid(row=1+len(gridaray)+1,   column=4) 
	#print len(gridaray)
	gridaray.append(row)

def callback_save():
	l=[]
	for w in gridaray:
		l.append(w.SiteWidget.get())
	json_values = {
    'PasswordLength': PasswordLength,
    'sites': l
	}
	print(json.dumps(json_values))
	json_string=json.dumps(json_values)
	print dir(public_globals.FileNameWidget)
	FileName=public_globals.FileNameWidget.get()
	
	result = tkMessageBox.askquestion("Save sites list", "Are You Sure you want to save the file " + FileName + " and overwrite it?", icon='warning')
	if result == 'yes':
		print "Saving..."
		file_ = open(FileName, 'w')
		file_.write(json_string)
		file_.close()
	else:
		print "I'm Not Saving Yet.."	
	
def callback_load():
	FileName_TMP = tkFileDialog.askopenfile(mode='w')
	if not FileName_TMP==None: #filename will be None when no file is selected	
		print FileName_TMP.name
		file = open(FileName_TMP.name, 'r')
		input_data=file.read()
		file.close()
		print input_data
		#delete all the UI for the previeus entries
		#for w in gridaray:
			#w.PasswordWidget.destroy()
			#w.PasswordLabel.destroy()
			#w.SiteWidget.destroy()
			#w.SiteLabel.destroy()
			#w.DeleteButton.destroy()
		#gridaray=[]
		try:
			parsed_json = json.loads(input_data)
		except: # catch *all* exceptions
			e = sys.exc_info()[0]
			tkMessageBox.showinfo("Error!", "Error: %s, if this error is value error, you are either opening an empty file or an invalid file" % e)
		PasswordLength = parsed_json['PasswordLength']
		SitesList = parsed_json['sites']
		for site in SitesList:
				print sire

class public_globals():
	FileNameWidget=None
def callback_master_password_ok():
	MasterPassword = e.get()
	random.seed(MasterPassword)
	l.destroy()
	e.destroy()
	b.destroy()
	MasterPasswordWidget = tk.Entry(root)
	MasterPasswordWidget.insert(0, MasterPassword)
	MasterPasswordLabel = tk.Label(root, text="Master Password:")
	PasswordLengthWidget = tk.Entry(root)
	PasswordLengthWidget.insert(0, PasswordLength)
	PasswordLengthLabel = tk.Label(root, text="Password Length:")
	AddPasswordButton = tk.Button(root, text="Add Password", command=callback_add_password_ok)
	SaveButton = tk.Button(root, text="Save site lables as file", command=callback_save)
	LoadButton = tk.Button(root, text="Load site labels from file", command=callback_load)
	public_globals.FileNameWidget = tk.Entry(root)
	public_globals.FileNameWidget.insert(0, FileName)
	FileNameLabel = tk.Label(root, text="File Name:")
	MasterPasswordLabel.grid(row=0,column=0)
	MasterPasswordWidget.grid(row=0,column=1)
	PasswordLengthLabel.grid(row=0,column=2)
	PasswordLengthWidget.grid(row=0,column=3)
	AddPasswordButton.grid(row=1,  column=0)
	SaveButton.grid(row=1,         column=1)
	LoadButton.grid(row=1,         column=2)
	FileNameLabel.grid(row=1,      column=3)
	public_globals.FileNameWidget.grid(row=1,     column=4)
	
e = tk.Entry(root)
l = tk.Label(root, text="Enter your master password:")
b = tk.Button(root, text="OK", command=callback_master_password_ok)
l.grid(row=0,column=0)
e.grid(row=1,column=0)
b.grid(row=2,column=0)
root.mainloop()
