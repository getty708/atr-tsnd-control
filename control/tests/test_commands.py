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
    
    


