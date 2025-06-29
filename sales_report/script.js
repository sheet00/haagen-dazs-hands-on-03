// カラーパレット定義
const colors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#48bb78',
    warning: '#ed8936',
    danger: '#f56565',
    info: '#4299e1',
    haagen: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7', '#a29bfe']
};

// Chart.jsのデフォルト設定
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#4a5568';

// 月次売上推移グラフ
function createMonthlyTrendChart() {
    const ctx = document.getElementById('monthlyTrendChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['5月', '6月'],
            datasets: [
                {
                    label: '売上金額 (円)',
                    data: [82000, 79100],
                    borderColor: colors.primary,
                    backgroundColor: colors.primary + '20',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    yAxisID: 'y'
                },
                {
                    label: '販売数量 (個)',
                    data: [560, 539],
                    borderColor: colors.secondary,
                    backgroundColor: colors.secondary + '20',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: colors.primary,
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: '売上金額 (円)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: '販売数量 (個)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// 商品別売上比較グラフ
function createProductSalesChart() {
    const ctx = document.getElementById('productSalesChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['バニラ', 'ストロベリー', 'チョコレート', 'クッキー&クリーム', 'マカダミア', 'ラムレーズン'],
            datasets: [{
                label: '売上金額 (円)',
                data: [18500, 15200, 14800, 12100, 9800, 8700],
                backgroundColor: colors.haagen,
                borderColor: colors.haagen.map(color => color + '80'),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    callbacks: {
                        label: function(context) {
                            return `売上: ¥${context.parsed.y.toLocaleString()}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '¥' + value.toLocaleString();
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// エリア別売上分布グラフ
function createAreaSalesChart() {
    const ctx = document.getElementById('areaSalesChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['新宿区', '渋谷区', '港区', '千代田区', '中央区', 'その他'],
            datasets: [{
                data: [22.1, 18.5, 16.3, 14.2, 12.8, 16.1],
                backgroundColor: colors.haagen,
                borderColor: '#fff',
                borderWidth: 3,
                hoverOffset: 10
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
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000
            },
            cutout: '60%'
        }
    });
}

// 目標達成率グラフ
function createAchievementChart() {
    const ctx = document.getElementById('achievementChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['バニラ', 'ストロベリー', 'チョコレート', 'クッキー&クリーム', 'マカダミア', 'ラムレーズン'],
            datasets: [{
                label: '達成率 (%)',
                data: [31.2, 28.5, 24.8, 22.1, 18.3, 15.7],
                backgroundColor: function(context) {
                    const value = context.parsed.y;
                    if (value >= 30) return colors.success;
                    if (value >= 20) return colors.warning;
                    return colors.danger;
                },
                borderColor: function(context) {
                    const value = context.parsed.y;
                    if (value >= 30) return colors.success;
                    if (value >= 20) return colors.warning;
                    return colors.danger;
                },
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    callbacks: {
                        label: function(context) {
                            return `達成率: ${context.parsed.x}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    max: 100
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// 数値のアニメーション効果
function animateNumbers() {
    const kpiValues = document.querySelectorAll('.kpi-value');
    
    kpiValues.forEach(element => {
        const finalValue = element.textContent;
        const isNegative = finalValue.includes('-');
        const isPercentage = finalValue.includes('%');
        const isCurrency = finalValue.includes('¥');
        const isCount = finalValue.includes('個');
        
        let numericValue = parseFloat(finalValue.replace(/[^0-9.-]/g, ''));
        
        if (isNaN(numericValue)) return;
        
        let currentValue = 0;
        const increment = numericValue / 60;
        const timer = setInterval(() => {
            currentValue += increment;
            
            if (currentValue >= numericValue) {
                currentValue = numericValue;
                clearInterval(timer);
            }
            
            let displayValue = Math.floor(currentValue);
            
            if (isCurrency) {
                element.textContent = `¥${displayValue.toLocaleString()}`;
            } else if (isPercentage) {
                element.textContent = `${isNegative ? '-' : ''}${Math.abs(displayValue * 10) / 10}%`;
            } else if (isCount) {
                element.textContent = `${displayValue}個`;
            } else {
                element.textContent = displayValue.toString();
            }
        }, 16);
    });
}

// DOMContentLoadedイベントリスナー
document.addEventListener('DOMContentLoaded', function() {
    // 少し遅延してからアニメーションを開始
    setTimeout(() => {
        createMonthlyTrendChart();
        createProductSalesChart();
        createAreaSalesChart();
        createAchievementChart();
        animateNumbers();
    }, 300);
    
    // ページ読み込み時のフェードインアニメーション
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// リサイズ時のChart.js再描画
window.addEventListener('resize', function() {
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.resize();
    });
});