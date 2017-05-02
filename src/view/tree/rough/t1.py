import wx

class TreeFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='TreeCtrl')
        tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                wx.TR_FULL_ROW_HIGHLIGHT | \
                                wx.TR_EDIT_LABELS)

        # NOTE: Bind callback which will be called when the button is clicked.
        button = wx.Button(self, -1, label='Add banana')
        button.Bind(wx.EVT_BUTTON, self.add_banana)

        # NOTE sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tree_ctrl, 1, wx.EXPAND|wx.ALL)
        sizer.Add(button, 0, wx.EXPAND|wx.ALL)
        self.SetSizer(sizer)


        # Add the tree root
        root = tree_ctrl.AddRoot('Food')
        tree_ctrl.AppendItem(root,'Fruit (3)')
        tree_ctrl.AppendItem(tree_ctrl.GetLastChild(root),'Apple (1)')
        tree_ctrl.AppendItem(tree_ctrl.GetLastChild(root),'Orange (2)')

        tree_ctrl.ExpandAll()
        self.Centre()

         # NOTE: Save tree_ctrl, root as attribute
         #       to make them available in add_banana method.
        self.tree_ctrl = tree_ctrl
        self.root = root

    # called when the button is clicked.
    def add_banana(self, evt):
        self.tree_ctrl.AppendItem(self.tree_ctrl.GetLastChild(self.root), 'Banana (3)')


if __name__ == '__main__':
    app = wx.App(0)
    frame = TreeFrame()
    frame.Show()
    app.MainLoop()