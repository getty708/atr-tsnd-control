from typing import List
import datetime

from .utils import get_h_m_s

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
    cmd_code: int = None 
    response_code: int = None
    response_param_size: int = None
    pyload: bytes = None
    
    def __init__(self):
        pass

    @property
    def response_size(self):
        return self.response_param_size + 3

    def encode(self):
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()
    

class SetDeviceTime(CmdTemplate):
    cmd_code = 0x11
    response_code = 0x8F
    response_param_size = 1

    def encode(self, ts: datetime.datetime=None):
        if ts is None:
            ts = datetime.datetime.now()

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

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetDeviceTime(CmdTemplate):
    cmd_code = 0x12
    response_code = 0x92
    response_param_size = 8

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)

        return bytes(cmd)

    def decode(self, response: bytes) -> datetime.datetime:
        # raise NotImplementedError()
        assert response[1] == self.response_code
        
        # -- Decode --
        ts = datetime.datetime(
            (response[2] + 2000), # year
            response[3], # month
            response[4], # day
            hour=response[5],
            minute=response[6],
            second=response[7],
            microsecond=(int.from_bytes(response[8:10], "little") * 1000),
        )
        return ts


class StartRecording(CmdTemplate):
    """計測開始 / 計測予約 (Command) & 計測時刻応答 (Response)

    (Command) 計測の開始または開始時刻及び終了時刻の設定を行う.
    開始時刻及び終了時刻は, 相対時間または絶対時間の指定が可能.

    (Response) 計測時刻の設定状態と設定された計測の開始時刻及び終了時刻を応答する.

    Note:
        現状では，開始時刻は相対時間による指定，終了時刻の指定なしのみサポート
    """
    cmd_code = 0x13
    response_code = 0x93
    response_param_size = 13

    def encode(
        self,
        mode:int = 0,
        td_start: datetime.timedelta=None,
        td_end: datetime.timedelta=None,
    ):
        assert mode == 0
        assert td_end is None
        if td_start is None:
            td_start = datetime.timedelta(seconds=5)

        cmd = [CMD_HEADER, self.cmd_code]
        
        # Start Time
        # NOTE: For mode=0 (relative time mode), year, month, day will be ignored.
        h, m, s = get_h_m_s(td_start) 
        cmd += [mode, 0, 1, 1, h, m, s] # mode, year, month, day, hour, minute, second
        
        # End Time (free run)
        # NOTE: For mode=0 (relative time mode), year, month, day will be ignored.
        cmd += [mode, 0, 1, 1, 0, 0, 0] # mode, year, month, day, hour, minute, second
        
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        status = response[2]

        ts_start = datetime.datetime(
            (response[3] + 2000), # year
            response[4], # month
            response[5], # day
            response[6], # hour
            response[7], # minute
            response[8], # second
        )
        ts_end = datetime.datetime(
            (response[9] + 2000), # year
            response[10], # month
            response[11], # day
            response[12], # hour
            response[13], # minute
            response[14], # second
        )

        outputs = {
            "status": status,
            "start": ts_start,
            "end": ts_end,
        }
        return outputs


class StopRecording(CmdTemplate):
    cmd_code = 0x15
    response_code = 0x8F
    response_param_size = 1

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response: bytes) -> dict:
        assert response[1] == self.response_code        
        outputs = {"status": response[2]}
        return outputs

class SetAgsMethod(CmdTemplate):
    """加速/角速度計測設定取得
    """
    cmd_code = 0x16
    response_code = 0x8F
    response_param_size = 1

    def encode(self, interval=None, send_freq=None, record_freq=None):
        """
        Args:
            interval (int): 計測の実施有無及び計測周期を設定.
                0:計測 OFF, 1~255: 計測周期 (1ms 単位指定)
            send_freq (int): 計測データ送信の実施有無及び送信時の平均回数を設定
                0:送信しない, 1~255: 平均回数
            record_freq (int): 計測データ記録の実施有無及び記録時の平均回数を設定
                0:記録しない, 1~255: 平均回数
        """
        assert interval >= 0 and interval < 256
        assert send_freq >= 0 and send_freq < 256
        assert record_freq >= 0 and record_freq < 256

        cmd = [
            CMD_HEADER,
            self.cmd_code,
            interval,
            send_freq,
            record_freq,
        ]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data


class GetAgsMethod(CmdTemplate):
    """加速/角速度計測設定
    """
    cmd_code = 0x17
    response_code = 0x97
    response_param_size = 3

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "interval": response[2],
            "send_freq": response[3],
            "record_freq": response[4],
        }
        return data

