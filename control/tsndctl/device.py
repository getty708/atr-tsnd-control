from ctypes import resize
from datetime import datetime
import time
import serial
import threading
from pprint import pprint

from . import commands as tsndcmd
from logging import getLogger


def split_response(res):
    """
    Note:
        Implement unit-test
    """
    res_out = []
    ind_head = 0
    for i in range(len(res)):
        if res[i] == 0x9a and i > 0:
            res_out.append(res[ind_head:i])
            ind_head = i
    return res_out


class TSND151(object):
    def __init__(
        self,
        name: str =None,
        port: str=None,
        logdir: str=None,
        baudrate: int =9600,
        timeout: float=5,
        conf: dict=None,
        logger = None,
    ) -> None:
        self.name = name
        self.port = port
        self.logdir = logdir
        self.conf = conf
        self.timeout = timeout
        self.is_running = False
        self.is_thread_running = False
        self.logger = None
        assert timeout is not None
        if self.logger is None:
            self.logger = getLogger(f"tsndctl.TSND151.{self.name}")

        # Setup serial port
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.thread = threading.Thread(target=self.event_listener)

    def start_event_listener(self):
        self.is_running = True
        self.is_thread_started = True
        self.thread.start()
        
    def stop_event_listener(self):
        self.is_running = False
        time.sleep(self.timeout * 2)
        if self.is_thread_running:
            self.thread.join()
            self.is_thread_running= False

    def terminate(self):
        self.logger.info(f"Teriminate Device[{self.name}]")
        self.is_running = False
        self.ser.close()

    def send(self, msg: bytes):
        while True:
            if self.ser.out_waiting == 0:
                break
        self.ser.write(msg)
        self.ser.flush()
        
    def listen(self, num_bytes) -> bytes:
        response = None
        while True:
            if self.ser.in_waiting > 0:
                response = self.ser.read(num_bytes)
                break
        return response

    def event_listener(self):
        handler = {
            0x80: tsndcmd.AgsDataEvent(),
            0x88: tsndcmd.RecodingStartedEvent(),
            0x89: tsndcmd.RecodingStoppedEvent(),
            0xB9: tsndcmd.ReadMemData(),
            0x8F: tsndcmd.StopRecording(), # FIXME: Use dummy decoder.
        }
        pprint(handler)
        
        server_on = True
        while server_on:
            if self.is_running == False:
                break
            if self.ser.in_waiting > 0:
                response = self.ser.readline()
                if len(response) == 0:
                    self.logger.warning(f"Timeout ({response})")
                    continue
                
                # TODO: (1) Split by \x9a
                responses = split_response(response)
                # TODO: (2) decode each segment
                for i, res in enumerate(responses):
                    if len(res) < 2:
                        self.logger.warning(f"ShortResponseMsg (response={res})")
                        continue
                    cmd = handler.get(res[1], None) 
                    if cmd is None:
                        self.logger.warning(f"Unknown Response (response={res})")
                        continue
                    elif cmd.name == "ReadMemData":
                        server_on = False
                        print("check10", res)
                        break
                    else:
                        res = cmd.decode(res)
                        self.logger.info(cmd.pformat(res))
                if server_on is False:
                    break
        self.logger.info("Stop server")
        
    def process_command(self, cmd: tsndcmd.CmdTemplate, params: dict=None):
        if params is None:
            msg = cmd.encode()
        else:
            msg = cmd.encode(**params)
        
        self.send(msg)
        response = self.listen(cmd.response_size)
        response = cmd.decode(response)
        return response

    def init_device(self):        
        self.logger.debug("== init_device ==")
        
        # == Send Device Time ==
        cmd = tsndcmd.SetDeviceTime()
        response = self.process_command(cmd)
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)
        
        # == Get Device Time ==
        cmd = tsndcmd.GetDeviceTime()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Set Ags Method ==
        cmd = tsndcmd.SetAgsMethod()
        response = self.process_command(
            cmd,
            params={"interval": 33, "send_freq": 30, "record_freq": 1},
        )
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)

        # == Get Ags Method ==
        cmd = tsndcmd.GetAgsMethod()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Set GeoMagnetic Method ==
        cmd = tsndcmd.SetGeoMagneticMethod()
        response = self.process_command(
            cmd,
            params={"interval": 0, "send_freq": 0, "record_freq": 0},
        )
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)

        # == Get GeoMagnetic Method ==
        cmd = tsndcmd.GetGeoMagneticMethod()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Set Pressure Method ==
        cmd = tsndcmd.SetPresMethod()
        response = self.process_command(
            cmd,
            params={"interval": 0, "send_freq": 0, "record_freq": 0},
        )
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)

        # == Get Pressure Method ==
        cmd = tsndcmd.GetPresMethod()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Set Battery Method ==
        cmd = tsndcmd.SetBattMethod()
        response = self.process_command(
            cmd,
            params={"send": 0, "record": 0},
        )
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)

        # == Get Battery Method ==
        cmd = tsndcmd.GetBattMethod()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Set Acc Range ==
        cmd = tsndcmd.SetAccRange()
        response = self.process_command(cmd, params={"mode": 1})
        self.logger.debug(cmd.pformat(response))
        time.sleep(1)

        # == Get Acc Range ==
        cmd = tsndcmd.GetAccRange()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Get Device Status ==
        cmd = tsndcmd.GetDeviceStatus()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)
        
        # == Set Auto-power-off Setting ==
        cmd = tsndcmd.SetAutoPowerOffTime()
        response = self.process_command(cmd, params={"minutes": 0})
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

        # == Get Auto-power-off Setting ==
        cmd = tsndcmd.GetAutoPowerOffTime()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        time.sleep(1)

    def start_recording(self):
        self.logger.info("== Start Recoding ==")
        
        # == Start Recording ==
        cmd = tsndcmd.StartRecording()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))

    def stop_recording(self):
        self.logger.info("== Stop Recoding ==")
        
        # == Stop Recordiang ==
        cmd = tsndcmd.StopRecording()
        msg = cmd.encode()
        self.send(msg)       
        self.logger.info(f"Stop Recoding ({msg})")

    def check_memory_status(self):
        self.logger.info("== Check Memory Status ==")
        outputs = dict()
        
        # == Memory Counts ==
        cmd = tsndcmd.GetMemEntryCount()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        outputs.update({
            "MemEntryCount": response,
        })

        # == Free Memory Size ==
        cmd = tsndcmd.GetFreeMemSize()
        response = self.process_command(cmd)
        self.logger.info(cmd.pformat(response))
        outputs.update({
            "FreeMemorySize": response,
        })
        return outputs

    def clear_memory(self):
        # == Memory Counts ==
        self.check_memory_status()

        self.logger.info("== Check Memory Status ==")
        print("Do you really want to clear memory? [Y/n] >>")
        res = input()
        if res == "Y":
            # == Clear Memory ==
            cmd = tsndcmd.ClearMemoery()
            response = self.process_command(cmd)
            self.logger.info(cmd.pformat(response))

            # == Memory Counts ==
            cmd = tsndcmd.GetMemEntryCount()
            response = self.process_command(cmd)
            self.logger.info(cmd.pformat(response))
        else:
            self.logger.info("Quit")


    def read_mem_data(self, entry_index):
        self.logger.info("== Read Mem Data ==")
        
        # Start Read Memoery Data
        cmd = tsndcmd.ReadMemData()
        msg = cmd.encode(entry_index)
        data = {"mode": "start", "entry": entry_index}
        self.logger.info(f"ReadMemDataCtl:: {data}")
        self.send(msg)

        # Read and Output to Log File
        try:
            self.is_running = True
            self.event_listener()
            self.is_running = False
        except KeyboardInterrupt:
            self.is_running = False

            # Send StopReadMemData Command
            cmd = tsndcmd.StopReadMemData()
            msg = cmd.encode()
            data = {"mode": "stop", "entry": entry_index}
            self.logger.info(f"ReadMemDataCtl:: {data}")
            self.send(msg)

        # Finish Read Out the Entry
        data = {"mode": "end", "entry": entry_index}
        self.logger.info(f"ReadMemDataCtl:: {data}")
        