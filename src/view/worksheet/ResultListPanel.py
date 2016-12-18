
import wx
import wx.dataview as dv
from wx import ListCtrl
import os

#----------------------------------------------------------------------

# This model class provides the data to the view when it is asked for.
# Since it is a list-only model (no hierachical data) then it is able
# to be referenced by row rather than by item object, so in this way
# it is easier to comprehend and use than other model types.  In this
# example we also provide a Compare function to assist with sorting of
# items in our model.  Notice that the data items in the data model
# object don't ever change position due to a sort or column
# reordering.  The view manages all of that and maps view rows and
# columns to the model's rows and columns as needed.
#
# For this example our data is stored in a simple list of lists.  In
# real life you can use whatever you want or need to hold your data.
ID_run=wx.NewId()
class ResultModel(dv.PyDataViewIndexListModel):
    def __init__(self, data):
        dv.PyDataViewIndexListModel.__init__(self, len(data))
        self.data = data

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        return "string"

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        return self.data[row][col]

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        print("SetValue: (%d,%d) %s\n" % (row, col, value))
        self.data[row][col] = value

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return len(self.data[0])

    # Report the number of rows in the model
    def GetCount(self):
        #print('GetCount')
        return len(self.data)
    
    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        ##print('GetAttrByRow: (%d, %d)' % (row, col))
        if col == 3:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0:
            return cmp(int(self.data[row1][col]), int(self.data[row2][col]))
        else:
            return cmp(self.data[row1][col], self.data[row2][col])

        
    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)
        
        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)
            
            
    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()

        
            
class ResultPanel(wx.Panel):
    def __init__(self, parent,model=None, data=None):
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )
        
        # Create an instance of our simple model...
        if model is None:
            self.model = ResultModel(data)
        else:
            self.model = model            

        # ...and associate it with the dataview control.  Models can
        # be shared between multiple DataViewCtrls, so this does not
        # assign ownership like many things in wx do.  There is some
        # internal reference counting happening so you don't really
        # need to hold a reference to it either, but we do for this
        # example so we can fiddle with the model from the widget
        # inspector or whatever.
        self.dvc.AssociateModel(self.model)

        # Now we create some columns.  The second parameter is the
        # column number within the model that the DataViewColumn will
        # fetch the data from.  This means that you can have views
        # using the same model that show different columns of data, or
        # that they can be in a different order than in the model.
        self.dvc.AppendTextColumn("Artist",  1, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Title",   2, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Genre",   3, width=80,  mode=dv.DATAVIEW_CELL_EDITABLE)

        # There are Prepend methods too, and also convenience methods
        # for other data types but we are only using strings in this
        # example.  You can also create a DataViewColumn object
        # yourself and then just use AppendColumn or PrependColumn.
        c0 = self.dvc.PrependTextColumn("Id", 0, width=40)

        # The DataViewColumn object is returned from the Append and
        # Prepend methods, and we can modify some of it's properties
        # like this.
        c0.Alignment = wx.ALIGN_RIGHT
        c0.Renderer.Alignment = wx.ALIGN_RIGHT
        c0.MinWidth = 40

        # Through the magic of Python we can also access the columns
        # as a list via the Columns property.  Here we'll mark them
        # all as sortable and reorderable.
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        # Let's change our minds and not let the first col be moved.
        c0.Reorderable = False

        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL) 
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)
        
        # Add some buttons to help out with the tests
        b1 = wx.Button(self, label="New View", name="newView")
        self.Bind(wx.EVT_BUTTON, self.OnNewView, b1)
        b2 = wx.Button(self, label="Add Row")
        self.Bind(wx.EVT_BUTTON, self.OnAddRow, b2)
        b3 = wx.Button(self, label="Delete Row(s)")
        self.Bind(wx.EVT_BUTTON, self.OnDeleteRows, b3)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        btnbox.Add(b1, 0, wx.LEFT|wx.RIGHT, 5)
        btnbox.Add(b2, 0, wx.LEFT|wx.RIGHT, 5)
        btnbox.Add(b3, 0, wx.LEFT|wx.RIGHT, 5)
        
        
        self.Sizer.Add(btnbox, 0, wx.TOP|wx.BOTTOM, 5)
        self.Sizer.Add(self.constructWorksheetToolBar(), 0, wx.TOP|wx.BOTTOM, 5)

        # Bind some events so we can see what the DVC sends us
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.OnEditingDone, self.dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self.dvc)
        


    def constructWorksheetToolBar(self):
        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(48, 48))
        
        if "worksheet"==os.path.split(os.getcwd())[-1:][0]:
            playImage=wx.Bitmap(os.path.join("..","..", "images", "play.png"))
        elif "view"==os.path.split(os.getcwd())[-1:][0]:
            playImage=wx.Bitmap(os.path.join("..", "images", "play.png"))
        
        tb1.AddLabelTool(id=ID_run, label="Run", shortHelp="run single line ", bitmap=playImage)
        tb1.AddSeparator()
        
