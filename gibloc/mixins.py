from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
  
  @method_decorator(login_required)
  def dispatch(self,*argv,**kwargs):
    return super(LoginRequiredMixin,self).dispatch(*argv,**kwargs)
