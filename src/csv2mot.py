import csv

filename = "../data/test.csv"

JOINT_NUM = 22  # 関節数
frame_count = 0  # キーフレーム数
data_body = []  # データ本体

with open(filename, encoding="utf8", newline="") as f:
    csvreader = csv.reader(f, delimiter=" ")
    pos2rot = lambda x: int((x - 7500) * 180 / 5300)
    for row in csvreader:
        frame_count += 1
        row = list(map(int, row))  # 文字列を数値に変換
        data_body.append([row[0], *map(pos2rot, row[1:])])  # 先頭は秒数なので除外

output = [[JOINT_NUM, frame_count], *data_body]

# CSVファイルのパス
csv_file_path = "../data/output.mot"

with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(output)

print(f"CSVファイルが作成されました: {csv_file_path}")
