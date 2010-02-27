from AA import *
from Watcher import *
import win32com.client, os, time, win32gui, threading

INIT_WAIT = 0.5
SAFE_WAIT = 0.5
SPIN_DELAY = 0.2
ANSWER = 9

# create an instance of WSH Shell
ws_shell = win32com.client.Dispatch("WScript.Shell")

# press some keys
def SendKeys(keys, shift=False):
  '''
  Inject a key press into the input queue of the focused window.

  @param keys: Keys to press
  @type keys: string
  @param shift: Hold the shift key?
  @type shift: boolean
  '''
  if shift: keys = '+'+keys
  ws_shell.SendKeys(keys)

class ConnectionManager(threading.Thread):
  def __init__(self, pid):
    threading.Thread.__init__(self)
    self.pid = pid
    self.last_time = time.time()
    self.watcher = Watcher()
    self.alive = False

  def run(self):
    self.alive = True
    # start watching for events in the program
    self.watcher.AddWinEventHook(callback=self.Disturb, process_id=self.pid)
    while self.alive:
      win32gui.PumpWaitingMessages()
      time.sleep(SPIN_DELAY)
    self.watcher.Destroy()
    print 'connection manager dead'

  def Destroy(self):
    self.alive = False

  def Disturb(self, event=None):
    self.last_time = time.time()

  def IsCalm(self):
    return ((time.time() - self.last_time) > SAFE_WAIT)

class Main(Watcher):
  def __init__(self, event, runs=1):
    Watcher.__init__(self)
    self.runs = runs
    self.program = None
    self.message = None
    self.attach = None
    self.conn_man = None
    self.event = event
    self.failures = 0

  def Start(self, *args):
    # quit if there are no runs left
    if self.runs == 0:
      print '***** Finished'
      self.event.set()
    else:
      # decrement the runs counter
      self.runs -= 1
      print '***** Starting test: %d runs left' % self.runs
      time.sleep(2)
      self.StartProgram()
    
  def SafeWait(self):
    time.sleep(INIT_WAIT)
    while 1:
      if self.conn_man.IsCalm(): break
      time.sleep(SPIN_DELAY)

  def GetConnection(self, conn):
    self.SafeWait()
    print '*', conn.Name, 'ready at', time.time()
    return conn

  def GetChildFromPred(self, conn, pred):
    self.SafeWait()
    print '*', conn.Name, ' ready for search at', time.time()
    return conn.FindOneChild(pred)

  def SendKeys(self, s):
    SendKeys(s)
    self.conn_man.Disturb()

  def Focus(self, conn):
    self.SafeWait()    
    conn.Select(Constants.SELFLAG_TAKEFOCUS)
    self.conn_man.Disturb()

  def StartProgram(self):
    print '** Starting program'
    # start the program
    w = WindowWatcher()
    r = w.NotifyOnOpen(title='Outlook Express', cls='Outlook Express Browser Class')
    r.AddCallback(self.StartMessage)
    os.startfile('msimn.exe')

  def StartMessage(self, result, *args):
    print '** Starting message'
    # start watching for events in the program
    pid, tid = result.ProcessID
    self.conn_man = ConnectionManager(pid)
    self.conn_man.start()

    # save the program connection
    self.program = self.GetConnection(result)
    # start a new message
    w = WindowWatcher()
    r = w.NotifyOnOpen(cls='ATH_Note')
    r.AddCallback(self.AttachFiles)
    self.SendKeys('%{f}{n}{m}')

  def AttachFiles(self, result, *args):
    print '** Attaching files'
    # save the message window connection
    self.message = self.GetConnection(result)
    # add attachments
    w = WindowWatcher()
    r = w.NotifyOnOpen(cls='#32770')
    r.AddCallback(self.ChangeFolder)
    self.SendKeys('%{i}{a}')

  def ChangeFolder(self, result, *args):
    print '** Changing folder'
    # save the attachments window connection
    self.attach = self.GetConnection(result)
    # locate the looking drop down dialog
    def LookInPred(x):
      return (x.Name.find('Look in:')>-1) and (x.Role==Constants.ROLE_SYSTEM_COMBOBOX)
    lookin = self.GetChildFromPred(self.attach, LookInPred)
    self.Focus(lookin)
    self.SendKeys('{DOWN}{HOME}{DOWN}{DOWN}{DOWN}{ENTER}')
    self.CountItems()

  def CountItems(self):
    print '** Counting files'
    # locate the file list
    def FileListPred(x):
      return (x.ClassName=='SysListView32') and (x.Role==Constants.ROLE_SYSTEM_LIST)
    # TODO: this line crashes Python for short SAFE_WAIT times
    filelist = self.GetChildFromPred(self.attach, FileListPred)
    try:
      if filelist.ChildCount != ANSWER:
        print 'XXXXX TEST FAILED XXXXX'
        self.failures += 1
    except:
      print 'XXXXX TEST FAILED XXXXX'
      self.failures += 1
    self.QuitAttach()

  def QuitAttach(self):
    print '** Closing attachment'
    # close the attach window
    w = WindowWatcher()
    r = w.NotifyOnClose(self.attach.Window)
    r.AddCallback(self.QuitMessage)
    # focus on the attachment window
    self.Focus(self.attach)
    self.SendKeys('%{F4}')

  def QuitMessage(self, result, *args):
    print '** Closing message', hex(self.message.Window)
    # close the message window
    w = WindowWatcher()
    r = w.NotifyOnClose(self.message.Window)
    r.AddCallback(self.QuitProgram)
    # focus on the message window
    self.Focus(self.message)
    self.SendKeys('%{F4}')

  def QuitProgram(self, result, *args):
    print '** Closing program', hex(self.program.Window)
    # close the program window
    w = WindowWatcher()
    r = w.NotifyOnClose(self.program.Window)
    r.AddCallback(self.Start)
    self.conn_man.Destroy()
    # focus on the program window
    self.Focus(self.program)
    self.SendKeys('%{F4}')

def run():
  f = file('log.txt', 'w')
  safe_tests = [0.5, 0.4, 0.3, 0.2, 0.1]
  init_tests = [0.5, 0.4, 0.3]
  for INIT_WAIT in init_tests:
    for SAFE_WAIT in safe_tests:
      e = threading.Event()
      runs = 20
      m = Main(e, runs)
      m.Start()
      while not e.isSet():
        win32gui.PumpWaitingMessages()
        time.sleep(0.1)
      print >>f, "{'safe_wait': %0.2f, 'pass': %d, 'fail': %d, 'runs': %d}" % \
            (SAFE_WAIT, runs-m.failures, m.failures, runs)
      f.flush()
  f.close()

if __name__ == '__main__':
  run()