

result = MessageBox.Show("Set Req Ship Date on Lines?", "MessageBox Example")
if result == DialogResult.OK:
#test aaaaaaaaaaaaaa
#	TravMessageBox.Show(None, lineItem.ItemId)
	TravMessageBox.Show("Something", "One")
	#main.lkpItemId.BackColor = Color.LightGreen
	
if main.lkpItemId.BackColor == Color.Pink:
	MessageBox.Show("Body", "Title")

#LottedM = main.IsLotted()
#print LottedM
#print "%s" % (LottedM)
#MessageBox.Show("IsLotted = %s" % (LottedM), "Title")

header = main.CurrentEntity
#test = header.chkLotted.Value.ToString
# 'Item' entity has no attribute 'chkLotted'
#test = header.IsLotted.Value.ToString
# 'bool' object has no attribute 'Value'
test = header.IsLotted

MessageBox.Show("Header: %s" %(test), "Title")

if header.IsLotted == False:
	TravMessageBox.Show("Title", "Body")

#if main.chkLotted.Value == 0:
#if main.chkLotted != 0:
#if main.GetControls()["chkLotted"].Value == 0:
#if main.chkLotted:
	#MessageBox.Show("chkLotted = %s" % main.chkLotted, "Field Status")
#	MessageBox.Show("chkLotted = %s" % main.chkLotted, "Field Status")
	# print "If I add %d, %d, and %d I get %d." % (my_age, my_height, my_weight, my_age + my_height + my_weight)
	
#if main.CurrentEntity.CustomValueCollection.Contains("Item ID"):
#if main.CurrentEntity.CustomValueCollection.Contains("Ite&m ID"):
if main.CurrentEntity.CustomValueCollection.Contains("Color"):
#if main.CurrentEntity.CustomValueCollection.Contains("layoutControlItem1"):
	TravMessageBox.Show("Something", "Two")

def RecordChanged(o, e):

	if main.CurrentEntity.CustomValueCollection.Contains("Item ID"):
		TravMessageBox.Show("Something", lineItem.ItemId)

	result = MessageBox.Show("Set Req Ship Date on Lines?", "MessageBox Example")
	if result == DialogResult.OK:
		TravMessageBox.Show(None, lineItem.ItemId)
	
	# Check the customer status and then change the background color
	if main.CurrentEntity.ItemStatus == 0:
		main.lkpItemId.BackColor = Color.LightGreen
	else:
		main.lkpItemId.BackColor = Color.Blue
		
main.BindingSource.PositionChanged += RecordChanged # if record changed, call RecordChanged
