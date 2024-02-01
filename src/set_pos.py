# coding: UTF-8
import platform
from Rcb4BaseLib import Rcb4BaseLib  # Rcb4BaseLib.pyの中のRcb4BaseLibが使えるように設定
import time

DEVICE_NAME_WIN = "COM3"
DEVICE_NAME_LINUX = "/dev/ttyUSB0"
BUNDRATE = 1250000  # ボーレート
TIMEOUT = 1.3  # タイムアウト(s)
FRAME_INTERVAL = 200
SIO1_4 = 0x01
SIO5_8 = 0x02


# サーボモーターのIDと位置を設定する関数
def set_servo_position(rcb4, servo_id, position, frame=200):
    if not rcb4.setSingleServo(servo_id, SIO1_4, position, frame):
        print(f"Failed to set position for servo ID {servo_id}")


def main():
    rcb4 = Rcb4BaseLib()  # rcb4をインスタンス(定義)
    device_name = (
        DEVICE_NAME_WIN if platform.system() == "Windows" else DEVICE_NAME_LINUX
    )

    # rcb4.openはcheckAcknowledgeの結果を返す
    if not rcb4.open(device_name, BUNDRATE, TIMEOUT):
        print("checkAcknowledge error")
        return

    # サーボモーターID 1 に位置 5000 を設定
    set_servo_position(rcb4, 1, 10000)
    time.sleep(2)  # 1秒間待機
    set_servo_position(rcb4, 1, 7500)

    rcb4.close()


if __name__ == "__main__":
    main()
