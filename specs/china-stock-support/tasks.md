# A股数据支持实现任务清单

**按验证难易程度排序（避免错误传染）**

## 🟢 1秒验证任务

- [ ] 1. 安装tushare库
  - 需求：REQ-1.1 多数据源支持
  - 文件：requirements.txt, pyproject.toml  
  - 验证：运行`python -c "import tushare; print('✅')"` → 无错误输出

- [ ] 2. 创建数据源管理器基础类
  - 需求：REQ-1.1 多数据源支持
  - 文件：data_sources.py
  - 验证：运行`python -c "from data_sources import DataSourceManager; print('✅')"` → 无错误输出

## 🟡 5秒验证任务  

- [ ] 3. 实现函数重载参数检测逻辑
  - 需求：REQ-1.1, REQ-3.1 保持现有功能
  - 文件：fetch_ohlcv.py
  - 验证：运行测试脚本 → Console显示`"Parameter detection: legacy_call"`和`"Parameter detection: new_call"`

- [ ] 4. 创建A股数据适配器
  - 需求：REQ-1.1, REQ-2.1 统一数据格式
  - 文件：data_sources.py
  - 验证：运行`python -c "from data_sources import ChinaStockAdapter; print(ChinaStockAdapter.__name__)"`→ 显示`"ChinaStockAdapter"`

- [ ] 5. 实现数据格式标准化
  - 需求：REQ-2.1 统一数据格式
  - 文件：data_sources.py  
  - 验证：运行格式转换测试 → Console显示`"Columns: ['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']"`

## 🟠 状态验证任务

- [ ] 6. 集成新接口到fetch_ohlcv函数
  - 需求：REQ-1.1, REQ-3.1 保持现有功能
  - 文件：fetch_ohlcv.py
  - 验证：调用`fetch_ohlcv('600848', source='cn_stock')` → 返回DataFrame包含6列数据

- [ ] 7. 测试向后兼容性  
  - 需求：REQ-3.1 保持现有功能
  - 文件：test_compatibility.py
  - 验证：运行现有crypto调用 → 返回结果与修改前一致

## 🔴 Console验证任务

- [ ] 8. 测试A股数据获取
  - 需求：REQ-1.1, REQ-2.1
  - 文件：test_china_stock.py  
  - 验证：获取600848数据 → Console显示`"Retrieved 365+ records for 600848"`

- [ ] 9. 测试错误处理
  - 需求：REQ-2.4 数据转换失败处理
  - 文件：test_error_handling.py
  - 验证：模拟token错误 → Console显示`"ConfigurationError: Invalid tushare token"`

## 实施顺序

1. **先做1秒验证任务** - 快速建立基础架构
2. **再做5秒验证任务** - 构建核心功能组件  
3. **然后状态验证任务** - 集成和兼容性测试
4. **最后Console验证任务** - 边缘情况和错误处理

**原则：越容易发现bug的功能，越早做**