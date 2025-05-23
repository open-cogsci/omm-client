from ._rfid_base import rfid
import serial
import time

class RfidRWeTTL(rfid):
    
    RFID_LENGTH = 16    # This board return 16 bytes
    RFID_SEP = b'\r'    # The byte that separates RFIDs in the buffer
    SERIAL_TIMEOUT = 0.1 # read_timeout need to be higher
    
    def __init__(self, **kwargs):   
        super(RfidRWeTTL, self).__init__(**kwargs)




    @staticmethod
    def _rfid_monitor(queue, reset_event, stop_event, ports, min_rep=1,
                      baudrate=9600,serial_read_timeout=0.1,
                      rfid_length = 16,rfid_sep = b'\r'):
        """
        Redefinition of this function for this card:
        1/ The tag format returned is in the form 995_NNNNNNNNNNNN and not 099NNNNNNNNNNNNNN.
        2/ A 'RAT' command must be sent to force the reading of a tag that has already been read and is still within range.
        """    
        
        readers = []
        try:
            for port in ports:
                reader = serial.Serial(port=port,baudrate=baudrate,timeout=serial_read_timeout)
                reader.flushInput()
                readers.append((port, reader))

            # One buffer and last RFID per reader
            buffers = {port: b'' for port, _ in readers}
            last_rfids = {port: None for port, _ in readers}
        
            last_rat_cmd = 0
            
            while not stop_event.is_set():
                if reset_event.is_set():
                    reset_event.clear()
                    for port, reader in readers:
                        reader.flushInput()
                        buffers[port] = b''
                        last_rfids[port] = None
                        last_rat_cmd = 0
    
                for port, reader in readers:
                    # Read incoming bytes and append to the buffer for that port
                    buffers[port] += reader.read(rfid_length)
    
                    # Extract potential RFID strings
                    rfids = [r for r in buffers[port].split(rfid_sep) if len(r) == rfid_length]
    
                    if len(set(rfids)) > 1:
                        # If inconsistent reads are detected, keep only the repeated valid entries
                        buffers[port] = RFID_SEP.join([rfids[-1]] * rfids.count(rfids[-1]))
                        continue
    
                    if len(rfids) >= min_rep:
                        rfid = rfids[0].decode()
                        if rfid != last_rfids[port]:

                            last_rfids[port] = rfid
                            
                            #Format the RFID number as the original board
                            rfid = rfid.replace("_","0")
                            rfid = "09" + str(rfid)
                            
                            queue.put((port, rfid))  # Include port to help identify source

                #Check if chip is already present
                if last_rat_cmd == 0:
                    #print("RAT",flush=True)
                    last_rat_cmd=time.time()
                    reader.write("RAT\r".encode())
    
            for _, reader in readers:
                reader.close()
    
        except Exception as e:
            print(f"Error in RFID monitor: {e}")
            stop_event.set()
            