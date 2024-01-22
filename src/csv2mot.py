# CSVを読み込み

import csv

filename = '../data/test.csv'

# 関節数を定義
JOINT_NUM = 22
FrameCount = 0
data = []

with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f, delimiter=' ')
    for row in csvreader:
        FrameCount += 1
        row = list(map(int,row))
        pos2rot = lambda x: (x - 7500) * (180 / 5300)
        data.append([row[0], *map(pos2rot,row[1:])])

# ファイル出力
output = [
    [JOINT_NUM, FrameCount],
    *data
]


# CSVファイルのパス
csv_file_path = '../data/output.csv'

# CSVファイルを書き込みモードで開く
with open(csv_file_path, 'w', newline='') as csv_file:
    # CSVライターを作成
    csv_writer = csv.writer(csv_file)

    # データをCSVファイルに書き込む
    csv_writer.writerows(output)

print(f'CSVファイルが作成されました: {csv_file_path}')
