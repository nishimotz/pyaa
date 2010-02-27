'''
Classes that wrap IAccessible and the Windows event hook mechanisms.
'''

from Queue import Queue, Empty
from threading import Lock
from traceback import print_exc
from pyAAc import Error
import pyAAc
import Path

# create a class containing pyAA constants
class Constants:
  '''Holds all public pyAA constants without polluting the namespace.'''
  pass
# get all event, role, and selection constants
for k,v in vars(pyAAc).items():
  if (k.startswith('EVENT_') or k.startswith('ROLE_') or k.startswith('STATE_')
    or k.startswith('SELFLAG_') or k.startswith('OBJID_') or k.startswith('NAVDIR_')):
    setattr(Constants, k, v)

# Provide a mapping from idEvent to the name of the constant.
WinEventNames = dict([(v,k) for (k,v) in vars(pyAAc).items() if k.startswith('EVENT_')])
# Provide a mapping from the ObjId to the type of the object.
ObjIdNames = dict([(v,k) for (k,v) in vars(pyAAc).items() if k.startswith('OBJID_')])

class AccessibleObject(object):
  '''
  Represents the properties and actions of some user interface object. Provides
  methods comparable to those of IAccessible and then some.

  @ivar ia: Pointer to an IAccessible interface
  @type ia: opaque pointer to IAccessible object
  @ivar child: Child ID if this is a proxy to a child window
  @type child: integer
  '''
  def __init__(self, ia=None, child=None):
    '''
    Initialize an instance.
    
    See instance variables for descriptions of parameters.
    '''
    self.ia = ia
    self.child = child
    
  def DoDefaultAction(self):
    '''Trigger the default action on the object.'''
    pyAAc.CaccDoDefaultAction(self.ia, self.child)
    
  def Select(self, flags_select):
    '''
    Select this object.
    
    @param flags_select: Selection constants
    @type flags_select: integer 
    '''
    pyAAc.CaccSelect(self.ia, flags_select, self.child)

  def HitTest(self, point):
    '''
    Return the AccessibleObject contained in this one that contains the point.
    
    @param point: Point on the display
    @type point: 2-tuple of integer
    @return: Object at the given point or None
    @rtype: AccessibleObject
    '''
    res = pyAAc.CaccHitTest(self.ia, point)
    if res == None:
      return None
    elif isinstance(res, int):
      return AccessibleObject(self.ia, res)
    else:
      return AccessibleObject(res, pyAAc.CHILDID_SELF)
      
  def ChildFromPath(self, path):
    '''
    Return a child object at the leaf of the given path starting at this object.
    
    @param path: XPath like repesentation to a unique descendent object of this object
    @type path: string
    '''
    return Path.Parse(path, self)
      
  def SetFocus(self):
    '''Give this object the focus using a Win32 SetFocus callif possible.'''
    pyAAc.Cset_accFocus(self.ia)      

  def GetName(self):
    '''
    @return: Name of the object
    @rtype: string
    '''
    return pyAAc.Cget_accName(self.ia, self.child)

  def GetClassName(self):
    '''
    @return: Window class name of the object
    @rtype: string
    '''
    return pyAAc.Cget_accClass(self.ia)

  def GetRole(self):
    '''
    @return: Role of the object
    @rtype: integer
    '''
    return pyAAc.Cget_accRole(self.ia, self.child)

  def GetRoleText(self):
    '''
    @return: Description of the role of the object
    @rtype: string
    '''
    r = self.Role
    if isinstance(r, str):
      return r
    else:
      return pyAAc.CGetRoleText(self.Role)

  def GetState(self):
    '''
    @return: State of the object as a bit mask
    @rtype: integer
    '''
    return pyAAc.Cget_accState(self.ia, self.child)

  def GetStateText(self):
    '''
    @return: Description of the state of the object
    @rtype: string
    '''
    result = ''
    state = self.State
    for i in range(32): # for each bit in the mask
      mask = 1<<i
      if (state & mask) != 0:
        if result:
          result = result + '+' + pyAAc.CGetStateText(mask)
        else:
          result = pyAAc.CGetStateText(mask)
    return result

  def GetChildCount(self):
    '''
    @return: Number of children of this object
    @rtype: integer
    '''
    if self.child == pyAAc.CHILDID_SELF:
      return pyAAc.Cget_accChildCount(self.ia)
    else:
      return 0

  def GetValue(self):
    '''
    @return: Value of the object
    @rtype: string
    '''
    return pyAAc.Cget_accValue(self.ia, self.child)

  def GetParent(self):
    '''
    @return: Parent of this object
    @rtype: AccessibleObject
    '''
    if self.child == pyAAc.CHILDID_SELF:
      return AccessibleObject(pyAAc.Cget_accParent(self.ia), pyAAc.CHILDID_SELF)
    else:
      return AccessibleObject(self.ia, pyAAc.CHILDID_SELF) 

  def GetFocus(self):
    '''
    @return: Object that has the focus or None if there is no focus
    @rtype: AccessibleObject
    @note: What is the scope? Children? Whole system?
    '''
    tmp = pyAAc.Cget_accFocus(self.ia)
    if tmp is None:
      return None
    if isinstance(tmp, int):
      return AccessibleObject(self.ia, tmp)
    else:
      return AccessibleObject(tmp, pyAAc.CHILDID_SELF)

  def GetSelection(self):
    '''
    @return: All selected children
    @rtype: list of AccessibleObject
    '''
    # light children can have no other children
    if self.child != pyAAc.CHILDID_SELF:
      return []
    tmp = pyAAc.Cget_accSelection(self.ia)
    # no selected objects
    if tmp is None:
      return []
    # only one selected object
    elif isinstance(tmp, int):
      return [AccessibleObject(self.ia, tmp)]
    # list of selected objects
    elif isinstance(tmp, list):
      result = []
      for t in tmp:
        if isinstance(t, int):
          result.append(AccessibleObject(self.ia, t))
        else:
          result.append(AccessibleObject(t, pyAAc.CHILDID_SELF))
      return result
    # this is the selected object
    else:
      return AccessibleObject(tmp, pyAAc.CHILDID_SELF)

  def GetChild(self, index):
    '''
    Gets the child with the given index.
    
    @param index: Index of the desired child
    @type index: integer
    @return: Child object
    @rtype: AccessibleObject
    '''
    if self.child != pyAAc.CHILDID_SELF:
      return None
    c = pyAAc.CAccessibleChild(self.ia, index)
    if isinstance(c, int):
      return AccessibleObject(self.ia, c)
    else:
      return AccessibleObject(c, pyAAc.CHILDID_SELF)

  def GetChildren(self):
    '''
    @return: Children of this object
    @rtype: list of AccessibleObject
    '''
    # light children have no other children
    if self.child != pyAAc.CHILDID_SELF:
      return []
    children = pyAAc.CFastAccessibleChildren(self.ia)
    res = []
    for c in children:
      if isinstance(c, int):
        res.append(AccessibleObject(self.ia, c))
      else:
        res.append(AccessibleObject(c, pyAAc.CHILDID_SELF))
    return res

  def GetLocation(self):
    '''
    @return: Bounding box of the object on the screen (x1, y1, x2, y2)
    @rtype: 4-tuple of integer
    '''
    return pyAAc.CaccLocation(self.ia, self.child)

  def GetDescription(self):
    '''
    @return: Description of the object
    @rtype: string
    '''
    return pyAAc.Cget_accDescription(self.ia, self.child)

  def GetHelp(self):
    '''
    @return: Help associated with the object
    @rtype: string
    '''
    return pyAAc.Cget_accHelp(self.ia, self.child)

  def GetKeyboardShortcut(self):
    '''
    @return: Shortcut or mnemonic associated with an object
    @rtype: string
    '''
    return pyAAc.Cget_accKeyboardShortcut(self.ia, self.child)

  def GetWindow(self):
    '''
    @return: Window handle for this object, not guaranteed unique
    @rtype: integer
    '''
    return pyAAc.CWindowFromAccessibleObject(self.ia)

  def FindOneChild(self, predicate, depth_first=True):
    '''
    Search for an object that satisfies the predicate.
    
    @param predicate: Function that evaluates to true for the desired object
    @type predicate: function
    @param depth_first: Search the tree depth first (true) or breadth first (false)?
    @type depth_first: boolean
    @return: Target object or None if not found
    @rtype: AccessibleObject
    '''
    if depth_first:
      return self.FindOneChildDepth(predicate)
    else:
      return self.FindOneChildBreadth(predicate)
      
  def FindOneChildBreadth(self, predicate):
    '''
    Performs a breadth first search for an object that satisfies the predicate.
    Do not call this method directly.
    
    @param predicate: Function that evaluates to true for the desired object
    @type predicate: function
    @return: Target object or None if not found
    @rtype: AccessibleObject
    '''
    nodes = [self]
    while len(nodes) > 0:
      n = nodes.pop(0)
      try:
        if predicate(n): return n
      except Exception:
        pass
      try:
        nodes.extend(n.Children)
      except pyAAc.Error:
        continue
    return None

  def FindOneChildDepth(self, predicate):
    '''
    Performs a depth first search for an object that satisfies the predicate.
    Do not call this method directly.
    
    @param predicate: Function that evaluates to true for the desired object
    @type predicate: function
    @return: Target object or None if not found
    @rtype: AccessibleObject
    '''
    # try this object
    try:
      if predicate(self): return self
    except Exception:
      pass

    # otherwise consider the children
    try:
      for ac in self.Children:
        # don't let one child error stop the iteration
        try: res = ac.FindOneChildDepth(predicate)
        except: continue
        if res is not None:
          return res
    # ignore errors generated by pyAA
    except pyAAc.Error:
      return None
      
  def FindAllChildren(self, predicate):
    '''
    Find all objects that satisfy the predicate.

    @param predicate: Function that evaluates to true for the desired object
    @type predicate: function
    @return: Target objects or None if not found
    @rtype: list of AccessibleObject
    '''
    return self.FindAllChildrenInternal(predicate, [])

  def FindAllChildrenInternal(self, predicate, result):
    '''
    Find all objects that satisfy the predicate. Do not call this method directly.

    @param predicate: Function that evaluates to true for the desired object
    @type predicate: function
    @param result: Temporary storage for recursive search
    @type result: list of AccessibleObject
    @return: Target objects or None if not found
    @rtype: list of AccessibleObject
    '''
    # try this object
    try:
      if predicate(self): result.append(self)
    except Exception:
      pass
      
    # try the children
    try:
      for ac in self.Children:
        ac.FindAllChildrenInternal(predicate, result)
    except pyAAc.Error:
      pass
    return result
    
  def IsNotReady(self):
    '''
    @return: Is the object invisible or unavailable?
    @rtype: boolean
    '''
    return self.State & Constants.STATE_SYSTEM_INVISIBLE or \
           self.State & Constants.STATE_SYSTEM_UNAVAILABLE
           
  def Navigate(self, direction):
    '''
    Get the AccessibleObject in the direction specified. The direction is one of the
    pyAA.Constants.NAVDIR_* constants which represent the spatial directions (up, down,
    left, and right) and the logical directions (previous and next). Constants for
    the first and last children are also included.
    
    @param direction: Direction to move
    @type direction: integer
    @return: Object in the direction specified if one exists
    @rtype: AccessibleObject
    '''
    tmp = pyAAc.CaccNavigate(self.ia, self.child, direction)
    if tmp is None:
      return None
    elif isinstance(tmp, int):
      return AccessibleObject(self.ia, tmp)
    else:
     return AccessibleObject(tmp, pyAAc.CHILDID_SELF)
    
  def GetPath(self):
    '''
    @return: XPath representation of this object from a root object below the Desktop
    @rtype: string
    '''
    return Path.Build(self)
    
  def GetProcessAndThreadID(self):
    '''
    @return: IDs of the process and thread that created this object
    @rtype: 2-tuple of integer
    '''
    return pyAAc.CProcessFromAccessibleObject(self.ia)
    
  def GetChildID(self):
    '''
    @return: Child ID of this object or CHILDID_SELF
    @rtype: integer
    '''
    return self.child
    
  Name = property(GetName)
  ClassName = property(GetClassName)
  Value = property(GetValue)
  Description = property(GetDescription)
  Role = property(GetRole)
  RoleText = property(GetRoleText)
  State = property(GetState)
  StateText = property(GetStateText)
  Help = property(GetHelp)
  Location = property(GetLocation)
  Children = property(GetChildren)
  ChildCount = property(GetChildCount)
  Parent = property(GetParent)
  Selection = property(GetSelection)
  Focus = property(GetFocus)
  KeyboardShortcut = property(GetKeyboardShortcut)
  Window = property(GetWindow)
  Path = property(GetPath)
  ProcessID = property(GetProcessAndThreadID)
  ChildID = property(GetChildID)

