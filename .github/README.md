# 開発環境のセットアップ

Windows 上で Dev Container を使用して開発環境を構築する場合，コンテナ内で USB デバイスを利用するためにあらかじめ Windows 側で設定を行う必要があります．

## 1. USB/IP ドライバのインストール

以下のコマンドを実行し，USB/IP ドライバをインストールします．

```pwsh
winget install usbipd
```

## 2. USB デバイスの共有

以下のコマンドを実行し，共有したい USB デバイスの BUSID を確認します．

```pwsh
usbipd list
```

確認した BUSID を用いて以下のコマンドを実行し，USB デバイスを共有します．

```
usbipd bind --busid=<BUSID>
```

デバイスの共有の設定は永続化されます．
デバイスを取り外しても，再度接続すると自動的に共有されます．
もし，共有を解除したい場合は以下のコマンドを実行します．

```
usbipd unbind --busid=<BUSID>
```

## 3. USB デバイスの接続

以下のコマンドを実行し，USB デバイスを接続します．

```pwsh
usbipd attach --wsl --busid=<BUSID>
```

詳細な情報については [公式ドキュメント](https://github.com/dorssel/usbipd-win) を参照してください．
