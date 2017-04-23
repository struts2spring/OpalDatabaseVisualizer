#used some code from the WxPython wiki:
#-1.4 Recursively building a list into a wxTreeCtrl (yet another sample) by Rob
#-1.5 Simple Drag and Drop by Titus
#-TraversingwxTree

#tested on wxPython 2.5.4 and Python 2.4, under Windows and Linux

import  wx

#---------------------------------------------------------------------------

class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style, log):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log

    def Traverse(self, func, startNode): 
        """Apply 'func' to each node in a branch, beginning with 'startNode'. """
        def TraverseAux(node, depth, func): 
            nc = self.GetChildrenCount(node, 0) 
            child, cookie = self.GetFirstChild(node)
            # In wxPython 2.5.4, GetFirstChild only takes 1 argument
            for i in xrange(nc): 
                func(child, depth)                
                TraverseAux(child, depth + 1, func)
                child, cookie = self.GetNextChild(node, cookie)
        func(startNode, 0) 
        TraverseAux(startNode, 1, func) 

    def ItemIsChildOf(self, item1, item2):
        ''' Tests if item1 is a child of item2, using the Traverse function '''
        self.result = False
        def test_func(node, depth):
            if node == item1:
                self.result = True
                
        self.Traverse(test_func, item2)
        return self.result

    def SaveItemsToList(self, startnode):
        ''' Generates a python object representation of the tree (or a branch of it),
            composed of a list of dictionaries with the following key/values:
            label:      the text that the tree item had
            data:       the node's data, returned from GetItemPyData(node)
            children:   a list containing the node's children (one of these dictionaries for each)
        '''
        global list
        list = []
        
        def save_func(node, depth):
            tmplist = list
            for x in range(depth):
                if type(tmplist[-1]) is not dict:
                    tmplist.append({})
                tmplist = tmplist[-1].setdefault('children', [])

            item = {}
            item['label'] = self.GetItemText(node)
            item['data'] = self.GetItemPyData(node)
            item['icon-normal'] = self.GetItemImage(node, wx.TreeItemIcon_Normal)
            item['icon-selected'] = self.GetItemImage(node, wx.TreeItemIcon_Selected)
            item['icon-expanded'] = self.GetItemImage(node, wx.TreeItemIcon_Expanded)
            item['icon-selectedexpanded'] = self.GetItemImage(node, wx.TreeItemIcon_SelectedExpanded)
           
            tmplist.append(item)
            
        self.Traverse(save_func, startnode)
        return list
        
    def InsertItemsFromList(self, itemlist, parent, insertafter=None, appendafter=False):
        ''' Takes a list, 'itemslist', generated by SaveItemsToList, and inserts
            it in to the tree. The items are inserted as children of the
            treeitem given by 'parent', and if 'insertafter' is specified, they
            are inserted directly after that treeitem. Otherwise, they are put at
            the beginning.
            
            If 'appendafter' is True, each item is appended. Otherwise it is prepended.
            In the case of children, you want to append them to keep them in the same order.
            However, to put an item at the start of a branch that has children, you need to
            use prepend. (This will need modification for multiple inserts. Probably reverse
            the list.)

            Returns a list of the newly inserted treeitems, so they can be
            selected, etc..'''
        newitems = []
        for item in itemlist:
            if insertafter:
                node = self.InsertItem(parent, insertafter, item['label'])
            elif appendafter:
                node = self.AppendItem(parent, item['label'])
            else:
                node = self.PrependItem(parent, item['label'])
            self.SetItemPyData(node, item['data'])
            self.SetItemImage(node, item['icon-normal'], wx.TreeItemIcon_Normal)
            self.SetItemImage(node, item['icon-selected'], wx.TreeItemIcon_Selected)
            self.SetItemImage(node, item['icon-expanded'], wx.TreeItemIcon_Expanded)
            self.SetItemImage(node, item['icon-selectedexpanded'], wx.TreeItemIcon_SelectedExpanded)

            newitems.append(node)
            if 'children' in item:
                self.InsertItemsFromList(item['children'], node, appendafter=True)
        return newitems
    
def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1


#---------------------------------------------------------------------------

