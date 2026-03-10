from ._rfid_base import rfid
import serial
import functools
import operator
import socket

class RfidLID650_665(rfid):
    SERIAL_READ_TIMEOUT = None

    def __init__(self, **kwargs):
        super(RfidLID650_665, self).__init__(**kwargs)

    @staticmethod
    def _rfid_monitor(
        queue,
        reset_event,
        stop_event,
        error_queue,
        ports,
        min_rep=1,
        baudrate=19200,
        serial_read_timeout=0.1,
        rfid_length=16,
        rfid_sep=b"\r",
    ):
        """
        Redefinition of this function for this card:
        String format
        <DLE><STX><Unit from><Unit to><Command><Data> …… <DLE><ETX><Checksum>

        String format Remarks
        <DLE><STX> 10h 02h Start of frame indication
        <Unit from>1 hexadecimal value between 00h-FEh From address
        <Unit to>1 hexadecimal value between 00h-FFh To address
        <Command>1 hexadecimal value between 00h-FFh Value is specified by the command
        <Data>1 hexadecimal value(s) between 00h-FFh Values are specified by the command
        <DLE><ETX> 10h 03h End of frame indication
        <Checksum> hexadecimal value between 00h-FFh XOR on all previous hexadecimal values
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
        # last_rfids = {port: None for port, _ in readers}

        # Socket is here to send RFID chip information to potential other process 4 executing some actions (like record video when monkey play)
        DEST_IP = "127.0.0.1"
        DEST_PORT = 6000
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while not stop_event.is_set():
            if reset_event.is_set():
                reset_event.clear()
                for port, reader in readers:
                    reader.flushInput()
                    buffers[port] = b""
                    # last_rfids[port] = None

            for port, reader in readers:
                # Read incoming bytes and append to the buffer for that port
                # buffers[port] += reader.read(rfid_length)
                try:
                    byte = reader.read(1)
                except serial.SerialException as e:
                    error_queue.put(f"Serial read error on {port}: {e}")
                    continue

                if not byte:
                    continue  # Timeout or nothing read, skip to next reader

                buffers[port] += byte

                # Check end of frame <DLE><ETX>
                if len(buffers[port]) >= 2 and buffers[port][-2:] == b"\x10\x03":
                    # Get checksum
                    try:
                        checksum = reader.read(1)
                    except serial.SerialException as e:
                        error_queue.put(f"Serial read error on {port}: {e}")
                        continue
                    buffers[port] += checksum
                else:
                    continue

                if len(buffers[port]) < 9:
                    error_queue.put(
                        f"RFID frame too short | buffer: {buffers[port].hex()}"
                    )
                    continue

                if not (buffers[port][0] == 0x10 and buffers[port][1] == 0x02):
                    error_queue.put(
                        f"RFID frame does not start with DLE STX | buffer: {buffers[port].hex()}"
                    )
                    continue

                unit_from = buffers[port][2]
                unit_to = buffers[port][3]
                checksum = buffers[port][-1]
                data = buffers[port][4:-3]

                # checksum_calc = sum(frame[:-1]) % 256
                checksum_calc = functools.reduce(operator.xor, buffers[port][:-1])

                if checksum_calc != checksum:
                    error_queue.put(
                        f"Checksum mismatch: got {checksum} calculated {checksum_calc} | buffer: {buffers[port].hex()}"
                    )
                    continue

                tag = buffers[port][4:-3].hex().upper()
                queue.put((port, tag))  # Include port to help identify source

                # Send info to socket
                try:
                    sock.sendto(tag.encode(), (DEST_IP, DEST_PORT))
                except OSError as e:
                    error_queue.put(f"UDP send error: {e}")

                # Retirer la trame traitée du buffer
                buffers[port] = b""

        for _, reader in readers:
            error_queue.put("Closing reader")
            reader.close()
