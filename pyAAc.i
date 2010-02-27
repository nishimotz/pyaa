%module pyAAc

%include typemaps.i

%{
#include "windows.h"
#include "oleacc.h"
#include "comdef.h"
#include "atlbase.h"
// #include "winable.h"
#include <mshtml.h>
#include <exdisp.h>
%}

/* Set up an exception to raise and its helpers */
%{
#if 1
#define DBprintf if(0) printf
#else
#define DBprintf printf
#endif

  // an error to raise
  PyObject *Error = NULL;

  // a helper to convert integer error codes to python ints
  PyObject* Error_code(int hr) {
    return PyInt_FromLong(hr);
  }
%}

%init %{ // when the module is loaded
  // create the error object
  Error = PyErr_NewException("pyAA.Error", NULL, NULL);
  // put it in the module name space
  PyDict_SetItemString(d, "Error", Error);
  %}

%pythoncode %{
  # so we can export it
  Error = _pyAAc.Error
    %}

/* make sure CoInitialize gets called */
%init %{ // this should probably be done using win32com
  // should this be here or should we use the one from win32com?
  CoInitialize(NULL);
  %}

/* helpers for code below */
%{
  long sequence = 0;

  // convert an IAccessible to a Python Object the same way SWIG does
  PyObject* pAccessible2Python(IAccessible *ia) {
    DBprintf("IAccessible(%x)%5d->Package\n", ia, sequence++);
    return SWIG_NewPointerObj((void *) ia, SWIGTYPE_p_IAccessible, 0);
  }
  /* convert wide strings to normal */
  PyObject* Unicode2PythonString(WCHAR* str, int str_len)
    {
      char *nstr = new char[str_len+1];
      if(nstr == 0) {
  PyErr_SetString(PyExc_MemoryError, "Out of memory.");
  return NULL;
      }
      WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, str, -1, nstr, str_len+1, NULL, NULL);
      PyObject* res = PyString_FromStringAndSize(nstr, str_len);
      delete [] nstr;
      return res;
    }
%}

/* define some constants we'll need */

%constant int CHILDID_SELF = CHILDID_SELF;
%constant int E_NOINTERFACE = E_NOINTERFACE;
%constant int STATE_SYSTEM_UNAVAILABLE = STATE_SYSTEM_UNAVAILABLE;
%constant int STATE_SYSTEM_SELECTED = STATE_SYSTEM_SELECTED;
%constant int STATE_SYSTEM_FOCUSED = STATE_SYSTEM_FOCUSED;
%constant int STATE_SYSTEM_PRESSED = STATE_SYSTEM_PRESSED;
%constant int STATE_SYSTEM_CHECKED = STATE_SYSTEM_CHECKED;
%constant int STATE_SYSTEM_MIXED = STATE_SYSTEM_MIXED;
%constant int STATE_SYSTEM_READONLY = STATE_SYSTEM_READONLY;
%constant int STATE_SYSTEM_HOTTRACKED = STATE_SYSTEM_HOTTRACKED;
%constant int STATE_SYSTEM_DEFAULT = STATE_SYSTEM_DEFAULT;
%constant int STATE_SYSTEM_EXPANDED = STATE_SYSTEM_EXPANDED;
%constant int STATE_SYSTEM_COLLAPSED = STATE_SYSTEM_COLLAPSED;
%constant int STATE_SYSTEM_BUSY = STATE_SYSTEM_BUSY;
%constant int STATE_SYSTEM_FLOATING = STATE_SYSTEM_FLOATING;
%constant int STATE_SYSTEM_MARQUEED = STATE_SYSTEM_MARQUEED;
%constant int STATE_SYSTEM_ANIMATED = STATE_SYSTEM_ANIMATED;
%constant int STATE_SYSTEM_INVISIBLE = STATE_SYSTEM_INVISIBLE;
%constant int STATE_SYSTEM_OFFSCREEN = STATE_SYSTEM_OFFSCREEN;
%constant int STATE_SYSTEM_SIZEABLE = STATE_SYSTEM_SIZEABLE;
%constant int STATE_SYSTEM_MOVEABLE = STATE_SYSTEM_MOVEABLE;
%constant int STATE_SYSTEM_SELFVOICING = STATE_SYSTEM_SELFVOICING;
%constant int STATE_SYSTEM_FOCUSABLE = STATE_SYSTEM_FOCUSABLE;
%constant int STATE_SYSTEM_SELECTABLE = STATE_SYSTEM_SELECTABLE;
%constant int STATE_SYSTEM_LINKED = STATE_SYSTEM_LINKED;
%constant int STATE_SYSTEM_TRAVERSED = STATE_SYSTEM_TRAVERSED;
%constant int STATE_SYSTEM_MULTISELECTABLE = STATE_SYSTEM_MULTISELECTABLE;
%constant int STATE_SYSTEM_EXTSELECTABLE = STATE_SYSTEM_EXTSELECTABLE;
%constant int STATE_SYSTEM_ALERT_LOW = STATE_SYSTEM_ALERT_LOW;
%constant int STATE_SYSTEM_ALERT_MEDIUM = STATE_SYSTEM_ALERT_MEDIUM;
%constant int STATE_SYSTEM_ALERT_HIGH = STATE_SYSTEM_ALERT_HIGH;
%constant int STATE_SYSTEM_VALID = STATE_SYSTEM_VALID;

