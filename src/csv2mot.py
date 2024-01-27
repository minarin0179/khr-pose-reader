import pandas as pd
import numpy as np
from tkinter import Tk, filedialog
import khr_structure

JOINT_NUM = 22  # 関節数


indecies = np.array(
    [
        khr_structure.CSV_STRUCTURE.index(element)
        for element in khr_structure.MOT_STRUCTURE
    ]
)  # csvからmotへの変換用のインデックス

# ファイルの読み込みダイアログを表示
Tk().withdraw()  # Tkinterのルートウィンドウを表示しない
input_file_path = filedialog.askopenfilename(
    title="Select CSV file", filetypes=[("CSV files", "*.csv")]
)

if not input_file_path:
    print("ファイルが選択されませんでした。プログラムを終了します。")
    exit()

data = pd.read_csv(input_file_path, header=None, delimiter=" ").values
frame_count = len(data)  # キーフレーム数を取得
data[:, 1:] = (data[:, 1:] - 7500) * 180 / 5300  # 位置データを回転角度に変換
data[:, 1:] = data[:, 1:][:, indecies]  # csvからmotの構造に変換

# ファイルの書き込み用テキストを作成
output_text = f"{JOINT_NUM} {frame_count}\n"
output_text += "\n".join([", ".join(map(str, row)) for row in data])

# ファイルの書き込みダイアログを表示
output_file_path = filedialog.asksaveasfilename(
    title="Save MOT file", filetypes=[("MOT files", "*.mot")], defaultextension=".mot"
)

if not output_file_path:
    print("保存先が選択されませんでした。プログラムを終了します。")
    exit()

# ファイルに書き込む
with open(output_file_path, "w", newline="") as mot_file:
    mot_file.write(output_text)

print(f"motファイルが作成されました: {output_file_path}")
