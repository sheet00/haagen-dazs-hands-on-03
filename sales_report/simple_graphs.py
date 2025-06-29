import matplotlib.pyplot as plt
import matplotlib_fontja
import csv
from collections import defaultdict
import numpy as np
from pathlib import Path

# 日本語フォント設定
matplotlib_fontja.japanize()

# 出力ディレクトリの作成
output_dir = Path('graphs')
output_dir.mkdir(exist_ok=True)

print("📊 ハーゲンダッツ売上分析グラフ作成開始！")
print(f"グラフ保存先: {output_dir}")

# CSVファイルの読み込み
def load_sales_data():
    sales_data = []
    with open('sales_summary.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales_data.append({
                '年月': row['年月'],
                '商品名': row['商品名'],
                '店舗名': row['店舗名'],
                '区': row['区'],
                '合計売上金額': int(row['合計売上金額']),
                '合計販売数量': int(row['合計販売数量'])
            })
    return sales_data

def load_target_data():
    target_data = []
    with open('sales_target.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            target_data.append({
                '期間': row['期間'],
                '商品名': row['商品名'],
                '売上目標': int(row['売上目標']),
                '販売数量目標': int(row['販売数量目標'])
            })
    return target_data

# データ読み込み
sales_data = load_sales_data()
target_data = load_target_data()