def AccessibleObjectFromPoint(point):
  '''
  Wrapper for the MSAA function to get an object from a point on the display. The 
  object returned is the leaf object in the the MSAA tree (I think).
  
  @param point: Point on the display
  @type point: 2-tuple of integer
  @return: Object containing the given point
  @rtype: AccessibleObject
  '''
  tmp = pyAAc.CAccessibleObjectFromPoint(point)
  return AccessibleObject(tmp[0], tmp[1])

def AccessibleObjectFromEvent(hwnd, obj_id, child_id):
  '''
  Wrapper for the MSSA function to get an object given an event.
  
  @param hwnd: Window handle from which the event originated
  @type hwnd: integer
  @param obj_id: Type of object that caused the event
  @type obj_id: integer
  @param child_id: Child ID of the object causing the event
  @type child_id: integer
  '''
  tmp = pyAAc.CAccessibleObjectFromEvent(hwnd, obj_id, child_id)
  return AccessibleObject(tmp[0], tmp[1])

def AccessibleObjectFromWindow(hwnd, obj_id):
  '''
  Wrapper for the MSSA function to get an object from a window handle.
  
  @param hwnd: Window handle
  @type hwnd: integer
  @param obj_id: Type of the object that caused the event
  @type obj_id: integer
  '''
  tmp = pyAAc.CAccessibleObjectFromWindow(hwnd, obj_id)
  return AccessibleObject(tmp[0], tmp[1])
  
