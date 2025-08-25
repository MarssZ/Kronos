# Kronos 加密货币价格预测

> **基于Kronos时间序列预测模型的加密货币价格预测工具**

## 📋 项目简介

本项目使用预训练的Kronos模型进行加密货币价格预测。Kronos是专门为金融市场K线数据设计的基础模型，通过分层离散化token技术处理OHLCV数据，实现高精度的时间序列预测。

## ✨ 核心功能

- 🚀 **实时数据获取**: 通过ccxt库从主流交易所获取实时K线数据
- 🧠 **AI预测引擎**: 使用预训练Kronos模型进行时间序列预测  
- ⚙️ **灵活配置**: 支持多种交易对、时间周期和预测参数
- 📊 **完整特征**: 支持OHLCV+Amount六维特征预测
- 🎯 **高精度**: 基于Transformer架构的自回归预测

## 🚀 快速开始

### 环境要求

- Python 3.10+
- CUDA支持的GPU (推荐)
- 代理工具 (国内用户访问海外交易所需要)

### 安装依赖

```bash
# 使用uv管理依赖 (推荐)
uv add ccxt pandas torch transformers

# 或使用pip
pip install ccxt pandas torch transformers
```

### 模型准备

将预训练模型放在以下路径：
```
./NeoQuasar/
├── Kronos-Tokenizer-base/
└── Kronos-small/
```

### 运行预测

```bash
python predict.py
```

## ⚙️ 配置说明

### 主要配置项

**1. 模型配置 (predict.py 第40-46行)**
```python
# 模型路径
tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")

# 设备选择
predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)
```

**2. 交易所配置 (第52-57行)**
```python
exchange = ccxt.okx({
    'proxies': {
        'http': 'http://localhost:1082',    # 代理端口
        'https': 'http://localhost:1082',   
    },
})
```

**3. 数据配置 (第64行)**
```python
df = fetch_ohlcv(exchange, 'BTC/USDT', '15m', 300)
#                          交易对      周期   数量
```

**4. 预测配置 (第75-76行)**
```python
lookback = 250  # 历史窗口长度
pred_len = 50   # 预测步长
```

**5. 生成参数 (第98-100行)**
```python
T=1.0,          # 温度: 0.5(保守) 1.0(中性) 1.5(激进)
top_p=0.9,      # 核采样: 保留前90%概率
sample_count=1  # 采样次数: 1(快速) 3-5(稳定)
```

### 配置建议

| 参数 | 推荐值 | 说明 |
|------|-------|------|
| **交易对** | BTC/USDT, ETH/USDT | 流动性好的主流币种 |
| **时间周期** | 15m, 1h | 平衡数据质量和预测精度 |
| **历史窗口** | 200-400 | 不超过max_context(512) |
| **预测长度** | 50-100 | 不超过历史窗口的1/4 |
| **温度** | 0.8-1.2 | 根据市场波动性调整 |

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