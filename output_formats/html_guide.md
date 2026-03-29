# HTML 输出格式指南

## 适用场景

| 场景 | 推荐程度 | 说明 |
|------|----------|------|
| 日常数据 Recap | ⭐⭐⭐⭐⭐ | 最佳选择 |
| 交互式探索 | ⭐⭐⭐⭐⭐ | 最佳选择 |
| 周报/月报 | ⭐⭐⭐⭐ | 配合 PPT |
| 高管汇报 | ⭐⭐⭐ | 作为补充材料 |
| 数据明细 | ⭐⭐ | Excel 更适合 |

## 技术栈

### 核心库
- **ECharts 5.x** - 图表库
- **XLSX.js** - Excel 导出
- **原生 CSS** - 样式（无框架依赖）

### CDN 引入
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18/dist/xlsx.full.min.js"></script>
```

## 图表类型

### 趋势图（折线图）
```javascript
{
    type: 'line',
    smooth: true,
    data: [...],
    areaStyle: { opacity: 0.1 },
    itemStyle: { color: '#667eea' }
}
```

### 占比图（饼图/环形图）
```javascript
{
    type: 'pie',
    radius: ['40%', '70%'],  // 环形图
    data: [
        { value: 1048, name: 'APP' },
        { value: 735, name: 'Web' },
        { value: 580, name: '小程序' }
    ]
}
```

### 漏斗图
```javascript
{
    type: 'funnel',
    data: [
        { value: 100, name: '浏览' },
        { value: 60, name: '加购' },
        { value: 40, name: '下单' },
        { value: 30, name: '支付' }
    ]
}
```

### 柱状图
```javascript
{
    type: 'bar',
    data: [...],
    itemStyle: {
        color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
                { offset: 0, color: '#667eea' },
                { offset: 1, color: '#764ba2' }
            ]
        }
    }
}
```

## 交互功能

### 时间筛选
```html
<select id="timeRange" onchange="updateData()">
    <option value="7d">近 7 天</option>
    <option value="30d">近 30 天</option>
    <option value="90d">近 90 天</option>
</select>
```

### 导出 Excel
```javascript
function exportToExcel() {
    const table = document.getElementById('data-table');
    const wb = XLSX.utils.table_to_book(table, { sheet: '数据' });
    XLSX.writeFile(wb, 'report_' + new Date().toISOString().slice(0,10) + '.xlsx');
}
```

### 打印优化
```css
@media print {
    .filter-bar { display: none; }
    .chart-card { break-inside: avoid; }
    body { background: white; }
}
```

## 响应式设计

### CSS Grid 布局
```css
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}

.two-col {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}

@media (max-width: 768px) {
    .two-col {
        grid-template-columns: 1fr;
    }
}
```

### 图表自适应
```javascript
window.addEventListener('resize', function() {
    echarts.getInstanceByDom(document.getElementById('chart-trend')).resize();
});
```

## 性能优化

### 大数据量处理
```javascript
// 数据采样
function sampleData(data, maxPoints = 100) {
    if (data.length <= maxPoints) return data;
    const step = Math.ceil(data.length / maxPoints);
    return data.filter((_, i) => i % step === 0);
}

// 懒加载图表
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            initChart(entry.target);
        }
    });
});
```

## 文件命名规范

```
{类型}_{时间范围}_{日期}.html

示例：
- gmv_recap_7d_20240115.html
- user_analysis_q4_202401.html
- weekly_report_20240115.html
```
