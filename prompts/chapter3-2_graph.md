# 指示

あなたはデータ分析担当者です。
2024 年 6 月度売上レポートを読み込め。
上記内容をもとに、レポートで利用するグラフを複数作って保存して

## 作業フォルダ

`sales_report`

## Todo

- `2024年6月度売上レポート.md`の読み込み
- `sales_summary.csv`の読み込み
- `sales_target.csv`の読み込み

## 利用ライブラリ

Python matplotlib

## 利用フォント

インストール済
import matplotlib.pyplot as plt
import matplotlib_fontja

seaborn 利用時以下のように、フォント上書き後に matplotlib_fontja.japanize()を実行してください。

sns.set_theme()
matplotlib_fontja.japanize()

## 画像フォルダ

`sales_report\image`

## 画像サイズ

marp スライドで利用想定
複数グラフの場合、縦にグラフ設置しないこと
size: 16:9