%constant int ROLE_SYSTEM_TITLEBAR = ROLE_SYSTEM_TITLEBAR;
%constant int ROLE_SYSTEM_MENUBAR = ROLE_SYSTEM_MENUBAR;
%constant int ROLE_SYSTEM_SCROLLBAR = ROLE_SYSTEM_SCROLLBAR;
%constant int ROLE_SYSTEM_GRIP = ROLE_SYSTEM_GRIP;
%constant int ROLE_SYSTEM_SOUND = ROLE_SYSTEM_SOUND;
%constant int ROLE_SYSTEM_CURSOR = ROLE_SYSTEM_CURSOR;
%constant int ROLE_SYSTEM_CARET = ROLE_SYSTEM_CARET;
%constant int ROLE_SYSTEM_ALERT = ROLE_SYSTEM_ALERT;
%constant int ROLE_SYSTEM_WINDOW = ROLE_SYSTEM_WINDOW;
%constant int ROLE_SYSTEM_CLIENT = ROLE_SYSTEM_CLIENT;
%constant int ROLE_SYSTEM_MENUPOPUP = ROLE_SYSTEM_MENUPOPUP;
%constant int ROLE_SYSTEM_MENUITEM = ROLE_SYSTEM_MENUITEM;
%constant int ROLE_SYSTEM_TOOLTIP = ROLE_SYSTEM_TOOLTIP;
%constant int ROLE_SYSTEM_APPLICATION = ROLE_SYSTEM_APPLICATION;
%constant int ROLE_SYSTEM_DOCUMENT = ROLE_SYSTEM_DOCUMENT;
%constant int ROLE_SYSTEM_PANE = ROLE_SYSTEM_PANE;
%constant int ROLE_SYSTEM_CHART = ROLE_SYSTEM_CHART;
%constant int ROLE_SYSTEM_DIALOG = ROLE_SYSTEM_DIALOG;
%constant int ROLE_SYSTEM_BORDER = ROLE_SYSTEM_BORDER;
%constant int ROLE_SYSTEM_GROUPING = ROLE_SYSTEM_GROUPING;
%constant int ROLE_SYSTEM_SEPARATOR = ROLE_SYSTEM_SEPARATOR;
%constant int ROLE_SYSTEM_TOOLBAR = ROLE_SYSTEM_TOOLBAR;
%constant int ROLE_SYSTEM_STATUSBAR = ROLE_SYSTEM_STATUSBAR;
%constant int ROLE_SYSTEM_TABLE = ROLE_SYSTEM_TABLE;
%constant int ROLE_SYSTEM_COLUMNHEADER = ROLE_SYSTEM_COLUMNHEADER;
%constant int ROLE_SYSTEM_ROWHEADER = ROLE_SYSTEM_ROWHEADER;
%constant int ROLE_SYSTEM_COLUMN = ROLE_SYSTEM_COLUMN;
%constant int ROLE_SYSTEM_ROW = ROLE_SYSTEM_ROW;
%constant int ROLE_SYSTEM_CELL = ROLE_SYSTEM_CELL;
%constant int ROLE_SYSTEM_LINK = ROLE_SYSTEM_LINK;
%constant int ROLE_SYSTEM_HELPBALLOON = ROLE_SYSTEM_HELPBALLOON;
%constant int ROLE_SYSTEM_CHARACTER = ROLE_SYSTEM_CHARACTER;
%constant int ROLE_SYSTEM_LIST = ROLE_SYSTEM_LIST;
%constant int ROLE_SYSTEM_LISTITEM = ROLE_SYSTEM_LISTITEM;
%constant int ROLE_SYSTEM_OUTLINE = ROLE_SYSTEM_OUTLINE;
%constant int ROLE_SYSTEM_OUTLINEITEM = ROLE_SYSTEM_OUTLINEITEM;
%constant int ROLE_SYSTEM_PAGETAB = ROLE_SYSTEM_PAGETAB;
%constant int ROLE_SYSTEM_PROPERTYPAGE = ROLE_SYSTEM_PROPERTYPAGE;
%constant int ROLE_SYSTEM_INDICATOR = ROLE_SYSTEM_INDICATOR;
%constant int ROLE_SYSTEM_GRAPHIC = ROLE_SYSTEM_GRAPHIC;
%constant int ROLE_SYSTEM_STATICTEXT = ROLE_SYSTEM_STATICTEXT;
%constant int ROLE_SYSTEM_TEXT = ROLE_SYSTEM_TEXT;
%constant int ROLE_SYSTEM_PUSHBUTTON = ROLE_SYSTEM_PUSHBUTTON;
%constant int ROLE_SYSTEM_CHECKBUTTON = ROLE_SYSTEM_CHECKBUTTON;
%constant int ROLE_SYSTEM_RADIOBUTTON = ROLE_SYSTEM_RADIOBUTTON;
%constant int ROLE_SYSTEM_COMBOBOX = ROLE_SYSTEM_COMBOBOX;
%constant int ROLE_SYSTEM_DROPLIST = ROLE_SYSTEM_DROPLIST;
%constant int ROLE_SYSTEM_PROGRESSBAR = ROLE_SYSTEM_PROGRESSBAR;
%constant int ROLE_SYSTEM_DIAL = ROLE_SYSTEM_DIAL;
%constant int ROLE_SYSTEM_HOTKEYFIELD = ROLE_SYSTEM_HOTKEYFIELD;
%constant int ROLE_SYSTEM_SLIDER = ROLE_SYSTEM_SLIDER;
%constant int ROLE_SYSTEM_SPINBUTTON = ROLE_SYSTEM_SPINBUTTON;
%constant int ROLE_SYSTEM_DIAGRAM = ROLE_SYSTEM_DIAGRAM;
%constant int ROLE_SYSTEM_ANIMATION = ROLE_SYSTEM_ANIMATION;
%constant int ROLE_SYSTEM_EQUATION = ROLE_SYSTEM_EQUATION;
%constant int ROLE_SYSTEM_BUTTONDROPDOWN = ROLE_SYSTEM_BUTTONDROPDOWN;
%constant int ROLE_SYSTEM_BUTTONMENU = ROLE_SYSTEM_BUTTONMENU;
%constant int ROLE_SYSTEM_BUTTONDROPDOWNGRID = ROLE_SYSTEM_BUTTONDROPDOWNGRID;
%constant int ROLE_SYSTEM_WHITESPACE = ROLE_SYSTEM_WHITESPACE;
%constant int ROLE_SYSTEM_PAGETABLIST = ROLE_SYSTEM_PAGETABLIST;
%constant int ROLE_SYSTEM_CLOCK = ROLE_SYSTEM_CLOCK;

%constant int GUI_CARETBLINKING = GUI_CARETBLINKING;
%constant int GUI_INMOVESIZE = GUI_INMOVESIZE;
%constant int GUI_INMENUMODE = GUI_INMENUMODE;
%constant int GUI_SYSTEMMENUMODE = GUI_SYSTEMMENUMODE;
%constant int GUI_POPUPMENUMODE = GUI_POPUPMENUMODE;
%constant int INPUT_MOUSE = INPUT_MOUSE;
%constant int INPUT_KEYBOARD = INPUT_KEYBOARD;
%constant int INPUT_HARDWARE = INPUT_HARDWARE;
%constant int OBJID_WINDOW = OBJID_WINDOW;
%constant int OBJID_SYSMENU = OBJID_SYSMENU;
%constant int OBJID_TITLEBAR = OBJID_TITLEBAR;
%constant int OBJID_MENU = OBJID_MENU;
%constant int OBJID_CLIENT = OBJID_CLIENT;
%constant int OBJID_VSCROLL = OBJID_VSCROLL;
%constant int OBJID_HSCROLL = OBJID_HSCROLL;
%constant int OBJID_SIZEGRIP = OBJID_SIZEGRIP;
%constant int OBJID_CARET = OBJID_CARET;
%constant int OBJID_CURSOR = OBJID_CURSOR;
%constant int OBJID_ALERT = OBJID_ALERT;
%constant int OBJID_SOUND = OBJID_SOUND;
// %constant int CCHILDREN_FRAME = CCHILDREN_FRAME;
%constant int ALERT_SYSTEM_INFORMATIONAL = ALERT_SYSTEM_INFORMATIONAL;
%constant int ALERT_SYSTEM_WARNING = ALERT_SYSTEM_WARNING;
%constant int ALERT_SYSTEM_ERROR = ALERT_SYSTEM_ERROR;
%constant int ALERT_SYSTEM_QUERY = ALERT_SYSTEM_QUERY;
%constant int ALERT_SYSTEM_CRITICAL = ALERT_SYSTEM_CRITICAL;
%constant int CALERT_SYSTEM = CALERT_SYSTEM;
%constant int WINEVENT_OUTOFCONTEXT = WINEVENT_OUTOFCONTEXT;
%constant int WINEVENT_SKIPOWNTHREAD = WINEVENT_SKIPOWNTHREAD;
%constant int WINEVENT_SKIPOWNPROCESS = WINEVENT_SKIPOWNPROCESS;
%constant int WINEVENT_INCONTEXT = WINEVENT_INCONTEXT;

