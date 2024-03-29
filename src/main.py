# coding: UTF-8
import csv
import platform
import tkinter as tk
from tkinter import filedialog
from Rcb4BaseLib import Rcb4BaseLib  # Rcb4BaseLib.pyの中のRcb4BaseLibが使えるように設定

DEVICE_NAME_WIN = "COM3"
DEVICE_NAME_LINUX = "/dev/ttyUSB0"
BUNDRATE = [115200, 625000, 1250000]  # ボーレート
TIMEOUT = 1.3  # タイムアウト(s)
FRAME_INTERVAL = 500
SIO1_4 = 0x01
SIO5_8 = 0x02


def main():
    device_name = (
        DEVICE_NAME_WIN if platform.system() == "Windows" else DEVICE_NAME_LINUX
    )

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

    servoDatas = [
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

    posDatas = []
    frame_count = 0

    print("press enter to get frame")
    print("type 'hold' to set servo motors to hold")
    print("type 'free' to set servo motors to free")
    print("type 'end' to end recording")

    while True:
        command = input()
        if command == "":
            positions = [0] * (len(servoDatas))
            for index, servodata in enumerate(servoDatas):
                (flag, posData) = rcb4.getSinglePos(servodata.Id, servodata.Sio)
                if not flag:
                    print("failed to get position")
                    break
                positions[index] = posData
            else:
                print(f"frame{frame_count} is successfully got")
                print(*positions)
                posDatas.append([FRAME_INTERVAL] + positions)
                frame_count += 1

        elif command == "hold":
            rcb4.setHoldPos(servoDatas)
            print("set servo motors to hold")

        elif command == "free":
            rcb4.setFreePos(servoDatas)
            print("set servo motors to free")

        elif command == "end":
            rcb4.setHoldPos(servoDatas)
            print("recording is ended")
            break

        else:
            print("invalid command")

    root = tk.Tk()
    root.withdraw()
    root.update()
    output_file_path = filedialog.asksaveasfilename(
        title="Save CSV file",
        filetypes=[("CSV files", "*.csv")],
        defaultextension=".csv",
        initialfile="motion.csv",
    )
    root.destroy()

    if not output_file_path:
        print("保存先が選択されませんでした。プログラムを終了します。")
        exit()

    with open(output_file_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter=" ")
        writer.writerows(posDatas)

    print(f"{output_file_path} is successfully written")

    rcb4.close()


if __name__ == "__main__":
    main()
