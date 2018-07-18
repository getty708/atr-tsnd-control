# ATR
ATRの加速度センサの前処理プログラム群.


------------------------------
## [ラベル有りデータ用] `log_to_adl.py`
ATRで取得したlogファイルから`ADLtagger`で使用可能なファイル形式に変換.

## [ラベル有りデータ用] `adl_to_csv.py`
### sub-command: MIX
+ ADLtaggerのファイルフォーマットのAccとGyroを単一のCSVに結合. 出力時に単位を変換.
+ 単位の変換を下記の通り行う.
+ 出力CSVの形式:
  + AGS: `time,label,label_id,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z`


------------------------
## [ラベル無しデータ用] `log_to_csv.py`

+ ラベル無しデータをLOGから直接CSVに変換.
+ 出力CSVの形式:
  + AGS: `time,label,label_id,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z`
  + Geo: `time,label,label_id,geo_x,geo_y,geo_z`
+ 単位の変換を下記の通り行う.

------------------
## Unit
+ Ref. [取得したデータのフォーマットは?](http://www.atr-p.com/support/TSND-QA.html)

| Sensor | Raw Data          | Output  |
|--------|-------------------|---------|
| Acc    | `0.1[mG]`         | `[G]`   |
| Gyro   | `0.01[dps]`       | `[dps]` |
| Geo:   | `0.1[x10^{-6} T]` | `[T]`   |



----------------------------
# その他
+ [ATR TSND151 Command Sheet](./ATR_CommandSheet.md)
