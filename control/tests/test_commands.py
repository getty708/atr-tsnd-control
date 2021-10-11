import datetime
import sys
import pytest
import numpy as np
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