%constant int EVENT_MIN = EVENT_MIN;
%constant int EVENT_MAX = EVENT_MAX;
%constant int EVENT_SYSTEM_SOUND = EVENT_SYSTEM_SOUND;
%constant int EVENT_SYSTEM_ALERT = EVENT_SYSTEM_ALERT;
%constant int EVENT_SYSTEM_FOREGROUND = EVENT_SYSTEM_FOREGROUND;
%constant int EVENT_SYSTEM_MENUSTART = EVENT_SYSTEM_MENUSTART;
%constant int EVENT_SYSTEM_MENUEND = EVENT_SYSTEM_MENUEND;
%constant int EVENT_SYSTEM_MENUPOPUPSTART = EVENT_SYSTEM_MENUPOPUPSTART;
%constant int EVENT_SYSTEM_MENUPOPUPEND = EVENT_SYSTEM_MENUPOPUPEND;
%constant int EVENT_SYSTEM_CAPTURESTART = EVENT_SYSTEM_CAPTURESTART;
%constant int EVENT_SYSTEM_CAPTUREEND = EVENT_SYSTEM_CAPTUREEND;
%constant int EVENT_SYSTEM_MOVESIZESTART = EVENT_SYSTEM_MOVESIZESTART;
%constant int EVENT_SYSTEM_MOVESIZEEND = EVENT_SYSTEM_MOVESIZEEND;
%constant int EVENT_SYSTEM_CONTEXTHELPSTART = EVENT_SYSTEM_CONTEXTHELPSTART;
%constant int EVENT_SYSTEM_CONTEXTHELPEND = EVENT_SYSTEM_CONTEXTHELPEND;
%constant int EVENT_SYSTEM_DRAGDROPSTART = EVENT_SYSTEM_DRAGDROPSTART;
%constant int EVENT_SYSTEM_DRAGDROPEND = EVENT_SYSTEM_DRAGDROPEND;
%constant int EVENT_SYSTEM_DIALOGSTART = EVENT_SYSTEM_DIALOGSTART;
%constant int EVENT_SYSTEM_DIALOGEND = EVENT_SYSTEM_DIALOGEND;
%constant int EVENT_SYSTEM_SCROLLINGSTART = EVENT_SYSTEM_SCROLLINGSTART;
%constant int EVENT_SYSTEM_SCROLLINGEND = EVENT_SYSTEM_SCROLLINGEND;
%constant int EVENT_SYSTEM_SWITCHSTART = EVENT_SYSTEM_SWITCHSTART;
%constant int EVENT_SYSTEM_SWITCHEND = EVENT_SYSTEM_SWITCHEND;
%constant int EVENT_SYSTEM_MINIMIZESTART = EVENT_SYSTEM_MINIMIZESTART;
%constant int EVENT_SYSTEM_MINIMIZEEND = EVENT_SYSTEM_MINIMIZEEND;
%constant int EVENT_OBJECT_CREATE = EVENT_OBJECT_CREATE;
%constant int EVENT_OBJECT_DESTROY = EVENT_OBJECT_DESTROY;
%constant int EVENT_OBJECT_SHOW = EVENT_OBJECT_SHOW;
%constant int EVENT_OBJECT_HIDE = EVENT_OBJECT_HIDE;
%constant int EVENT_OBJECT_REORDER = EVENT_OBJECT_REORDER;
%constant int EVENT_OBJECT_FOCUS = EVENT_OBJECT_FOCUS;
%constant int EVENT_OBJECT_SELECTION = EVENT_OBJECT_SELECTION;
%constant int EVENT_OBJECT_SELECTIONADD = EVENT_OBJECT_SELECTIONADD;
%constant int EVENT_OBJECT_SELECTIONREMOVE = EVENT_OBJECT_SELECTIONREMOVE;
%constant int EVENT_OBJECT_SELECTIONWITHIN = EVENT_OBJECT_SELECTIONWITHIN;
%constant int EVENT_OBJECT_STATECHANGE = EVENT_OBJECT_STATECHANGE;
%constant int EVENT_OBJECT_LOCATIONCHANGE = EVENT_OBJECT_LOCATIONCHANGE;
%constant int EVENT_OBJECT_NAMECHANGE = EVENT_OBJECT_NAMECHANGE;
%constant int EVENT_OBJECT_DESCRIPTIONCHANGE = EVENT_OBJECT_DESCRIPTIONCHANGE;
%constant int EVENT_OBJECT_VALUECHANGE = EVENT_OBJECT_VALUECHANGE;
%constant int EVENT_OBJECT_PARENTCHANGE = EVENT_OBJECT_PARENTCHANGE;
%constant int EVENT_OBJECT_HELPCHANGE = EVENT_OBJECT_HELPCHANGE;
%constant int EVENT_OBJECT_DEFACTIONCHANGE = EVENT_OBJECT_DEFACTIONCHANGE;
%constant int EVENT_OBJECT_ACCELERATORCHANGE = EVENT_OBJECT_ACCELERATORCHANGE;

%constant int SELFLAG_NONE = SELFLAG_NONE;
%constant int SELFLAG_TAKEFOCUS = SELFLAG_TAKEFOCUS;
%constant int SELFLAG_TAKESELECTION = SELFLAG_TAKESELECTION;
%constant int SELFLAG_EXTENDSELECTION = SELFLAG_EXTENDSELECTION;
%constant int SELFLAG_ADDSELECTION = SELFLAG_ADDSELECTION;
%constant int SELFLAG_REMOVESELECTION = SELFLAG_REMOVESELECTION;

%constant int NAVDIR_FIRSTCHILD = NAVDIR_FIRSTCHILD;
%constant int NAVDIR_LASTCHILD = NAVDIR_LASTCHILD;
%constant int NAVDIR_LEFT = NAVDIR_LEFT;
%constant int NAVDIR_RIGHT = NAVDIR_RIGHT;
%constant int NAVDIR_UP = NAVDIR_UP;
%constant int NAVDIR_DOWN = NAVDIR_DOWN;
%constant int NAVDIR_PREVIOUS = NAVDIR_PREVIOUS;
%constant int NAVDIR_NEXT = NAVDIR_NEXT;

// Tell SWIG about IAccessible
struct IAccessible {
};

// Add a destructor to the python interface
%extend IAccessible {
  void __del__() {
    DBprintf("IAccessible(%x)%5d->Release()\n", self, sequence++);
    Py_BEGIN_ALLOW_THREADS
    self->Release();
    Py_END_ALLOW_THREADS
    DBprintf("done\n");
  }
};

%typemap(check) IAccessible {
  if($1 == NULL) {
    PyErr_SetString(ValueError, "IAccessible is NULL.");
    return NULL;
  }
}

%wrapper %{
  void IAccessible_Release(IAccessible* self) {
    DBprintf("IAccessible(%x)%5d->Release()\n", self, sequence++);
    Py_BEGIN_ALLOW_THREADS;
    self->Release();
    Py_END_ALLOW_THREADS;
  }
  %}
void IAccessible_Release(IAccessible* self);

/* Implement IAccessible methods */

%wrapper %{
PyObject* Cget_accName(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d ", self, child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accName(varID, &bname);
  Py_END_ALLOW_THREADS
    DBprintf("hr=%x\n", hr);
  if(hr == S_FALSE || hr == E_NOTIMPL || hr == DISP_E_MEMBERNOTFOUND) {
    DBprintf("None\n");
    Py_INCREF(Py_None);
    return Py_None;
  } else if(hr != S_OK) {
    DBprintf("err\n");
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
  DBprintf("after\n");
#ifdef USE_UNICODE
  PyObject* res = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
  PyObject* res = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  ::SysFreeString(bname);
  DBprintf("done\n");
  return res;
}
 %}
PyObject* Cget_accName(IAccessible* self, long child);

%wrapper %{
  PyObject *Cget_accClass(IAccessible *self) {
    HWND hwnd;
    int hr;
    TCHAR buffer[256];
    PyObject* result = NULL;

    // get the window for the accessible object
    Py_BEGIN_ALLOW_THREADS;
    hr = WindowFromAccessibleObject(self, &hwnd);
    Py_END_ALLOW_THREADS;
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    // get the class name
    hr = GetClassName(hwnd, buffer, sizeof(buffer)/sizeof(TCHAR));
    if(hr == 0) {
      PyErr_SetObject(Error, Error_code(hr));
    } else {
#ifdef USE_UNICODE
      result = PyUnicode_FromWideChar(buffer, hr);
#else
      result = PyString_FromStringAndSize(buffer, hr);
#endif
    }
    return result;
  }
%}
PyObject *Cget_accClass(IAccessible *self);

%wrapper %{
PyObject* Cget_accDefaultAction(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d\n", self, child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accDefaultAction(varID, &bname);
  Py_END_ALLOW_THREADS
  VariantClear(&varID);
  if(hr == S_FALSE || hr == E_NOTIMPL || hr == DISP_E_MEMBERNOTFOUND) {
    Py_INCREF(Py_None);
    return Py_None;
  } else if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
#ifdef USE_UNICODE
  PyObject* res = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
  PyObject* res = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  ::SysFreeString(bname);
  return res;
}
 %}
PyObject* Cget_accDefaultAction(IAccessible* self, long child);

%wrapper %{
PyObject* Cget_accDescription(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d\n", self, child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accDescription(varID, &bname);
  Py_END_ALLOW_THREADS
  VariantClear(&varID);
  if(hr == S_FALSE || hr == E_NOTIMPL || hr == DISP_E_MEMBERNOTFOUND) {
    Py_INCREF(Py_None);
    return Py_None;
  } else if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
#ifdef USE_UNICODE
  PyObject* res = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
  PyObject* res = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  ::SysFreeString(bname);
  return res;
}
 %}
PyObject* Cget_accDescription(IAccessible* self, long child);

%wrapper %{
PyObject* Cget_accKeyboardShortcut(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d\n", self, child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accKeyboardShortcut(varID, &bname);
  Py_END_ALLOW_THREADS
  VariantClear(&varID);
  if(hr == S_FALSE || hr == E_NOTIMPL || hr == DISP_E_MEMBERNOTFOUND) {
    Py_INCREF(Py_None);
    return Py_None;
  } else if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
#ifdef USE_UNICODE
  PyObject* res = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
  PyObject* res = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  ::SysFreeString(bname);
  return res;
}
 %}
PyObject* Cget_accKeyboardShortcut(IAccessible* self, long child);

%wrapper %{
PyObject* Cget_accRole(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;
  _variant_t res = NULL;
  DBprintf("C++ self=%x child=%d %d\n", self, varID.vt, varID.iVal);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accRole(varID, &res);
  Py_END_ALLOW_THREADS
  if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  } else if (res.vt == VT_BSTR) {
  	PyObject *s;
#ifdef USE_UNICODE
	s = PyUnicode_FromWideChar(res.bstrVal, SysStringLen(res.bstrVal));
#else
  	s = Unicode2PythonString(res.bstrVal, SysStringByteLen(res.bstrVal));
#endif
	VariantClear(&res);
    return s;
  } else if (res.vt == VT_I4) {
  	return PyInt_FromLong(res);
  } else {
	Py_INCREF(Py_None);
  	return Py_None;
  }
}
%}
PyObject* Cget_accRole(IAccessible* self, long child);

