import pandas as pd
import numpy as np
from tkinter import Tk, filedialog
import khr_structure


JOINT_NUM = 22  # 関節数


def convert_csv_to_mot(data: np.ndarray) -> np.ndarray:
    indecies = [
        khr_structure.CSV_STRUCTURE.index(element)
        for element in khr_structure.MOT_STRUCTURE
    ]  # csvからmotへの変換用のインデックス

    data[:, 1:] = (data[:, 1:] - 7500) * 180 / 5300
    return data[:, 1:][:, indecies]


def main():
    Tk().withdraw()
    input_file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")],
        defaultextension=".csv",
    )

    if not input_file_path:
        print("ファイルが選択されませんでした。プログラムを終了します。")
        exit()

    csv_data = pd.read_csv(input_file_path, header=None, delimiter=" ").values
    mot_data = convert_csv_to_mot(csv_data)
    output_text = f"{JOINT_NUM} {len(mot_data)}\n" + "\n".join(
        [", ".join(map(str, row)) for row in mot_data]
    )

    output_file_path = filedialog.asksaveasfilename(
        title="Save MOT file",
        filetypes=[("MOT files", "*.mot")],
        defaultextension=".mot",
    )

    if not output_file_path:
        print("保存先が選択されませんでした。プログラムを終了します。")
        exit()

    with open(output_file_path, "w", newline="") as mot_file:
        mot_file.write(output_text)

    print(f"motファイルが作成されました: {output_file_path}")


if __name__ == "__main__":
    main()
