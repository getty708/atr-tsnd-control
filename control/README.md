# Sensor Node Control via Bluetooth

## System Requirements

- TBA

## Usage

### Initialize Sensor Status 

Include clock sync.

```bash
python init_sensor.py client=<client>
```

client choices:

- atr01 (macOS)
- atr02 (macOS)
- atr01-win (windows)
- atr02-win (windows)

### Recoding

```bash
# Start 
python start_recording.py client=<client>

# Monitor the Values
python listen_event.py client=<client>

# Stop
python start_recording.py client=<client>
```

### Clear Memory

```bash
python clear_mem.py client=<client>
```

### Download Recorded Data

Data is stored as logfile on `./outputs/ATR0X/YYYY-mm-dd/HH-MM-SS/download.log`

```bash
python download.py client=<client>
```

Example of outputs:
```text
client:
  name: ATR01
  port: /dev/tty.TSND151-AP03160248-Blue
timeout: 5

[2021-10-21 20:16:38,700][__main__][INFO] - == Download Data in Device's Memory ==
[2021-10-21 20:16:48,324][__main__][DEBUG] - Success ... Initialize TSND151() object and open connection.
[2021-10-21 20:16:48,324][tsndctl.TSND151.ATR01][INFO] - == Check Memory Status ==
[2021-10-21 20:16:48,371][tsndctl.TSND151.ATR01][INFO] - MemEntryCount:: {'status': 0, 'num_entry': 4}
[2021-10-21 20:16:48,522][tsndctl.TSND151.ATR01][INFO] - FreeMemSize:: {'status': 0, 'num_free_entries': 76, 'num_free_records': 4286578764}
Which entry do you want to download ? (Entry.1 ~ 4) [type the number] >> 
```

For convert logfile to CSV, check [this notebook](https://github.com/getty708/atr-tk/blob/master/control/notebooks/Dev_CheckDownloadedRecords.ipynb).

## Supported Command

TBA

## Reference

- [ATR - 小型無線多機能センサ「TSND121/151」](http://www.atr-p.com/products/TSND121_151.html)
- [ATR - 小型無線多機能センサ（TSND151) コマンドインタフェース仕様書](http://www.atr-p.com/products/pdf/TSND151-cmd-spec.pdf)
