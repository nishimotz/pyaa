'''
Functions for creating and parsing XPath like representations for objects in the
MSAA DOM.
'''
import AA

def Join(p1, p2):
  '''
  Join two paths together.
  
  @param p1: Left side of path
  @type p1: string
  @param p2: Right side of path
  @type p2: string
  @return: Joined path
  @rtype: string
  '''
  if p1 is None:
    p1 = ''
  if p2[0] == '/':
    return '%s%s' % (p1, p2)
  else:
    return '%s/%s' % (p1, p2)

def Build(ao):
  '''
  Build a path to the given AccessibleObject from the root object, the object
  just below the Desktop object in the DOM.
  
  @param ao: Object whose path we wish to build
  @type ao: L{AA.AccessibleObject}
  @return: Path to the object
  @rtype: string
  '''
  path = []
  parent = ao.Parent

  while parent.Name != 'Desktop' or parent.Role == AA.Constants.ROLE_SYSTEM_WINDOW:
    n = 0
    children = parent.Children
    for i in range(len(children)):
      child = children[i]
      # SNAFU: will comparing these four properties guarantee uniqueness?
      if (child.Role == ao.Role and child.State == ao.State and 
          child.ClassName == ao.ClassName and child.Location == ao.Location):
        n = i
        break

    # build this segment of the path
    path.append('%s[%d]' % (ao.RoleText, i))

    # iterate
    ao = parent
    parent = ao.Parent
  path.reverse()
  return '/' + '/'.join(path)

def Parse(path, ao):
  '''
  Retrieve a child object using its path rooted at the given ancestor.
  
  @param path: Path to the target object
  @type path: string
  @param ao: Object at the root of the path
  @type ao: AccessibleObject
  '''
  if path == '/':
    return ao
  segs = path.split('/')[1:]

  # handle one part of the path at a time
  for s in segs:
    i = s.find('[')
    role = s[:i]
    c = int(s[i+1:-1])
    try:
      child = ao.GetChild(c)
      if child.RoleText == role:
        ao = child
      else:
        # roles in path don't match
        return None
    except:
      return None

  return ao