# 1. 月別売上比較グラフ
def create_monthly_sales_comparison():
    monthly_sales = defaultdict(int)
    for record in sales_data:
        monthly_sales[record['年月']] += record['合計売上金額']
    
    months = list(monthly_sales.keys())
    values = list(monthly_sales.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(months, values, color=['#FF6B9D', '#4ECDC4'], alpha=0.8)
    
    # 値をバーの上に表示
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                f'¥{value:,}', ha='center', va='bottom', fontweight='bold')
    
    plt.title('📈 月別売上比較（2024年5月 vs 6月）', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('月', fontsize=12)
    plt.ylabel('売上金額 (円)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '1_monthly_sales_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 月別売上比較グラフ完成！")

# 2. 商品別売上実績vs目標達成率（6月のみ）
def create_product_performance():
    # 6月の売上実績
    june_sales = defaultdict(int)
    for record in sales_data:
        if record['年月'] == '2024-06':
            june_sales[record['商品名']] += record['合計売上金額']
    
    # 6月の目標
    june_targets = {}
    for record in target_data:
        if record['期間'] == '2024-06':
            june_targets[record['商品名']] = record['売上目標']
    
    # 商品名を短縮
    product_mapping = {
        'ハーゲンダッツ バニラ': 'バニラ',
        'ハーゲンダッツ ストロベリー': 'ストロベリー', 
        'ハーゲンダッツ チョコレート': 'チョコレート',
        'ハーゲンダッツ 抹茶': '抹茶',
        'ハーゲンダッツ クッキー&クリーム': 'クッキー&クリーム'
    }
    
    products = []
    actual_values = []
    target_values = []
    achievement_rates = []
    
    for full_name, short_name in product_mapping.items():
        if full_name in june_sales:
            products.append(short_name)
            actual = june_sales[full_name]
            target = june_targets[full_name]
            actual_values.append(actual)
            target_values.append(target)
            achievement_rates.append((actual / target) * 100)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 実績vs目標
    x = np.arange(len(products))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, actual_values, width, 
                    label='実績', color='#FF6B9D', alpha=0.8)
    bars2 = ax1.bar(x + width/2, target_values, width, 
                    label='目標', color='#4ECDC4', alpha=0.8)
    
    # 値をバーの上に表示
    for bars, values in [(bars1, actual_values), (bars2, target_values)]:
        for bar, value in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                    f'¥{int(value):,}', ha='center', va='bottom', fontsize=9)
    
    ax1.set_title('🎯 商品別売上実績 vs 目標（6月）', fontweight='bold')
    ax1.set_xlabel('商品名')
    ax1.set_ylabel('売上金額 (円)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(products, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 達成率
    colors = ['#FF4757' if rate < 30 else '#FFA502' if rate < 50 else '#2ED573' 
              for rate in achievement_rates]
    bars3 = ax2.bar(products, achievement_rates, color=colors, alpha=0.8)
    
    for bar, rate in zip(bars3, achievement_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('📊 目標達成率（6月）', fontweight='bold')
    ax2.set_xlabel('商品名')
    ax2.set_ylabel('達成率 (%)')
    ax2.set_xticklabels(products, rotation=45, ha='right')
    ax2.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='目標ライン')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '2_product_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 商品別パフォーマンスグラフ完成！")

# 3. エリア別売上分析（6月）
def create_area_analysis():
    # 6月のエリア別売上
    june_area_sales = defaultdict(int)
    for record in sales_data:
        if record['年月'] == '2024-06':
            june_area_sales[record['区']] += record['合計売上金額']
    
    areas = list(june_area_sales.keys())
    values = list(june_area_sales.values())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 棒グラフ
    colors = ['#FF6B9D', '#4ECDC4', '#FFD93D', '#6BCF7F', '#A8E6CF']
    bars = ax1.bar(areas, values, color=colors, alpha=0.8)
    
    for bar, value in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                f'¥{value:,}', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('🗺️ エリア別売上実績（6月）', fontweight='bold')
    ax1.set_xlabel('エリア')
    ax1.set_ylabel('売上金額 (円)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 円グラフ
    wedges, texts, autotexts = ax2.pie(values, labels=areas, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('🥧 エリア別売上構成比（6月）', fontweight='bold')
    
    # パーセンテージのフォントサイズ調整
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    plt.tight_layout()
    plt.savefig(output_dir / '3_area_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ エリア別売上分析グラフ完成！")

# 4. 商品別販売数量vs平均単価（6月）
def create_quantity_price_analysis():
    # 6月の商品別データ
    june_product_data = defaultdict(lambda: {'sales': 0, 'quantity': 0})
    
    for record in sales_data:
        if record['年月'] == '2024-06':
            product = record['商品名']
            june_product_data[product]['sales'] += record['合計売上金額']
            june_product_data[product]['quantity'] += record['合計販売数量']
    
    # 商品名を短縮
    product_mapping = {
        'ハーゲンダッツ バニラ': 'バニラ',
        'ハーゲンダッツ ストロベリー': 'ストロベリー', 
        'ハーゲンダッツ チョコレート': 'チョコレート',
        'ハーゲンダッツ 抹茶': '抹茶',
        'ハーゲンダッツ クッキー&クリーム': 'クッキー&クリーム'
    }
    
    products = []
    quantities = []
    avg_prices = []
    
    for full_name, short_name in product_mapping.items():
        if full_name in june_product_data:
            data = june_product_data[full_name]
            products.append(short_name)
            quantities.append(data['quantity'])
            avg_prices.append(data['sales'] / data['quantity'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 販売数量
    colors = ['#FF6B9D', '#4ECDC4', '#FFD93D', '#6BCF7F', '#A8E6CF']
    bars1 = ax1.bar(products, quantities, color=colors, alpha=0.8)
    
    for bar, value in zip(bars1, quantities):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{int(value)}個', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('📦 商品別販売数量（6月）', fontweight='bold')
    ax1.set_xlabel('商品名')
    ax1.set_ylabel('販売数量 (個)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 平均単価
    bars2 = ax2.bar(products, avg_prices, color=colors, alpha=0.8)
    
    for bar, value in zip(bars2, avg_prices):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'¥{value:.0f}', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('💰 商品別平均単価（6月）', fontweight='bold')
    ax2.set_xlabel('商品名')
    ax2.set_ylabel('平均単価 (円)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '4_quantity_price_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 販売数量・平均単価分析グラフ完成！")

# 全てのグラフを作成
if __name__ == "__main__":
    create_monthly_sales_comparison()
    create_product_performance()
    create_area_analysis()
    create_quantity_price_analysis()
    
    print("\n🎉 全てのグラフ作成完了！")
    print(f"📁 保存場所: {output_dir.absolute()}")
    print("\n作成されたグラフ:")
    print("1. 月別売上比較（5月 vs 6月）")
    print("2. 商品別パフォーマンス（実績 vs 目標 & 達成率）")
    print("3. エリア別売上分析（棒グラフ & 円グラフ）")
    print("4. 商品別販売数量・平均単価分析")