from libopensesame.py3compat import *


class BaseDetector:
    
    def __init__(self, **kwargs):
        
        if 'experiment' not in kwargs:
            raise ValueError('BaseDetectors expects experiment keyword')
        self._experiment = kwargs['experiment']
        self._participant_variable = kwargs['participant_variable']

        
    @property
    def clock(self):
        
        return self._experiment.clock
    
    def prepare(self):
        
        pass
    
    def run(self):
        
        pass

    def close(self):
        
        pass
