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
    cmd_code: int = None 
    response_code: int = None
    pyload: bytes = None
    
    def __init__(self):
        pass

    def encode(self):
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()
    

class SetDeviceTime(CmdTemplate):
    cmd_code = 0x11
    response_code = 0x8F

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

    def decode(self, response):
        assert response[1] == self.response_code
        data = response[2]
        return data

class GetDeviceTime(CmdTemplate):
    cmd_code = 0x12
    response_code = 0x92

    def encode(self):
        cmd = [CMD_HEADER, self.cmd_code, 0x00]
        cmd = add_bcc(cmd)

        return bytes(cmd)

    def decode(self, response: bytes) -> datetime.datetime:
        # raise NotImplementedError()
        assert response[1] == self.response_code
        
        # -- Decode --
        # # year
        # data = [(response[2] + 2000)]
        # # month, day, hour, minute, second 
        # data += list(response[3:8])
        # # milli second,
        # data.append(int.from_bytes(response[8:10], 'little'))
        # ts = datetime.datetime(*data)
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


class SetAgsMethod(CmdTemplate):
    """加速/角速度計測設定取得
    """
    cmd_code = 0x16
    response_code = 0x8F

    def encode(self, interval, send_freq, record_freq):
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

    def encode(self, interval, send_freq, record_freq):
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

    def encode(self, interval, send_freq, record_freq):
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

    def encode(self, send, record):
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
    translation = {
        0: "+/-2G",
        1: "+/-4G",
        2: "+/-8G",
        3: "+/-16G",
    }

    def encode(self, mode):
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

    def encode(self, minutes):
        """
        Args:
            minutes (int): オートパワーオフ時間
                0: オートパワーオフ機能無効, 1-20: オートパワーオフ時間（分）
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