def AccessibleObjectFromDesktop(obj_id=Constants.OBJID_WINDOW):
  '''
  Convenience function that gets the window or client Desktop object.
  
  @param obj_id: Part of desktop to acquire, defaults to window
  @type obj_id: integer
  @return: AccessibleObject for the desktop
  @rtype: AccessibleObject
  '''
  hwnd = pyAAc.GetDesktopWindowHandle()
  return AccessibleObjectFromWindow(hwnd, obj_id)

class WinEvent(object):
  '''
  Holds information about an event.

  @ivar EventHandle: Handle of the event used for dispatch
  @type EventHandle: integer
  @ivar EventID: Type of event
  @type EventID: integer
  @ivar Window: Handle of the window from which the event originated
  @type Window: integer
  @ivar ObjectID: Type of object that caused the event
  @type ObjectID: integer
  @ivar ChildID: Child object of a window that caused the event
  @type ChildID: integer
  @ivar ThreadID: Thread from which the event originated
  @type ThreadID: integer
  @ivar EventTime: Time at which the event occurred
  @type EventTime: integer
  @ivar ao: Object associated with the event
  @type ao: AccessibleObject
  '''
  def __init__(self, event_handle, event_id, hwnd, obj_id, child_id, thread_id,
               event_time, ao=None):
    '''
    Initialize an instance
    
    See instance variables for a description of parameters.
    '''
    self.EventHandle = event_handle
    self.EventID = event_id
    self.Window = hwnd
    self.ObjectID = obj_id
    self.ChildID = child_id
    self.ThreadID = thread_id
    self.EventTime = event_time
    self.ao = ao
    
  def GetAccessibleObject(self):
    '''
    @return: Object associated with the event
    @rtype: AccessibleObject
    '''
    if self.ao is None:
      try:
        self.ao = AccessibleObjectFromEvent(self.Window, self.ObjectID, self.ChildID)
      except pyAAc.Error, e:
        pass
    return self.ao

  def GetEventName(self):
    '''
    @return: Name of the event type
    @rtype: string
    '''
    return WinEventNames.get(self.EventID, hex(self.EventID))

  def GetObjectName(self):
    '''
    @return: Name of the object type
    @rtype: string
    '''
    return ObjIdNames.get(self.ObjectID, hex(self.ObjectID))

  AccessibleObject = property(fget=GetAccessibleObject)
  EventName = property(fget=GetEventName)
  ObjectName = property(fget=GetObjectName)

