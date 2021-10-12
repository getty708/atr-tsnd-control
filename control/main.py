from tsndctl.device import TSND151
import time

DEVICE_NAME = "ATR-01"
DEVICE_PORT = "/dev/tty.TSND151-AP03160248-Blue"

if __name__ == "__main__":
    device = TSND151(DEVICE_NAME, DEVICE_PORT, timeout=None)
    print("check0-1", device)


    # == Setup Device Parameters ==
    time.sleep(5)
    device.init_device()
    time.sleep(5)
    
    # # == Recordeing ===
    # time.sleep(5)
    # device.start_recording()
    # device.start()
    # time.sleep(20)
    # device.stop()
    # device.stop_recording()
    # # device.start()
    # time.sleep(5)

    # -- End --
    device.terminate()