%wrapper %{
PyObject* Cget_accState(IAccessible *self, long child) {
  int hr;
  _variant_t varID(child);
  _variant_t res;
  DBprintf("C++ self=%x child=%d %d\n", self, varID.vt, varID.iVal);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accState(varID, &res);
  Py_END_ALLOW_THREADS
  if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
  return PyInt_FromLong(res);
}
 %}
PyObject* Cget_accState(IAccessible* self, long child);

%wrapper %{
PyObject *CaccDoDefaultAction(IAccessible *self, long child) {
  int hr;
  _variant_t varID(child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->accDoDefaultAction(varID);
  Py_END_ALLOW_THREADS
  if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}
 %}
PyObject *CaccDoDefaultAction(IAccessible *self, long child);

%wrapper %{
PyObject *Cget_accValue(IAccessible *self, long child) {
  int hr;
  _variant_t varID = child;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d\n", self, child);
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accValue(varID, &bname);
  Py_END_ALLOW_THREADS
  if(hr == DISP_E_MEMBERNOTFOUND || hr == S_FALSE) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    return NULL;
  }
#ifdef USE_UNICODE
  PyObject* res = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
  PyObject* res = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  ::SysFreeString(bname);
  return res;
}
 %}
PyObject *Cget_accValue(IAccessible *self, long child);

%wrapper %{
PyObject *Cget_accSelection(IAccessible *self) {
  _variant_t res;
  PyObject* result;
  unsigned long fetched;

  int hr;
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accSelection(&res);
  Py_END_ALLOW_THREADS
// PP: Ignore the return value, it seems to be lying to us
//   if(hr == VT_EMPTY) {
//     Py_INCREF(Py_None);
//     DBprintf("==> accSelection: VT_EMPTY returned\n");
//     result = Py_None;
//   } else if(hr != S_OK) {
//     PyErr_SetObject(Error, Error_code(hr));
//     result = NULL;
//   } else {
  switch(res.vt) {
  case VT_EMPTY: {
    DBprintf("==> accSelection: VT_EMPTY in variant\n");
    Py_INCREF(Py_None);
    result = Py_None;
    break;
  }
  case VT_DISPATCH: {
    IAccessible* ia = NULL;
    IDispatch* pdisp = res;
    Py_BEGIN_ALLOW_THREADS
    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&ia);
    pdisp->Release();
    Py_END_ALLOW_THREADS
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
      result = pAccessible2Python(ia);
    }
    DBprintf("==> accSelection: VT_DISPATCH in variant\n");
    break;
  }
  case VT_I4: {
    result = PyInt_FromLong(res);
    DBprintf("==> accSelection: VT_I4 in variant\n");
    break;
  }
  case VT_UNKNOWN: {
    IEnumVARIANT *pev = NULL;
    IUnknown *puk = res;
    Py_BEGIN_ALLOW_THREADS
    hr = puk->QueryInterface(IID_IEnumVARIANT, (void**)&pev);
    puk->Release();
    Py_END_ALLOW_THREADS
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
      DBprintf("==> accSelection: VT_UNKNOWN in variant\n");
      // Brendon says: Basically, if IEnumVARIANT is supported, call
      // Next() once for each child with a count of 1 (some servers
      // have bugs if you pass anything else - eg. IE toolbar).
      Py_BEGIN_ALLOW_THREADS;
      pev->Reset();
      Py_END_ALLOW_THREADS;
      result = PyList_New(0);
      while(1) {
        _variant_t nxt;
        Py_BEGIN_ALLOW_THREADS;
        hr = pev->Next(1, &nxt, &fetched);
        Py_END_ALLOW_THREADS;
        if(hr == S_FALSE || hr == E_FAIL) { // done
          break;
        } else if (hr != S_OK) {
          PyErr_SetObject(Error, Error_code(hr));
          Py_DECREF(result);
          Py_BEGIN_ALLOW_THREADS;
          pev->Release();
          Py_END_ALLOW_THREADS;
          DBprintf("==> accSelection: next failed\n");
          return NULL;
        }
        if(nxt.vt == VT_I4) {
          // If the resulting VARIANT has a vt of VT_I4, call get_accChild
          // on it to see if you get back a dispatch - if you do, QI to
          // IAccessible pAccChild and use { pAccChild, CHILDID_SELF } as
          // your IAccessible/ChildID pair. If get_accChild didn't return
          // anything, then just use { pAccParent, lval } as the
          // IAccessible/ChildID pair.
          DBprintf("==> accSelection: child I4\n");
          IDispatch* pdisp = NULL;

          Py_BEGIN_ALLOW_THREADS;
          hr = self->get_accChild(nxt, &pdisp);
          Py_END_ALLOW_THREADS;

          if(hr == S_FALSE || hr == E_NOINTERFACE) { // not accessible use parent + this int
            PyObject* n = PyInt_FromLong(nxt);
            PyList_Append(result, n);
            Py_DECREF(n);
          } else if(hr != S_OK) {
            PyErr_SetObject(Error, Error_code(hr));
            Py_DECREF(result);
            Py_BEGIN_ALLOW_THREADS;
            pev->Release();
            Py_END_ALLOW_THREADS;
            DBprintf("get_accChild for next int hr=%x\n", hr);
            return NULL;
          } else {
            // got a dispatch, convert to IAccessible
            IAccessible *pacc;
            Py_BEGIN_ALLOW_THREADS;
            hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
            pdisp->Release();
            Py_END_ALLOW_THREADS;
            if(hr == S_OK) {
              PyObject* tmp = pAccessible2Python(pacc);
              PyList_Append(result, tmp);
              Py_DECREF(tmp);
            } else {
              PyErr_SetObject(Error, Error_code(hr));
              Py_DECREF(result);
              Py_BEGIN_ALLOW_THREADS;
              pev->Release();
              Py_END_ALLOW_THREADS;
              DBprintf("QI failed for disp->AI for VT_I4 hr=%x\n", hr);
              return NULL;
            }
          }
        } else if(nxt.vt == VT_DISPATCH) {
          // If the resulting VARIANT has a vt of VT_DISPATCH, QI it
          // to IAccessible "pAccChild", and use { pAccChild,
          // CHILDID_SELF } as your IAccessible/ChildID pair.
          DBprintf("DISPATCH\n");
          IDispatch *pdisp = nxt;
          IAccessible *pacc;
          Py_BEGIN_ALLOW_THREADS;
          hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
          pdisp->Release();
          Py_END_ALLOW_THREADS;
          if(hr == S_OK) {
            PyObject* tmp = pAccessible2Python(pacc);
            PyList_Append(result, tmp);
            Py_DECREF(tmp);
          } else {
            PyErr_SetObject(Error, Error_code(hr));
            Py_DECREF(result);
            Py_BEGIN_ALLOW_THREADS;
            pev->Release();
            Py_END_ALLOW_THREADS;
            DBprintf("QI failed for disp->AI for VT_DISPATCH hr=%x\n", hr);
            return NULL;
          }
        } else {
          fprintf(stderr, "unexpected VT in myAccessibleChildren\n");
        }
      }
      Py_BEGIN_ALLOW_THREADS;
      pev->Release();
      Py_END_ALLOW_THREADS;
    }
    break;
  }
	default: {
    PyErr_SetString(Error, "Invalid VARIANT in get_accSelection");
		result = NULL;
	}
	}
  return result;
}
 %}
