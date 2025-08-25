"""
Kronos时间序列预测模型 - 加密货币价格预测demo
核心功能：使用预训练的Kronos模型预测加密货币未来价格走势

【快速配置指南】
1. 模型路径配置 (第14-15行):
   - 确保./NeoQuasar/目录下有模型文件
   
2. 设备配置 (第20行):
   - 有GPU: device="cuda:0" 
   - 仅CPU: device="cpu"
   
3. 代理配置 (第28-29行):
   - 海外服务器: 删除proxies配置
   - 国内用户: 确保本地代理端口1082已启动
   
4. 交易配置 (第38行):
   - 交易对: 'BTC/USDT', 'ETH/USDT', 'SOL/USDT'等
   - 时间周期: '1m', '5m', '15m', '1h', '4h', '1d'
   - 数据量: 建议300-1000条，影响预测质量
   
5. 预测配置 (第49-50行):
   - lookback: 历史窗口，越大越准确但越慢
   - pred_len: 预测长度，不宜超过历史窗口的1/4
   
6. 生成参数调优 (第96-98行):
   - T(温度): 控制预测随机性，越低越确定(0.1-2.0)
   - top_p(核采样): 概率阈值，保留累积概率前p的token(0.1-1.0)
   - sample_count: 多次采样求均值，提高预测稳定性(1-10)
"""

import ccxt
import pandas as pd
from model import Kronos, KronosTokenizer, KronosPredictor
from fetch_ohlcv import fetch_ohlcv

def train_mode_predict():
    """
    训练模式预测 - 使用已知未来数据做验证
    注意：这不是真正的预测，而是模型在已知数据上的拟合测试
    保留此函数仅用于与真正预测的对比分析
    """
    # ==================== 模型配置区域 ====================
    # 【需手动配置】模型路径 - 确保模型文件存在于指定路径
    tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")
    
    # 【需手动配置】设备和上下文长度
    # device: "cuda:0"(GPU) 或 "cpu"(CPU)
    # max_context: 模型上下文窗口大小，影响计算效率
    predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)
    
    print("模型加载完成！")
    
    # ==================== 交易所配置区域 ====================
    # 【需手动配置】代理设置 - 如果在中国大陆访问海外交易所
    exchange = ccxt.okx({
        'proxies': {
            'http': 'http://localhost:1082',    # 本地代理端口
            'https': 'http://localhost:1082',   # 确保代理服务已启动
        },
    })
    
    # ==================== 数据获取配置区域 ====================
    # 【需手动配置】交易对、时间周期、数据量
    # symbol: 'BTC/USDT', 'ETH/USDT', 'SOL/USDT' 等
    # timeframe: '1m', '5m', '15m', '1h', '4h', '1d' 等
    # limit: 获取K线数量，影响预测质量和计算时间
    df = fetch_ohlcv(exchange, 'BTC/USDT', '15m', 300)
    if df is None or len(df) == 0:
        raise ValueError("获取数据失败或数据为空")
        
    # 时间戳转换 - ccxt返回毫秒级时间戳，转换为datetime
    df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    
    # ==================== 预测参数配置区域 ====================
    # 【需手动配置】预测窗口设置
    # lookback: 用于训练的历史数据点数 - 越多越准确但计算越慢
    # pred_len: 预测的未来数据点数 - 不宜过长，预测质量随时间衰减
    lookback = 250  # 使用200个历史点(15分钟*200 = 50小时历史)
    pred_len = 50   # 预测50个未来点(15分钟*50 = 12.5小时未来)
    
    # 数据充足性验证
    if len(df) < lookback + pred_len:
        raise ValueError(f"数据不足: 需要{lookback + pred_len}条, 实际{len(df)}条")
    
    # ==================== 数据准备区域 ====================
    # 准备模型输入数据
    # x_df: 历史价格数据(OHLCV+Amount) - 模型需要6个特征
    # x_timestamp: 历史时间戳 - 用于时间特征编码(minute/hour/day/month/weekday)
    # y_timestamp: 预测目标时间戳 - 需要预测的时间点
    x_df = df.loc[:lookback-1, ['open', 'high', 'low', 'close', 'volume', 'amount']]
    x_timestamp = df.loc[:lookback-1, 'timestamps']
    y_timestamp = df.loc[lookback:lookback+pred_len-1, 'timestamps']
    
    # ==================== 模型推理配置区域 ====================
    # 【需手动配置】生成参数 - 控制预测质量和随机性
    pred_df = predictor.predict(
        df=x_df,                # 历史OHLCV+A数据
        x_timestamp=x_timestamp, # 历史时间戳
        y_timestamp=y_timestamp, # 预测目标时间戳
        pred_len=pred_len,       # 预测长度
        T=1.0,          # 【可调节】温度: 0.5(保守) 1.0(中性) 1.5(激进)
        top_p=0.9,      # 【可调节】核采样: 保留前90%概率的选择
        sample_count=1  # 【可调节】采样次数: 1(快速) 3-5(稳定) 10+(高质量)
    )
    
    # ==================== 结果展示区域 ====================
    print(f"\n预测完成！预测了{len(pred_df)}个时间点")
    print(f"预测时间范围: {pred_df.index[0]} 到 {pred_df.index[-1]}")
    print("\n预测数据前5行:")
    print(pred_df.head())
    return pred_df

