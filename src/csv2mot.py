import csv
from tkinter import Tk, filedialog
import khr_structure

JOINT_NUM = 22  # 関節数
frame_count = 0  # キーフレーム数
data_body = []  # データ本体

indecies = [
    khr_structure.CSV_STRUCTURE.index(element)
    for element in khr_structure.MOT_STRUCTURE
]  # csvからmotへの変換用のインデックス


def pos2rot(pos: int) -> int:
    """サーボモーターの位置を角度に変換する

    Args:
        pos (int): サーボモーターの位置

    Returns:
        int: 角度
    """
    return round((pos - 7500) * 180 / 5300)


def csv_to_mot(data: list[str]) -> list[int]:
    """csvのデータをmotのデータに変換する

    Args:
        data (list[str]): csvのデータ

    Returns:
        list[int]: motのデータ
    """
    data = list(map(int, data))  # 文字列を数値に変換
    time, positions = data[0], data[1:]
    positions = [positions[i] for i in indecies]
    rotations = map(pos2rot, positions)
    return [time, *rotations]


# ファイルの読み込みダイアログを表示
Tk().withdraw()  # Tkinterのルートウィンドウを表示しない
input_file_path = filedialog.askopenfilename(
    title="Select CSV file", filetypes=[("CSV files", "*.csv")]
)

if not input_file_path:
    print("ファイルが選択されませんでした。プログラムを終了します。")
    exit()

with open(input_file_path, encoding="utf8", newline="") as f:
    csvreader = csv.reader(f, delimiter=" ")
    for row in csvreader:
        frame_count += 1
        data_body.append(csv_to_mot(row))

# ファイルの書き込みダイアログを表示
output_file_path = filedialog.asksaveasfilename(
    title="Save MOT file", filetypes=[("MOT files", "*.mot")], defaultextension=".mot"
)

if not output_file_path:
    print("保存先が選択されませんでした。プログラムを終了します。")
    exit()

output_text = f"{JOINT_NUM} {frame_count}\n"
for row in data_body:
    output_text += f"{', '.join(map(str, row))} \n"

with open(output_file_path, "w", newline="") as mot_file:
    mot_file.write(output_text)

print(f"motファイルが作成されました: {output_file_path}")
