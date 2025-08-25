"""
Kronos时间序列预测模型 - 加密货币价格预测demo
核心功能：使用预训练的Kronos模型预测加密货币未来价格走势

【快速配置指南】
1. 模型路径配置 (第134-135行):
   - 确保./NeoQuasar/目录下有模型文件
   
2. 设备配置 (第137行):
   - 有GPU: device="cuda:0" 
   - 仅CPU: device="cpu"
   
3. 代理配置 (第196-199行):
   - 海外服务器: 删除proxies配置
   - 国内用户: 确保本地代理端口1082已启动
   
4. 交易配置 (第205-208行):
   - 交易对: 'BTC/USDT', 'ETH/USDT', 'SOL/USDT'等
   - 时间周期: '1m', '5m', '15m', '1h', '4h', '1d'
   - history_count: 历史数据量(默认300，ccxt单次获取上限)
   
5. 预测配置 (第208行):
   - pred_len: 预测长度(默认30)
   - 重要限制: history_count + pred_len ≤ 512 (模型上下文限制)
   
6. 生成参数调优 (第178-180行):
   - T(温度): 控制预测随机性，越低越确定(0.1-2.0)
   - top_p(核采样): 概率阈值，保留累积概率前p的token(0.1-1.0)
   - sample_count: 多次采样求均值，提高预测稳定性(1-10)

【重要改进】
✅ 真正的未来预测：predict_real_future() - 基于纯历史数据预测真实未来
❌ 训练模式伪预测：train_mode_predict() - 使用已知未来数据做验证(仅用于对比)
✅ 参数简化：合并了limit和lookback，消除数据浪费
✅ 上下文验证：防止超出模型512长度限制
"""

import ccxt
import pandas as pd
from model import Kronos, KronosTokenizer, KronosPredictor
from src.fetch_ohlcv import fetch_ohlcv

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
    if df is None or len(df) == 0:
        raise ValueError("获取数据失败或数据为空")
        
    # 时间戳转换 - 根据数据源类型处理
    # crypto数据(ccxt): 毫秒时间戳需要转换
    # A股数据(tushare): 已经是datetime对象，无需转换
    if df['timestamps'].dtype == 'int64':  # 毫秒时间戳
        df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    # 如果已经是datetime类型，保持不变
    
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

def predict_real_future(symbol, source='crypto', exchange=None, timeframe='15m', history_count=300, pred_len=50):
    """
    真正的未来预测 - 支持crypto和A股两种数据源
    
    Args:
        symbol: 标的代码 ('BTC/USDT' 或 '600848')
        source: 数据源类型 ('crypto' 或 'cn_stock')
        exchange: 交易所对象 (仅crypto需要)
        timeframe: 时间周期 (仅crypto需要)
        history_count: 历史数据量
        pred_len: 预测长度
        
    注意:
        history_count + pred_len 不能超过模型上下文限制(512)
    
    Returns:
        pd.DataFrame: 预测结果
    """
    # 加载模型
    tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")
    max_context = 512  # 模型上下文窗口限制
    predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=max_context)
    print("模型加载完成！")
    
    # 关键验证：防止超出模型上下文限制
    total_length = history_count + pred_len
    if total_length > max_context:
        raise ValueError(f"序列长度超出模型限制: {total_length} > {max_context} "
                        f"(history_count={history_count} + pred_len={pred_len})")
    
    # 根据数据源获取历史数据
    if source == 'crypto':
        if exchange is None:
            raise ValueError("crypto数据源需要提供exchange参数")
        df = fetch_ohlcv(exchange, symbol, timeframe, history_count)
    elif source == 'cn_stock':
        df = fetch_ohlcv(symbol, source='cn_stock', limit=history_count)
    else:
        raise ValueError(f"不支持的数据源: {source}")
        
    if df is None or len(df) == 0:
        raise ValueError("获取数据失败或数据为空")
        
    # 时间戳转换 - 根据数据源类型处理
    if df['timestamps'].dtype == 'int64':  # crypto毫秒时间戳
        df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
    # A股数据已经是datetime类型，无需转换
    
    # 验证数据充足性
    if len(df) < history_count:
        raise ValueError(f"获取数据不足: 需要{history_count}条, 实际{len(df)}条")
    
    # 使用所有历史数据
    x_df = df[['open', 'high', 'low', 'close', 'volume', 'amount']]
    x_timestamp = df['timestamps']
    
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
    print("\n预测数据:")
    print(pred_df)
    return pred_df

def main():
    """
    主函数 - 演示crypto和A股两种预测方式
    """
    print("=== Kronos多数据源预测演示 ===\n")
    
    # 方式1: A股预测 (推荐，无需代理)
    print("1. A股预测示例:")
    try:
        pred_df = predict_real_future(
            symbol='600104',           # 上汽集团
            source='cn_stock',
            history_count=365,         # 使用200天历史数据
            pred_len=30               # 预测未来30天
        )
        return pred_df
    except Exception as e:
        print(f"A股预测失败: {e}")
    
    # 方式2: Crypto预测 (需要代理)
    # print("\n2. Crypto预测示例:")
    # try:
    #     exchange = ccxt.okx({
    #         'proxies': {
    #             'http': 'http://localhost:1082',
    #             'https': 'http://localhost:1082',
    #         },
    #     })
        
    #     return predict_real_future(
    #         symbol='BTC/USDT',
    #         source='crypto',
    #         exchange=exchange,
    #         timeframe='15m',
    #         history_count=300,
    #         pred_len=30
    #     )
    # except Exception as e:
    #     print(f"Crypto预测失败: {e}")
    #     return None

if __name__ == "__main__":
    main()