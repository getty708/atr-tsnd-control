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
python recording.py client=<client>
```

### Clear Memory

```bash
python clear_mem.py client=<client>
```

### Download Recorded Data

```bash
python download.py client=<client>
```

## Supported Command

TBA

## Reference

- [ATR - 小型無線多機能センサ「TSND121/151」](http://www.atr-p.com/products/TSND121_151.html)
- [ATR - 小型無線多機能センサ（TSND151) コマンドインタフェース仕様書](http://www.atr-p.com/products/pdf/TSND151-cmd-spec.pdf)
