
"""
Mainetti Lotted Validation check
Peter Danshov 08.29.2014 Fri 1500 EST
pdanshv@gmail.com
To discover the available Methods/Fields/Properties, open the relevant .dll
in Visual Studio Object Browser, and RedGate .NET Reflector/Decompiler.
In this case the .dll's are TRAVERSE.Business.Inventory and TRAVERSE.Client.Inventory.
The modules are called Item, and ItemControl, respectively.
chkLotted and ItemId are fields found in the Client dll,
while IsLotted is a method found in Business dll.
Paste this code into the script section of the IN Item screen in
Traverse Design Studio, then compile, save, and copy/move to Traverse directory.
Path to this file should be:
S:\Version Control\Mainetti\scripts\IN Item
"""

def HeaderSaved(o, e):	# Define HeaderSaved function/method
	if ValidatePO():	# Step through ValidatePO and if true, cancel event (save or change record)
		e.Cancel = True

def HeaderPropertyChanged(o, e):	# Define Method/Function
	if (e.PropertyName == "chkLotted") or (e.PropertyName == "ItemId"):
		ValidatePO()	# If the field that fired the event is ItemId or chkLotted step through ValidatePO

def ValidatePO():	# Define Method/Function
	header = main.CurrentEntity	# Create variable & store current record
	if header.IsLotted == True:	# Lotted is a bool, check for True value
		#TravMessageBox.Show(None,"Lotted must not be ticked.")
		MessageBox.Show("'Lotted' must not be ticked.", "Alert")
		return 1

def HeaderCurrentChanged(o, e):
	if main.CurrentEntity != None:	# check for loaded record, if the record is changed up/down, call HeaderPropertyChanged method
		main.CurrentEntity.PropertyChanged -= HeaderPropertyChanged
		main.CurrentEntity.PropertyChanged += HeaderPropertyChanged

main.SavingRow += HeaderSaved	# if record is saved, call HeaderSaved
main.BindingSource.CurrentChanged += HeaderCurrentChanged	# if record is changed, call HeaderCurrentChanged