class SetGeoMagneticMethod(CmdTemplate):
    """地磁気計測設定
    """
    cmd_code = 0x18
    response_code = 0x8F
    response_param_size = 1

    def encode(self, interval=None, send_freq=None, record_freq=None):
        """
        Args:
            interval (int): 計測の実施有無及び計測周期を設定.
                0:計測 OFF, 1~255: 計測周期 (1ms 単位指定)
            send_freq (int): 計測データ送信の実施有無及び送信時の平均回数を設定
                0:送信しない, 1~255: 平均回数
            record_freq (int): 計測データ記録の実施有無及び記録時の平均回数を設定
                0:記録しない, 1~255: 平均回数
        """
        assert interval >= 0 and interval < 256
        assert send_freq >= 0 and send_freq < 256
        assert record_freq >= 0 and record_freq < 256

        cmd = [
            CMD_HEADER,
            self.cmd_code,
            interval,
            send_freq,
            record_freq,
        ]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetGeoMagneticMethod(CmdTemplate):
    """地磁気計測設定取得
    """
    cmd_code = 0x19
    response_code = 0x99
    response_param_size = 3

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "interval": response[2],
            "send_freq": response[3],
            "record_freq": response[4],
        }
        return data


class SetPresMethod(CmdTemplate):
    """気圧計測設定
    """
    cmd_code = 0x1A
    response_code = 0x8F
    response_param_size = 1

    def encode(self, interval=None, send_freq=None, record_freq=None):
        """
        Args:
            interval (int): 計測の実施有無及び計測周期を設定.
                0:計測 OFF, 1~255: 計測周期 (1ms 単位指定)
            send_freq (int): 計測データ送信の実施有無及び送信時の平均回数を設定
                0:送信しない, 1~255: 平均回数
            record_freq (int): 計測データ記録の実施有無及び記録時の平均回数を設定
                0:記録しない, 1~255: 平均回数
        """
        assert interval >= 0 and interval < 256
        assert send_freq >= 0 and send_freq < 256
        assert record_freq >= 0 and record_freq < 256

        cmd = [
            CMD_HEADER,
            self.cmd_code,
            interval,
            send_freq,
            record_freq,
        ]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetPresMethod(CmdTemplate):
    """地磁気計測設定取得
    """
    cmd_code = 0x1B
    response_code = 0x9B
    response_param_size = 3

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "interval": response[2],
            "send_freq": response[3],
            "record_freq": response[4],
        }
        return data


class SetBattMethod(CmdTemplate):
    """バッテリ電圧計測設定
    """
    cmd_code = 0x1C
    response_code = 0x8F
    response_param_size = 1

    def encode(self, send=None, record=None):
        """
        Args:
            is_send (int): 計測データ送信の実施有無を設定
                0:送信しない, 1:送信する.
            is_record (int): 計測データ記録の実施有無を選択
                0:記録しない、1:記録する
        """
        assert send in [0, 1]
        assert record in [0, 1]

        cmd = [
            CMD_HEADER,
            self.cmd_code,
            send,
            record,
        ]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetBattMethod(CmdTemplate):
    """バッテリ電圧計測設定取得
    """
    cmd_code = 0x1D
    response_code = 0x9D
    response_param_size = 2

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "send": response[2],
            "record": response[3],
        }
        return data



class SetAccRange(CmdTemplate):
    """加速度センサ計測レンジ設定
    """
    cmd_code = 0x22
    response_code = 0x8F
    response_param_size = 1
    translation = {
        0: "+/-2G",
        1: "+/-4G",
        2: "+/-8G",
        3: "+/-16G",
    }

    def encode(self, mode=None):
        """
        Args:
            mode (Literal[0, 1, 2, 3]): 加速度センサの計測レンジを設定
                0: +/-2G, 1:+/-4G, 2: +/-8G, 3: +/-16G
        """
        assert mode in [0, 1, 2, 3]
        
        cmd = [CMD_HEADER, self.cmd_code, mode]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetAccRange(CmdTemplate):
    """加速度センサ計測レンジ設定取得
    """
    cmd_code = 0x23
    response_code = 0xA3
    response_param_size = 1
    translation = {
        0: "+/-2G",
        1: "+/-4G",
        2: "+/-8G",
        3: "+/-16G",
    }

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "mode": response[2],
        }
        return data



class GetDeviceStatus(CmdTemplate):
    """動作状態取得
    
    Status Code:
    * 0: USB 接続中コマンドモード
    * 1: USB 接続中計測モード
    * 2: Bluetooth 接続中コマンドモード
    * 3: Bluetooth 接続中計測モード
    """
    cmd_code = 0x3C
    response_code = 0xBC
    response_param_size = 1

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "status": response[2],
        }
        return data



class SetAutoPowerOffTime(CmdTemplate):
    """オートパワーオフ時間設定

    BT 接続待機モード時のオートパワーオフ時間を設定する.
    """
    cmd_code = 0x50
    response_code = 0x8F
    response_param_size = 1

    def encode(self, minutes):
        """
        Args:
            minutes (int): オートパワーオフ時間
                0: オートパワーオフ機能無効, 1-20: オートパワーオフ時間 (分)
        """
        assert minutes >= 0 and minutes <= 20
        
        cmd = [CMD_HEADER, self.cmd_code, minutes]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetAutoPowerOffTime(CmdTemplate):
    """オートパワーオフ時間設定取得
    """
    cmd_code = 0x51
    response_code = 0xD1
    response_param_size = 1

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)
        return bytes(cmd)

    def decode(self, response):
        assert response[1] == self.response_code
        data = {
            "minutes": response[2],
        }
        return data

