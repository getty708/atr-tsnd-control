import datetime
import sys
import pytest
import numpy as np
from control.tsndctl.commands import GetMemEntryCount, RecodingStartedEvent
sys.path.append("../")

from tsndctl import commands as cmd

@pytest.mark.parametrize("msg_in,msg_out", (
    (
        [0x57, 0x1a, 0x63, 0x70],
        [0x57, 0x1a, 0x63, 0x70, 0x5e],
    ),
))
def test_add_bcc__01(msg_in, msg_out):
    msg_out_act = cmd.add_bcc(msg_in)
    print("msg[Expected]:", msg_out)
    print("msg[Outputs ]:", msg_out_act)

    np.testing.assert_array_equal(msg_out, msg_out_act)

@pytest.mark.parametrize("ts,msg_exp", (
    (
        datetime.datetime(2001, 1, 1, 1, 1, 1, 0),
        bytes([0x9A, 0x11, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x8b]),
    ),
))
def test_SetDeviceTime__01(ts,msg_exp):
    print("Timestamp:", ts)

    cobj = cmd.SetDeviceTime()
    msg_out = cobj.encode(ts)
    print("msg[Expected]:", msg_exp)
    print("msg[Outputs ]:", msg_out)

    # np.testing.assert_array_equal(msg_out, msg_exp)
    assert msg_out == msg_exp


def test_GetDeviceTime__encode__01():
    msg_exp = bytes([0x9A, 0x12, 0x00, 0x88])
    
    cobj = cmd.GetDeviceTime()
    msg_out = cobj.encode()
    print("msg[Expected]:", msg_exp)
    print("msg[Outputs ]:", msg_out)

    assert msg_out == msg_exp
    
 
@pytest.mark.parametrize("response,ts_exp", (
    (
        bytes([0x9A, 0x92, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x8b]),
        datetime.datetime(2001, 1, 1, 1, 1, 1, 0),
    ),
    (
        bytes([0x9A, 0x92, 0x15, 0x0A, 0x0B, 0x01, 0x01, 0x01, 0x01, 0x01, 0x8b]),
        datetime.datetime(2021, 10, 11, 1, 1, 1, 257000),
    ),
))
def test_GetDeviceTime__decode__01(response,ts_exp):
    print("response", response)

    cobj = cmd.GetDeviceTime()
    ts_out = cobj.decode(response)
    print("ts[Expected]:", ts_exp)
    print("ts[Outputs ]:", ts_out)

    assert ts_out == ts_exp
    
@pytest.mark.parametrize("td_start,msg_exp", (
    (
        None,
        bytes([
            0x9A, 0x13,
            0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x05,
            0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00,
            0x8c,
        ]),
    ),
))
def test_StartRecording__encode__01(td_start, msg_exp):
    print("Start Time:", td_start)

    cobj = cmd.StartRecording()
    msg_out = cobj.encode(mode=0, td_start=td_start)
    print("msg[Expected]:", msg_exp)
    print("msg[Outputs ]:", msg_out)

    assert msg_out == msg_exp

@pytest.mark.parametrize("response, status, ts_start, ts_end", (
    (
        bytes([
            0x9A, 0x93,
            0x01,
            0x00, 0x01, 0x01, 0x00, 0x00, 0x05,
            0x00, 0x01, 0x01, 0x00, 0x00, 0x00,
            0x8c,
        ]),
        1,
        datetime.datetime(2000, 1, 1, 0, 0, 5),
        datetime.datetime(2000, 1, 1, 0, 0, 0),
    ),
))
def test_StartRecording__decode__01(response, status, ts_start, ts_end):
    cobj = cmd.StartRecording()
    outputs = cobj.decode(response)
    print("Outputs:", outputs)
    
    assert outputs["status"] == status
    assert outputs["start"] == ts_start
    assert outputs["end"] == ts_end
    

@pytest.mark.parametrize("msg_exp,response, status", (
    (
        bytes([0x9A, 0x15, 0x00, 0x8f]),
        bytes([0x9A, 0x8F, 0x01, 0x00]),
        1,
    ),
))
def test_StopRecording__01(msg_exp, response, status):
    # Command 
    msg_out = cmd.StopRecording().encode()
    print("msg_out:", msg_out)
    assert msg_out == msg_exp

    # Response
    data = cmd.StopRecording().decode(response)
    print("data:", data)

    assert data["status"] == status

