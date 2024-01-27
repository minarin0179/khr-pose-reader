import pandas as pd
import numpy as np
from tkinter import Tk, filedialog
import khr_structure


JOINT_NUM = 22  # 関節数


def read_csv_file() -> np.ndarray:
    Tk().withdraw()
    input_file_path = filedialog.askopenfilename(
        title="Select CSV file", filetypes=[("CSV files", "*.csv")]
    )

    if not input_file_path:
        print("ファイルが選択されませんでした。プログラムを終了します。")
        exit()

    return pd.read_csv(input_file_path, header=None, delimiter=" ").values


def convert_csv_to_mot(data: np.ndarray) -> np.ndarray:
    indecies = [
        khr_structure.CSV_STRUCTURE.index(element)
        for element in khr_structure.MOT_STRUCTURE
    ]  # csvからmotへの変換用のインデックス

    data[:, 1:] = (data[:, 1:] - 7500) * 180 / 5300
    return data[:, 1:][:, indecies]


def create_output_text(data):
    return f"{JOINT_NUM} {len(data)}\n" + "\n".join(
        [", ".join(map(str, row)) for row in data]
    )


def write_mot_file(output_text):
    Tk().withdraw()
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


def main():
    input_data = read_csv_file()
    converted_data = convert_csv_to_mot(input_data)
    output_text = create_output_text(converted_data)
    write_mot_file(output_text)


if __name__ == "__main__":
    main()
