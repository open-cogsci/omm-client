from libopensesame.py3compat import *
from ._base_detector import BaseDetector
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard

class KeyPress(BaseDetector):
    
    def __init__(self, **kwargs):
        super(KeyPress, self).__init__(**kwargs)

    def clock(self):
        
        return self._experiment.clock
    
    def prepare(self):
        
        self._keyboard = Keyboard(self._experiment)
        
        
    def run(self):
        oslogger.info('ID VAR {}'.format(self._participant_variable))
        key, timestamp = self._keyboard.get_key()
        #oslogger.info('identifier: {}'.format(key))
        self._experiment.var.set(
            self._participant_variable,
            '/{}/'.format(key)
        )
        
        
    def close(self):
        
        pass
