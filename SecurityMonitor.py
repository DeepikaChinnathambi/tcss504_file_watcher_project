from observer import Observer
from observable import Observable



class SecurityMonitor(Observer, Observable):
    def __init__(self, observable, obs_id):
        Observer.__init__(self, observable, obs_id)
        Observable.__init__(self)





