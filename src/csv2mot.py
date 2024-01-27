import csv
import khr_structure

filename = "../data/test.csv"

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


with open(filename, encoding="utf8", newline="") as f:
    csvreader = csv.reader(f, delimiter=" ")
    for row in csvreader:
        frame_count += 1
        data_body.append(csv_to_mot(row))


# CSVファイルのパス
csv_file_path = "../data/output.mot"

output_text = f"{JOINT_NUM} {frame_count}\n"
for row in data_body:
    output_text += f"{", ".join(map(str, row))} \n"

with open(csv_file_path, "w", newline="") as mot_file:
    mot_file.write(output_text)

print(f"motファイルが作成されました: {csv_file_path}")
