class Choices(object):
  def __init__(self):
    self._registry={}

  def register(self,cls):
    id=len(self._registry)+1
    cls.id=id
    self._registry[id]=cls

  def as_list(self):
    l=[]
    for id in sorted(self._registry):
      l.append((id,self._registry[id].name))
    return l

  def get_choice(self,id):
    return self._registry[id]
