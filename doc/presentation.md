# 知能ロボット制御論 KHR 演習 競技会 UI 部門

## ライブラリ

やりたいこと：

- サーボモータの角度を取得して，なにかしら利用したい

演習で使用している機材：

- KHR-3HV Ver.2（22 軸バージョン）
    - コントロールボード RCB-4HV
    - サーボモーター KRS-2552RHV ICS

<!-- ## 第 0 の罠：埋もれる大量のドキュメント 
2週目まではただ調べるだけで終わり何も動かしていない状態
焦り、不安 
-->

## 第 1 の罠：サーボモータが一見すると角度の取得に非対応

サーボモータが角度の取得に対応している必要がある．
[サーボモータの機能一覧](https://kondo-robot.com/faq/ics3-5-explain)：

![image](https://hackmd.io/_uploads/SkDMSfFq6.png)

- サーボモータが ICS3.**6** に対応していれば角度が取得可能

[使用されているサーボモータの仕様](https://kondo-robot.com/product/krs-2552rhv-ics)：

![image](https://hackmd.io/_uploads/ByjrrfK96.png)

- 使用されているサーボモータは ICS3.**5**

じゃあ，このサーボモータは角度の取得に非対応なのか？
[KHR サーボから角度を取得する Python のプログラム](https://kondo-robot.com/faq/krs_tutorial_py1) があった．
実は対応している：

![image](https://hackmd.io/_uploads/H1968MK5T.png)

現在位置はポジションコマンドを送信した時に返事で返ってくるらしい．

## 第 2 の罠：CSE で動かない C# ライブラリ
<!-- RCB4「ここを通るなら、俺を倒してから行け」 -->

上述のサーボモータは下図のような構成で PC に直接サーボモータを接続している：

![image](https://hackmd.io/_uploads/HJgPOzt9T.png)

今回のロボットは，間にマイコンボードを挟むことになる．
マイコンボードの製品説明を眺めているとライブラリがあった：

![image](https://hackmd.io/_uploads/H1vNZ7Yca.png)
![image](https://hackmd.io/_uploads/ryJOhGF5T.png)

しかし，ライブラリは DLL 形式で実行には .NET ランタイムが必要で CSE では動かない：

![image](https://hackmd.io/_uploads/r1ykrmF9a.png)

そうなると `khrsend` が使えないのでつらい．

マイコンボードのサポート情報を眺めていると Python ライブラリ（ベータ版）があった：

![image](https://hackmd.io/_uploads/ryGPSXtqT.png)

Python なら CSE でも動くしカンペキ．．．なはずだった．．．

## 第 3 の罠：酷すぎる公式の Python ライブラリ

### エラーだらけのライブラリ

インデントでタブとスペースが統一されていない：

![image](https://hackmd.io/_uploads/rkV7d7K5T.png)

変数名のタイポ（リンター使ってくれ～）：

![image](https://hackmd.io/_uploads/ryXBdmtq6.png)

乏しいうえに動かないサンプルコード

サンプルコードのRcb4AckTestでCOMポートを開けなかった場合の実装がミスっていてエラーになる

![image](https://hackmd.io/_uploads/r1A83QFcT.png)

サンプルコード自体も非常に少なく、網羅的でない  
ACKテスト,登録済みのモーションの再生, 仮想ボタン入力 についての3例のみ  
サーボモータの制御に関する実装例は一切なし

エラーメッセージが未実装

エラーが発生しても実行結果の成否をboolで返すだけ

エラー箇所やエラー内容は教えてくれない

確認するためにライブラリを書き換えて地道にprintデバッグ つらい

### パッケージングされていないライブラリ

![image](https://hackmd.io/_uploads/By7QqXKqa.png)

手動でパスを指定する必要があり煩雑．
`pip` でインストールしたいよ～．
PyPI で公開してくれ～．

## 第 4 の罠：ロボットの個体差

No.1のロボットは不幸な事故により前日に骨折して

＿人人 人人＿  
＞ 突然の死 ＜  
￣Y^Y^Y^Y￣

他のロボットに乗り換えると何故か今まで動いていたコードが動かない．．．

- ケーブルを替えてみる
- ロボットを替えてみる
- 端末を変えてみる
- OS を変えてみる

何をやっても動かない 焦燥, 諦め, 絶望

そして奇跡、天啓は突然にして訪れる

ボーレートが合ってないのではないか？

![image](https://hackmd.io/_uploads/SyJXhzK56.png)

RCB4 の通信速度は 115200, 625000, 1250000 の 3 段階で設定できる

ボーレートを変えながら試してみるとバチコリ動作
原因 : ロボットごとにマイコンに設定されているボーレートが違った

先生へ 

来年度以降は揃えた上で,UI班向けに情報として公開してください  
それによって救われる命があります

## 環境構築

### 仮想環境

![image](https://hackmd.io/_uploads/SJTlzVKc6.png)

仮想環境って環境が統一できて便利ですよね～
しかし，Dokcer は USB デバイスに対応していないらしいです：

![image](https://hackmd.io/_uploads/H1ATTXY9a.png)

諦めずに調べていると Microsoft が出している面白い情報を見つけました：

![image](https://hackmd.io/_uploads/SkLOCQFcp.png)

ハイパーバイザである WSL2 が USB に対応するなら Dokcer でも USB が使えるのでは？
ためしてみました：

![image](https://hackmd.io/_uploads/Hk13zEFqp.png)
![image](https://hackmd.io/_uploads/r15aMVYqa.png)

本来なら `/dev` 上に `ttyUSB0` ｔ
`lsusb` では認識されているが，デバイスとしては認識されていない．
どうやら WSL2 に USB のシリアル通信用のカーネルが存在せず，カーネルのリビルドが必要！

ほかの手法：

- usbipd-win 以外の USB over IP 接続ツール
    - VirtualHere
    - USB/IP プロジェクト
- 仮想マシン
    - VirtualBox + Vagrant

本末転倒感が否めないので諦めました．．．

### tasks.json によるセットアップの自動化



## 成果物
今回作成したものはGitHubにて公開しています

https://github.com/minarin0179/khr-pose-reader

### csv から mot への変換ツール「[csv2mot](https://github.com/minarin0179/khr-pose-reader/blob/main/src/csv2mot.py)」

khrmedit3 に対する不満

- 実行用の csv と保存用の mot ファイルが別管理
- csv から mot への変換ができない

更新漏れ、保存忘れが発生する

csv から mot への逆変換を実装し，csv ファイルでの一元管理を実現する

#### モーションデータの形式

csv と mot はかなり構造が違う

| ファイル形式 | 区切り文字 | 並び順 | ヘッダー | 関節角度の表現 |
| --------   | -------- | -------- | -------- | -------- |
|     csv    |  スペース | サーボのID順 | なし | 7500±5300 |
|     mot    | カンマ&スペース(?) | 部位ごと | 関節数,総フレーム数 | 90°±135° |

ファイルの構造さえ分かれば後はその通りに実装するだけ

### ロボットの姿勢を取得してモーションを作成するツール「[khr-pose-reader](https://github.com/minarin0179/khr-pose-reader/blob/main/src/main.py)」

khrmedit3 に対する不満 part2

香ばしいワークフロー

1. khrmeditでモーションを作成 : 地獄の手動パラメーター調整
2. csvで出力 : なぜそのまま送れないのか…
4. khrshimで動作確認 : 面倒だから形骸化
5. khrsendで実機確認 : ロボットのバランスを取るのは簡単ではない
 
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

前述の csv2mot と組み合わせれば収録したモーションの編集も可能

### ロボットをコントローラーにロボットを動かすツール「[sync_motion](https://github.com/minarin0179/khr-pose-reader/blob/feature/set-position/src/set_all_pos.py)」

サーボの角度ができたらどんなことができそうか

1台のロボットから取得した関節角度をもう一台にそのまま送信

⇒2台のロボットが同期してリアルタイムで動く

結論 : 実装が間に合わなかった

原因 : サーボモーターを複数同時に動かすコマンドが動かなかった

成果 : 一つの関節だけを同期するところまではできていて欲しい(願望)