PyObject *Cget_accSelection(IAccessible *self);

%wrapper %{
PyObject *Cget_accFocus(IAccessible *self) {
  _variant_t res;
  PyObject* result;

  int hr;
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accFocus(&res);
  Py_END_ALLOW_THREADS

  if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    result = NULL;
  } else {
    switch(res.vt) {
    case VT_EMPTY: {
      Py_INCREF(Py_None);
      result = Py_None;
      break;
    }
    case VT_DISPATCH: {
      IAccessible* ia = NULL;
      IUnknown* puk = res;
      Py_BEGIN_ALLOW_THREADS
      hr = puk->QueryInterface(IID_IAccessible, (void**)&ia);
      puk->Release();
      Py_END_ALLOW_THREADS
      if(hr != S_OK) {
        PyErr_SetObject(Error, Error_code(hr));
        result = NULL;
      } else {
        result = pAccessible2Python(ia);
      }
      break;
    }
    case VT_I4: {
      result = PyInt_FromLong(res);
      break;
    }
    default: {
      PyErr_SetString(Error, "Invalid VARIANT in get_accFocus");
      result = NULL;
    }
    }
  }
  return result;
}
 %}
PyObject *Cget_accFocus(IAccessible *self);

%wrapper %{
  PyObject* Cset_accFocus(IAccessible* ia) {
    HWND hwnd, old;
    DWORD me, other;
    int hr;
    PyObject *result;

    // get the window for the accessible object
    Py_BEGIN_ALLOW_THREADS;
    hr = WindowFromAccessibleObject(ia, &hwnd);
    Py_END_ALLOW_THREADS;
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(0));
      return NULL;
    }
    // get our thread id
    Py_BEGIN_ALLOW_THREADS;
    me = GetCurrentThreadId();
    // get the target window thread id
    other = GetWindowThreadProcessId(hwnd, NULL);
    // attach to that window's message queue
    hr = AttachThreadInput(other, me, 1);
    Py_END_ALLOW_THREADS;
    if(hr != 0) {
      // set the focus
      Py_BEGIN_ALLOW_THREADS;
      old = SetFocus(hwnd);
      Py_END_ALLOW_THREADS;
      if(old == NULL) {
        hr = SetForegroundWindow(hwnd);
        if(hr == 0) {
          PyErr_SetObject(Error, Error_code(1));
          result = NULL;
        } else {
          Py_INCREF(Py_None);
          result = Py_None;
        }
      } else {
        Py_INCREF(Py_None);
        result = Py_None;
      }
      // detach from the window's message queue
      Py_BEGIN_ALLOW_THREADS;
      AttachThreadInput(other, me, 0);
      Py_END_ALLOW_THREADS;
    } else {
      PyErr_SetObject(Error, Error_code(2));
      result = NULL;
    }
    return result;
  }
%}
PyObject* Cset_accFocus(IAccessible* self);

// # set a particular control to have the focus
// def SetFocus(hwnd):
//   me = kernel32.GetCurrentThreadId()
//   other = user32.GetWindowThreadProcessId(hwnd, None)
//   user32.AttachThreadInput(other, me, True)
//   try:
//     win32gui.SetFocus(hwnd)
//   except:
//     pass
//   user32.AttachThreadInput(other, me, False)

%wrapper %{
PyObject* Cget_accHelp(IAccessible *self, long child) {
  _variant_t varID = child;
  PyObject* result;

  BSTR bname = NULL;

  DBprintf("here self=%x child=%d\n", self, child);
  int hr;
  Py_BEGIN_ALLOW_THREADS
  hr = self->get_accHelp(varID, &bname);
  Py_END_ALLOW_THREADS

  if(hr == S_FALSE) {
    Py_INCREF(Py_None);
    result = Py_None;
  } else if(hr != S_OK) {
    PyErr_SetObject(Error, Error_code(hr));
    result = NULL;
  } else {
#ifdef USE_UNICODE
    result = PyUnicode_FromWideChar(bname, SysStringLen(bname));
#else
    result = Unicode2PythonString(bname, SysStringByteLen(bname));
#endif
  }
  ::SysFreeString(bname);
  return result;
}
 %}
PyObject* Cget_accHelp(IAccessible* self, long child);

%wrapper %{
  long Cget_accChildCount(IAccessible* self) {
    long result = 0;
    Py_BEGIN_ALLOW_THREADS
    int hr = self->get_accChildCount(&result);
    Py_END_ALLOW_THREADS
    return result;
  }
  %}
long Cget_accChildCount(IAccessible* self);
/*
%wrapper %{
  PyObject* Cget_accChild(IAccessible* self, long child) {
    int hr;
    _variant_t varID = child;
    IDispatch *pdisp = NULL;

    Py_BEGIN_ALLOW_THREADS
    hr = self->get_accChild(varID, &pdisp);
    Py_END_ALLOW_THREADS
    DBprintf("hr=%x pdisp=%x\n", hr, pdisp);
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    IAccessible *res = NULL;
    Py_BEGIN_ALLOW_THREADS
    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&res);
    pdisp->Release();
    Py_END_ALLOW_THREADS
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    return pAccessible2Python(res);
  }
  %}
PyObject* Cget_accChild(IAccessible* self, long child);
*/
%wrapper %{
  PyObject* Cget_accParent(IAccessible* self) {
    int hr;
    IDispatch *pdisp = NULL;

    Py_BEGIN_ALLOW_THREADS
    hr = self->get_accParent(&pdisp);
    Py_END_ALLOW_THREADS
    DBprintf("hr=%x pdisp=%x\n", hr, pdisp);
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    IAccessible *res = NULL;
    Py_BEGIN_ALLOW_THREADS
    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&res);
    pdisp->Release();
    Py_END_ALLOW_THREADS
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    return pAccessible2Python(res);
  }
  %}
PyObject* Cget_accParent(IAccessible* self);

%wrapper %{
  PyObject* CaccLocation(IAccessible* self, long child) {
    PyObject* result;

    _variant_t varID = child;
    long left, top, width, height;
    int hr;
    Py_BEGIN_ALLOW_THREADS
    hr = self->accLocation(&left, &top, &width, &height, varID);
    Py_END_ALLOW_THREADS
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
      result = Py_BuildValue("(iiii)", left, top, width, height);
    }
    return result;
  }
%}
PyObject* CaccLocation(IAccessible* self, long child);

%wrapper %{
  PyObject* CaccSelect(IAccessible* self, long flagsSelect, long child) {
    _variant_t varID = child;
//    HWND hwnd;
//    DWORD me, other;
    int hr;
    PyObject *result = NULL;

//     // get the window for the accessible object
//     Py_BEGIN_ALLOW_THREADS;
//     hr = WindowFromAccessibleObject(self, &hwnd);
//     Py_END_ALLOW_THREADS;
//     if(hr != S_OK) {
//       PyErr_SetObject(Error, Error_code(hr));
//       return NULL;
//     }
//     // get our thread id
//     Py_BEGIN_ALLOW_THREADS;
//     me = GetCurrentThreadId();
//     // get the target window thread id
//     other = GetWindowThreadProcessId(hwnd, NULL);
//     // attach to that window's message queue
//     AttachThreadInput(other, me, 1);
    Py_BEGIN_ALLOW_THREADS;
    hr = self->accSelect(flagsSelect, varID);
    Py_END_ALLOW_THREADS;
    if (hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
    } else {
      Py_INCREF(Py_None);
      result = Py_None;
    }
//     Py_BEGIN_ALLOW_THREADS;
//     AttachThreadInput(other, me, 0);
//     Py_END_ALLOW_THREADS;
    return result;
  }
%}
PyObject* CaccSelect(IAccessible* self, long flagsSelect, long child);