@pytest.mark.parametrize("interval,send_interval,recording_interval,msg_exp", (
    (
        33, 
        1,
        0,
        bytes([0x9A, 0x16, 0x21, 0x01, 0x00, 0xac]),
    ),
    (
        33, 
        255,
        1,
        bytes([0x9A, 0x16, 0x21, 0xFF, 0x01, 0x53]),
    ),
))
def test_SetAgsMethod__01(interval,send_interval,recording_interval,msg_exp):
    print("Interval [ms]:", interval)
    print("Send Interval [ms]:", send_interval)
    print("Recording Interval [ms]:", recording_interval)

    cobj = cmd.SetAgsMethod()
    msg_out = cobj.encode(interval,send_interval,recording_interval)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    # np.testing.assert_array_equal(msg_out, msg_exp)
    assert msg_out == msg_exp




@pytest.mark.parametrize("response, interval, send_freq, record_freq", (
    (
        bytes([0x9A, 0x97, 0x21, 0x01, 0x00, 0x00]),
        33, 
        1,
        0,
    ),
    (
        bytes([0x9A, 0x97, 0x21, 0xFF, 0x01, 0x00]),
        33, 
        255,
        1,
    ),
))
def test_GetAgsMethod__01(response, interval, send_freq, record_freq):
    cobj = cmd.GetAgsMethod()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("interval") == interval
    assert data.get("send_freq") == send_freq
    assert data.get("record_freq") == record_freq


@pytest.mark.parametrize("interval,send_interval,recording_interval,msg_exp", (
    (
        0, 
        0,
        0,
        bytes([0x9A, 0x18, 0x00, 0x00, 0x00, 0x82]),
    ),
))
def test_SetGeoMagneticMethod__01(interval,send_interval,recording_interval,msg_exp):
    print("Interval [ms]:", interval)
    print("Send Interval [ms]:", send_interval)
    print("Recording Interval [ms]:", recording_interval)

    cobj = cmd.SetGeoMagneticMethod()
    msg_out = cobj.encode(interval,send_interval,recording_interval)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    # np.testing.assert_array_equal(msg_out, msg_exp)
    assert msg_out == msg_exp



@pytest.mark.parametrize("response, interval, send_freq, record_freq", (
    (
        bytes([0x9A, 0x99, 0x00, 0x00, 0x00, 0x00]),
        0, 
        0,
        0,
    ),
))
def test_GetGeoMagneticMethod__01(response, interval, send_freq, record_freq):
    cobj = cmd.GetGeoMagneticMethod()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("interval") == interval
    assert data.get("send_freq") == send_freq
    assert data.get("record_freq") == record_freq



@pytest.mark.parametrize("interval,send_interval,recording_interval,msg_exp", (
    (
        0, 
        0,
        0,
        bytes([0x9A, 0x1A, 0x00, 0x00, 0x00, 0x80]),
    ),
))
def test_SetPresMethod__01(interval,send_interval,recording_interval,msg_exp):
    print("Interval [ms]:", interval)
    print("Send Interval [ms]:", send_interval)
    print("Recording Interval [ms]:", recording_interval)

    cobj = cmd.SetPresMethod()
    msg_out = cobj.encode(interval,send_interval,recording_interval)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    # np.testing.assert_array_equal(msg_out, msg_exp)
    assert msg_out == msg_exp



@pytest.mark.parametrize("response, interval, send_freq, record_freq", (
    (
        bytes([0x9A, 0x9B, 0x00, 0x00, 0x00, 0x00]),
        0, 
        0,
        0,
    ),
))
def test_GetPresMethod__01(response, interval, send_freq, record_freq):
    cobj = cmd.GetPresMethod()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("interval") == interval
    assert data.get("send_freq") == send_freq
    assert data.get("record_freq") == record_freq