#         tb1.AddLabelTool(id=ID_openConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
#         tb1.AddLabelTool(id=ID_newConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
        tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        return tb1 
    def OnNewView(self, evt):
        f = wx.Frame(None, title="New view, shared model", size=(600,400))
        ResultPanel(f, self.log, self.model)
        b = f.FindWindowByName("newView")
        b.Disable()
        f.Show()


    def OnDeleteRows(self, evt):
        # Remove the selected row(s) from the model. The model will take care
        # of notifying the view (and any other observers) that the change has
        # happened.
        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]
        self.model.DeleteRows(rows)

        
    def OnAddRow(self, evt):
        # Add some bogus data to a new row in the model's data
        id = len(self.model.data) + 1
        value = [str(id),
                 'new artist %d' % id,
                 'new title %d' % id,
                 'genre %d' % id]
        self.model.AddRow(value)
                

    def OnEditingDone(self, evt):
        print("OnEditingDone\n")

    def OnValueChanged(self, evt):
        print("OnValueChanged\n")

        
#----------------------------------------------------------------------

# def runTest(frame, nb, log):
#     # Get the data from the ListCtrl sample to play with, converting it
#     # from a dictionary to a list of lists, including the dictionary key
#     # as the first element of each sublist.
#     import ListCtrl
#     musicdata = ListCtrl.musicdata.items()
#     musicdata.sort()
#     musicdata = [[str(k)] + list(v) for k,v in musicdata]
# 
#     win = TestPanel(nb, log, data=musicdata)
#     return win




#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    
    
    # Get the data from the ListCtrl sample to play with, converting it
    # from a dictionary to a list of lists, including the dictionary key
    # as the first element of each sublist.
    musicdata = {
    1 : ("Bad English", "The Price Of Love", "Rock"),
    2 : ("DNA featuring Suzanne Vega", "Tom's Diner", "Rock"),
    3 : ("George Michael", "Praying For Time", "Rock"),
    4 : ("Gloria Estefan", "Here We Are", "Rock"),
    5 : ("Linda Ronstadt", "Don't Know Much", "Rock"),
    6 : ("Michael Bolton", "How Am I Supposed To Live Without You", "Blues"),
    7 : ("Paul Young", "Oh Girl", "Rock"),
    8 : ("Paula Abdul", "Opposites Attract", "Rock"),
    9 : ("Richard Marx", "Should've Known Better", "Rock"),
    10: ("Rod Stewart", "Forever Young", "Rock"),
    11: ("Roxette", "Dangerous", "Rock"),
    12: ("Sheena Easton", "The Lover In Me", "Rock"),
    13: ("Sinead O'Connor", "Nothing Compares 2 U", "Rock"),
    14: ("Stevie B.", "Because I Love You", "Rock"),
    15: ("Taylor Dayne", "Love Will Lead You Back", "Rock"),
    16: ("The Bangles", "Eternal Flame", "Rock"),
    17: ("Wilson Phillips", "Release Me", "Rock"),
    18: ("Billy Joel", "Blonde Over Blue", "Rock"),
    19: ("Billy Joel", "Famous Last Words", "Rock"),
    20: ("Janet Jackson", "State Of The World", "Rock"),
    21: ("Janet Jackson", "The Knowledge", "Rock"),
    22: ("Spyro Gyra", "End of Romanticism", "Jazz"),
    23: ("Spyro Gyra", "Heliopolis", "Jazz"),
    24: ("Spyro Gyra", "Jubilee", "Jazz"),
    25: ("Spyro Gyra", "Little Linda", "Jazz"),
    26: ("Spyro Gyra", "Morning Dance", "Jazz"),
    27: ("Spyro Gyra", "Song for Lorraine", "Jazz"),
    28: ("Yes", "Owner Of A Lonely Heart", "Rock"),
    29: ("Yes", "Rhythm Of Love", "Rock"),
    30: ("Billy Joel", "Lullabye (Goodnight, My Angel)", "Rock"),
    31: ("Billy Joel", "The River Of Dreams", "Rock"),
    32: ("Billy Joel", "Two Thousand Years", "Rock"),
    33: ("Janet Jackson", "Alright", "Rock"),
    34: ("Janet Jackson", "Black Cat", "Rock"),
    35: ("Janet Jackson", "Come Back To Me", "Rock"),
    36: ("Janet Jackson", "Escapade", "Rock"),
    37: ("Janet Jackson", "Love Will Never Do (Without You)", "Rock"),
    38: ("Janet Jackson", "Miss You Much", "Rock"),
    39: ("Janet Jackson", "Rhythm Nation", "Rock"),
    40: ("Cusco", "Dream Catcher", "New Age"),
    41: ("Cusco", "Geronimos Laughter", "New Age"),
    42: ("Cusco", "Ghost Dance", "New Age"),
    43: ("Blue Man Group", "Drumbone", "New Age"),
    44: ("Blue Man Group", "Endless Column", "New Age"),
    45: ("Blue Man Group", "Klein Mandelbrot", "New Age"),
    46: ("Kenny G", "Silhouette", "Jazz"),
    47: ("Sade", "Smooth Operator", "Jazz"),
    48: ("David Arkenstone", "Papillon (On The Wings Of The Butterfly)", "New Age"),
    49: ("David Arkenstone", "Stepping Stars", "New Age"),
    50: ("David Arkenstone", "Carnation Lily Lily Rose", "New Age"),
    51: ("David Lanz", "Behind The Waterfall", "New Age"),
    52: ("David Lanz", "Cristofori's Dream", "New Age"),
    53: ("David Lanz", "Heartsounds", "New Age"),
    54: ("David Lanz", "Leaves on the Seine", "New Age"),
    }
    musicdata = musicdata.items()
    musicdata.sort()
    musicdata = [[str(k)] + list(v) for k,v in musicdata]
    panel = ResultPanel(frame, data=musicdata)
    frame.Show()
    app.MainLoop()