%typemap(in) POINT p (POINT tmp) {
  if(!PySequence_Check($input) || PySequence_Size($input) != 2) {
    PyErr_SetString(PyExc_ValueError, "Point argument must be length 2 sequence.");
    return NULL;
  }
  PyObject* tx = PySequence_GetItem($input, 0);
  PyObject* ty = PySequence_GetItem($input, 1);
  if(!PyInt_Check(tx) || !PyInt_Check(ty)) {
    PyErr_SetString(PyExc_ValueError, "Point argument must be 2 integers.");
    return NULL;
  }
  tmp.x = PyInt_AsLong(tx);
  tmp.y = PyInt_AsLong(ty);
  $1 = tmp;
}

%wrapper %{
  PyObject* CAccessibleObjectFromPoint(POINT p)
   {
     PyObject* result;
     _variant_t pvarChild;
     IAccessible *ia;

     int hr;
     Py_BEGIN_ALLOW_THREADS
     hr = AccessibleObjectFromPoint(p, &ia, &pvarChild);
     Py_END_ALLOW_THREADS

     if(hr != S_OK) {
       PyErr_SetObject(Error, Error_code(hr));
       result = NULL;
     } else {
       result = Py_BuildValue("(Ni)", pAccessible2Python(ia), (long)pvarChild);
     }
     return result;
   }
  %}
PyObject* CAccessibleObjectFromPoint(POINT p);

%wrapper %{
  PyObject* CAccessibleObjectFromWindow(int hwnd, long objid)
   {
     PyObject* result;
     IAccessible *ia;

     int hr;
     Py_BEGIN_ALLOW_THREADS
     hr = AccessibleObjectFromWindow((HWND)hwnd, objid, IID_IAccessible, (void **)&ia);
     Py_END_ALLOW_THREADS

     if(hr != S_OK) {
       PyErr_SetObject(Error, Error_code(hr));
       result = NULL;
     } else {

       result = Py_BuildValue("(Ni)", pAccessible2Python(ia), (long)CHILDID_SELF);
     }
     return result;
   }
  %}
PyObject* CAccessibleObjectFromWindow(int hwnd, long objid);

%wrapper %{
  PyObject* CaccHitTest(IAccessible* self, POINT p) {
    PyObject* result;
    _variant_t res;
    int hr;

    Py_BEGIN_ALLOW_THREADS
    hr = self->accHitTest(p.x, p.y, &res);
    Py_END_ALLOW_THREADS
    if(hr == S_FALSE || hr == DISP_E_MEMBERNOTFOUND || res.vt == VT_EMPTY) {
      Py_INCREF(Py_None);
      result = Py_None;
    } else {
      switch(res.vt) {
      case VT_I4: {
        result = PyInt_FromLong(res);
        break;
      }
      case VT_DISPATCH: {
        IDispatch* pdisp = res;
        IAccessible* pacc = NULL;
        Py_BEGIN_ALLOW_THREADS
        hr = self->QueryInterface(IID_IAccessible, (void**)&pacc);
        Py_END_ALLOW_THREADS
        if(hr != S_OK) {
          PyErr_SetObject(Error, Error_code(hr));
          result = NULL;
        } else {
          result = pAccessible2Python(pacc);
        }
        break;
      }
      default: {
        PyErr_SetString(Error, "Invalid vt from accHitTest");
        result = NULL;
      }
      }
    }
    return result;
  }
%}
PyObject* CaccHitTest(IAccessible* self, POINT p);

%wrapper %{
	PyObject *CaccNavigate(IAccessible* self, long child, long navDir) {
		int hr;
		_variant_t varID = child;
		_variant_t res;
		PyObject *result = NULL;;

    Py_BEGIN_ALLOW_THREADS
    hr = self->accNavigate(navDir, varID, &res);
    Py_END_ALLOW_THREADS

    // check the return value first
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return result;
    }

    // now check the return variant for a result
    switch(res.vt) {
    case VT_EMPTY: {
      Py_INCREF(Py_None);
      result = Py_None;
    	break;
   	}
    case VT_I4: {
	    result = PyInt_FromLong(res);
  	  DBprintf("==> accSelection: VT_I4 in variant\n");
    	break;
    }
    case VT_DISPATCH: {
	    IAccessible* ia = NULL;
	    IDispatch* pdisp = res;
	    Py_BEGIN_ALLOW_THREADS
	    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&ia);
	    pdisp->Release();
	    Py_END_ALLOW_THREADS
	    if(hr != S_OK) {
	      PyErr_SetObject(Error, Error_code(hr));
	      result = NULL;
	    } else {
	      result = pAccessible2Python(ia);
	    }
	    DBprintf("==> accSelection: VT_DISPATCH in variant\n");
	    break;
	  }
    default: {
			PyErr_SetString(Error, "Invalid vt from accHitTest");
			result = NULL;
    }
    }
    return result;
	}
%}
PyObject *CaccNavigate(IAccessible* self, long child, long navDir);

%wrapper %{
	PyObject *CAccessibleChild(IAccessible *ia, long index) {
		VARIANT *child;
		long num_got;
		long hr;
		long count;
		IDispatch* pdisp = NULL;
		PyObject *res = NULL;

    // allocate space for all children
    Py_BEGIN_ALLOW_THREADS
 		hr = ia->get_accChildCount(&count);
	  Py_END_ALLOW_THREADS
	  child = new VARIANT[count];
		Py_BEGIN_ALLOW_THREADS
	  hr = AccessibleChildren(ia, 0, count, child, &num_got);
	  Py_END_ALLOW_THREADS
	  if (index >= num_got) {
		  PyErr_SetString(Error, "Child index out of range");
		  res = NULL;
	  } else if(hr == S_OK || hr == S_FALSE) {
	  	if(child[index].vt == VT_I4) {
			  // not accessible use parent + this int
			  PyObject* n = PyInt_FromLong(child[index].lVal);
				return n;
		 	} else if(child[index].vt == VT_DISPATCH) {
				// got a dispatch, convert to IAccessible
			  IAccessible *pacc;
			  IDispatch *pdisp = child[index].pdispVal;
			  Py_BEGIN_ALLOW_THREADS
			  hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
			  pdisp->Release();
			  Py_END_ALLOW_THREADS
			  if(hr == S_OK) {
 			    return pAccessible2Python(pacc);
			  } else {
			    PyErr_SetObject(Error, Error_code(hr));
			    DBprintf("QI failed in CAccessibleChild hr=%x\n", hr);
			    res = NULL;
			  }
		  } else {
		    PyErr_SetObject(Error, Error_code(hr));
		    DBprintf("Unexpected value in CAccessibleChild hr=%x\n", hr);
				res = NULL;
			}
	  } else {
	    PyErr_SetObject(Error, Error_code(hr));
	    DBprintf("AccessibleChildren failed in CAccessibleChild hr=%x\n", hr);
	    res = NULL;
	  }
	  delete [] child;
	  return res;
	}
%}
PyObject *CAccessibleChild(IAccessible *ia, long index);

