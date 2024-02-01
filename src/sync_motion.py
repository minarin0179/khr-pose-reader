# coding: UTF-8
import platform
from Rcb4BaseLib import Rcb4BaseLib  # Rcb4BaseLib.pyの中のRcb4BaseLibが使えるように設定
import time

DEVICE_NAME_WIN_SRC = "COM3"
DEVICE_NAME_WIN_DST = "COM6"
DEVICE_NAME_LINUX_SRC = "/dev/ttyUSB0"
DEVICE_NAME_LINUX_DST = "/dev/ttyUSB1"
BUNDRATE = [115200, 625000, 1250000]  # ボーレート
TIMEOUT = 1.3  # タイムアウト(s)
FRAME_INTERVAL = 200
SIO1_4 = 0x01
SIO5_8 = 0x02


# サーボモーターのIDと位置を設定する関数
def set_servo_position(rcb4, servo_id, position, frame=100):
    if not rcb4.setSingleServo(servo_id, SIO1_4, position, frame):
        print(f"Failed to set position for servo ID {servo_id}")


def main():
    device_name_src = (
        DEVICE_NAME_WIN_SRC if platform.system() == "Windows" else DEVICE_NAME_LINUX_SRC
    )

    device_name_dst = (
        DEVICE_NAME_WIN_DST if platform.system() == "Windows" else DEVICE_NAME_LINUX_DST
    )

    for b in BUNDRATE:
        print(f"try to connect with {b}...")
        rcb4_src = Rcb4BaseLib()
        if rcb4_src.open(device_name_src, b, TIMEOUT):
            print("connected")
            break
        else:
            print("failed to connect")
    else:
        print("failed to connect any baudrate")
        return

    for b in BUNDRATE:
        print(f"try to connect with {b}...")
        rcb4_dst = Rcb4BaseLib()
        if rcb4_dst.open(device_name_dst, b, TIMEOUT):
            print("connected")
            break
        else:
            print("failed to connect")
    else:
        print("failed to connect any baudrate")
        return

    servoDatas = [
        rcb4_src.ServoData(0, SIO1_4, 0),  # 首
        rcb4_src.ServoData(0, SIO5_8, 0),  # 腰捻り
        rcb4_src.ServoData(1, SIO1_4, 0),  # 左肩捻り
        rcb4_src.ServoData(1, SIO5_8, 0),  # 右肩捻り
        rcb4_src.ServoData(2, SIO1_4, 0),  # 左肩曲げ
        rcb4_src.ServoData(2, SIO5_8, 0),  # 右肩曲げ
        rcb4_src.ServoData(3, SIO1_4, 0),  # 左肘曲げ
        rcb4_src.ServoData(3, SIO5_8, 0),  # 右肘曲げ
        rcb4_src.ServoData(4, SIO1_4, 0),  # 左手捻り
        rcb4_src.ServoData(4, SIO5_8, 0),  # 右手捻り
        rcb4_src.ServoData(5, SIO1_4, 0),  # 左足捻り
        rcb4_src.ServoData(5, SIO5_8, 0),  # 右足捻り
        rcb4_src.ServoData(6, SIO1_4, 0),  # 左足開閉
        rcb4_src.ServoData(6, SIO5_8, 0),  # 右足開閉
        rcb4_src.ServoData(7, SIO1_4, 0),  # 左足前後
        rcb4_src.ServoData(7, SIO5_8, 0),  # 右足前後
        rcb4_src.ServoData(8, SIO1_4, 0),  # 左足膝
        rcb4_src.ServoData(8, SIO5_8, 0),  # 右足膝
        rcb4_src.ServoData(9, SIO1_4, 0),  # 左足首
        rcb4_src.ServoData(9, SIO5_8, 0),  # 右足首
        rcb4_src.ServoData(10, SIO1_4, 0),  # 左足首捻り
        rcb4_src.ServoData(10, SIO5_8, 0),  # 右足首捻り
    ]

    rcb4_src.setFreePos(servoDatas)
    servodata = rcb4_src.ServoData(1, SIO1_4, 0)

    while True:
        (flag, posData) = rcb4_src.getSinglePos(servodata.Id, servodata.Sio)
        if flag:
            set_servo_position(rcb4_dst, servodata.Id, posData)

        time.sleep(2)

    rcb4_src.close()
    rcb4_dst.close()


if __name__ == "__main__":
    main()
