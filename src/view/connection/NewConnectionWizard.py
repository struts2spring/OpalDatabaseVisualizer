'''
Created on 04-Feb-2017

@author: vijay
'''

import wx
import wx.wizard
from src.view.connection.DatabaseNavigation import DatabaseNavigationTree
import os
from src.sqlite_executer.ConnectExecuteSqlite import ManageSqliteDatabase,\
    SQLExecuter
from sqlite3 import OperationalError
import logging

logger = logging.getLogger('extensive')

class TitledPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        titleText.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0,
                wx.EXPAND | wx.ALL, 5)
        
class SelectDatabaseNamePage(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title='Select new connection type'):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        
        
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        titleText.SetFont(bf)
        ####################################################################
        '''
        Header section
        '''        
        self.tree = DatabaseNavigationTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter database name")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.RecreateTree()
        
        ####################################################################        
        
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        try:
            for category, items in self._treeList[1]:
                self.searchItems[category] = []
                for childItem in items:
    #                 if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)
        except Exception as e:
            logger.error(e, exc_info=True)
        wx.EndBusyCursor()
        self.RecreateTree()   
    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
#         searchMenu = self.filter.GetMenu().GetMenuItems()
#         fullSearch = searchMenu[1].IsChecked()
        fullSearch = False   
            
        if evt:
            if fullSearch:
                # Do not`scan all the demo files for every char
                # the user input, use wx.EVT_TEXT_ENTER instead
                return

        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
                    
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Connections")
        self.tree.SetItemImage(self.root, 0)
        self.tree.SetItemPyData(self.root, 0)

        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The native treectrl on MSW has a bug where it doesn't draw
        # all of the text for an item if the font is larger than the
        # default.  It seems to be clipping the item's label as if it
        # was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo:
            treeFont.SetPointSize(treeFont.GetPointSize() + 2)
            
        treeFont.SetWeight(wx.BOLD)
        catFont.SetWeight(wx.BOLD)
#         self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        

        databaseLeaf = self.tree.AppendItem(self.root, 'SQLite', image=16)

class ConncectionSettings(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title='define title'):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        
        
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        titleText.SetFont(bf)    
        
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        #################################################################### 
        self.panel = wx.Panel(self, -1)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL) 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        connectionNameLabel = wx.StaticText(self.panel, -1, "Connection name :   ")
        self.connectionNameTextCtrl = wx.TextCtrl(self.panel, size=(300,23))
        hbox1.Add(connectionNameLabel) 
        hbox1.Add(self.connectionNameTextCtrl,0,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,1)
        
        import wx.lib.filebrowsebutton as brows
        self.markFile = brows.FileBrowseButton(self.panel,labelText="File path                  :",  fileMode=wx.OPEN, size=(400,30))

        vbox1.Add(hbox1)
        vbox1.Add(self.markFile)
        self.panel.SetSizer(vbox1) 
        self.sizer.Add(self.panel, 0, wx.ALL , 5)
        ####################################################################        
        
class CreateNewConncetionWixard():
    
    def __init__(self):
        pass
    def createWizard(self):
        wizard = wx.wizard.Wizard(None, -1, "Create new connection")
        page1 = SelectDatabaseNamePage(wizard, "Select new connection type")
        page2 = ConncectionSettings(wizard, "Connection settings")
#         page3 = TitledPage(wizard, "Page 3")
#         page4 = TitledPage(wizard, "Page 4")
#         page1.sizer.Add(wx.StaticText(page1, -1, "Testing the wizard"))
#         page4.sizer.Add(wx.StaticText(page4, -1, "This is the last page."))
        wx.wizard.WizardPageSimple_Chain(page1, page2)
#         wx.wizard.WizardPageSimple_Chain(page2, page3)
#         wx.wizard.WizardPageSimple_Chain(page3, page4)
        wizard.FitToPage(page1)
    
        if wizard.RunWizard(page1):
            logger.debug("Success")
            selectedItem=page1.tree.GetSelection()
            logger.debug(page1.tree.GetItemText(selectedItem))
            logger.debug("%s, %s",page2.connectionNameTextCtrl.GetValue(),page2.markFile.GetValue() )
            databasefile=page2.markFile.GetValue() 
            connectionName=page2.connectionNameTextCtrl.GetValue()
            self.createNewDatabase( connectionName=connectionName,databaseAbsolutePath=databasefile)
        wizard.Destroy()        
    
    def createNewDatabase(self, databaseAbsolutePath=None,connectionName=None):
        try:
            manageSqliteDatabase=ManageSqliteDatabase(databaseAbsolutePath=databaseAbsolutePath,connectionName=connectionName)
            manageSqliteDatabase.createTable()
            sqlExecuter=SQLExecuter()
            obj=sqlExecuter.getObject()
            if len(obj[1])==0:
                sqlExecuter.createOpalTables()
            sqlExecuter.addNewConnectionRow(databaseAbsolutePath, connectionName)
        except OperationalError as err:
            logger.error(err, exc_info=True)
if __name__ == "__main__":

    app = wx.App()
    CreateNewConncetionWixard().createWizard()