%wrapper %{
	PyObject *CAccessibleChildren(IAccessible *ia, long index, long count) {
		VARIANT *child;
		long num_got;
		long hr;
		IDispatch* pdisp = NULL;
		// list to return
		PyObject *res = PyList_New(0);

	  // allocate space for all children
	  child = new VARIANT[count];
		Py_BEGIN_ALLOW_THREADS
	  hr = AccessibleChildren(ia, index, count, child, &num_got);
	  Py_END_ALLOW_THREADS
	  if(hr == S_OK || hr == S_FALSE) {
	  	//fprintf(stderr, "index=%d requested=%d got=%d code=%d\n", index, count, num_got, hr);
	  	for(long i = 0; i < num_got; i++) {
		  	if(child[i].vt == VT_I4) {
			  	// not accessible use parent + this int
			    PyObject* n = PyInt_FromLong(child[i].lVal);
			    PyList_Append(res, n);
			    Py_DECREF(n);
		  	} else if(child[i].vt == VT_DISPATCH) {
			  	// got a dispatch, convert to IAccessible
			    IAccessible *pacc;
			    IDispatch *pdisp = child[i].pdispVal;
			    Py_BEGIN_ALLOW_THREADS
			    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
			    pdisp->Release();
			    Py_END_ALLOW_THREADS
			    if(hr == S_OK) {
 			      PyObject* tmp = pAccessible2Python(pacc);
			      PyList_Append(res, tmp);
			      Py_DECREF(tmp);
			    } else {
			      PyErr_SetObject(Error, Error_code(hr));
			      DBprintf("QI failed in CAccessibleChild hr=%x\n", hr);
						Py_DECREF(res);
			      res = NULL;
			      break;
			    }
			  } else {
		      PyErr_SetObject(Error, Error_code(hr));
		      DBprintf("Unexpected value in CAccessibleChild hr=%x\n", hr);
		      Py_DECREF(res);
					res = NULL;
				}
		  }
	  } else {
	    PyErr_SetObject(Error, Error_code(hr));
	    DBprintf("AccessibleChildren failed in CAccessibleChild hr=%x\n", hr);
	    Py_DECREF(res);
	    res = NULL;
	  }
	  delete [] child;
	  return res;
	}
%}
PyObject *CAccessibleChildren(IAccessible *ia, long index, long count);

%wrapper %{
  PyObject* CFastAccessibleChildren(IAccessible* ia) {
  	unsigned long fetched;
  	long N = 0;
		int hr;
		Py_BEGIN_ALLOW_THREADS
		hr = ia->get_accChildCount(&N);
		Py_END_ALLOW_THREADS
		DBprintf("N=%d\n", N);
		PyObject *res;

		// return an empty list if no children
    if(N==0) return PyList_New(0);

    // does it support IEnumVARIANT?
    IEnumVARIANT *pev = NULL;
    Py_BEGIN_ALLOW_THREADS
    hr = ia->QueryInterface(IID_IEnumVARIANT, (void**)&pev);
    Py_END_ALLOW_THREADS
    if(hr == S_OK) {
      // Brendon says: Basically, if IEnumVARIANT is supported, call
      // Next() once for each child with a count of 1 (some servers
      // have bugs if you pass anything else - eg. IE toolbar).
      // build list to return
      res = PyList_New(0);
      DBprintf("IEnum\n");
      Py_BEGIN_ALLOW_THREADS
      pev->Reset();
      Py_END_ALLOW_THREADS
      for(int i=1; i<=N; i++) {
	      _variant_t nxt;
			  DBprintf("i=%d\n", i);

			  Py_BEGIN_ALLOW_THREADS
			  // PP: need to pass unsigned long as third param, not NULL
			  hr = pev->Next(1, &nxt, &fetched);
			  Py_END_ALLOW_THREADS

			  if(hr == S_FALSE || hr == E_FAIL) { // done
			    DBprintf("early quit\n");
			    break;
			  } else if (hr != S_OK) {
			    PyErr_SetObject(Error, Error_code(hr));
			    Py_DECREF(res);
			    Py_BEGIN_ALLOW_THREADS
			    pev->Release();
			    Py_END_ALLOW_THREADS
			    DBprintf("next failed hr=%x\n", hr);
			    return NULL;
			  } else if(nxt.vt == VT_I4) {
			    // If the resulting VARIANT has a vt of VT_I4, call get_accChild
			    // on it to see if you get back a dispatch - if you do, QI to
			    // IAccessible pAccChild and use { pAccChild, CHILDID_SELF } as
			    // your IAccessible/ChildID pair. If get_accChild didn't return
			    // anything, then just use { pAccParent, lval } as the
			    // IAccessible/ChildID pair.
			    DBprintf("I4\n");
			    IDispatch* pdisp = NULL;

			    Py_BEGIN_ALLOW_THREADS
			    hr = ia->get_accChild(nxt, &pdisp);
			    Py_END_ALLOW_THREADS

			    if(hr == S_FALSE || hr == E_NOINTERFACE) { // not accessible use parent + this int
			      PyObject* n = PyInt_FromLong(nxt);
			      PyList_Append(res, n);
			      Py_DECREF(n);
			    } else if(hr != S_OK) {
			      PyErr_SetObject(Error, Error_code(hr));
			      Py_DECREF(res);
			      Py_BEGIN_ALLOW_THREADS
			      pev->Release();
			      Py_END_ALLOW_THREADS
			      DBprintf("get_accChild for next int hr=%x\n", hr);
			      return NULL;
			    } else {
			      // got a dispatch, convert to IAccessible
			      IAccessible *pacc;
			      Py_BEGIN_ALLOW_THREADS
			      hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
			      pdisp->Release();
			      Py_END_ALLOW_THREADS
			      if(hr == S_OK) {
			        PyObject* tmp = pAccessible2Python(pacc);
			        PyList_Append(res, tmp);
			        Py_DECREF(tmp);
			      } else {
			        PyErr_SetObject(Error, Error_code(hr));
			        Py_DECREF(res);
			        Py_BEGIN_ALLOW_THREADS
			        pev->Release();
			        Py_END_ALLOW_THREADS
			        DBprintf("QI failed for disp->AI for VT_I4 hr=%x\n", hr);
			        return NULL;
			      }
			    }
			  } else if(nxt.vt == VT_DISPATCH) {
			    // If the resulting VARIANT has a vt of VT_DISPATCH, QI it
			    // to IAccessible "pAccChild", and use { pAccChild,
			    // CHILDID_SELF } as your IAccessible/ChildID pair.
			    DBprintf("DISPATCH\n");
			    IDispatch *pdisp = nxt;
			    IAccessible *pacc;
			    Py_BEGIN_ALLOW_THREADS
			    hr = pdisp->QueryInterface(IID_IAccessible, (void**)&pacc);
			    pdisp->Release();
			    Py_END_ALLOW_THREADS
			    if(hr == S_OK) {
				    DBprintf("DISPATCH: S_OK\n");
			      PyObject* tmp = pAccessible2Python(pacc);
			      PyList_Append(res, tmp);
			      Py_DECREF(tmp);
			    } else {
			      PyErr_SetObject(Error, Error_code(hr));
			      Py_DECREF(res);
			      Py_BEGIN_ALLOW_THREADS
			      pev->Release();
			      Py_END_ALLOW_THREADS
			      DBprintf("QI failed for disp->AI for VT_DISPATCH hr=%x\n", hr);
			      return NULL;
			    }
			  } else {
			    fprintf(stderr, "unexpected VT in myAccessibleChildren\n");
			  }
      }
	    DBprintf("Done iterating IEnum\n");
      Py_BEGIN_ALLOW_THREADS
      pev->Release();
      Py_END_ALLOW_THREADS

    } else {
    	// no IEnumVARIANT interface, use CAccessibleChildren
			res = CAccessibleChildren(ia, 0, N);
    }
    DBprintf("returning normally");
    return res;
  }
%}
PyObject* CFastAccessibleChildren(IAccessible *ia);

%wrapper %{
  PyObject* CAccessibleObjectFromEvent(long hwnd, long objid, long childid) {
    IAccessible* ia;
    PyObject* result;
    _variant_t varId;
    int hr;

    DBprintf("AOFE hwnd=%x objid=%x childid=%x\n", hwnd, objid, childid);
    Py_BEGIN_ALLOW_THREADS
    hr = AccessibleObjectFromEvent((HWND)hwnd, objid, childid, &ia, &varId);
    Py_END_ALLOW_THREADS
      DBprintf("AOFE hr=%x\n", hr);
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
      result = Py_BuildValue("(Ni)", pAccessible2Python(ia), (long)varId);
    }
    DBprintf("exit aofe\n");
    return result;
  }
  %}
