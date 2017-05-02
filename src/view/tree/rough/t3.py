import wx
import keyword
import string

class TreeFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='TreeCtrl example')

        tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                                wx.TR_FULL_ROW_HIGHLIGHT | \
                                                wx.TR_EDIT_LABELS)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, tree_ctrl)
        self.tree = tree_ctrl

        # Add the tree root
        root = tree_ctrl.AddRoot('Python keywords')

        letters = []
        
        for kwd in keyword.kwlist:
            first = kwd[0]
            if first not in letters:
                letters.append(first)

        for letter in letters:
            item = tree_ctrl.AppendItem(root, letter)
            for kwd in keyword.kwlist:
                first = kwd[0]
                if first == letter:
                    sub_item = tree_ctrl.AppendItem(item, kwd)
                    
        #tree_ctrl.ExpandAll()
        self.Centre()
        
    #----------------------------------------------------------------------
    def OnSelChanged(self, event):
        """"""
        item = event.GetItem()
        if item:
            self.tree.Expand(item)


if __name__ == '__main__':
    app = wx.App(0)
    frame = TreeFrame()
    frame.Show()
    app.MainLoop()