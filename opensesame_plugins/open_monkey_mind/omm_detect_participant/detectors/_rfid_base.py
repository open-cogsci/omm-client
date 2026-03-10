import queue
import time
from libopensesame.py3compat import *
from openmonkeymind._exceptions import OMMException
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
import serial


# A dummy class to signal that the RFID monitor crashed
class RFIDMonitorProcessCrashed(OMMException):
    pass


class rfid:
    SERIAL_READ_TIMEOUT = 0.5  # Greater timout = less cpu. None is great too if only one serial port is used.

    def __init__(self, **kwargs):

        if "experiment" not in kwargs:
            raise ValueError("BaseRFID expects experiment keyword")
        self.experiment = kwargs["experiment"]

        self.participant_variable = kwargs["participant_variable"]
        self.serial_ports = kwargs["serial_ports"]
        self.min_rep = kwargs["min_rep"]
        self.enable_duration = kwargs["enable_duration"]
        self.read_duration = kwargs["read_duration"]
        self.serial_baud = kwargs["serial_baud"]
        self.rfid_length = kwargs["rfid_length"]
        self.rfid_sep = kwargs["rfid_sep"]

    @staticmethod
    def _rfid_monitor(
        queue,
        reset_event,
        stop_event,
        error_queue,
        ports,
        min_rep=3,
        baudrate=9600,
        serial_read_timeout=0.01,
        rfid_length=18,
        rfid_sep=b"\r",
    ):
        """
        Monitor function that runs in a subprocess.
        Modified version that supports multiple RFID readers (each on its own port).
        Each reader has its own input buffer and tracking for last detected RFID.
        """

        readers = []

        for port in ports:
            try:
                reader = serial.Serial(
                    port=port, baudrate=baudrate, timeout=serial_read_timeout
                )
            except serial.SerialException as e:
                error_queue.put(f"Cannot open RFID reader {port}: {e}")
                return
            reader.flushInput()
            readers.append((port, reader))

        # One buffer and last RFID per reader
        buffers = {port: b"" for port, _ in readers}
        last_rfids = {port: None for port, _ in readers}

        while not stop_event.is_set():
            if (
                reset_event.is_set()
            ):  # Set when last detect_participant_plugin is run (in entry point)
                reset_event.clear()
                for port, reader in readers:
                    reader.flushInput()
                    buffers[port] = b""
                    last_rfids[port] = None

            for port, reader in readers:
                # Read incoming bytes
                sread = reader.read(rfid_length)

                # If reset_event is set when reader is stuck by serial read timeout
                # clear the last_rfids number, otherwise it can block indefinitely
                # the detection of RFID if the same one is read
                if reset_event.is_set():
                    reset_event.clear()
                    last_rfids = {port: None for port, _ in readers}
                    buffers = {port: b"" for port, _ in readers}

                # Append last RFID read to buffer for that port
                buffers[port] += sread

                # Extract potential RFID strings
                rfids = [
                    r
                    for r in buffers[port].split(rfid_sep)
                    if len(r) == rfid_length - 1
                ]

                # Original code in comments doesn't work well, I don't know why.
                # It replaced by the code above (keep here for memory)
                # if len(set(rfids)) > 1:
                #    # If inconsistent reads are detected, keep only the repeated valid entries
                #    buffers[port] = RFID_SEP.join([rfids[-1]] * rfids.count(rfids[-1]))
                #    error_queue.put(buffers[port])
                #    continue

                # For each tag, count how many times it appears to try to eliminate read errors.
                for i in range(len(rfids) - 1, -1, -1):
                    if rfids.count(rfids[i]) >= min_rep:
                        rfid = rfids[i].decode()

                        if (
                            rfid != last_rfids[port]
                        ):  # Only send to queue if it's a new RFID for that reader(used by omm.current_participant_changed)
                            queue.put(
                                (port, rfid)
                            )  # Include port to help identify source
                            last_rfids[port] = rfid
                            buffers[port] = b""  # Clear buffer after successful read

        for _, reader in readers:
            reader.close()

    def prepare(self):

        if not hasattr(self.experiment, "_omm_participant_process"):
            oslogger.info("starting RFID monitor process")
            import multiprocessing

            # Important : define start method to avoid Windows/macOS error when using multiprocessing in a submodule of the main experiment (like here in omm_detect_participant)
            if __name__ == "__main__":
                if multiprocessing.get_start_method(allow_none=True) != "spawn":
                    multiprocessing.set_start_method("spawn")

            self.experiment._omm_participant_queue = multiprocessing.Queue()
            self.experiment._omm_participant_reset_event = multiprocessing.Event()
            self.experiment._omm_participant_stop_event = multiprocessing.Event()

            # Parse multiple ports from comma-separated list
            ports = [p.strip() for p in self.serial_ports.split(",")]

            self.experiment._omm_participant_error_queue = multiprocessing.Queue()

            self.experiment._omm_participant_process = multiprocessing.Process(
                target=self.__class__._rfid_monitor,
                args=(
                    self.experiment._omm_participant_queue,
                    self.experiment._omm_participant_reset_event,
                    self.experiment._omm_participant_stop_event,
                    self.experiment._omm_participant_error_queue,
                    ports,
                    self.min_rep,
                    self.serial_baud,
                    self.SERIAL_READ_TIMEOUT,
                    self.rfid_length,
                    self.rfid_sep,
                ),
            )

            self.experiment._omm_participant_process.start()
            self.experiment.cleanup_functions.append(self.close)

        # self.run = self.run_rfid
        self._keyboard = Keyboard(self.experiment, timeout=0)

    def run(self):

        # Reset the monitor so that it accepts any RFID, not only new ones
        self.experiment._omm_participant_reset_event.set()
        # Eat up any pending RFIDs on the queue
        while not self.experiment._omm_participant_queue.empty():
            try:
                self.experiment._omm_participant_queue.get_nowait()
            except queue.Empty:
                break

        # Optional timeout logic (new feature)
        duration_enabled = "yes" if self.enable_duration == "yes" else "no"

        read_duration = float(self.read_duration) if self.read_duration > 0 else 0
        start_time = time.time()

        # Wait for a new RFID. While waiting, we make sure that the process
        # is still alive, and we also poll the keyboard to allow for testing
        # identifications with a key press
        while self.experiment._omm_participant_queue.empty():
            time.sleep(0.01)

            # Check RFID process error
            while not self.experiment._omm_participant_error_queue.empty():
                error = self.experiment._omm_participant_error_queue.get_nowait()
                oslogger.error("RFIDMonitorProcess error :", error)

            # if not self.experiment._omm_participant_process.is_alive():
            #    raise RFIDMonitorProcessCrashed()

            key, timestamp = self._keyboard.get_key()
            if key is not None:
                oslogger.info("identifier by key: {}".format(key))
                self.experiment.var.set(self.participant_variable, "/{}/".format(key))
                return

            if duration_enabled == "yes" and (time.time() - start_time) > read_duration:
                oslogger.info("Read duration expired, no RFID detected.")
                return

        # Retrieve RFID from queue (port + RFID tuple)
        rfid_data = self.experiment._omm_participant_queue.get()

        if isinstance(rfid_data, tuple) and len(rfid_data) == 2:
            port, rfid = rfid_data
            oslogger.info(f"RFID detected from {port}: {rfid}")
        else:
            rfid = rfid_data
            oslogger.info(f"RFID detected (no port info): {rfid}")

        self.experiment.var.set(self.participant_variable, "/{}/".format(rfid))

    def close(self):
        # When serial process is started on entrypoint, we don't want to close between tasks
        # We let the master experiment (the entrypoint) to close it.
        # _omm_participant_no_close_process is created in omm_announce
        if not hasattr(self.experiment, "_omm_participant_no_close_process"):
            # Stop the monitor process so the signal isn't blocked on the next
            # experiment
            oslogger.info("stopping RFID monitor process")
            self.experiment._omm_participant_stop_event.set()
            self.experiment._omm_participant_process.join()
