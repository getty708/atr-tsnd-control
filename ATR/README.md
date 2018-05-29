## ATR
ATRの加速度センサの前処理プログラム群.

### LOG2ADL
ATRで取得したlogファイルから`ADLtagger`で使用可能なファイル形式に変換.


### adl_to_csv.py

#### sub-command: MIX
ADLtaggerのファイルフォーマットのAccとGyroを単一のCSVに結合. 出力時に単位を変換.

+ Acc : `0.1[mG]` => `[G]`
+ Gyro: `0.01[dps]` => `[dps]`

Ref: 取得したデータのフォーマットは?,  http://www.atr-p.com/support/TSND-QA.html
