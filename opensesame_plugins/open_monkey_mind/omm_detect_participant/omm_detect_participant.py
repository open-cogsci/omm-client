from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame.item import Item
from . import detectors

from libqtopensesame.items.qtautoplugin import QtAutoPlugin
import codecs


class OmmDetectParticipant(Item):
    def reset(self):

        self.var.detector = "Form"
        self.var.fallback_detector = "Form"
        self.var.serial_ports = (
            "/dev/ttyRFID"  # If multiple board use ',' separator COM3,COM4
        )
        self.var.serial_baud = 9600
        self.var.rfid_length = 19
        self.var.rfid_sep = "\\r"
        self.var.participant_variable = "participant"
        self.var.min_rep = 1
        self.var.enable_duration = "no"  # Optional timeout feature for RFID read
        self.var.read_duration = 5  # Timeout in seconds

    def prepare(self):

        self._init_detect_participant()
        self._detector.prepare()

    def _init_detect_participant(self):

        if hasattr(self, "_detector"):
            return
        if "omm_detector" in self.python_workspace:
            self._detector = self.python_workspace["omm_detector"]
            oslogger.info("reusing participant detector")
            return
        oslogger.info("initializing participant detector: {}".format(self.var.detector))

        cls = getattr(detectors, self.var.detector)
        try:
            self._detector = cls(
                experiment=self.experiment,
                participant_variable=self.var.participant_variable,
                serial_ports=self.var.serial_ports,
                min_rep=self.var.min_rep,
                enable_duration=self.var.enable_duration,
                read_duration=self.var.read_duration,
                serial_baud=self.var.serial_baud,
                rfid_length=self.var.rfid_length,
                rfid_sep=codecs.decode(
                    self.var.rfid_sep, "unicode_escape"
                ).encode(),  # convert \r \n \x03 into bytes...
            )
        except Exception as e:
            oslogger.info(
                "failed to initialize ({}), falling back to: {}".format(
                    e, self.var.fallback_detector
                )
            )
            cls = getattr(detectors, self.var.fallback_detector)
            self._detector = cls(experiment=self.experiment, port=self.var.serial_ports)
        self.python_workspace["omm_detector"] = self._detector
        self.experiment.cleanup_functions.append(self._close_detector)

    def _close_detector(self):

        oslogger.info("closing detector")
        self._detector.close()

    def run(self):
        self.set_item_onset()
        self._detector.run()
        oslogger.info(
            "identifier: {}".format(
                self.experiment.var.get(self.var.participant_variable)
            )
        )


class QtOmmDetectParticipant(OmmDetectParticipant, QtAutoPlugin):
    """This class handles the GUI aspect of the plug-in. The name should be the
    same as that of the runtime class with the added prefix Qt.

    Important: defining a GUI class is optional, and only necessary if you need
    to implement non-standard interfaces or interactions. In this case, we use
    the GUI class to dynamically enable/ disable some controls (see below).
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        OmmDetectParticipant.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        """
        Constructs connection between the GUI controls.
        """

        super().init_edit_widget()

        self.checkbox_enable_duration.stateChanged.connect(
            self.spinbox_read_duration.setEnabled
        )

        self.combobox_detector.currentTextChanged.connect(self.combobox_detectorChange)

    def combobox_detectorChange(self, val):

        if val == "rfid":
            self.line_edit_serial_port.setText("/dev/ttyRFID")
            self.line_edit_serial_baud.setText("9600")
            self.line_edit_rfid_length.setText("19")
            self.line_edit_rfid_sep.setText("\\r")
        elif val == "RfidRWeTTL":
            self.line_edit_serial_port.setText("/dev/ttyRFID")
            self.line_edit_serial_baud.setText("9600")
            self.line_edit_rfid_length.setText("16")
            self.line_edit_rfid_sep.setText("\\r")
        if val == "RfidLID650_665":
            self.line_edit_serial_port.setText("/dev/ttyRFID")
            self.line_edit_serial_baud.setText("19200")
            self.line_edit_rfid_length.setText("9")
            self.line_edit_rfid_sep.setText("\\x03")
