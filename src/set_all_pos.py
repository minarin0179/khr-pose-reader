# coding: UTF-8
import platform
from Rcb4BaseLib import Rcb4BaseLib  # Rcb4BaseLib.pyの中のRcb4BaseLibを使用

DEVICE_NAME_WIN = "COM3"
DEVICE_NAME_LINUX = "/dev/ttyUSB0"
BUNDRATE = [115200, 625000, 1250000]  # ボーレート
TIMEOUT = 1.3  # タイムアウト(s)
FRAME_INTERVAL = 500
SIO1_4 = 0x01
SIO5_8 = 0x02


def set_servo_positions(rcb4, servo_datas, positions):
    """
    指定されたサーボモータのセットに角度を設定する関数
    :param rcb4: Rcb4BaseLib のインスタンス
    :param servo_datas: サーボモータのデータのリスト
    :param positions: 各サーボモータの目標位置
    """
    if len(servo_datas) != len(positions):
        print("サーボモータの数と位置データの数が一致しません。")
        return

    for servo_data, position in zip(servo_datas, positions):
        servo_data.Data = position

    rcb4.setServoPos(servo_datas, FRAME_INTERVAL)


def main():
    device_name = (
        DEVICE_NAME_WIN if platform.system() == "Windows" else DEVICE_NAME_LINUX
    )

    rcb4 = Rcb4BaseLib()

    for b in BUNDRATE:
        print(f"try to connect with {b}...")
        rcb4 = Rcb4BaseLib()
        if rcb4.open(device_name, b, TIMEOUT):
            print("connected")
            break
        else:
            print("failed to connect")
    else:
        print("failed to connect any baudrate")
        return

    # サーボモータの初期化（サーボモータのIDとSIOを設定）
    servo_datas = [
        rcb4.ServoData(0, SIO1_4, 0),  # 首
        rcb4.ServoData(0, SIO5_8, 0),  # 腰捻り
        rcb4.ServoData(1, SIO1_4, 0),  # 左肩捻り
        rcb4.ServoData(1, SIO5_8, 0),  # 右肩捻り
        rcb4.ServoData(2, SIO1_4, 0),  # 左肩曲げ
        rcb4.ServoData(2, SIO5_8, 0),  # 右肩曲げ
        rcb4.ServoData(3, SIO1_4, 0),  # 左肘曲げ
        rcb4.ServoData(3, SIO5_8, 0),  # 右肘曲げ
        rcb4.ServoData(4, SIO1_4, 0),  # 左手捻り
        rcb4.ServoData(4, SIO5_8, 0),  # 右手捻り
        rcb4.ServoData(5, SIO1_4, 0),  # 左足捻り
        rcb4.ServoData(5, SIO5_8, 0),  # 右足捻り
        rcb4.ServoData(6, SIO1_4, 0),  # 左足開閉
        rcb4.ServoData(6, SIO5_8, 0),  # 右足開閉
        rcb4.ServoData(7, SIO1_4, 0),  # 左足前後
        rcb4.ServoData(7, SIO5_8, 0),  # 右足前後
        rcb4.ServoData(8, SIO1_4, 0),  # 左足膝
        rcb4.ServoData(8, SIO5_8, 0),  # 右足膝
        rcb4.ServoData(9, SIO1_4, 0),  # 左足首
        rcb4.ServoData(9, SIO5_8, 0),  # 右足首
        rcb4.ServoData(10, SIO1_4, 0),  # 左足首捻り
        rcb4.ServoData(10, SIO5_8, 0),  # 右足首捻り
    ]

    # サーボモータの目標位置を設定
    positions = [
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
    ]

    set_servo_positions(rcb4, servo_datas, positions)

    # 接続解除
    rcb4.close()


if __name__ == "__main__":
    main()
