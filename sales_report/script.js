document.addEventListener('DOMContentLoaded', async () => {
    // --- グローバル設定 ---
    Chart.defaults.font.family = "'Noto Sans JP', sans-serif";
    Chart.defaults.color = '#2C3E50';

    // --- データ読み込み (文字化け対策) ---
    const fetchAndDecode = async (url) => {
        const response = await fetch(url);
        const buffer = await response.arrayBuffer();
        return new TextDecoder('utf-8').decode(buffer);
    };

    const salesSummaryPromise = fetchAndDecode('sales_summary.csv');
    const salesTargetPromise = fetchAndDecode('sales_target.csv');

    const [summaryText, targetText] = await Promise.all([salesSummaryPromise, salesTargetPromise]);

    const summaryData = Papa.parse(summaryText, { header: true, dynamicTyping: true }).data;
    const targetData = Papa.parse(targetText, { header: true, dynamicTyping: true }).data;

    // --- データ加工 ---
    const juneSales = summaryData.filter(row => row.年月 === '2024-06');
    const maySales = summaryData.filter(row => row.年月 === '2024-05');
    const juneTarget = targetData.filter(row => row.期間 === '2024-06');

    // 1. KPIサマリー
    const totalSales = juneSales.reduce((sum, row) => sum + row.合計売上金額, 0);
    const totalQuantity = juneSales.reduce((sum, row) => sum + row.合計販売数量, 0);
    const totalTarget = juneTarget.reduce((sum, row) => sum + row.売上目標, 0);
    const achievementRate = totalTarget > 0 ? (totalSales / totalTarget) * 100 : 0;

    document.getElementById('total-sales').textContent = `¥${totalSales.toLocaleString()}`;
    document.getElementById('total-quantity').textContent = `${totalQuantity.toLocaleString()}個`;
    document.getElementById('achievement-rate').textContent = `${achievementRate.toFixed(1)}%`;

    // --- グラフデータ作成 ---

    // 2. 商品別売上実績 (棒グラフ)
    const productSales = {};
    juneSales.forEach(row => {
        if (!productSales[row.商品名]) {
            productSales[row.商品名] = 0;
        }
        productSales[row.商品名] += row.合計売上金額;
    });

    // 3. エリア別売上構成比 (円グラフ)
    const areaSales = {};
    juneSales.forEach(row => {
        if (!areaSales[row.区]) {
            areaSales[row.区] = 0;
        }
        areaSales[row.区] += row.合計売上金額;
    });

    // 4. 目標達成率比較 (横棒グラフ)
    const achievementByProduct = {};
    juneTarget.forEach(targetRow => {
        const productName = targetRow.商品名;
        const actualSales = productSales[productName] || 0;
        const targetSales = targetRow.売上目標;
        achievementByProduct[productName] = targetSales > 0 ? (actualSales / targetSales) * 100 : 0;
    });

    // 5. 前月比較 (線グラフ)
    const mayProductSales = {};
    maySales.forEach(row => {
        if (!mayProductSales[row.商品名]) {
            mayProductSales[row.商品名] = 0;
        }
        mayProductSales[row.商品名] += row.合計売上金額;
    });
    const productNames = Object.keys(productSales).sort();
    const maySalesData = productNames.map(name => mayProductSales[name] || 0);
    const juneSalesData = productNames.map(name => productSales[name] || 0);


    // --- グラフ描画 ---
    const ctxProduct = document.getElementById('productSalesChart').getContext('2d');
    new Chart(ctxProduct, {
        type: 'bar',
        data: {
            labels: Object.keys(productSales),
            datasets: [{
                label: '売上金額',
                data: Object.values(productSales),
                backgroundColor: ['#FF6B9D', '#4ECDC4', '#FFCE56', '#FF8A80', '#A1887F'],
                borderRadius: 5,
            }]
        },
        options: { 
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    const ctxArea = document.getElementById('areaCompositionChart').getContext('2d');
    new Chart(ctxArea, {
        type: 'pie',
        data: {
            labels: Object.keys(areaSales),
            datasets: [{
                data: Object.values(areaSales),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
                borderColor: '#F8F9FA',
                borderWidth: 2,
            }]
        },
        options: { 
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });

    const ctxAchievement = document.getElementById('achievementChart').getContext('2d');
    new Chart(ctxAchievement, {
        type: 'bar',
        data: {
            labels: Object.keys(achievementByProduct),
            datasets: [{
                label: '目標達成率 (%)',
                data: Object.values(achievementByProduct),
                backgroundColor: Object.values(achievementByProduct).map(rate => rate >= 100 ? '#4ECDC4' : '#FF6B9D'),
                borderRadius: 5,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + '%'
                        }
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    const ctxMonth = document.getElementById('monthComparisonChart').getContext('2d');
    new Chart(ctxMonth, {
        type: 'line',
        data: {
            labels: productNames,
            datasets: [
                {
                    label: '5月売上',
                    data: maySalesData,
                    borderColor: '#FF6B9D',
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3,
                },
                {
                    label: '6月売上',
                    data: juneSalesData,
                    borderColor: '#4ECDC4',
                    fill: false,
                    tension: 0.3,
                }
            ]
        },
        options: { 
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });

    // --- フッター ---
    document.getElementById('created-date').textContent = new Date().toLocaleDateString();
});