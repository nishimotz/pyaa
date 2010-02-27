'''
Classes that aid in handling asynchronous results from MSAA.
'''
import threading, traceback, Queue

class Deferred(object):
  '''
  A placeholder for a result to be returned at a later time. An object can add
  handlers to this object that will be called in the order added when the result is
  ready.
  
  Instances of this object are thread safe.
  
  @ivar callbacks: Queue of callbacks the make when the result is ready
  @type callbacks: Queue.Queue
  @ivar called: Is the result ready?
  @type called: boolean
  @ivar result: Result to be returned to listeners
  @type result: list
  @ivar lock: Prevents reentry while making callbacks
  @type lock: threading.Lock  
  @ivar put_lock: Prevents new callbacks from being added while servicing a callback
  @type put_lock: threading.Lock
  '''
  def __init__(self):
    '''Initialize an instance.'''
    self.callbacks = Queue.Queue()
    self.called = False
    self.result = None
    self.lock = threading.Lock()
    self.put_lock = threading.Lock()

  def AddCallback(self, func, *args, **kwargs):
    '''
    Add a callback to this deferred object. The provided function will be called with
    a list of positional parameters followed by the positional and keyword arguments 
    given to this method.
    
    @param func: Function to be called when the result is ready
    @type func: function
    @param args: Positional arguments for the callback function
    @type args: list
    @param kwargs: Keyword arguments for the callback function
    @type kwargs: dictionary
    '''
    item = (func, args, kwargs)
    self.put_lock.acquire()
    self.callbacks.put(item)
    self.put_lock.release()
    # if we've been called, see if we need to make the callback ourself
    if self.called: self.MakeCalls()

  def Callback(self, *args):
    '''
    Called when the result is ready.
    
    @param args: Results to be passed to listeners
    @type args: list
    '''
    self.result = args
    self.called = True
    self.MakeCalls()

  def IsCalled(self):
    '''
    @return: Is the result ready?
    @rtype: boolean
    '''
    return self.called

  def MakeCalls(self):
    '''
    Inform all listeners of the result. Let each listener return its own result to
    be passed to all listeners further down the chain. Exceptions currently
    do no propogate.
    '''
    # check if someone else is handling the callbacks
    if not self.lock.acquire(False): return
    
    while 1:
      try:
        # prevent new material from getting added
        self.put_lock.acquire()
        func, args, kwargs = self.callbacks.get_nowait()
      except Queue.Empty:
        # no calls left to make
        # make sure we unlock the function lock before unlocking, otherwise
        #  some listeners might not be notified
        self.lock.release()
        self.put_lock.release()
        break
      self.put_lock.release()
      
      try:
        # let the callback return another result to pass to other listeners
        self.result = (func(*(self.result+args), **kwargs),)
      except Exception:
        traceback.print_exc()