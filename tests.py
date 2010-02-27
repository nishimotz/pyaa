'''Unit tests for pyAA.'''
import unittest, os, time, pythoncom
import AA, Watcher, Path

# path to the list control in the explorer window
list_path = '/client[3]/window[3]/client[3]/window[0]/list[3]'
close_path = '/title bar[1]/push button[4]'

# time to sleep between pumping messages
WAIT = 1

class AccessibleObjectTests(unittest.TestCase):
  def onShow(self, result):
    # hang onto the window
    self.root = result
    # get the list box
    self.list = self.root.ChildFromPath(list_path)
    # indicate we're ready to test
    self.ready = True
    
  def onHide(self, result):
    # indicate the window is gone
    self.ready = False
  
  def setUp(self):
    self.ready = False
    # watch for the creation of a file explorer window
    w = Watcher.WindowWatcher()
    defer = w.NotifyOnOpen(ClassName='ExploreWClass')
    defer.AddCallback(self.onShow)
    # start an instance of windows file explorer
    os.startfile('explorer.exe')
    # sleep until the app is running
    while not self.ready:
      pythoncom.PumpWaitingMessages()      
      time.sleep(WAIT)
    
  def tearDown(self):
    # watch for the window death
    w = Watcher.WindowWatcher()
    defer = w.NotifyOnClose(self.root.Window)
    defer.AddCallback(self.onHide)
    # press the close button
    self.root.ChildFromPath(close_path).DoDefaultAction()
    # wait for the window to die
    while self.ready:
      pythoncom.PumpWaitingMessages()
      time.sleep(WAIT)
    
  def testNames(self):
    self.assertEqual(self.list.Name, None)
    self.assertEqual(self.list.ClassName, 'SysListView32')
    
  def testRole(self):
    self.assertEqual(self.list.Role, AA.Constants.ROLE_SYSTEM_LIST)
    self.assertEqual(self.list.RoleText, 'list')
    
  def testState(self):
    self.assert_(self.list.Children[0].State & AA.Constants.STATE_SYSTEM_SELECTABLE)
    self.assertEqual(self.list.Children[0].StateText, 'selectable+multiple selectable')
    
  def testChildren(self):
    self.assert_(isinstance(self.list.ChildCount, int))
    self.assert_(isinstance(self.list.Children, list))
    self.assertEqual(self.list.ChildCount, len(self.list.Children))
    
  def testParent(self):
    self.assertEqual(self.root.Parent.Name, 'Desktop')
    
  def testValues(self):
    self.assertEqual(self.list.Value, None)
    self.assertEqual(self.list.Description, None)
    self.assertEqual(self.list.Help, None)
    self.assertEqual(self.list.KeyboardShortcut, None)
    
  def testLocation(self):
    self.assert_(isinstance(self.root.Location, tuple))
    loc = self.list.Location
    ht = self.list.HitTest((loc[0], loc[1]))
    self.assertNotEqual(ht, None)
    self.assertEqual(self.list.Location, ht.Location)
    
  def testFocus(self):
    self.assertNotEqual(self.root.Focus, None)
    
  def testSelection(self):
    self.assertNotEqual(self.list.ChildCount, 0)
    self.list.Children[0].Select(AA.Constants.SELFLAG_TAKEFOCUS|AA.Constants.SELFLAG_TAKESELECTION)
    self.assertNotEqual(len(self.list.Selection), 0)
    self.assertEqual(self.list.Selection[0].Name, self.list.Children[0].Name)
    
  def testFind(self):
    c = self.root.FindOneChild(lambda x: x.Location == self.list.Location and
                                         x.Role == self.list.Role)
    self.assertEqual(c.Location, self.list.Location)
    c = self.root.FindAllChildren(lambda x: x.RoleText == 'list item')
    self.assertEqual(len(c), len([c for c in self.list.Children 
                                             if c.RoleText == 'list item']))
                                             
  def testNavigate(self):
    first = self.list.Navigate(AA.Constants.NAVDIR_FIRSTCHILD)
    self.assert_((first is None) or first.Name)
    last = self.list.Navigate(AA.Constants.NAVDIR_LASTCHILD)
    self.assert_((last is None) or last.Name)
    if first is not None:
      s1 = first.Navigate(AA.Constants.NAVDIR_NEXT)
      s2 = first.Navigate(AA.Constants.NAVDIR_DOWN)
      self.assert_((s1 is s2) or (s1.Name == s2.Name))
      try:
        first.Navigate(AA.Constants.NAVDIR_UP)
        self.assert_(False)
      except AA.Error:
        pass
      try:
        first.Navigate(AA.Constants.NAVDIR_PREVIOUS)
        self.assert_(False)
      except AA.Error:
        pass
    if last is not None:
      s1 = last.Navigate(AA.Constants.NAVDIR_PREVIOUS)
      s2 = last.Navigate(AA.Constants.NAVDIR_UP)
      self.assert_((s1 is s2) or (s1.Name == s2.Name))
      try:
        last.Navigate(AA.Constants.NAVDIR_DOWN)
        self.assert_(False)
      except AA.Error:
        pass
      try:
        last.Navigate(AA.Constants.NAVDIR_NEXT)
        self.assert_(False)
      except AA.Error:
        pass    
      
ao_suite = unittest.makeSuite(AccessibleObjectTests)

forward_path = '/client[3]/window[1]/client[3]/window[0]/client[3]/window[0]/tool bar[3]/push button[2]'
class PathTests(unittest.TestCase):
  def onShow(self, result):
    # hang onto the window
    self.root = result
    # indicate we're ready to test
    self.ready = True
    
  def onHide(self, result):
    # indicate the window is gone
    self.ready = False
  
  def setUp(self):
    self.ready = False
    # watch for the creation of a file explorer window
    w = Watcher.WindowWatcher()
    defer = w.NotifyOnOpen(ClassName='Outlook Express Browser Class')
    defer.AddCallback(self.onShow)
    # start an instance of windows file explorer
    os.startfile('msimn.exe')
    # sleep until the app is running
    while not self.ready:
      pythoncom.PumpWaitingMessages()      
      time.sleep(WAIT)
    
  def tearDown(self):
    # watch for the window death
    w = Watcher.WindowWatcher()
    defer = w.NotifyOnClose(self.root.Window)
    defer.AddCallback(self.onHide)
    # press the close button
    self.root.ChildFromPath(close_path).DoDefaultAction()
    # wait for the window to die
    while self.ready:
      pythoncom.PumpWaitingMessages()
      time.sleep(WAIT)
      
  def testPaths(self):
    import timeit
    
    t1 = timeit.default_timer()
    ao = Path.Parse(forward_path, self.root)
    t2 = timeit.default_timer()
    print t2-t1
    self.assert_(ao.Role == AA.Constants.ROLE_SYSTEM_PUSHBUTTON)   
    
path_suite = unittest.makeSuite(PathTests)

if __name__ == '__main__':
  import sys

  # run all suites if not told otherwise
  if len(sys.argv[1:]) == 0:
    tests = [ao_suite] # , path_suite
  else:
    # determine which suite to run
    tests = []
    for name in sys.argv[1:]:
      try:
        tests.append(globals()[name])
      except Exception, msg:
        print msg
        continue

  # run the selected suites
  for suite in tests:
    unittest.TextTestRunner(verbosity=2).run(suite)  