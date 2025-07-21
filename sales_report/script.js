// ハーゲンダッツ売上レポート JavaScript

// グローバル変数
let salesData = [];
let targetData = [];

// ハーゲンダッツブランドカラー
const colors = {
    strawberry: '#FFB6C1',
    chocolate: '#8B4513', 
    vanilla: '#F5F5DC',
    gold: '#DAA520',
    cream: '#FFF8DC',
    brown: '#8B4513'
};

// データ読み込み
async function loadData() {
    try {
        console.log('データ読み込み開始...');
        
        // CSV読み込み
        const [salesResponse, targetResponse] = await Promise.all([
            fetch('sales_summary.csv'),
            fetch('sales_target.csv')
        ]);

        if (!salesResponse.ok || !targetResponse.ok) {
            throw new Error('CSVファイルの読み込みに失敗しました');
        }

        const salesCsv = await salesResponse.text();
        const targetCsv = await targetResponse.text();

        // CSV解析
        salesData = parseCSV(salesCsv);
        targetData = parseCSV(targetCsv);

        console.log('売上データ:', salesData);
        console.log('目標データ:', targetData);

        // データ処理と表示
        await displayData();
        
    } catch (error) {
        console.error('データ読み込みエラー:', error);
        displayError('データの読み込みに失敗しました。CSVファイルを確認してください。');
    }
}

// CSV解析関数
function parseCSV(csvText) {
    const lines = csvText.split('\n').filter(line => line.trim());
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    
    return lines.slice(1).map(line => {
        const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
        const row = {};
        
        headers.forEach((header, index) => {
            row[header] = values[index] || '';
        });
        
        return row;
    });
}

// エラー表示
function displayError(message) {
    document.body.innerHTML = `
        <div style="
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            background: linear-gradient(135deg, #FFF8DC 0%, #F5F5DC 100%);
            font-family: Arial, sans-serif;
        ">
            <div style="
                background: white; 
                padding: 2rem; 
                border-radius: 10px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
            ">
                <h2 style="color: #DAA520; margin-bottom: 1rem;">⚠️ エラー</h2>
                <p style="color: #666; line-height: 1.6;">${message}</p>
            </div>
        </div>
    `;
}

// データ表示メイン関数
async function displayData() {
    try {
        // KPI計算と表示
        displayKPIs();
        
        // グラフ描画
        await Promise.all([
            drawProductSalesChart(),
            drawProductPieChart(),
            drawProductProgress(),
            drawAreaSalesChart(),
            drawMonthlyTrendChart()
        ]);

        console.log('全てのグラフ描画完了');
        
    } catch (error) {
        console.error('データ表示エラー:', error);
    }
}

// KPI計算と表示
function displayKPIs() {
    // 6月度実績計算
    const june2024Data = salesData.filter(row => row['年月'] === '2024-06');
    const may2024Data = salesData.filter(row => row['年月'] === '2024-05');
    
    const juneTotalSales = june2024Data.reduce((sum, row) => sum + parseInt(row['合計売上金額'] || 0), 0);
    const mayTotalSales = may2024Data.reduce((sum, row) => sum + parseInt(row['合計売上金額'] || 0), 0);
    
    // 6月度目標計算
    const juneTargets = targetData.filter(row => row['期間'] === '2024-06');
    const juneTargetTotal = juneTargets.reduce((sum, row) => sum + parseInt(row['売上目標'] || 0), 0);
    
    // 計算
    const monthlyGrowth = mayTotalSales > 0 ? ((juneTotalSales - mayTotalSales) / mayTotalSales * 100) : 0;
    const targetAchievement = juneTargetTotal > 0 ? (juneTotalSales / juneTargetTotal * 100) : 0;

    // 表示
    document.getElementById('total-sales').textContent = juneTotalSales.toLocaleString();
    document.getElementById('monthly-growth').textContent = monthlyGrowth.toFixed(1);
    document.getElementById('target-achievement').textContent = targetAchievement.toFixed(1);

    // 前月比の色分け
    const growthElement = document.getElementById('monthly-growth');
    growthElement.style.color = monthlyGrowth >= 0 ? '#28A745' : '#DC3545';
    
    // 目標達成率の色分け
    const achievementElement = document.getElementById('target-achievement');
    achievementElement.style.color = targetAchievement >= 100 ? '#28A745' : 
                                     targetAchievement >= 80 ? '#FFC107' : '#DC3545';
}

// 商品別売上グラフ（棒グラフ）
async function drawProductSalesChart() {
    const ctx = document.getElementById('product-sales-chart').getContext('2d');
    
    // 6月度商品別データ集計
    const june2024Data = salesData.filter(row => row['年月'] === '2024-06');
    const productSales = {};
    
    june2024Data.forEach(row => {
        const product = row['商品名'];
        if (!productSales[product]) {
            productSales[product] = 0;
        }
        productSales[product] += parseInt(row['合計売上金額'] || 0);
    });

    const labels = Object.keys(productSales).map(name => name.replace('ハーゲンダッツ ', ''));
    const data = Object.values(productSales);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '売上金額 (円)',
                data: data,
                backgroundColor: [colors.strawberry, colors.chocolate, colors.vanilla],
                borderColor: [colors.strawberry, colors.chocolate, colors.vanilla],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString() + '円';
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}

