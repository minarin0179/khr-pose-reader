# coding: UTF-8
import sys
from os.path import dirname, abspath, join

lib_path = "../lib"
lib_abs_path = abspath(join(dirname(__file__), lib_path))
sys.path.append(lib_abs_path)  # Rcb4Libの検索パスを追加

from Rcb4BaseLib import Rcb4BaseLib  # Rcb4BaseLib.pyの中のRcb4BaseLibが使えるように設定
import time  # timeが使えるように宣言

rcb4 = Rcb4BaseLib()  # rcb4をインスタンス(定義)

isOpened = rcb4.open("/dev/ttyUSB0", 115200, 1.3)  # (portName,bundrate,timeout(s))

# rcb4.openはcheckAcknowledgeの結果を返す
# 失敗した場合に再度checkAcknowledgeを行うとエラーになるので注意

if isOpened == True:  # 通信が返ってきたとき
    servoDatas = [
        # SIO1-2
        rcb4.ServoData(0, 0x01, 0),  # 首
        rcb4.ServoData(1, 0x01, 0),  # 左肩捻り
        rcb4.ServoData(2, 0x01, 0),  # 左肩曲げ
        rcb4.ServoData(3, 0x01, 0),  # 左肘曲げ
        rcb4.ServoData(4, 0x01, 0),  # 左手捻り
        # SIO3-4
        rcb4.ServoData(5, 0x01, 0),  # 左足捻り
        rcb4.ServoData(6, 0x01, 0),  # 左足開閉
        rcb4.ServoData(7, 0x01, 0),  # 左足前後
        rcb4.ServoData(8, 0x01, 0),  # 左足膝
        rcb4.ServoData(9, 0x01, 0),  # 左足首
        rcb4.ServoData(10, 0x01, 0),  # 左足首捻り
        # SIO5-6
        rcb4.ServoData(0, 0x02, 0),  # 腰捻り
        rcb4.ServoData(1, 0x02, 0),  # 右肩捻り
        rcb4.ServoData(2, 0x02, 0),  # 右肩曲げ
        rcb4.ServoData(3, 0x02, 0),  # 右肘曲げ
        rcb4.ServoData(4, 0x02, 0),  # 右手捻り
        # SIO7-8
        rcb4.ServoData(5, 0x02, 0),  # 右足捻り
        rcb4.ServoData(6, 0x02, 0),  # 右足開閉
        rcb4.ServoData(7, 0x02, 0),  # 右足前後
        rcb4.ServoData(8, 0x02, 0),  # 右足膝
        rcb4.ServoData(9, 0x02, 0),  # 右足首
        rcb4.ServoData(10, 0x02, 0),  # 右足首捻り
    ]

    while True:
        command = input()

        if command == "hold":
            rcb4.setHoldPos(servoDatas)
        if command == "free":
            rcb4.setFreePos(servoDatas)
        if command == "get":
            # サーボモーターの現在位置を取得する
            rotations = []
            for servodata in servoDatas:
                (flag, posData) = rcb4.getSinglePos(servodata.Id, servodata.Sio)
                rotation = (posData - 7500) * (180 / 5300)
                rotations.append(rotation)
                if flag:
                    pass
                    # print(f"servoId:{servodata.Id} posData:{posData} rotation:{rotation}")

                else:
                    pass
                    # print(f"servoId:{servodata.Id} error")e

            formatted_nums = [format(num, ".1f") for num in rotations]
            print(*formatted_nums)

else:  # 通信が返ってきていないときはエラー
    print("checkAcknowledge error")


rcb4.close()