@pytest.mark.parametrize("send,record,msg_exp", (
    (
        0,
        0,
        bytes([0x9A, 0x1C, 0x00, 0x00, 0x86]),
    ),
))
def test_SetBattMethod__01(send,record,msg_exp):
    print("Send [0/1]:", send)
    print("Record [0/1]:", record)

    cobj = cmd.SetBattMethod()
    msg_out = cobj.encode(send, record)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    # np.testing.assert_array_equal(msg_out, msg_exp)
    assert msg_out == msg_exp



@pytest.mark.parametrize("response, send, record", (
    (
        bytes([0x9A, 0x9D, 0x00, 0x00, 0x00]),
        0, 
        0,
    ),
))
def test_GetBattMethod__01(response, send, record):
    cobj = cmd.GetBattMethod()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("send") == send
    assert data.get("record") == record




@pytest.mark.parametrize("mode,msg_exp", (
    (
        0,
        bytes([0x9A, 0x22, 0x00, 0xb8]),
    ),
))
def test_SetAccRange__01(mode,msg_exp):
    print("mode:", mode)
    
    cobj = cmd.SetAccRange()
    msg_out = cobj.encode(mode)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    assert msg_out == msg_exp

@pytest.mark.parametrize("response, mode", (
    (
        bytes([0x9A, 0xA3, 0x00, 0x00]),
        0,
    ),
))
def test_GetAccRange__01(response, mode):
    cobj = cmd.GetAccRange()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("mode") == mode


def test_ClearMemory__01(response):
    raise NotImplementedError()

def test_GetMemEntryCount__01(response):
    raise NotImplementedError()

def test_GetFreeMemSize__01(response):
    raise NotImplementedError()

@pytest.mark.parametrize("response, status", (
    (
        bytes([0x9A, 0xBC, 0x00, 0x00]),
        0,
    ),
    (
        bytes([0x9A, 0xBC, 0x02, 0x00]),
        2,
    ),
    (
        bytes([0x9A, 0xBC, 0x03, 0x00]),
        3,
    ),
))
def test_GetDeviceStatus__01(response, status):
    cobj = cmd.GetDeviceStatus()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("status") == status




@pytest.mark.parametrize("minutes,msg_exp", (
    (
        0,
        bytes([0x9A, 0x50, 0x00, 0xca]),
    ),
))
def test_SetAutoPowerOffTime__01(minutes,msg_exp):
    print("minutes:", minutes)
    
    cobj = cmd.SetAutoPowerOffTime()
    msg_out = cobj.encode(minutes)
    print("msg[Expected]:", list(msg_exp))
    print("msg[Outputs ]:", list(msg_out))

    assert msg_out == msg_exp

@pytest.mark.parametrize("response, minutes", (
    (
        bytes([0x9A, 0xD1, 0x00, 0x00]),
        0,
    ),
))
def test_GetAutoPowerOffTime__01(response, minutes):
    cobj = cmd.GetAutoPowerOffTime()
    data = cobj.decode(response)
    print("data:", data)

    assert data.get("minutes") == minutes


@pytest.mark.parametrize("response,ts,acc,gyro", (
    (
        bytes([
            0x9A, 0x80,
            0x0B, 0x00, 0x00, 0x00, # ts
            0x01, 0x00, 0x00, # Acc-X
            0x02, 0x00, 0x00, # Acc-Y
            0x03, 0x00, 0x00, # Acc-Z
            0x04, 0x00, 0x00, # Gyro-X
            0x05, 0x00, 0x00, # Gyro-Y
            0x06, 0x00, 0x00, # Gyro-Z
        ]),
        11,
        [1, 2, 3],
        [4, 5, 6],
    ),
))
def test_AgsDataEvent__01(response, ts, acc, gyro):
    outputs = cmd.AgsDataEvent().decode(response)
    print("outputs:", outputs)

    assert outputs["ts"] == ts
    np.testing.assert_array_equal(outputs["acc"], acc)
    np.testing.assert_array_equal(outputs["gyro"], gyro)


def test_RecodingStartedEvent__01(response):
    raise NotImplementedError()

def test_RecodingStoppedEvent__01(response):
    raise NotImplementedError()
