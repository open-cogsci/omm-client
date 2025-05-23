=====================================================
plugins/omm_conditionner
=====================================================
_juice_pump_cdp.py
    juice() method renamed to reward()  (prevent to modify omm_conditionner.py)

_polulu_tic_t825
    Device added to control stepper motor base on polulu Tic t825


=====================================================
plugins/omm_detect_participant
=====================================================
restructuring omm_detect_participant similarly to how omm_conditionner is organized, with a dedicated subdirectory for each detection method (e.g., Form, Keypress, RFID Card 1, RFID Card N, etc.).
This structure would make it easier for everyone to contribute or maintain their own modules without interfering with others’, and would simplify future development and code reviews. What do you think?

omm_detect_participant/
├── init.py
├── omm_detect_participant.py                  # common interface
   ├── detectors/
        ├── init.py
        ├── _base_detector.py
        ├── _form_detector.py
        ├── _keyboard_detector.py
        ├── _rfid_base.py                      #generic rfid support
        ├── _rfid_rfidrwettl.py                #RFIDRWETTL from priority1Design support added



_rfid_base.py
    .Integration of the code to support multiple RFID readers writed by Clement Yasar 
    The _rfid_monitor function has been changed to a static method of the RFID object to allow it to be redefined when needed (for example, in _rfid_rfidrwettl.py).
    Extra argument added (baudrate)