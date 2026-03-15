from ._rfid_base import RFID
import serial
import time


class RFIDRWeTTL(RFID):
    SERIAL_TIMEOUT = 0.1  # read_timeout need to be higher then 0.0X

    @staticmethod
    def _rfid_monitor(
        queue,
        reset_event,
        stop_event,
        error_queue,
        ports,
        min_rep=1,
        baudrate=9600,
        serial_read_timeout=0.1,
        rfid_length=16,
        rfid_sep=b"\r",
    ):
        """
        Redefinition of this function for this card:
        1/ The tag format returned is in the form 995_NNNNNNNNNNNN and not 099NNNNNNNNNNNNNN.
        2/ A 'RAT' command must be sent to force the reading of a tag that has already been read and is still within range.
        """

        readers = []
        for port in ports:
            try:
                reader = serial.Serial(
                    port=port, baudrate=baudrate, timeout=serial_read_timeout
                )
            except serial.SerialException as e:
                error_queue.put(f"Cannot open serial port {port}: {e}")
                return
            reader.flushInput()
            readers.append((port, reader))

        # One buffer and last RFID per reader
        buffers = {port: b"" for port, _ in readers}
        last_rfids = {port: None for port, _ in readers}

        last_rat_cmd = 0
        tag = b""

        while not stop_event.is_set():
            if reset_event.is_set():
                reset_event.clear()
                for port, reader in readers:
                    reader.flushInput()
                    buffers[port] = b""
                    last_rfids[port] = None
                    last_rat_cmd = 0

            for port, reader in readers:
                try:
                    # Read incoming bytes and append to the buffer for that port
                    tag = reader.read(rfid_length)
                except serial.SerialException as e:
                    error_queue.put(f"Serial read error on {port}: {e}")
                    continue  # skip this reader iteration

                if not tag:
                    continue  # Timeout or nothing read, skip to next reader

                buffers[port] += tag

                # Extract potential RFID strings
                rfids = [
                    r for r in buffers[port].split(rfid_sep) if len(r) == rfid_length
                ]

                if len(set(rfids)) > 1:
                    # If inconsistent reads are detected, keep only the repeated valid entries
                    buffers[port] = rfid_sep.join([rfids[-1]] * rfids.count(rfids[-1]))
                    continue

                if len(rfids) >= min_rep:
                    rfid = rfids[0].decode()
                    if rfid != last_rfids[port]:
                        last_rfids[port] = rfid

                        # Format the RFID number as the original board
                        rfid = rfid.replace("_", "0")
                        rfid = "09" + str(rfid)

                        queue.put((port, rfid))  # Include port to help identify source

            # Check if chip is already present
            if last_rat_cmd == 0:
                last_rat_cmd = time.time()
                try:
                    reader.write("RAT\r".encode())
                except serial.SerialException as e:
                    error_queue.put(f"Serial write error on {port}: {e}")

        for _, reader in readers:
            reader.close()
