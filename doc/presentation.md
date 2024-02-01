# 知能ロボット制御論 KHR 演習 競技会 UI 部門

## やりたいこと

サーボモータの角度を取得して，なにかしら利用したい．

<!-- ## 第 0 の罠：埋もれる大量のドキュメント 
2週目まではただ調べるだけで終わり何も動かしていない状態
焦り、不安 
-->

## UI 部門を待ち受ける数々の罠

### 第 1 の罠：サーボモータが一見すると角度取得に非対応

演習で使用している機材：

- KHR-3HV Ver.2（22 軸バージョン）
    - コントロールボード RCB-4HV
    - サーボモーター KRS-2552RHV ICS

サーボモータが角度の取得に対応している必要がある．
[サーボモータの機能一覧](https://kondo-robot.com/faq/ics3-5-explain)：

![image](https://hackmd.io/_uploads/SkDMSfFq6.png)

- サーボモータが ICS3.**6** に対応していれば角度が取得可能

[使用されているサーボモータの仕様](https://kondo-robot.com/product/krs-2552rhv-ics)：

![image](https://hackmd.io/_uploads/ByjrrfK96.png)

- 使用されているサーボモータは ICS3.**5**

では，このサーボモータは角度の取得に非対応なのか？
[KHR サーボから角度を取得する Python のプログラム](https://kondo-robot.com/faq/krs_tutorial_py1) があった．
実は対応している：

![image](https://hackmd.io/_uploads/H1968MK5T.png)

現在位置はポジションコマンドを送信した時に返事で返ってくるらしい．

### 第 2 の罠：CSE で動かない C# ライブラリ
<!-- RCB4「ここを通るなら、俺を倒してから行け」 -->

上述のサーボモータは下図のような構成で PC に直接サーボモータを接続している：

![image](https://hackmd.io/_uploads/HJgPOzt9T.png)

今回のロボットは，間にマイコンボードを挟むことになる．

マイコンボードの製品説明を眺めているとライブラリがあった：

![image](https://hackmd.io/_uploads/H1vNZ7Yca.png)
![image](https://hackmd.io/_uploads/ryJOhGF5T.png)

しかし，ライブラリは `DLL` 形式で実行には `mono` が必要で CSE では動かない：

![image](https://hackmd.io/_uploads/r1ykrmF9a.png)

そうなると `khrsend` が使えないのでつらい．

マイコンボードのサポート情報を眺めていると Python ライブラリ（ベータ版）があった：

![image](https://hackmd.io/_uploads/ryGPSXtqT.png)

Python なら CSE でも動くしカンペキ．．．なはずだった．．．

### 第 3 の罠：酷すぎる公式の Python ライブラリ

#### エラーだらけのライブラリ

インデントでタブとスペースが統一されていない：

![image](https://hackmd.io/_uploads/rkV7d7K5T.png)

変数名のタイポ（リンター使ってくれ～）：

![image](https://hackmd.io/_uploads/ryXBdmtq6.png)

#### 少ないうえに動かないサンプルコード

サンプルコードの `Rcb4AckTest.py` で COM ポートを開けなかった場合の実装がミスっていてエラーになる．

![image](https://hackmd.io/_uploads/r1A83QFcT.png)

サンプルコード自体も非常に少なく、網羅的でない．

ACK テスト・登録済みのモーションの再生・仮想ボタン入力 についての 3 例のみ

サーボモータの制御に関する実装例は一切なし．

#### エラーメッセージが未実装

実行結果の成否を bool で返すだけ．

エラー箇所やエラー内容は教えてくれない．

確認するためにライブラリを書き換えて地道に print デバッグ つらい．

#### パッケージングされていないライブラリ

![image](https://hackmd.io/_uploads/By7QqXKqa.png)

手動でパスを指定する必要があり煩雑．
`pip` でインストールしたいよ～．
PyPI で公開してくれ～．

## ライブラリのパッケージング

`RCB4Lib` を pip でインストールできる形にするためのソースコードを書いた：

![image](https://hackmd.io/_uploads/HJ2VwVF96.png)

実際にインストールしてみる：

![image](https://hackmd.io/_uploads/rkrFD4KcT.png)

`pip` でローカルのパスを指定することでインストールできた！
実際にインポートしてみる：

![image](https://hackmd.io/_uploads/rkvW_VFcT.png)

ライブラリのパスを指定しないでもインポートが機能している．
せめてこれを近藤科学のほうで公開してくれればなぁ．．．

## 環境構築

### 仮想環境

![image](https://hackmd.io/_uploads/SJTlzVKc6.png)

仮想環境って環境が統一できて便利ですよね～

しかし，Dokcer は USB デバイスに対応していないらしい：

![image](https://hackmd.io/_uploads/H1ATTXY9a.png)

諦めずに調べていると Microsoft が出している面白い情報を見つけた：

![image](https://hackmd.io/_uploads/SkLOCQFcp.png)

ハイパーバイザである WSL2 が USB に対応するなら Dokcer でも USB が使えるのでは？

ためしてみた：

![image](https://hackmd.io/_uploads/Hk13zEFqp.png)
![image](https://hackmd.io/_uploads/r15aMVYqa.png)

- 本来なら `/dev` 上に `ttyUSB0` として認識されるはず．
- `lsusb` では認識されているが，デバイスとしては認識されていない．
- どうやら WSL2 に USB のシリアル通信用のカーネルが存在せず，カーネルのリビルドが必要！

本末転倒感が否めないので諦めた．．．
ほかの手法：

- `usbipd-win` 以外の USB over IP 接続ツール
    - VirtualHere
    - USB/IP プロジェクト
- 仮想マシン
    - VirtualBox + Vagrant

これらも手順が煩雑で本末転倒感が否めないので諦めた．．．

### Visual Studio Code の tasks.json によるセットアップの自動化

![image](https://hackmd.io/_uploads/ByqMVNFqa.png)

#### ステップ 1 : Python 仮想環境の作成

#### ステップ 2 : RCB4Lib のダウンロード

GitHub でソースコードを公開したい．．．けど，近藤科学のライブラリをそのまま公開するのは権利的に心配．

なので，ライブラリを自動でダウンロードして配置するシェルスクリプト & BAT ファイルを書いた！

ダウンロードしたライブラリを `.gitignore` に追加することで，GitHub に公開してもライブラリ自体は公開されない．

#### ステップ 3 : RCB4Lib の自動修正

![image](https://hackmd.io/_uploads/S1RjB4Yq6.png)

- Python のフォーマッタ Black でフォーマットする
    - タブとスペースが統一されていない問題が解消される
- sed コマンドでエラーのある行を置き換える
    - `buf` を `txbuf` に置き換える

#### ステップ 4 : RCB4Lib を `pip` でインストール

## 4 週間後に命運が決まる、`khr-pose-reader` という偶然の物語

ここまでたどり着く過程でいくつもの奇跡に支えられてきた

### 奇跡 1：想像で書いたソースコードが一発で動いた

ロボットの実機がないと動作確認ができない

そうは言っても時間がないから家でも作業をするしかない

必死にライブラリを読み解きながら，おそらく動くであろうコードを書き上げる

そして翌週，実際にコードを実行すると見事一発で動作

### 奇跡 2：たまたま動くロボットを引き当てる

UI 班のロボットは不幸な事故により発表前日に足を骨折した

仕方なく他のロボットに乗り換えると何故か今まで動いていたコードが動かない．．．

- ケーブルを替えてみる
- ロボットを替えてみる
- 端末を変えてみる
- OS を変えてみる

何をやっても動かない 焦燥, 諦め, 絶望．

そして奇跡、天啓は突然にして訪れる．

「通信速度が合ってないのではないか？」

![image](https://hackmd.io/_uploads/SyJXhzK56.png)

RCB4 の通信速度（bps）は `115200`, `625000`, `1250000` の 3 段階で設定できる．

通信速度を変えながら試してみるとバチコリ動作．

原因 : ロボットごとにマイコンに設定されている通信速度が違った

たまたま最初に通信レートが合うロボットを引いていなければ，おそらく挫折してた


先生へ

> 来年度以降は揃えた上で，UI 班向けに情報として公開してください．  
> それによって救われる命があります．


## 成果物

今回作成したものは[GitHub](
https://github.com/minarin0179/khr-pose-reader)で公開しています


### ロボットの姿勢を取得してモーションを作成するツール「[khr-pose-reader](https://github.com/minarin0179/khr-pose-reader/blob/main/src/main.py)」

`khrmedit3` に対する不満

香ばしいワークフロー

1. `khrmedit` でモーションを作成 : 地獄の手動パラメーター調整
2. csv で出力 : なぜそのまま送れないのか…
4. `khrshim` で動作確認 : 面倒だから形骸化
5. `khrsend` で実機確認 : ロボットのバランスを取るのは簡単ではない
 
メリット

1. パラメーターの手入力不要
2. 複数の関節を同時に動かす複雑な動きも短時間で作成
3. パーツ同士の物理干渉は実機で確認しながら調整
4. バランスの調整も実機を動かしながら調整可能

使い方

1. サーボモーターをフリー状態にする
2. ロボットにポーズをとらせる
3. 関節角度を取得する
4. 取得したデータをcsvで保存する


### csv から mot への変換ツール「[csv2mot](https://github.com/minarin0179/khr-pose-reader/blob/main/src/csv2mot.py)」

`khrmedit3` に対する不満 part2

- 実行用の csv と保存用の mot ファイルが別管理
- csv から mot への変換ができない

更新漏れ、保存忘れが発生する

csv から mot への逆変換を実装することで，csv ファイルでの一元管理を実現する

前述の `khr-pose-reader` と併用することで収録したモーションの編集が可能


#### モーションデータの形式

| ファイル形式   | 区切り文字        | 並び順       | ヘッダー       |  関節角度の表現  |
| ------------ | --------------- | ----------- | -----------   | ------------- |
| csv          | スペース          | サーボのID順 | なし           | 7500±5300     |
| mot          | カンマ+スペース    | 部位ごと     | 関節数,総フレーム数 | 90°±135°   |

手作業による地道な仕様調査 このあたりの情報も公開してほしい

ファイルの構造さえ分かれば後はその通りに実装するだけ

### ロボットをコントローラーにロボットを動かすツール「[sync_motion](https://github.com/minarin0179/khr-pose-reader/blob/feature/set-position/src/set_all_pos.py)」

サーボの角度ができたらどんなことができそうか

1 台のロボットから取得した関節角度をもう一台にそのまま送信

⇒ 2 台のロボットが同期してリアルタイムで動く

結論 : 実装が間に合わなかった

原因 : サーボモーターを複数同時に動かすコマンドが動かなかった

成果 : 一つの関節だけを同期するところまではできていて欲しい(願望)
