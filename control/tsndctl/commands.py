from typing import List
import datetime

# Header is a message header byte
CMD_HEADER: int = 0x9A

def add_bcc(cmd: List[int]):
    """Compute BCC (= Block Checking Charactor) and append to command sequence.
    
    Returns:
        list of binary data with BCC code.
    """
    check: int = 0x00
    for b in cmd:
        check = check ^ b
    cmd.append(check)
    return cmd

class CmdTemplate(object):
    """ Base class for TSDN command  serial communication.
    """
    cmd_code: bytes = None 
    pyload: bytes = None
    
    def __init__(self):
        pass

    def encode(self):
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()
    

class SetDeviceTime(CmdTemplate):
    cmd_code = 0x11

    def encode(self, ts: datetime.datetime):
        ms = int(ts.microsecond // 1e3)
        cmd = [
            CMD_HEADER,
            self.cmd_code,
            ts.year - 2000,
            ts.month,
            ts.day,
            ts.hour,
            ts.minute,
            ts.second,
            (ms//256),
            (ms%256),
        ]
        cmd = add_bcc(cmd)
        return bytes(cmd)

class GetDeviceTime(CmdTemplate):
    cmd_code = 0x12

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)

        return bytes(cmd)

    def decode(self, response):
        raise NotImplementedError()

    
