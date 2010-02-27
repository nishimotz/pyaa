# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_pyAAc', [dirname(__file__)])
        except ImportError:
            import _pyAAc
            return _pyAAc
        if fp is not None:
            try:
                _mod = imp.load_module('_pyAAc', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pyAAc = swig_import_helper()
    del swig_import_helper
else:
    import _pyAAc
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


# so we can export it
Error = _pyAAc.Error
  
CHILDID_SELF = _pyAAc.CHILDID_SELF
E_NOINTERFACE = _pyAAc.E_NOINTERFACE
STATE_SYSTEM_UNAVAILABLE = _pyAAc.STATE_SYSTEM_UNAVAILABLE
STATE_SYSTEM_SELECTED = _pyAAc.STATE_SYSTEM_SELECTED
STATE_SYSTEM_FOCUSED = _pyAAc.STATE_SYSTEM_FOCUSED
STATE_SYSTEM_PRESSED = _pyAAc.STATE_SYSTEM_PRESSED
STATE_SYSTEM_CHECKED = _pyAAc.STATE_SYSTEM_CHECKED
STATE_SYSTEM_MIXED = _pyAAc.STATE_SYSTEM_MIXED
STATE_SYSTEM_READONLY = _pyAAc.STATE_SYSTEM_READONLY
STATE_SYSTEM_HOTTRACKED = _pyAAc.STATE_SYSTEM_HOTTRACKED
STATE_SYSTEM_DEFAULT = _pyAAc.STATE_SYSTEM_DEFAULT
STATE_SYSTEM_EXPANDED = _pyAAc.STATE_SYSTEM_EXPANDED
STATE_SYSTEM_COLLAPSED = _pyAAc.STATE_SYSTEM_COLLAPSED
STATE_SYSTEM_BUSY = _pyAAc.STATE_SYSTEM_BUSY
STATE_SYSTEM_FLOATING = _pyAAc.STATE_SYSTEM_FLOATING
STATE_SYSTEM_MARQUEED = _pyAAc.STATE_SYSTEM_MARQUEED
STATE_SYSTEM_ANIMATED = _pyAAc.STATE_SYSTEM_ANIMATED
STATE_SYSTEM_INVISIBLE = _pyAAc.STATE_SYSTEM_INVISIBLE
STATE_SYSTEM_OFFSCREEN = _pyAAc.STATE_SYSTEM_OFFSCREEN
STATE_SYSTEM_SIZEABLE = _pyAAc.STATE_SYSTEM_SIZEABLE
STATE_SYSTEM_MOVEABLE = _pyAAc.STATE_SYSTEM_MOVEABLE
STATE_SYSTEM_SELFVOICING = _pyAAc.STATE_SYSTEM_SELFVOICING
STATE_SYSTEM_FOCUSABLE = _pyAAc.STATE_SYSTEM_FOCUSABLE
STATE_SYSTEM_SELECTABLE = _pyAAc.STATE_SYSTEM_SELECTABLE
STATE_SYSTEM_LINKED = _pyAAc.STATE_SYSTEM_LINKED
STATE_SYSTEM_TRAVERSED = _pyAAc.STATE_SYSTEM_TRAVERSED
STATE_SYSTEM_MULTISELECTABLE = _pyAAc.STATE_SYSTEM_MULTISELECTABLE
STATE_SYSTEM_EXTSELECTABLE = _pyAAc.STATE_SYSTEM_EXTSELECTABLE
STATE_SYSTEM_ALERT_LOW = _pyAAc.STATE_SYSTEM_ALERT_LOW
STATE_SYSTEM_ALERT_MEDIUM = _pyAAc.STATE_SYSTEM_ALERT_MEDIUM
STATE_SYSTEM_ALERT_HIGH = _pyAAc.STATE_SYSTEM_ALERT_HIGH
STATE_SYSTEM_VALID = _pyAAc.STATE_SYSTEM_VALID
ROLE_SYSTEM_TITLEBAR = _pyAAc.ROLE_SYSTEM_TITLEBAR
ROLE_SYSTEM_MENUBAR = _pyAAc.ROLE_SYSTEM_MENUBAR
ROLE_SYSTEM_SCROLLBAR = _pyAAc.ROLE_SYSTEM_SCROLLBAR
ROLE_SYSTEM_GRIP = _pyAAc.ROLE_SYSTEM_GRIP
ROLE_SYSTEM_SOUND = _pyAAc.ROLE_SYSTEM_SOUND
ROLE_SYSTEM_CURSOR = _pyAAc.ROLE_SYSTEM_CURSOR
ROLE_SYSTEM_CARET = _pyAAc.ROLE_SYSTEM_CARET
ROLE_SYSTEM_ALERT = _pyAAc.ROLE_SYSTEM_ALERT
ROLE_SYSTEM_WINDOW = _pyAAc.ROLE_SYSTEM_WINDOW
ROLE_SYSTEM_CLIENT = _pyAAc.ROLE_SYSTEM_CLIENT
ROLE_SYSTEM_MENUPOPUP = _pyAAc.ROLE_SYSTEM_MENUPOPUP
ROLE_SYSTEM_MENUITEM = _pyAAc.ROLE_SYSTEM_MENUITEM
ROLE_SYSTEM_TOOLTIP = _pyAAc.ROLE_SYSTEM_TOOLTIP
ROLE_SYSTEM_APPLICATION = _pyAAc.ROLE_SYSTEM_APPLICATION
ROLE_SYSTEM_DOCUMENT = _pyAAc.ROLE_SYSTEM_DOCUMENT
ROLE_SYSTEM_PANE = _pyAAc.ROLE_SYSTEM_PANE
ROLE_SYSTEM_CHART = _pyAAc.ROLE_SYSTEM_CHART
ROLE_SYSTEM_DIALOG = _pyAAc.ROLE_SYSTEM_DIALOG
ROLE_SYSTEM_BORDER = _pyAAc.ROLE_SYSTEM_BORDER
ROLE_SYSTEM_GROUPING = _pyAAc.ROLE_SYSTEM_GROUPING
ROLE_SYSTEM_SEPARATOR = _pyAAc.ROLE_SYSTEM_SEPARATOR
ROLE_SYSTEM_TOOLBAR = _pyAAc.ROLE_SYSTEM_TOOLBAR
ROLE_SYSTEM_STATUSBAR = _pyAAc.ROLE_SYSTEM_STATUSBAR
ROLE_SYSTEM_TABLE = _pyAAc.ROLE_SYSTEM_TABLE
ROLE_SYSTEM_COLUMNHEADER = _pyAAc.ROLE_SYSTEM_COLUMNHEADER
ROLE_SYSTEM_ROWHEADER = _pyAAc.ROLE_SYSTEM_ROWHEADER
ROLE_SYSTEM_COLUMN = _pyAAc.ROLE_SYSTEM_COLUMN
ROLE_SYSTEM_ROW = _pyAAc.ROLE_SYSTEM_ROW
ROLE_SYSTEM_CELL = _pyAAc.ROLE_SYSTEM_CELL
ROLE_SYSTEM_LINK = _pyAAc.ROLE_SYSTEM_LINK
ROLE_SYSTEM_HELPBALLOON = _pyAAc.ROLE_SYSTEM_HELPBALLOON
ROLE_SYSTEM_CHARACTER = _pyAAc.ROLE_SYSTEM_CHARACTER
ROLE_SYSTEM_LIST = _pyAAc.ROLE_SYSTEM_LIST
ROLE_SYSTEM_LISTITEM = _pyAAc.ROLE_SYSTEM_LISTITEM
ROLE_SYSTEM_OUTLINE = _pyAAc.ROLE_SYSTEM_OUTLINE
ROLE_SYSTEM_OUTLINEITEM = _pyAAc.ROLE_SYSTEM_OUTLINEITEM
ROLE_SYSTEM_PAGETAB = _pyAAc.ROLE_SYSTEM_PAGETAB
ROLE_SYSTEM_PROPERTYPAGE = _pyAAc.ROLE_SYSTEM_PROPERTYPAGE
ROLE_SYSTEM_INDICATOR = _pyAAc.ROLE_SYSTEM_INDICATOR
ROLE_SYSTEM_GRAPHIC = _pyAAc.ROLE_SYSTEM_GRAPHIC
ROLE_SYSTEM_STATICTEXT = _pyAAc.ROLE_SYSTEM_STATICTEXT
ROLE_SYSTEM_TEXT = _pyAAc.ROLE_SYSTEM_TEXT
ROLE_SYSTEM_PUSHBUTTON = _pyAAc.ROLE_SYSTEM_PUSHBUTTON
ROLE_SYSTEM_CHECKBUTTON = _pyAAc.ROLE_SYSTEM_CHECKBUTTON
ROLE_SYSTEM_RADIOBUTTON = _pyAAc.ROLE_SYSTEM_RADIOBUTTON
ROLE_SYSTEM_COMBOBOX = _pyAAc.ROLE_SYSTEM_COMBOBOX
ROLE_SYSTEM_DROPLIST = _pyAAc.ROLE_SYSTEM_DROPLIST
ROLE_SYSTEM_PROGRESSBAR = _pyAAc.ROLE_SYSTEM_PROGRESSBAR
ROLE_SYSTEM_DIAL = _pyAAc.ROLE_SYSTEM_DIAL
ROLE_SYSTEM_HOTKEYFIELD = _pyAAc.ROLE_SYSTEM_HOTKEYFIELD
ROLE_SYSTEM_SLIDER = _pyAAc.ROLE_SYSTEM_SLIDER
ROLE_SYSTEM_SPINBUTTON = _pyAAc.ROLE_SYSTEM_SPINBUTTON
ROLE_SYSTEM_DIAGRAM = _pyAAc.ROLE_SYSTEM_DIAGRAM
ROLE_SYSTEM_ANIMATION = _pyAAc.ROLE_SYSTEM_ANIMATION
ROLE_SYSTEM_EQUATION = _pyAAc.ROLE_SYSTEM_EQUATION
ROLE_SYSTEM_BUTTONDROPDOWN = _pyAAc.ROLE_SYSTEM_BUTTONDROPDOWN
ROLE_SYSTEM_BUTTONMENU = _pyAAc.ROLE_SYSTEM_BUTTONMENU
ROLE_SYSTEM_BUTTONDROPDOWNGRID = _pyAAc.ROLE_SYSTEM_BUTTONDROPDOWNGRID
ROLE_SYSTEM_WHITESPACE = _pyAAc.ROLE_SYSTEM_WHITESPACE
ROLE_SYSTEM_PAGETABLIST = _pyAAc.ROLE_SYSTEM_PAGETABLIST
ROLE_SYSTEM_CLOCK = _pyAAc.ROLE_SYSTEM_CLOCK
GUI_CARETBLINKING = _pyAAc.GUI_CARETBLINKING
GUI_INMOVESIZE = _pyAAc.GUI_INMOVESIZE
GUI_INMENUMODE = _pyAAc.GUI_INMENUMODE
GUI_SYSTEMMENUMODE = _pyAAc.GUI_SYSTEMMENUMODE
GUI_POPUPMENUMODE = _pyAAc.GUI_POPUPMENUMODE
INPUT_MOUSE = _pyAAc.INPUT_MOUSE
INPUT_KEYBOARD = _pyAAc.INPUT_KEYBOARD
INPUT_HARDWARE = _pyAAc.INPUT_HARDWARE
OBJID_WINDOW = _pyAAc.OBJID_WINDOW
OBJID_SYSMENU = _pyAAc.OBJID_SYSMENU
OBJID_TITLEBAR = _pyAAc.OBJID_TITLEBAR
OBJID_MENU = _pyAAc.OBJID_MENU
OBJID_CLIENT = _pyAAc.OBJID_CLIENT
OBJID_VSCROLL = _pyAAc.OBJID_VSCROLL
OBJID_HSCROLL = _pyAAc.OBJID_HSCROLL
OBJID_SIZEGRIP = _pyAAc.OBJID_SIZEGRIP
OBJID_CARET = _pyAAc.OBJID_CARET
OBJID_CURSOR = _pyAAc.OBJID_CURSOR
OBJID_ALERT = _pyAAc.OBJID_ALERT
OBJID_SOUND = _pyAAc.OBJID_SOUND
ALERT_SYSTEM_INFORMATIONAL = _pyAAc.ALERT_SYSTEM_INFORMATIONAL
ALERT_SYSTEM_WARNING = _pyAAc.ALERT_SYSTEM_WARNING
ALERT_SYSTEM_ERROR = _pyAAc.ALERT_SYSTEM_ERROR
ALERT_SYSTEM_QUERY = _pyAAc.ALERT_SYSTEM_QUERY
ALERT_SYSTEM_CRITICAL = _pyAAc.ALERT_SYSTEM_CRITICAL
CALERT_SYSTEM = _pyAAc.CALERT_SYSTEM
WINEVENT_OUTOFCONTEXT = _pyAAc.WINEVENT_OUTOFCONTEXT
WINEVENT_SKIPOWNTHREAD = _pyAAc.WINEVENT_SKIPOWNTHREAD
WINEVENT_SKIPOWNPROCESS = _pyAAc.WINEVENT_SKIPOWNPROCESS
WINEVENT_INCONTEXT = _pyAAc.WINEVENT_INCONTEXT
EVENT_MIN = _pyAAc.EVENT_MIN
EVENT_MAX = _pyAAc.EVENT_MAX
EVENT_SYSTEM_SOUND = _pyAAc.EVENT_SYSTEM_SOUND
EVENT_SYSTEM_ALERT = _pyAAc.EVENT_SYSTEM_ALERT
EVENT_SYSTEM_FOREGROUND = _pyAAc.EVENT_SYSTEM_FOREGROUND
EVENT_SYSTEM_MENUSTART = _pyAAc.EVENT_SYSTEM_MENUSTART
EVENT_SYSTEM_MENUEND = _pyAAc.EVENT_SYSTEM_MENUEND
EVENT_SYSTEM_MENUPOPUPSTART = _pyAAc.EVENT_SYSTEM_MENUPOPUPSTART
EVENT_SYSTEM_MENUPOPUPEND = _pyAAc.EVENT_SYSTEM_MENUPOPUPEND
EVENT_SYSTEM_CAPTURESTART = _pyAAc.EVENT_SYSTEM_CAPTURESTART
EVENT_SYSTEM_CAPTUREEND = _pyAAc.EVENT_SYSTEM_CAPTUREEND
EVENT_SYSTEM_MOVESIZESTART = _pyAAc.EVENT_SYSTEM_MOVESIZESTART
EVENT_SYSTEM_MOVESIZEEND = _pyAAc.EVENT_SYSTEM_MOVESIZEEND
EVENT_SYSTEM_CONTEXTHELPSTART = _pyAAc.EVENT_SYSTEM_CONTEXTHELPSTART
EVENT_SYSTEM_CONTEXTHELPEND = _pyAAc.EVENT_SYSTEM_CONTEXTHELPEND
EVENT_SYSTEM_DRAGDROPSTART = _pyAAc.EVENT_SYSTEM_DRAGDROPSTART
EVENT_SYSTEM_DRAGDROPEND = _pyAAc.EVENT_SYSTEM_DRAGDROPEND
EVENT_SYSTEM_DIALOGSTART = _pyAAc.EVENT_SYSTEM_DIALOGSTART
EVENT_SYSTEM_DIALOGEND = _pyAAc.EVENT_SYSTEM_DIALOGEND
EVENT_SYSTEM_SCROLLINGSTART = _pyAAc.EVENT_SYSTEM_SCROLLINGSTART
EVENT_SYSTEM_SCROLLINGEND = _pyAAc.EVENT_SYSTEM_SCROLLINGEND
EVENT_SYSTEM_SWITCHSTART = _pyAAc.EVENT_SYSTEM_SWITCHSTART
EVENT_SYSTEM_SWITCHEND = _pyAAc.EVENT_SYSTEM_SWITCHEND
EVENT_SYSTEM_MINIMIZESTART = _pyAAc.EVENT_SYSTEM_MINIMIZESTART
EVENT_SYSTEM_MINIMIZEEND = _pyAAc.EVENT_SYSTEM_MINIMIZEEND
EVENT_OBJECT_CREATE = _pyAAc.EVENT_OBJECT_CREATE
EVENT_OBJECT_DESTROY = _pyAAc.EVENT_OBJECT_DESTROY
EVENT_OBJECT_SHOW = _pyAAc.EVENT_OBJECT_SHOW
EVENT_OBJECT_HIDE = _pyAAc.EVENT_OBJECT_HIDE
EVENT_OBJECT_REORDER = _pyAAc.EVENT_OBJECT_REORDER
EVENT_OBJECT_FOCUS = _pyAAc.EVENT_OBJECT_FOCUS
EVENT_OBJECT_SELECTION = _pyAAc.EVENT_OBJECT_SELECTION
EVENT_OBJECT_SELECTIONADD = _pyAAc.EVENT_OBJECT_SELECTIONADD
EVENT_OBJECT_SELECTIONREMOVE = _pyAAc.EVENT_OBJECT_SELECTIONREMOVE
EVENT_OBJECT_SELECTIONWITHIN = _pyAAc.EVENT_OBJECT_SELECTIONWITHIN
EVENT_OBJECT_STATECHANGE = _pyAAc.EVENT_OBJECT_STATECHANGE
EVENT_OBJECT_LOCATIONCHANGE = _pyAAc.EVENT_OBJECT_LOCATIONCHANGE
EVENT_OBJECT_NAMECHANGE = _pyAAc.EVENT_OBJECT_NAMECHANGE
EVENT_OBJECT_DESCRIPTIONCHANGE = _pyAAc.EVENT_OBJECT_DESCRIPTIONCHANGE
EVENT_OBJECT_VALUECHANGE = _pyAAc.EVENT_OBJECT_VALUECHANGE
EVENT_OBJECT_PARENTCHANGE = _pyAAc.EVENT_OBJECT_PARENTCHANGE
EVENT_OBJECT_HELPCHANGE = _pyAAc.EVENT_OBJECT_HELPCHANGE
EVENT_OBJECT_DEFACTIONCHANGE = _pyAAc.EVENT_OBJECT_DEFACTIONCHANGE
EVENT_OBJECT_ACCELERATORCHANGE = _pyAAc.EVENT_OBJECT_ACCELERATORCHANGE
SELFLAG_NONE = _pyAAc.SELFLAG_NONE
SELFLAG_TAKEFOCUS = _pyAAc.SELFLAG_TAKEFOCUS
SELFLAG_TAKESELECTION = _pyAAc.SELFLAG_TAKESELECTION
SELFLAG_EXTENDSELECTION = _pyAAc.SELFLAG_EXTENDSELECTION
SELFLAG_ADDSELECTION = _pyAAc.SELFLAG_ADDSELECTION
SELFLAG_REMOVESELECTION = _pyAAc.SELFLAG_REMOVESELECTION
NAVDIR_FIRSTCHILD = _pyAAc.NAVDIR_FIRSTCHILD
NAVDIR_LASTCHILD = _pyAAc.NAVDIR_LASTCHILD
NAVDIR_LEFT = _pyAAc.NAVDIR_LEFT
NAVDIR_RIGHT = _pyAAc.NAVDIR_RIGHT
NAVDIR_UP = _pyAAc.NAVDIR_UP
NAVDIR_DOWN = _pyAAc.NAVDIR_DOWN
NAVDIR_PREVIOUS = _pyAAc.NAVDIR_PREVIOUS
NAVDIR_NEXT = _pyAAc.NAVDIR_NEXT
class IAccessible(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IAccessible, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IAccessible, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    def __del__(self): return _pyAAc.IAccessible___del__(self)
IAccessible_swigregister = _pyAAc.IAccessible_swigregister
IAccessible_swigregister(IAccessible)


def IAccessible_Release(*args):
  return _pyAAc.IAccessible_Release(*args)
IAccessible_Release = _pyAAc.IAccessible_Release

def Cget_accName(*args):
  return _pyAAc.Cget_accName(*args)
Cget_accName = _pyAAc.Cget_accName

def Cget_accClass(*args):
  return _pyAAc.Cget_accClass(*args)
Cget_accClass = _pyAAc.Cget_accClass

def Cget_accDefaultAction(*args):
  return _pyAAc.Cget_accDefaultAction(*args)
Cget_accDefaultAction = _pyAAc.Cget_accDefaultAction

def Cget_accDescription(*args):
  return _pyAAc.Cget_accDescription(*args)
Cget_accDescription = _pyAAc.Cget_accDescription

def Cget_accKeyboardShortcut(*args):
  return _pyAAc.Cget_accKeyboardShortcut(*args)
Cget_accKeyboardShortcut = _pyAAc.Cget_accKeyboardShortcut

def Cget_accRole(*args):
  return _pyAAc.Cget_accRole(*args)
Cget_accRole = _pyAAc.Cget_accRole

def Cget_accState(*args):
  return _pyAAc.Cget_accState(*args)
Cget_accState = _pyAAc.Cget_accState

def CaccDoDefaultAction(*args):
  return _pyAAc.CaccDoDefaultAction(*args)
CaccDoDefaultAction = _pyAAc.CaccDoDefaultAction

def Cget_accValue(*args):
  return _pyAAc.Cget_accValue(*args)
Cget_accValue = _pyAAc.Cget_accValue

def Cget_accSelection(*args):
  return _pyAAc.Cget_accSelection(*args)
Cget_accSelection = _pyAAc.Cget_accSelection

def Cget_accFocus(*args):
  return _pyAAc.Cget_accFocus(*args)
Cget_accFocus = _pyAAc.Cget_accFocus

def Cset_accFocus(*args):
  return _pyAAc.Cset_accFocus(*args)
Cset_accFocus = _pyAAc.Cset_accFocus

def Cget_accHelp(*args):
  return _pyAAc.Cget_accHelp(*args)
Cget_accHelp = _pyAAc.Cget_accHelp

def Cget_accChildCount(*args):
  return _pyAAc.Cget_accChildCount(*args)
Cget_accChildCount = _pyAAc.Cget_accChildCount

def Cget_accParent(*args):
  return _pyAAc.Cget_accParent(*args)
Cget_accParent = _pyAAc.Cget_accParent

def CaccLocation(*args):
  return _pyAAc.CaccLocation(*args)
CaccLocation = _pyAAc.CaccLocation

def CaccSelect(*args):
  return _pyAAc.CaccSelect(*args)
CaccSelect = _pyAAc.CaccSelect

def CAccessibleObjectFromPoint(*args):
  return _pyAAc.CAccessibleObjectFromPoint(*args)
CAccessibleObjectFromPoint = _pyAAc.CAccessibleObjectFromPoint

def CAccessibleObjectFromWindow(*args):
  return _pyAAc.CAccessibleObjectFromWindow(*args)
CAccessibleObjectFromWindow = _pyAAc.CAccessibleObjectFromWindow

def CaccHitTest(*args):
  return _pyAAc.CaccHitTest(*args)
CaccHitTest = _pyAAc.CaccHitTest

def CaccNavigate(*args):
  return _pyAAc.CaccNavigate(*args)
CaccNavigate = _pyAAc.CaccNavigate

def CAccessibleChild(*args):
  return _pyAAc.CAccessibleChild(*args)
CAccessibleChild = _pyAAc.CAccessibleChild

def CAccessibleChildren(*args):
  return _pyAAc.CAccessibleChildren(*args)
CAccessibleChildren = _pyAAc.CAccessibleChildren

def CFastAccessibleChildren(*args):
  return _pyAAc.CFastAccessibleChildren(*args)
CFastAccessibleChildren = _pyAAc.CFastAccessibleChildren

def CAccessibleObjectFromEvent(*args):
  return _pyAAc.CAccessibleObjectFromEvent(*args)
CAccessibleObjectFromEvent = _pyAAc.CAccessibleObjectFromEvent

def CGetRoleText(*args):
  return _pyAAc.CGetRoleText(*args)
CGetRoleText = _pyAAc.CGetRoleText

def CGetStateText(*args):
  return _pyAAc.CGetStateText(*args)
CGetStateText = _pyAAc.CGetStateText

def CWindowFromAccessibleObject(*args):
  return _pyAAc.CWindowFromAccessibleObject(*args)
CWindowFromAccessibleObject = _pyAAc.CWindowFromAccessibleObject

def CSetWinEventHook(*args):
  return _pyAAc.CSetWinEventHook(*args)
CSetWinEventHook = _pyAAc.CSetWinEventHook

def CUnhookWinEvent(*args):
  return _pyAAc.CUnhookWinEvent(*args)
CUnhookWinEvent = _pyAAc.CUnhookWinEvent

def CComObject(*args):
  return _pyAAc.CComObject(*args)
CComObject = _pyAAc.CComObject

def CProcessFromAccessibleObject(*args):
  return _pyAAc.CProcessFromAccessibleObject(*args)
CProcessFromAccessibleObject = _pyAAc.CProcessFromAccessibleObject

def GetDesktopWindowHandle():
  return _pyAAc.GetDesktopWindowHandle()
GetDesktopWindowHandle = _pyAAc.GetDesktopWindowHandle


