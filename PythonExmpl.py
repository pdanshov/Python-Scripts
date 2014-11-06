
########################################
# 1 - Effect changes on record change
########################################
def RecordChanged(o, e):
	# Check the customer status and then change the background color
	if main.CurrentEntity.Status == 0:
		main.lkpCustId.BackColor = Color.LightGreen
	else:
		main.lkpCustId.BackColor = Color.Blue
		
		
main.BindingSource.PositionChanged += RecordChanged # if record changed, call RecordChanged


### http://76.164.58.39/viewtopic.php?t=8001&highlight=python+debug
### http://76.164.58.39/viewtopic.php?t=7962&highlight=python+debug
### http://76.164.58.39/viewtopic.php?t=7820&highlight=python+debug
"""
I had asked Traverse support this question and was guided to this forum to get my question answered.

I have been going through some of the training videos and attempting to replicate what I see in them. One of the simpler ones was the example demonstrating the use of a python script to change the color of the CustomerID box green for an active customer or red for an inactive one. The event the script was listening to was for when a record changed thus someone had to switch records and back to get the color to update properly.

My question is simply what event do I listen to for when the Status changes?

Here is the script as it exists in the video:

[code]def RecordChanged(o, e):
if main.CurrentEntity.Status == 0:
main.lkpCustId.BackColor= Color.LightGreen
else:
main.lkpCustId.BackColor = Color.Pink

main.BindingSource.PositionChanged += RecordChanged

main.Status.Changed += RecordChanged[/code]

I will ask one more related question if you have the time to answer it. In Design Studio when I try to look at the property window when I have a control selected I do not see anything such as the control's name. Is this a bug, still in development, or am I using the tool wrong?

Thanks for your


You could try handling main.CurrentEntity.PropertyChanged event. This event gets trigerred for change in every field, so you have to isolate your field by checking for e.PropertyName.

For the 2nd part of your question, that feature is under dev. 
"""

###################################
# 2 - Effect changes immediately
###################################
def RecordChanged(o, e):
  ChangeStatusBackColor()

def CustomerPropertyChanged(o, e):
  if e.PropertyName == "Status":
    ChangeStatusBackColor()

def CustomerCurrentChanged(o, e):
  if main.CurrentEntity != None:
    main.CurrentEntity.PropertyChanged -= CustomerPropertyChanged
    main.CurrentEntity.PropertyChanged += CustomerPropertyChanged
  
def ChangeStatusBackColor():
  if main.CurrentEntity.Status == 0:
    main.GetControls()["lkpCustId"].BackColor = Color.LightGreen
  else:
    main.GetControls()["lkpCustId"].BackColor = Color.Blue

main.BindingSource.PositionChanged += RecordChanged			# if record changed, call RecordChanged
main.BindingSource.CurrentChanged += CustomerCurrentChanged	# if field changed, call CustomerCurrentChanged

################################
# 3 - Require data in a field
################################
def Req (o, e):
   if main.CurrentEntity.CustomValueCollection.Contains("Customer Type"):
        v=main.CurrentEntity.CustomValueCollection["Customer Type"].Value   
        if (v == ""):
           e.Cancel=True
   else:
        MessageBox.Show("Value required in Customer Type field.")
        e.Cancel=True

main.SavingRow += Req # no effect until record is saved

############################################
#####	4 - Validate PO
############################################
def HeaderSaved(o, e):
  if ValidatePO():
    e.Cancel = True

def HeaderPropertyChanged(o, e):
  if (e.PropertyName == "CustPONum") or (e.PropertyName == "SoldToId"):
    ValidatePO()

def ValidatePO():
  header = main.ViewComponents.HeaderControl.CurrentEntity
  if header.SoldToCustomer.CustomValueCollection.Contains("PO Required"):
    po = header.SoldToCustomer.CustomValueCollection["PO Required"].Value.ToString()
    if header.CustPONum == None or header.CustPONum == "":
      if po == "True":
        TravMessageBox.Show(None,"Purchase Order required.")
        return 1

def HeaderCurrentChanged(o, e):
  if main.ViewComponents.HeaderControl.CurrentEntity != None:
    main.ViewComponents.HeaderControl.CurrentEntity.PropertyChanged -= HeaderPropertyChanged
    main.ViewComponents.HeaderControl.CurrentEntity.PropertyChanged += HeaderPropertyChanged

main.ViewComponents.HeaderControl.SavingRow+=HeaderSaved
main.ViewComponents.HeaderControl.BindingSource.CurrentChanged+=HeaderCurrentChanged



