def predict_real_future(exchange, symbol, timeframe, limit, lookback=250, pred_len=50):
    """
    真正的未来预测 - 基于历史数据预测真实未来
    
    Args:
        exchange: 交易所对象
        symbol: 交易对
        timeframe: 时间周期 
        limit: 获取数据量
        lookback: 历史窗口长度
        pred_len: 预测长度
    
    Returns:
        pd.DataFrame: 预测结果
    """
    # 加载模型
    tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")
    predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)
    print("模型加载完成！")
    
    # 获取历史数据
    df = fetch_ohlcv(exchange, symbol, timeframe, limit)
    if df is None or len(df) == 0:
        raise ValueError("获取数据失败或数据为空")
        
    df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    
    # 真正的预测只需要历史数据
    if len(df) < lookback:
        raise ValueError(f"历史数据不足: 需要{lookback}条, 实际{len(df)}条")
    
    # 使用最近的历史数据
    x_df = df.iloc[-lookback:][['open', 'high', 'low', 'close', 'volume', 'amount']]
    x_timestamp = df.iloc[-lookback:]['timestamps']
    
    # 计算时间间隔（分钟）
    time_diff = (x_timestamp.iloc[-1] - x_timestamp.iloc[-2]).total_seconds() / 60
    
    # 生成真正的未来时间戳
    last_time = x_timestamp.iloc[-1]
    future_timestamps = pd.date_range(
        start=last_time + pd.Timedelta(minutes=time_diff),
        periods=pred_len,
        freq=f'{int(time_diff)}min'
    )
    
    # 执行真正的预测
    pred_df = predictor.predict(
        df=x_df,
        x_timestamp=x_timestamp,
        y_timestamp=pd.Series(future_timestamps),  # 转为Series避免DatetimeIndex.dt错误
        pred_len=pred_len,
        T=1.0,
        top_p=0.9,
        sample_count=1
    )
    
    print(f"\n真实未来预测完成！预测了{len(pred_df)}个时间点")
    print(f"历史数据截止时间: {x_timestamp.iloc[-1]}")
    print(f"预测时间范围: {pred_df.index[0]} 到 {pred_df.index[-1]}")
    print("\n预测数据前5行:")
    print(pred_df.head())
    return pred_df

def main():
    """
    主函数 - 执行真正的未来预测
    """
    # 配置交易所
    exchange = ccxt.okx({
        'proxies': {
            'http': 'http://localhost:1082',
            'https': 'http://localhost:1082',
        },
    })
    
    # 执行真正的预测
    return predict_real_future(
        exchange=exchange,
        symbol='BTC/USDT',
        timeframe='15m',
        limit=300,
        lookback=250,
        pred_len=50
    )

if __name__ == "__main__":
    main()