# A股数据支持需求

## 使用场景
按需预测A股标的，需要365-700条历史日线数据进行预测分析。

## 需求

### 需求1：多数据源支持
**用户故事：** 作为预测分析师，我希望通过指定数据源类型来获取不同市场的数据，以便预测A股和加密货币标的

#### 验收标准
1. WHEN 调用 `fetch_ohlcv('600848', source='cn_stock')` THEN 系统 SHALL 使用tushare获取A股数据
2. WHEN 调用 `fetch_ohlcv('BTC/USDT', source='crypto')` THEN 系统 SHALL 使用ccxt获取加密货币数据
3. WHEN 调用 `fetch_ohlcv('BTC/USDT')` THEN 系统 SHALL 默认使用crypto源保持向后兼容
4. IF source参数无效 THEN 系统 SHALL 抛出ValueError异常

### 需求2：统一数据格式
**用户故事：** 作为预测模型，我希望接收统一的OHLCV+Amount格式数据，以便无缝处理不同数据源

#### 验收标准
1. WHEN tushare返回数据 THEN 系统 SHALL 转换为标准6列格式[Open,High,Low,Close,Volume,Amount]
2. WHEN tushare数据缺少amount列 THEN 系统 SHALL 通过volume*close计算
3. WHEN 数据获取失败 THEN 系统 SHALL 返回空DataFrame并记录错误
4. IF 数据转换失败 THEN 系统 SHALL 抛出异常而不是静默失败

### 需求3：保持现有功能
**用户故事：** 作为现有用户，我希望A股功能不影响现有加密货币预测，以便继续使用已有工作流

#### 验收标准
1. WHEN 调用现有 `predict_real_future('BTC/USDT')` THEN 系统 SHALL 保持原有行为
2. WHEN tushare配置缺失 THEN 系统 SHALL 仅影响cn_stock源，不影响crypto源
3. WHEN 调用 `fetch_ohlcv('600848', source='cn_stock')` THEN 系统 SHALL 获取足够预测的365-700条数据

## 技术约束
- 仅支持A股日线数据
- 需要有效tushare token
- 不修改现有crypto相关代码逻辑