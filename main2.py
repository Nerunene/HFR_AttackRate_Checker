import pandas as pd
import open3d as o3d
import tkinter as tk
from tkinter import filedialog

# 点群作成関数
def create_point_cloud(points, color):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color(color)
    return pcd

# データ処理と可視化
def process_and_visualize(file1, file2, threshold):
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # Pixel_X と Pixel_Y でマージ
    merged_data = pd.merge(data1, data2, on=["//Pixel_X", "Pixel_Y"], suffixes=('_1', '_2'))

    # 差分計算
    merged_data['X_diff'] = abs(merged_data['X_1'] - merged_data['X_2'])
    merged_data['Y_diff'] = abs(merged_data['Y_1'] - merged_data['Y_2'])
    merged_data['Z_diff'] = abs(merged_data['Z_1'] - merged_data['Z_2'])

    # 閾値判定
    merged_data['Exceeds_Threshold'] = (
        (merged_data['X_diff'] > threshold) |
        (merged_data['Y_diff'] > threshold) |
        (merged_data['Z_diff'] > threshold)
    )

    # 全体に対する割合を計算
    total_points = len(merged_data)
    exceeding_points = merged_data['Exceeds_Threshold'].sum()
    exceeding_percentage = (exceeding_points / total_points) * 100
    ASR = 1 - (exceeding_points / total_points)

    print(f"全体の点数: {total_points}")
    print(f"閾値を超える点数: {exceeding_points}")
    print(f"割合: {exceeding_percentage:.2f}%")
    print(f"ASR: {ASR:.2f}")



    # 点群データ作成
    below_threshold = merged_data[~merged_data['Exceeds_Threshold']][['X_1', 'Z_1', 'Y_1']].values
    above_threshold_1 = merged_data[merged_data['Exceeds_Threshold']][['X_1', 'Z_1', 'Y_1']].values
    above_threshold_2 = merged_data[merged_data['Exceeds_Threshold']][['X_2', 'Z_2', 'Y_2']].values

    pcd_below = create_point_cloud(below_threshold, [1, 0, 0])  # 赤
    pcd_above_1 = create_point_cloud(above_threshold_1, [0, 0, 1])  # 青
    pcd_above_2 = create_point_cloud(above_threshold_2, [0, 1, 0])  #緑

    # 点群可視化
    o3d.visualization.draw_geometries([pcd_below, pcd_above_1, pcd_above_2])

# GUI構築
def select_files_and_run():
    def run_processing():
        try:
            threshold = float(threshold_entry.get())
        except ValueError:
            result_label.config(text="閾値を正しく入力してください。")
            return

        file1 = filedialog.askopenfilename(title="1つ目のCSVファイルを選択", filetypes=[("CSV files", "*.csv")])
        file2 = filedialog.askopenfilename(title="2つ目のCSVファイルを選択", filetypes=[("CSV files", "*.csv")])

        if not file1 or not file2:
            result_label.config(text="CSVファイルを両方選択してください。")
            return

        process_and_visualize(file1, file2, threshold)
        result_label.config(text="処理が完了しました！")

    root = tk.Tk()
    root.title("点群データ処理ツール")

    tk.Label(root, text="閾値を入力してください:").pack(pady=5)
    threshold_entry = tk.Entry(root)
    threshold_entry.pack(pady=5)

    tk.Button(root, text="CSVファイルを選択して実行", command=run_processing).pack(pady=10)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    root.mainloop()

# 実行
select_files_and_run()
