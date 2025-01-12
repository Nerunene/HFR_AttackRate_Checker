import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# データ処理と3Dプロット
def process_and_visualize(file1, file2, threshold):
    # CSVファイルを読み込み
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # Pixel_X と Pixel_Y をキーとしてデータをマージ
    merged_data = pd.merge(data1, data2, on=["//Pixel_X", "Pixel_Y"], suffixes=('_1', '_2'))

    # X, Y, Z の差を計算
    merged_data['X_diff'] = abs(merged_data['X_1'] - merged_data['X_2'])
    merged_data['Y_diff'] = abs(merged_data['Y_1'] - merged_data['Y_2'])
    merged_data['Z_diff'] = abs(merged_data['Z_1'] - merged_data['Z_2'])

    # 差が閾値を超える点を検出
    merged_data['Exceeds_Threshold'] = (
        (merged_data['X_diff'] > threshold) |
        (merged_data['Y_diff'] > threshold) |
        (merged_data['Z_diff'] > threshold)
    )

    # 全体に対する割合を計算
    total_points = len(merged_data)
    exceeding_points = merged_data['Exceeds_Threshold'].sum()
    exceeding_percentage = (exceeding_points / total_points) * 100

    print(f"全体の点数: {total_points}")
    print(f"閾値を超える点数: {exceeding_points}")
    print(f"割合: {exceeding_percentage:.2f}%")

    # 3Dプロットで可視化
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # 閾値以下の点
    below_threshold = merged_data[~merged_data['Exceeds_Threshold']]
    ax.scatter(
        below_threshold['X_1'], below_threshold['Y_1'], below_threshold['Z_1'],
        c='blue', s=10, label='Below Threshold'
    )

    # 閾値を超える点
    above_threshold = merged_data[merged_data['Exceeds_Threshold']]
    ax.scatter(
        above_threshold['X_1'], above_threshold['Y_1'], above_threshold['Z_1'],
        c='red', s=10, label='Above Threshold'
    )

    # グラフ設定
    ax.set_title("3D Point Cloud - Threshold Visualization")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

# GUIを構築
def select_files_and_run():
    def run_processing():
        # 閾値を取得
        try:
            threshold = float(threshold_entry.get())
        except ValueError:
            result_label.config(text="閾値を正しく入力してください。")
            return

        # CSVファイルを選択
        file1 = filedialog.askopenfilename(title="1つ目のCSVファイルを選択", filetypes=[("CSV files", "*.csv")])
        file2 = filedialog.askopenfilename(title="2つ目のCSVファイルを選択", filetypes=[("CSV files", "*.csv")])

        if not file1 or not file2:
            result_label.config(text="CSVファイルを両方選択してください。")
            return

        # データ処理とプロット
        process_and_visualize(file1, file2, threshold)
        result_label.config(text="処理が完了しました！")

    # メインウィンドウ
    root = tk.Tk()
    root.title("点群データ処理ツール")

    # 閾値入力
    tk.Label(root, text="閾値を入力してください:").pack(pady=5)
    threshold_entry = tk.Entry(root)
    threshold_entry.pack(pady=5)

    # 実行ボタン
    tk.Button(root, text="CSVファイルを選択して実行", command=run_processing).pack(pady=10)

    # 結果ラベル
    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    root.mainloop()

# GUIを起動
select_files_and_run()
