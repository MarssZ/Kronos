# Kronos 金融预测系统

> **基于Kronos模型的多数据源金融预测工具**

## 核心功能

- **多数据源**: 支持A股(tushare) + 加密货币(ccxt)
- **真实预测**: 基于纯历史数据预测真实未来
- **统一接口**: `fetch_ohlcv()`统一处理所有数据源
- **智能测试**: 测试文件统一管理在`tests/`目录

## 快速开始

### 1分钟启动

```bash
# 安装依赖
uv sync

# 运行A股预测(推荐 - 无需代理)
python predict.py

# 运行测试
python tests/test_integration.py
```

### 模型文件

确保`./NeoQuasar/`下有预训练模型文件。

## ⚙️ 配置说明

### 主要配置项

**1. 模型配置 (predict.py 第134-137行)**
```python
# 模型路径
tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")
max_context = 512  # 模型上下文窗口限制

# 设备选择
predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=max_context)
```

**2. 交易所配置 (第195-200行)**
```python
exchange = ccxt.okx({
    'proxies': {
        'http': 'http://localhost:1082',    # 代理端口
        'https': 'http://localhost:1082',   
    },
})
```

**3. 预测调用 (第203-209行)**
```python
predict_real_future(
    exchange=exchange,
    symbol='BTC/USDT',        # 交易对
    timeframe='15m',          # 时间周期
    history_count=300,        # 历史数据量
    pred_len=30               # 预测长度
)
```

**4. 生成参数 (第178-180行)**
```python
T=1.0,          # 温度: 0.5(保守) 1.0(中性) 1.5(激进)
top_p=0.9,      # 核采样: 保留前90%概率
sample_count=1  # 采样次数: 1(快速) 3-5(稳定)
```

**⚠️ 重要限制**
```python
# 关键约束：history_count + pred_len ≤ 512
# 当前默认：300 + 30 = 330 < 512 ✓
# 如果超出：会在运行前报错并提示
```

### 配置建议

| 参数 | 推荐值 | 说明 |
|------|-------|------|
| **交易对** | BTC/USDT, ETH/USDT | 流动性好的主流币种 |
| **时间周期** | 15m, 1h | 平衡数据质量和预测精度 |
| **历史数据量** | 250-400 | 受限于 history_count + pred_len ≤ 512 |
| **预测长度** | 20-50 | 较短预测更准确，避免超出上下文限制 |
| **温度** | 0.8-1.2 | 根据市场波动性调整 |

**⚡ 快速配置示例**

```python
# 保守配置 (高准确性)
history_count=400, pred_len=20, T=0.8

# 平衡配置 (推荐)  
history_count=300, pred_len=30, T=1.0

# 激进配置 (长预测)
history_count=250, pred_len=50, T=1.2
```

## 📊 输出示例

```
模型加载完成！
读取到 300 根蜡烛

预测完成！预测了50个时间点
预测时间范围: 2025-08-24 04:15:00 到 2025-08-24 16:30:00

预测数据前5行:
                              open           high  ...     volume      amount
timestamps                                         ...
2025-08-24 04:15:00  115239.984375  115309.195312  ...  25.452509  3064430.75
2025-08-24 04:30:00  115016.898438  115442.117188  ...  37.004250  4482188.00
2025-08-24 04:45:00  115120.062500  115135.945312  ...  27.784729  3209671.00
```

## 🔧 项目结构

```
Kronos/
├── predict.py              # 主入口文件
├── fetch_ohlcv.py         # 数据获取模块  
├── model/                 # 模型定义
│   ├── kronos.py          # 核心模型
│   └── module.py          # 模型组件
├── NeoQuasar/             # 预训练模型
└── README.md              # 项目文档
```

## 🛠️ 常见问题

**Q: 如何更换交易所？**
A: 修改`predict.py`第52行的exchange配置，ccxt支持100+交易所

**Q: 预测精度如何提升？**
A: 1) 增加历史窗口长度 2) 提高sample_count 3) 选择流动性好的交易对

**Q: GPU内存不足怎么办？**
A: 1) 设置device="cpu" 2) 减少max_context 3) 降低batch处理量

**Q: 网络连接失败？**
A: 1) 检查代理设置 2) 更换交易所 3) 检查网络连接

## 📈 性能优化

- **GPU加速**: 使用CUDA显著提升推理速度
- **批量预测**: sample_count>1时并行处理多个预测路径
- **内存优化**: 合理设置max_context避免OOM
- **网络优化**: 使用稳定的代理服务

## 📄 开源协议

MIT License

---

**⚠️ 风险提示**: 本工具仅供学习研究使用，加密货币投资存在高风险，请谨慎决策。