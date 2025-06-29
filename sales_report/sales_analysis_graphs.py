import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_fontja
import seaborn as sns
import numpy as np
from pathlib import Path

# 日本語フォント設定
sns.set_theme()
matplotlib_fontja.japanize()

# データ読み込み
sales_data = pd.read_csv('sales_summary.csv')
target_data = pd.read_csv('sales_target.csv')

# データ型の変換
sales_data['年月'] = pd.to_datetime(sales_data['年月'])
target_data['期間'] = pd.to_datetime(target_data['期間'])

# 出力ディレクトリの作成
output_dir = Path('graphs')
output_dir.mkdir(exist_ok=True)

print("📊 ハーゲンダッツ売上分析グラフ作成開始！")
print(f"グラフ保存先: {output_dir}")

# 1. 月別売上比較グラフ
def create_monthly_sales_comparison():
    monthly_sales = sales_data.groupby('年月')['合計売上金額'].sum()
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_sales.index.strftime('%Y-%m'), monthly_sales.values, 
                   color=['#FF6B9D', '#4ECDC4'], alpha=0.8)
    
    # 値をバーの上に表示
    for bar, value in zip(bars, monthly_sales.values):
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

# 2. 商品別売上実績vs目標達成率
def create_product_performance():
    # 6月のデータのみ
    june_sales = sales_data[sales_data['年月'] == '2024-06-01'].groupby('商品名')['合計売上金額'].sum()
    june_targets = target_data[target_data['期間'] == '2024-06-01'].set_index('商品名')['売上目標']
    
    # 商品名を短縮
    product_names = ['バニラ', 'ストロベリー', 'チョコレート', '抹茶', 'クッキー&クリーム']
    performance_data = pd.DataFrame({
        '実績': june_sales.values,
        '目標': june_targets.values,
        '達成率': (june_sales.values / june_targets.values * 100)
    }, index=product_names)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 実績vs目標
    x = np.arange(len(product_names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, performance_data['実績'], width, 
                    label='実績', color='#FF6B9D', alpha=0.8)
    bars2 = ax1.bar(x + width/2, performance_data['目標'], width, 
                    label='目標', color='#4ECDC4', alpha=0.8)
    
    # 値をバーの上に表示
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + 500,
                    f'¥{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    ax1.set_title('🎯 商品別売上実績 vs 目標（6月）', fontweight='bold')
    ax1.set_xlabel('商品名')
    ax1.set_ylabel('売上金額 (円)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(product_names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 達成率
    colors = ['#FF4757' if rate < 30 else '#FFA502' if rate < 50 else '#2ED573' 
              for rate in performance_data['達成率']]
    bars3 = ax2.bar(product_names, performance_data['達成率'], color=colors, alpha=0.8)
    
    for bar, rate in zip(bars3, performance_data['達成率']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('📊 目標達成率（6月）', fontweight='bold')
    ax2.set_xlabel('商品名')
    ax2.set_ylabel('達成率 (%)')
    ax2.set_xticklabels(product_names, rotation=45, ha='right')
    ax2.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='目標ライン')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '2_product_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 商品別パフォーマンスグラフ完成！")

# 3. エリア別売上分析
def create_area_analysis():
    # 6月のエリア別売上
    june_area_sales = sales_data[sales_data['年月'] == '2024-06-01'].groupby('区')['合計売上金額'].sum()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 棒グラフ
    colors = plt.cm.Set3(np.arange(len(june_area_sales)))
    bars = ax1.bar(june_area_sales.index, june_area_sales.values, color=colors, alpha=0.8)
    
    for bar, value in zip(bars, june_area_sales.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                f'¥{value:,}', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('🗺️ エリア別売上実績（6月）', fontweight='bold')
    ax1.set_xlabel('エリア')
    ax1.set_ylabel('売上金額 (円)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 円グラフ
    wedges, texts, autotexts = ax2.pie(june_area_sales.values, labels=june_area_sales.index, 
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

# 4. 商品別販売数量vs平均単価
def create_quantity_price_analysis():
    # 6月のデータ
    june_product_data = sales_data[sales_data['年月'] == '2024-06-01'].groupby('商品名').agg({
        '合計販売数量': 'sum',
        '合計売上金額': 'sum'
    }).reset_index()
    
    june_product_data['平均単価'] = june_product_data['合計売上金額'] / june_product_data['合計販売数量']
    
    # 商品名を短縮
    product_mapping = {
        'ハーゲンダッツ バニラ': 'バニラ',
        'ハーゲンダッツ ストロベリー': 'ストロベリー', 
        'ハーゲンダッツ チョコレート': 'チョコレート',
        'ハーゲンダッツ 抹茶': '抹茶',
        'ハーゲンダッツ クッキー&クリーム': 'クッキー&クリーム'
    }
    june_product_data['商品名_短縮'] = june_product_data['商品名'].map(product_mapping)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 販売数量
    colors = ['#FF6B9D', '#4ECDC4', '#FFD93D', '#6BCF7F', '#A8E6CF']
    bars1 = ax1.bar(june_product_data['商品名_短縮'], june_product_data['合計販売数量'], 
                    color=colors, alpha=0.8)
    
    for bar, value in zip(bars1, june_product_data['合計販売数量']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{int(value)}個', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('📦 商品別販売数量（6月）', fontweight='bold')
    ax1.set_xlabel('商品名')
    ax1.set_ylabel('販売数量 (個)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 平均単価
    bars2 = ax2.bar(june_product_data['商品名_短縮'], june_product_data['平均単価'], 
                    color=colors, alpha=0.8)
    
    for bar, value in zip(bars2, june_product_data['平均単価']):
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

# 5. 月次トレンド分析（5月 vs 6月）
def create_trend_analysis():
    # 商品別月次データ
    monthly_product_sales = sales_data.groupby(['年月', '商品名'])['合計売上金額'].sum().unstack(fill_value=0)
    
    # 商品名を短縮
    column_mapping = {
        'ハーゲンダッツ バニラ': 'バニラ',
        'ハーゲンダッツ ストロベリー': 'ストロベリー', 
        'ハーゲンダッツ チョコレート': 'チョコレート',
        'ハーゲンダッツ 抹茶': '抹茶',
        'ハーゲンダッツ クッキー&クリーム': 'クッキー&クリーム'
    }
    monthly_product_sales.columns = [column_mapping.get(col, col) for col in monthly_product_sales.columns]
    
    plt.figure(figsize=(12, 8))
    
    colors = ['#FF6B9D', '#4ECDC4', '#FFD93D', '#6BCF7F', '#A8E6CF']
    x = ['2024-05', '2024-06']
    
    for i, product in enumerate(monthly_product_sales.columns):
        values = monthly_product_sales[product].values
        plt.plot(x, values, marker='o', linewidth=3, markersize=8, 
                label=product, color=colors[i])
        
        # 値をプロット上に表示
        for j, value in enumerate(values):
            plt.text(j, value + 500, f'¥{value:,}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=9)
    
    plt.title('📈 商品別月次売上トレンド（5月→6月）', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('月', fontsize=12)
    plt.ylabel('売上金額 (円)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '5_trend_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 月次トレンド分析グラフ完成！")

# 6. 店舗別パフォーマンス（6月）
def create_store_performance():
    # 6月の店舗別データ
    june_store_data = sales_data[sales_data['年月'] == '2024-06-01'].groupby(['店舗名', '区']).agg({
        '合計売上金額': 'sum',
        '合計販売数量': 'sum'
    }).reset_index()
    
    june_store_data = june_store_data.sort_values('合計売上金額', ascending=True)
    
    plt.figure(figsize=(12, 8))
    
    # エリア別に色分け
    area_colors = {
        '渋谷区': '#FF6B9D',
        '港区': '#4ECDC4', 
        '新宿区': '#FFD93D',
        '豊島区': '#6BCF7F',
        '中央区': '#A8E6CF'
    }
    
    colors = [area_colors[area] for area in june_store_data['区']]
    
    bars = plt.barh(june_store_data['店舗名'], june_store_data['合計売上金額'], 
                    color=colors, alpha=0.8)
    
    # 値をバーの右側に表示
    for bar, value in zip(bars, june_store_data['合計売上金額']):
        plt.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
                f'¥{value:,}', va='center', fontweight='bold', fontsize=9)
    
    plt.title('🏪 店舗別売上実績（6月）', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('売上金額 (円)', fontsize=12)
    plt.ylabel('店舗名', fontsize=12)
    
    # 凡例（エリア別）
    handles = [plt.Rectangle((0,0),1,1, color=color, alpha=0.8) for color in area_colors.values()]
    plt.legend(handles, area_colors.keys(), title='エリア', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '6_store_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 店舗別パフォーマンスグラフ完成！")

# 全てのグラフを作成
if __name__ == "__main__":
    create_monthly_sales_comparison()
    create_product_performance()
    create_area_analysis()
    create_quantity_price_analysis()
    create_trend_analysis()
    create_store_performance()
    
    print("\n🎉 全てのグラフ作成完了！")
    print(f"📁 保存場所: {output_dir.absolute()}")
    print("\n作成されたグラフ:")
    print("1. 月別売上比較（5月 vs 6月）")
    print("2. 商品別パフォーマンス（実績 vs 目標 & 達成率）")
    print("3. エリア別売上分析（棒グラフ & 円グラフ）")
    print("4. 商品別販売数量・平均単価分析")
    print("5. 商品別月次売上トレンド")
    print("6. 店舗別パフォーマンス")