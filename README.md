# sensor_utils
ATRやsmart phone, smart watchなどのセンサデータの前処理ライブラリ


## Build
`docker-compose`を使用.

```bash
docker-compose build
docker-compose up
```
### Passwordの設定
コンテナを起動した状態で以下のコマンドを実行.
```
# コンテナ内
jupyter notebook password
# コンテナ外
docker-compose exec work jupyter notebook password
```
コンテナを再起動させて、設定したpasswordでログイン.


----------------------------------
# Components
## ATR
ATRの加速度センサの前処理プログラム群.

### LOG2ADL
ATRで取得したlogファイルから`ADLtagger`で使用可能なファイル形式に変換.

#### Usage


#### Params

