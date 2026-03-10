from libopensesame.py3compat import *
from ._base_detector import BaseDetector
from libopensesame.oslogging import oslogger
from libopensesame import widgets

class Form(BaseDetector):
    
    def __init__(self, **kwargs):   
        super(Form, self).__init__(**kwargs)
        
    def clock(self):
        
        return self._experiment.clock
    
    def prepare(self):
        
        self._form = widgets.form(
            self._experiment,
            cols=(1),
            rows=(1, 5),
            item=self._experiment,
            clicks=self._experiment.var.form_clicks == u'yes'
        )
        label = widgets.label(
            self._form,
            text='Enter OMM participant identifier'
        )
        self._text_input = widgets.text_input(
            self._form,
            return_accepts=True,
            var=self._participant_variable
        )
        self._form.set_widget(label, (0, 0))
        self._form.set_widget(self._text_input, (0, 1))        

        
        
    def run(self):
        self._form._exec(focus_widget=self._text_input)
        self._experiment.var.set(
            self._participant_variable,
            '/{}/'.format(self._experiment.var.get(self._participant_variable))
        )
        
    def close(self):
        
        pass
