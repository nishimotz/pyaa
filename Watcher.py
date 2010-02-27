'''
Classes that make watching for common window events easier.
'''
import AA, Defer

class Watcher(AA.AAbase):
  '''
  Watches for system and application events. Defines a destroy method 
  that releases event hooks and a held deferred.
  
  @ivar result: Placeholder for a result that will be returned later
  @type result: L{Defer.Deferred}
  '''
  def __init__(self):
    '''Initialize an instance.'''
    AA.AAbase.__init__(self)
    self.result = None
    
  def Destroy(self):
    '''Unset event hooks and destroy result object.'''
    self.Release()
    self.result = None

class WindowWatcher(Watcher):
  '''
  Watches for events coming from a particular window. Can compare any property
  of an accessible object with a set value, the result of a callable, or a 
  regular expression.
  
  @ivar features: Properties identifying the target window
  @type features: dictionary
  @ivar thread_id: Thread ID on which to filter events
  @type thread_id: integer
  @ivar process_id: Process ID on which to filter events
  @type process_id: integer
  '''
  def __init__(self, thread_id=0, process_id=0):
    '''Initialize an instance.'''
    super(WindowWatcher, self).__init__()
    self.features = {}
    self.thread_id = thread_id
    self.process_id = process_id
    
  def NotifyOnEvents(self, events, **features):
    '''
    Sets a hook to watch for the given events. Tests the events for the given
    features.
    
    @param events: List of events to watch
    @type events: list
    @param features: Other features to monitor, given by their AA property name
    @type features: dictionary
    @return: Result on which to notify about changes
    @rtype: L{Defer.Deferred}
    '''
    self.features.update(features)
    # create a deferred
    self.result = Defer.Deferred()
    # register all hooks
    for e in events:
      self.AddWinEventHook(callback=self.OnResultEvent, event=e,
                           thread_id=self.thread_id,
                           process_id=self.process_id)
    return self.result
  
  def NotifyOnOpen(self, **features):
    '''
    Sets a hook to watch for an object show or foreground event.
    
    @return: Result on which to notify about changes
    @rtype: L{Defer.Deferred}
    '''
    self.features.update(features)
    # create a deferred
    self.result = Defer.Deferred()
    # register a hook to watch for window appearances
    self.AddWinEventHook(callback=self.OnResultEvent,
                         event=AA.Constants.EVENT_OBJECT_SHOW,
                         thread_id=self.thread_id,
                         process_id=self.process_id)
    # register a hook to watch for windows being brought to the foreground
    self.AddWinEventHook(callback=self.OnResultEvent,
                         event=AA.Constants.EVENT_SYSTEM_FOREGROUND,
                         thread_id=self.thread_id,
                         process_id=self.process_id)
    return self.result

  def NotifyOnClose(self, hwnd):
    '''
    Sets a hook to watch for a particular window being destroyed.
    
    @param hwnd: Window handle of the target window
    @type hwnd: number
    @return: Result on which to notify about changes
    @rtype: L{Defer.Deferred}    
    '''
    # create a deferred
    self.result = Defer.Deferred()
    # add a hook to watch for window death
    self.AddWinEventHook(callback=self.OnEmptyEvent,
                         event=AA.Constants.EVENT_OBJECT_DESTROY,
                         hwnd=hwnd, thread_id=self.thread_id,
                         process_id=self.process_id)
    return self.result
    
  def OnResultEvent(self, event):
    '''
    Removes all hooks and makes the callback if the criteria have been met.
    
    @param event: Event that occurred
    @type event: L{AA.WinEvent}
    '''
    # quit if we can't get the AO
    ao = event.AccessibleObject
    if ao is None: return
    # see if the window matches our features
    val = self.TestFeatures(ao)
    if not val: return
    # stop watching for events
    self.Release()
    # return the deferred result
    self.result.Callback(ao)
    self.result = None

  def OnEmptyEvent(self, event):
    '''
    Removes all hooks and makes the callback without checking criteria.
    
    @param event: Event that occurred
    @type event: L{AA.WinEvent}
    '''
    # the destroy is registered for a particular window so there's nothing to test
    # stop watching for events immediately
    self.Release()
    # return the deferred result
    self.result.Callback(None)
    self.result = None

  def TestFeatures(self, ao):
    '''
    Compares the features of the target window to the object that fired the 
    event.
    
    @param ao: Object that fired an event
    @type ao: L{AA.AccessibleObject}
    '''
    # test the name and class
    for name in self.features:
      if self.features[name] is None:
        continue
      val = self.TestGeneral(ao, name, self.features[name])
      if not val:
        return False
    return True
    
  def TestGeneral(self, ao, name, target):
    '''
    Compares the given property of the accessible object to the target value.
    
    @param ao: Object that fired an event
    @type ao: L{AA.AccessibleObject}
    @param property: Name of the property to compare
    @type property: string
    @param target: Window class of the target window
    @type target: string
    @return: True if property matches the target, False otherwise
    @rtype: boolean
    '''
    try:
      pval = getattr(ao, name)
    except AttributeError, pyAA.Error:
      return False
    # treat the target as a callable first
    try:
      return target(pval)
    except TypeError:
      pass
    # treat the target as a regex next
    try:
      return (target.search(pval) is not None)
    except AttributeError:
      pass
    # finally, just do a straightforward comparison in lowercase
    try:
      return pval.lower().find(target.lower()) > -1
    except AttributeError:
      return False

#  def TestClass(self, ao, target_class):
#    '''
#    Compares the window class of the provided object to the target window class.
#    
#    @param ao: Object that fired an event
#    @type ao: L{AA.AccessibleObject}
#    @param target_class: Window class of the target window
#    @type target_class: string
#    @return: True if the classes match, False otherwise
#    @rtype: boolean
#    '''
#    try:
#      cls = ao.ClassName
#    except:
#      return False
#    return cls == target_class
#
#  def TestTitle(self, ao, target_title):
#    '''
#    Compares the lowercase title of the provided object to the lowercase target
#    window title.
#    
#    @param ao: Object that fired an event
#    @type ao: L{AA.AccessibleObject}
#    @param target_title: Window title of the target window
#    @type target_title: string
#    @return: True if the titles match, False otherwise
#    @rtype: boolean
#    '''
#    try:
#      title = ao.Name
#    except:
#      return False
#    if title is not None:
#      return title.lower().find(target_title.lower()) > -1
#    else:
#      return title == target_title