PyObject* CAccessibleObjectFromEvent(int hwnd, long objid, long childid);

%wrapper %{
  PyObject* CGetRoleText(long role) {
    int len;
    char* rolestring;

    Py_BEGIN_ALLOW_THREADS
    len = GetRoleText(role, 0, 0);
    rolestring = new char[len+1];
    GetRoleText(role, rolestring, len+1);
    Py_END_ALLOW_THREADS
    PyObject* res = PyString_FromString(rolestring);
    delete [] rolestring;
    return res;
  }
  %}
PyObject* CGetRoleText(long role);

%wrapper %{
  PyObject* CGetStateText(long state) {
    int len;
    char* statestring;
    Py_BEGIN_ALLOW_THREADS
    len = GetStateText(state, 0, 0);
    statestring = new char[len+1];
    GetStateText(state, statestring, len+1);
    Py_END_ALLOW_THREADS
    PyObject* res = PyString_FromString(statestring);
    delete [] statestring;
    return res;
  }
  %}
PyObject* CGetStateText(long state);

%wrapper %{
  PyObject* CWindowFromAccessibleObject(IAccessible* ia) {
    HWND hwnd;
    int hr;
    PyObject* result;
    Py_BEGIN_ALLOW_THREADS;
    hr = WindowFromAccessibleObject(ia, &hwnd);
    Py_END_ALLOW_THREADS;
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
      result = PyInt_FromLong((long)hwnd);
    }
    return result;
  }
  %}
PyObject* CWindowFromAccessibleObject(IAccessible* ia);

%wrapper %{
  PyObject* pyproc = NULL;
  void CALLBACK myproc(HWINEVENTHOOK hWinEventHook,
           DWORD event,
           HWND hwnd,
           LONG idObject,
           LONG idChild,
           DWORD dwEventThread,
           DWORD dwmsEventTime) {
    //printf("* C: callback %x %x %x %x %x %x %x\n", hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime);
	  // acquire the GIL using new 2.3 function

  	PyGILState_STATE gil = PyGILState_Ensure();
	  // Now we can use the API to get the python callback
  	if(pyproc) {
    	PyObject* args = Py_BuildValue("(iiiiiii)", (long)hWinEventHook, event, hwnd, idObject,
  	                                 idChild, dwEventThread, dwmsEventTime);
	    PyObject* res = PyEval_CallObject(pyproc, args);
	    Py_DECREF(args);
	    if(res == NULL) { // error in the callback
	      PyErr_Print();
	    } else {
	      Py_DECREF(res);
	    }
	  }
	  PyGILState_Release(gil);
  	DBprintf("GIL released\n");
  }

  PyObject* CSetWinEventHook(int emin, int emax, PyObject* callback, int idProcess, int idThread, int flags) {
    PyObject *result;
    if(!PyCallable_Check(callback)) {
      PyErr_SetString(PyExc_TypeError, "callback must be callable");
      return NULL;
    }

    // store the callback the first time only
    if(!pyproc) pyproc = callback;
    HWINEVENTHOOK he;

    Py_BEGIN_ALLOW_THREADS
    he = SetWinEventHook(emin, emax, 0, myproc, idProcess, idThread, flags);
    DBprintf("he=%x\n", he);
    Py_END_ALLOW_THREADS;
		result = PyInt_FromLong((long)he);
    return result;
  }

  %}
PyObject* CSetWinEventHook(int emin, int emax, PyObject* callback, int idProcess, int idThread, int flags);

%wrapper %{
  int CUnhookWinEvent(int hevent) {
    int result;
    Py_BEGIN_ALLOW_THREADS;
    //printf("C: CUnhookWinEvent %x\n", hevent);
    result = UnhookWinEvent((HWINEVENTHOOK)hevent);
    Py_END_ALLOW_THREADS;
    return result;
  }
  %}
int CUnhookWinEvent(int hevent);

%wrapper %{
  /* get the function we need from the win32com package using explicit linking */
  typedef PyObject* (*PYCOM_PYOBJECTFROMIUNKNOWN)(IUnknown *punk,
              REFIID riid,
              BOOL bAddRef);
  PYCOM_PYOBJECTFROMIUNKNOWN PyCom_PyObjectFromIUnknown = NULL;
  void GetPythoncomDLL() {
    /* this should use the version of figure out the name */
    HINSTANCE hDLL = LoadLibrary("pythoncom26");
    if (hDLL != NULL) {
      PyCom_PyObjectFromIUnknown = (PYCOM_PYOBJECTFROMIUNKNOWN)
  GetProcAddress(hDLL, "PyCom_PyObjectFromIUnknown");
    }
    if (hDLL == NULL || PyCom_PyObjectFromIUnknown == NULL) {
      fprintf(stderr, "Explicit link to pythoncom26.dll failed\n");
    }
  }
  %}
%init %{
  GetPythoncomDLL();
  %}

%wrapper %{
  // From Mark Hammond's code
// Convert a "char *" to a BSTR - free via ::SysFreeString()

  PyObject* CComObject(IAccessible *self, char* iidstr) {
    HRESULT hr;
    IServiceProvider* pSP;

    Py_BEGIN_ALLOW_THREADS;
    hr = self->QueryInterface(IID_IServiceProvider, (void**)&pSP);
    Py_END_ALLOW_THREADS;

    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }

    // convert the string into a BSTR
    int len = strlen(iidstr);
    BSTR bstr = SysAllocStringLen(NULL, len);
    if (bstr==NULL) {
      PyErr_SetString(PyExc_MemoryError, "allocating BSTR");
      return NULL;
    }
    MultiByteToWideChar(CP_ACP, 0, iidstr, len, bstr, len);

    // get the clsid
    CLSID clsid;
    Py_BEGIN_ALLOW_THREADS;
    hr = CLSIDFromString(bstr, &clsid);
    Py_END_ALLOW_THREADS;
    if (!SUCCEEDED(hr)) {
      PyErr_SetObject(Error, Error_code(hr));
      Py_BEGIN_ALLOW_THREADS;
      pSP->Release();
      Py_END_ALLOW_THREADS;
      return NULL;
    }
    SysFreeString(bstr);

    // try to get the requested interface
    IUnknown *pUnk;
    Py_BEGIN_ALLOW_THREADS;
    hr = pSP->QueryService(clsid, clsid, (void**)&pUnk);
    pSP->Release();
    Py_END_ALLOW_THREADS;
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      return NULL;
    }
    // wrap it for use by Mark Hammond's win32com package
    PyObject* result = PyCom_PyObjectFromIUnknown(pUnk, IID_IDispatch, FALSE);

    return result;
  }
  %}
PyObject* CComObject(IAccessible* self, char* str_iid);

// PP: added function retrieve process and thread IDs
%wrapper %{
  PyObject* CProcessFromAccessibleObject(IAccessible* self) {
  	PyObject *result;
  	HWND hwnd;
    int hr;
    DWORD processID;
    DWORD threadID;

    Py_BEGIN_ALLOW_THREADS;
    hr = WindowFromAccessibleObject(self, &hwnd);
    Py_END_ALLOW_THREADS;
    if(hr != S_OK) {
      PyErr_SetObject(Error, Error_code(hr));
      result = NULL;
    } else {
	    Py_BEGIN_ALLOW_THREADS;
	 		threadID = GetWindowThreadProcessId(hwnd, &processID);
	 		Py_END_ALLOW_THREADS;
      result = Py_BuildValue("(ii)", processID, threadID);
    }
    return result;
  }
  %}
PyObject* CProcessFromAccessibleObject(IAccessible* self);

%wrapper %{
	PyObject *GetDesktopWindowHandle() {
		HWND hwnd;
		Py_BEGIN_ALLOW_THREADS
		hwnd = GetDesktopWindow();
		Py_END_ALLOW_THREADS
		return PyInt_FromLong((long)hwnd);
	}
%}
PyObject *GetDesktopWindowHandle();