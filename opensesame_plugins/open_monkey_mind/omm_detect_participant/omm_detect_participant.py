from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame.item import Item
from . import detectors


class OmmDetectParticipant(Item):
    
    def reset(self):
        
        self.var.detector = 'Form'
        self.var.fallback_detector = 'Form'
        self.var.serial_ports = 'COM3,COM4'  # Default: two example ports for RFID readers
        self.var.participant_variable = 'participant'
        self.var.min_rep = 1
        self.var.enable_duration = 'no'  # Optional timeout feature for RFID read
        self.var.read_duration = 5  # Timeout in seconds
        
    def prepare(self):
        
        self._init_detect_participant()
        self._detector.prepare()
        

    def _init_detect_participant(self):
            
        if hasattr(self, '_detector'):
            return
        if 'omm_detector' in self.python_workspace:
            self._detector = self.python_workspace['omm_detector']
            oslogger.info('reusing participant detector')
            return
        oslogger.info('initializing participant detector: {}'.format(
            self.var.detector))
        
          
        cls = getattr(detectors, self.var.detector)
        try:
            self._detector = cls(
                experiment=self.experiment,
                participant_variable=self.var.participant_variable,
                serial_ports=self.var.serial_ports,
                min_rep=self.var.min_rep,
                enable_duration=self.var.enable_duration,
                read_duration=self.var.read_duration
            )
        except Exception as e:
            oslogger.info(
                'failed to initialize ({}), falling back to: {}'.format(
                    e, self.var.fallback_detector))
            cls = getattr(detectors, self.var.fallback_detector)
            self._detector = cls(
                experiment=self.experiment,
                port=self.var.serial_ports
            )
        self.python_workspace['omm_detector'] = self._detector
        self.experiment.cleanup_functions.append(self._close_detector)
        
        
    def _close_detector(self):
        
        oslogger.info('closing detector')
        self._detector.close()
        
        
    def run(self):
        self.set_item_onset()
        self._detector.run()
        oslogger.info('identifier: {}'.format(self.experiment.var.get(self.var.participant_variable)))
    
        
        
        
        
        
        
        