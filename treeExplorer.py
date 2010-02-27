import wx, win32gui
from pyHook.HookManager import HookManager
import AA, Watcher

ID_INFO_LIST = wx.NewId()
ID_AA_TREE = wx.NewId()
ID_FOCUS_BUTTON = wx.NewId()
ID_SELECT_BUTTON = wx.NewId()
ID_TRIGGER_BUTTON = wx.NewId()

class AAFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, 'Tree Explorer', size=wx.Size(500,500),
                      pos=wx.Point(0,0))

    # create the hook manager
    self.hm = HookManager()
    self.hm.KeyDown = self.OnBuildTree
    self.hm.HookKeyboard()
    self.last = None

    # create the tree in the first split
    spl1 = wx.SplitterWindow(self, -1)
    self.tree = wx.TreeCtrl(spl1, ID_AA_TREE)
    # create a info window and a button panel
    spl2 = wx.SplitterWindow(spl1,-1)
    self.info = wx.TextCtrl(spl2, ID_INFO_LIST, style=wx.TE_RICH2|wx.TE_LINEWRAP|wx.TE_MULTILINE)
    # create a button panel
    panel = wx.Panel(spl2, -1)
    sizer = wx.BoxSizer(wx.VERTICAL)
    b = wx.Button(panel, ID_FOCUS_BUTTON, '&Focus')
    sizer.Add(b)
    b = wx.Button(panel, ID_TRIGGER_BUTTON, '&Do default')
    sizer.Add(b)
    b = wx.Button(panel, ID_SELECT_BUTTON, '&Select')
    sizer.Add(b)
    self.select_text = wx.TextCtrl(panel, -1)
    sizer.Add(self.select_text)    
    panel.SetSizer(sizer)
    # configure the splitters
    spl1.SplitVertically(self.tree, spl2, 300)
    spl2.SplitHorizontally(self.info, panel, 300)
    spl2.SetMinimumPaneSize(10)
    spl1.SetMinimumPaneSize(10)
    
    # reference to a deferred result for events
    self.result = None
    self.watcher = None

    wx.EVT_CLOSE(self, self.OnClose)
    wx.EVT_BUTTON(self, ID_FOCUS_BUTTON, self.OnFocus)
    wx.EVT_BUTTON(self, ID_SELECT_BUTTON, self.OnSelect)
    wx.EVT_BUTTON(self, ID_TRIGGER_BUTTON, self.OnDoDefault)
    wx.EVT_TREE_SEL_CHANGED(self, ID_AA_TREE, self.OnShowInfo)

  def OnClose(self, event):
    del self.hm
    self.Destroy()

  def OnBuildTree(self, event):
    if event.Key == 'Rcontrol':
      # get the mouse position at the time of the event
      pt = win32gui.GetCursorPos()
      # schedule a call to find the root and build the tree
      wx.CallAfter(self.FindRoot, pt)
    elif event.Key == 'Lcontrol':
      wx.CallAfter(self.OnShowInfo, None)

  def FindRoot(self, pt):
    # get the accessible object from this point
    ao = AA.AccessibleObjectFromPoint(pt)

    # drill up until we find the topmost parent
    try:
      if ao.Name != 'Desktop':
        parent = ao.Parent
        while parent.Name != 'Desktop':
          ao = parent
          parent = ao.Parent
    except:
      self.CreateTree(ao)

    # build the tree starting at the top of this window
    self.CreateTree(ao)

  def CreateTree(self, ao):
    #reset the tree
    self.tree.DeleteAllItems()

    # add the root
    node = self.tree.AddRoot(str(ao.Name))
    self.tree.SetPyData(node, ao)

    # recursively add all other nodes
    for child in ao.Children:
      self.AddNode(child, node)

    # show the root
    self.tree.Expand(node)

  def AddNode(self, ao, parent):
    #if ao.State() & 32768: return
    #if ao.Role in [1,2,3,4]: return
    # append this node to its parent
    node = self.tree.AppendItem(parent, str(ao.RoleText))
    self.tree.SetPyData(node, ao)

    # add all its children
    for child in ao.Children:
      self.AddNode(child, node)

    self.tree.Expand(node)

  def OnFocus(self, event):
    node = self.tree.GetSelection()
    ao = self.tree.GetPyData(node)
    ao.SetFocus()

  def OnSelect(self, event):
    node = self.tree.GetSelection()
    ao = self.tree.GetPyData(node)
    ao.SetFocus()
    ao.Select(int(self.select_text.GetValue()))

  def OnDoDefault(self, event):
    node = self.tree.GetSelection()
    ao = self.tree.GetPyData(node)
    ao.DoDefaultAction()

  def OnShowInfo(self, event=None):  
    # get the accessible object for this node
    if event is not None:
      node = event.GetItem()
      self.last = node
    else:
      node = self.last
    ao = self.tree.GetPyData(node)
    
    # show the accessible info
    self.info.Clear()
    self.info.AppendText(str(ao.Name)+'\n')
    try: self.info.AppendText(str(ao.Value)+'\n')
    except: self.info.AppendText('error\n')
    self.info.AppendText(str(ao.Role) + ':' + str(ao.RoleText)+'\n')
    self.info.AppendText(str(ao.State) + ':' + str(ao.StateText)+'\n')
    self.info.AppendText(str(ao.ChildCount)+'\n')
    self.info.AppendText(str(ao.Description)+'\n')
    self.info.AppendText(str(ao.Window)+'\n')
    self.info.AppendText(ao.ClassName+'\n')
    # create the xpath to this node
    #p = AA.Path.Build(ao)
    #self.info.AppendText(p+'\n')
    #self.info.AppendText(str([child.Name for child in ao.Selection])+'\n')

if __name__ == '__main__':
  app = wx.PySimpleApp(0)
  frame = AAFrame()
  app.SetTopWindow(frame)
  frame.Show(True)
  app.MainLoop()