// 商品別売上構成比グラフ（円グラフ）
async function drawProductPieChart() {
    const ctx = document.getElementById('product-pie-chart').getContext('2d');
    
    // 6月度商品別データ集計
    const june2024Data = salesData.filter(row => row['年月'] === '2024-06');
    const productSales = {};
    
    june2024Data.forEach(row => {
        const product = row['商品名'];
        if (!productSales[product]) {
            productSales[product] = 0;
        }
        productSales[product] += parseInt(row['合計売上金額'] || 0);
    });

    const labels = Object.keys(productSales).map(name => name.replace('ハーゲンダッツ ', ''));
    const data = Object.values(productSales);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [colors.strawberry, colors.chocolate, colors.vanilla],
                borderColor: '#FFFFFF',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}

// 商品別目標達成率プログレスバー
function drawProductProgress() {
    const june2024Data = salesData.filter(row => row['年月'] === '2024-06');
    const juneTargets = targetData.filter(row => row['期間'] === '2024-06');
    
    // 商品別実績集計
    const productSales = {};
    june2024Data.forEach(row => {
        const product = row['商品名'];
        if (!productSales[product]) {
            productSales[product] = 0;
        }
        productSales[product] += parseInt(row['合計売上金額'] || 0);
    });
    
    // 目標データ整理
    const productTargets = {};
    juneTargets.forEach(row => {
        const product = '✨ ' + row['商品名'];
        productTargets[product] = parseInt(row['売上目標'] || 0);
    });

    const progressContainer = document.getElementById('product-progress');
    progressContainer.innerHTML = '';

    Object.keys(productSales).forEach(product => {
        const sales = productSales[product];
        const target = productTargets[product] || 0;
        const achievement = target > 0 ? (sales / target * 100) : 0;
        
        const progressItem = document.createElement('div');
        progressItem.className = 'progress-item';
        
        const shortName = product.replace('ハーゲンダッツ ', '');
        
        progressItem.innerHTML = `
            <div class="progress-label">${shortName}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${Math.min(achievement, 100)}%"></div>
            </div>
            <div class="progress-value">${achievement.toFixed(1)}%</div>
        `;
        
        progressContainer.appendChild(progressItem);
    });
}

// エリア別売上グラフ（棒グラフ）
async function drawAreaSalesChart() {
    const ctx = document.getElementById('area-sales-chart').getContext('2d');
    
    // 6月度エリア別データ集計
    const june2024Data = salesData.filter(row => row['年月'] === '2024-06');
    const areaSales = {};
    
    june2024Data.forEach(row => {
        const area = row['区'] || '不明';
        if (!areaSales[area]) {
            areaSales[area] = 0;
        }
        areaSales[area] += parseInt(row['合計売上金額'] || 0);
    });

    // 売上順でソート
    const sortedAreas = Object.entries(areaSales)
        .sort((a, b) => b[1] - a[1]);

    const labels = sortedAreas.map(([area]) => area);
    const data = sortedAreas.map(([, sales]) => sales);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '売上金額 (円)',
                data: data,
                backgroundColor: colors.gold,
                borderColor: colors.brown,
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString() + '円';
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}

// 月次推移グラフ（線グラフ）
async function drawMonthlyTrendChart() {
    const ctx = document.getElementById('monthly-trend-chart').getContext('2d');
    
    // 月別・商品別データ集計
    const monthlyData = {};
    
    salesData.forEach(row => {
        const month = row['年月'];
        const product = row['商品名'];
        
        if (!monthlyData[month]) {
            monthlyData[month] = {};
        }
        if (!monthlyData[month][product]) {
            monthlyData[month][product] = 0;
        }
        monthlyData[month][product] += parseInt(row['合計売上金額'] || 0);
    });

    const months = Object.keys(monthlyData).sort();
    const products = [...new Set(salesData.map(row => row['商品名']))];
    
    const datasets = products.map((product, index) => {
        const productData = months.map(month => monthlyData[month][product] || 0);
        const colorKey = product.includes('ストロベリー') ? 'strawberry' : 
                        product.includes('チョコレート') ? 'chocolate' : 'vanilla';
        
        return {
            label: product.replace('ハーゲンダッツ ', ''),
            data: productData,
            borderColor: colors[colorKey],
            backgroundColor: colors[colorKey] + '20',
            borderWidth: 3,
            fill: false,
            tension: 0.4,
            pointRadius: 6,
            pointHoverRadius: 8,
        };
    });
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: months.map(month => {
                const [year, monthNum] = month.split('-');
                return `${monthNum}月`;
            }),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString() + '円';
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// ページ読み込み時にデータを読み込み
document.addEventListener('DOMContentLoaded', function() {
    console.log('ページ読み込み完了、データ読み込み開始');
    loadData();
});