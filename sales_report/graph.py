
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_fontja
import seaborn as sns

# Load the data
sales_summary = pd.read_csv('sales_report/sales_summary.csv')
sales_target = pd.read_csv('sales_report/sales_target.csv')

# データのクリーニング
sales_summary.columns = sales_summary.columns.str.strip()
sales_target.columns = sales_target.columns.str.strip()

# 2024年6月のデータに絞り込み
sales_june = sales_summary[sales_summary['年月'] == '2024-06']
target_june = sales_target[sales_target['期間'] == '2024-06']

# 商品別売上実績
product_sales = sales_june.groupby('商品名')['合計売上金額'].sum().reset_index()

# グラフ作成
plt.figure(figsize=(12, 6.75))
sns.set_theme()
matplotlib_fontja.japanize()
sns.barplot(x='商品名', y='合計売上金額', data=product_sales)
plt.title('2024年6月 商品別売上実績')
plt.xlabel('商品名')
plt.ylabel('売上金額（円）')
plt.tight_layout()
plt.savefig('image/product_sales.png')
plt.close()

# 区エリア別売上実績
area_sales = sales_june.groupby('区')['合計売上金額'].sum().reset_index()

plt.figure(figsize=(12, 6.75))
sns.set_theme()
matplotlib_fontja.japanize()
sns.barplot(x='区', y='合計売上金額', data=area_sales)
plt.title('2024年6月 区エリア別売上実績')
plt.xlabel('区')
plt.ylabel('売上金額（円）')
plt.tight_layout()
plt.savefig('image/area_sales.png')
plt.close()

# 商品別売上目標達成率
merged_data = pd.merge(product_sales, target_june, on='商品名')
merged_data['達成率'] = (merged_data['合計売上金額'] / merged_data['売上目標']) * 100

plt.figure(figsize=(12, 6.75))
sns.set_theme()
matplotlib_fontja.japanize()
ax = sns.barplot(x='商品名', y='達成率', data=merged_data)
plt.title('2024年6月 商品別売上目標達成率')
plt.xlabel('商品名')
plt.ylabel('達成率（%）')
# y軸の範囲を0から120までに設定
ax.set_ylim(0, 120)

# 達成率の数値をグラフ上に表示
for index, row in merged_data.iterrows():
    ax.text(index, row['達成率'] + 1, f"{row['達成率']:.1f}%", color='black', ha="center")

plt.axhline(100, color='r', linestyle='--')
plt.tight_layout()
plt.savefig('image/product_kpi.png')
plt.close()

# 前月比較 - 商品別
sales_may = sales_summary[sales_summary['年月'] == '2024-05']
product_sales_may = sales_may.groupby('商品名')['合計売上金額'].sum().reset_index()
product_sales_may = product_sales_may.rename(columns={'合計売上金額': '5月売上'})
product_sales_june = sales_june.groupby('商品名')['合計売上金額'].sum().reset_index()
product_sales_june = product_sales_june.rename(columns={'合計売上金額': '6月売上'})

product_comparison = pd.merge(product_sales_may, product_sales_june, on='商品名')
product_comparison_melt = product_comparison.melt(id_vars='商品名', value_vars=['5月売上', '6月売上'], var_name='月', value_name='売上')

plt.figure(figsize=(12, 6.75))
sns.set_theme()
matplotlib_fontja.japanize()
sns.barplot(x='商品名', y='売上', hue='月', data=product_comparison_melt)
plt.title('商品別 前月比較')
plt.xlabel('商品名')
plt.ylabel('売上金額（円）')
plt.tight_layout()
plt.savefig('image/product_comparison.png')
plt.close()

# 前月比較 - 区エリア別
area_sales_may = sales_may.groupby('区')['合計売上金額'].sum().reset_index()
area_sales_may = area_sales_may.rename(columns={'合計売上金額': '5月売上'})
area_sales_june = sales_june.groupby('区')['合計売上金額'].sum().reset_index()
area_sales_june = area_sales_june.rename(columns={'合計売上金額': '6月売上'})

area_comparison = pd.merge(area_sales_may, area_sales_june, on='区')
area_comparison_melt = area_comparison.melt(id_vars='区', value_vars=['5月売上', '6月売上'], var_name='月', value_name='売上')

plt.figure(figsize=(12, 6.75))
sns.set_theme()
matplotlib_fontja.japanize()
sns.barplot(x='区', y='売上', hue='月', data=area_comparison_melt)
plt.title('区エリア別 前月比較')
plt.xlabel('区')
plt.ylabel('売上金額（円）')
plt.tight_layout()
plt.savefig('image/area_comparison.png')
plt.close()