class TestTreeCtrlPanel(wx.Panel):
    def __init__(self, parent, log):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.log = log
        tID = wx.NewId()

        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, wx.DefaultSize,
                                    wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS, self.log)
        # Example needs some more work to use wx.TR_MULTIPLE

        isize = (16,16)
        il = wx.ImageList(isize[0], isize[1])
        fldridx   = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,  wx.ART_OTHER, isize))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER,isize))
        fileidx   = il.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER,isize))

        self.tree.SetImageList(il)
        self.il = il

        self.root = self.tree.AddRoot("The Root Item")
        self.tree.SetPyData(self.root, {"type":"container"})
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)

        for x in range(15):
            child = self.tree.AppendItem(self.root, "Item %d" % x)
            self.tree.SetPyData(child, {"type":"container"})
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
            for y in range(5):
                last = self.tree.AppendItem(child, "item %d-%s" % (x,chr(ord("a")+y)))
                self.tree.SetPyData(last,{"type":"container"})
                self.tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, fldropenidx,wx.TreeItemIcon_Expanded)
                for z in range(5):
                    item = self.tree.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                    self.tree.SetPyData(item, {"type":"item"})
                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Selected)

        self.tree.Expand(self.root)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        # These go at the end of __init__
        self.tree.Bind(wx.EVT_TREE_BEGIN_RDRAG, self.OnBeginRightDrag)
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginLeftDrag)
        self.tree.Bind(wx.EVT_TREE_END_DRAG, self.OnEndDrag)

    def OnBeginLeftDrag(self, event):
        '''Allow drag-and-drop for leaf nodes.'''
        self.log.WriteText("OnBeginDrag")
        event.Allow()
        self.dragType = "left button"
        self.dragItem = event.GetItem()

    def OnBeginRightDrag(self, event):
        '''Allow drag-and-drop for leaf nodes.'''
        self.log.WriteText("OnBeginDrag")
        event.Allow()
        self.dragType = "right button"
        self.dragItem = event.GetItem()

    def OnEndDrag(self, event):
        print "OnEndDrag"
        
        # If we dropped somewhere that isn't on top of an item, ignore the event
        if event.GetItem().IsOk():
            target = event.GetItem()
        else:
            return

        # Make sure this member exists.
        try:
            source = self.dragItem
        except:
            return

        # Prevent the user from dropping an item inside of itself
        if self.tree.ItemIsChildOf(target, source):
            print "the tree item can not be moved in to itself! "
            self.tree.Unselect()
            return
        
        # Get the target's parent's ID
        targetparent = self.tree.GetItemParent(target)
        if not targetparent.IsOk():
            targetparent = self.tree.GetRootItem()
       
        # One of the following methods of inserting will be called...   
        def MoveHere(event):
            # Save + delete the source
            save = self.tree.SaveItemsToList(source)
            self.tree.Delete(source)
            newitems = self.tree.InsertItemsFromList(save, targetparent, target)
            #self.tree.UnselectAll()
            for item in newitems:
                self.tree.SelectItem(item)
            
        def InsertInToThisGroup(event):
            # Save + delete the source
            save = self.tree.SaveItemsToList(source)
            self.tree.Delete(source)
            newitems = self.tree.InsertItemsFromList(save, target)
            #self.tree.UnselectAll()
            for item in newitems:
                self.tree.SelectItem(item)
        #---------------------------------------
            
        if self.tree.GetPyData(target)["type"] == "container" and self.dragType == "right button":
            menu = wx.Menu()
            menu.Append(101, "Move to after this group", "")
            menu.Append(102, "Insert into this group", "")
            menu.UpdateUI()
            menu.Bind(wx.EVT_MENU, MoveHere, id=101)
            menu.Bind(wx.EVT_MENU, InsertInToThisGroup,id=102)
            self.PopupMenu(menu)
        else:
            if self.tree.IsExpanded(target):
               InsertInToThisGroup(None)
            else:
               MoveHere(None)

    def OnRightUp(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        self.log.WriteText("OnRightUp: %s (manually starting label edit)\n" % self.tree.GetItemText(item))
        self.tree.EditLabel(item)

    def OnLeftDown(self, event):
        print "control key is", event.m_controlDown

        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        self.tree.SelectItem(item)
        event.Skip()

    def OnRightDown(self, event):
        print "control key is", event.m_controlDown
        
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        self.tree.SelectItem(item)
        event.Skip()

    def OnLeftDClick(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        self.log.WriteText("OnLeftDClick: %s\n" % self.tree.GetItemText(item))

        #expand/collapse toggle
        self.tree.Toggle(item)
        print "toggled ", item
        #event.Skip()

    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)


#---------------------------------------------------------------------------

class MyLog:
    def __init__(self):
        pass                    
    def WriteText(self, text):
        print text

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        log = MyLog()
        pnl = TestTreeCtrlPanel(self, log)
                  
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show(1)
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