# module level dispatch map
_event_dispatch_map = {}

def event_dispatch(event_handle, event_id, hwnd, obj_id, child_id, 
                   thread_id, event_time):
  '''
  Dispatches events received from our C callback. The old version of this function
  used a number of locks to prevent more than one re-entrant call from handling any
  callbacks. That approach proved problematic for unknown reasons. This version
  forgoes using locks because 1) this function cannot be re-entered since
  the GIL is held when it is invoked by the C callback and 2) supposedly MSAA 
  serializes all out-of-context callbacks anyways, which are the only kind we get.
  
  Events are guaranteed to be delivered in order for a registered hook handle but no
  such guarantee is made on ordering across handles.
  
  See the instance variables in the L{WinEvent} class for a description of the 
  parameters of this function.
  '''
  # build a convenient event object
  event = WinEvent(event_handle, event_id, hwnd, obj_id, child_id, 
                   thread_id, event_time)
                   
  # try to get the callback and its parameters
  try:
    disp_func, disp_hwnd, disp_obj_id = _event_dispatch_map[event.EventHandle]
  except:
    return
    
  # filter on hwnd and obj_id if desired
  if ((disp_hwnd is None or disp_hwnd == event.Window) and
      (disp_obj_id is None or disp_obj_id == event.ObjectID)):
    try:
      disp_func(event)
    except:
      print_exc()

