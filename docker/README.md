# Use Doker with GPU enable

参考
+ http://qiita.com/shouta-dev/items/22a5c387cac82bef9f83



## docker-composeを使う
### Build & Run

```bash
docker-compose build
docker-compose up
```

### Jupyter notebook
+ まずPWのtokenを生成する.

```bash
# configファイルを作成
$ jupyter notebook --generate-config
# パスワードの生成 (token)
$ python -c 'from notebook.auth import passwd;print(passwd())'
```

+ パスワードを登録
`~/.jupyter/jupyter_notebook_config.py `に以下の記述を追加. 

```
c.NotebookApp.password = '<generated token>'
```




-----------------------------------------------
## Build Command
#### コンテナのbuild
コンテナの設定を行っているときは毎回コンテナを削除できる`--rm`をoptionに含めると良い.

```bash
# 最もシンプルな起動(毎回コンテナを削除)
$ docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0  --name <container name>  -p 8888:8888 -p 6006:6006 -it  --rm <docker image>
# directoryをマウント
$  docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 -v <host dir>:<container dir>  --name <container name>  -p 8888:8888 -p 6006:6006 -it <docker image> <起動コマンド>
# Jupyuerを起動
$  docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 -v <host dir>:<container dir>  --name <container name>  -p 8888:8888 -p 6006:6006 -it <docker image> <起動コマンド>

```

例:
```
$ docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 -v /home/naoya/code708/upconversion:/root/upconversion  --name upconversion  -p 8888:8888 -p 6006:6006 -it upconversion:tmp jupyter notebook --allow-root
```

#### コンテナの起動
```
$ docker start <container name>
```

#### コンテナのbashに入る
```
# [1] 推奨
$ docker exec upconversion bash
# [2]: 直接メインのコンテナに接続するので, 意図しないところでコンテナを止める可能性がある.
$ docker attach upconversion
```