def AddWinEventHook(callback, event=(pyAAc.EVENT_MIN, pyAAc.EVENT_MAX),
                    process_id=0, thread_id=0, hwnd=None, obj_id=None):
  '''
  Add a hook to be invoked when an event matching the criteria occurs.
  
  @param callback: Object that is called when a target event occurs
  @type callback: function
  @param event: Number of an event or range of events
  @type event: integer or 2-tuple of integer
  @param process_id: Restrict notifications to those coming from this process
  @type process_id: integer
  @param thread_id: Restrict notifications to those coming from this thread
  @type thread_id: integer
  @param hwnd: Filter on the window handle
  @type hwnd: integer
  @param obj_id: Filter on object type
  @type obj_id: integer
  '''
  # convert single event into a range
  if isinstance(event, int):
    event = (event, event)

  # SNAFU: an event could occur between setting the hook and storing the callback
  handle = pyAAc.CSetWinEventHook(event[0], event[1], event_dispatch, process_id,
                                  thread_id, pyAAc.WINEVENT_SKIPOWNPROCESS)
  _event_dispatch_map[handle] = (callback, hwnd, obj_id)
  return handle

def DeleteWinEventHook(handle):
  '''
  Disable a previously established hook.

  @param handle: Hook handle returned earlier
  @type handle: integer
  '''
  r = pyAAc.CUnhookWinEvent(handle)
  del _event_dispatch_map[handle]

class AAbase(object):
  '''
  Basic class that supports setting hooks and automatically removing hooks when the
  object dies.
  
  @ivar release_hooks: Callbacks to make on release
  @type release_hooks: list
  '''
  def __init__(self):
    '''Initialize an instance.'''
    self.release_hooks = []

  def Release(self):
    '''Run any cleanup hooks that have been requested.'''
    if self.release_hooks is None: return
    # avoid a recursive call    
    hooks = self.release_hooks
    self.release_hooks = None
    for hook, hook_args in hooks:
      if hook is not None:
        hook(*hook_args)

  def AddReleaseHook(self, hook, *args):
    '''Add a function to be called on Release.'''
    self.release_hooks.append((hook, args))

  def AddWinEventHook(self, callback=None, 
                      event=(pyAAc.EVENT_MIN, pyAAc.EVENT_MAX),
                      process_id=0, thread_id=0, hwnd=None, obj_id=None):
    '''
    Add an event hook and release hook to clean it up on object death.
    
    @param callback: Object that is called when a target event occurs
    @type callback: function
    @param event: Number of an event or range of events
    @type event: integer or 2-tuple of integer
    @param process_id: Restrict notifications to those coming from this process
    @type process_id: integer
    @param thread_id: Restrict notifications to those coming from this thread
    @type thread_id: integer
    @param hwnd: Filter on the window handle
    @type hwnd: integer
    @param obj_id: Filter on object type
    @type obj_id: integer
    '''
    handle = AddWinEventHook(callback=callback, event=event, process_id=process_id,
                             thread_id=thread_id, hwnd=hwnd, obj_id=obj_id)
    self.AddReleaseHook(DeleteWinEventHook, handle)