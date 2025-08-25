import ccxt
import pandas as pd
import mplfinance as mpf
try:
    from data_sources import data_manager
except ImportError:
    from src.data_sources import data_manager


def fetch_ohlcv(*args, **kwargs):
    """
    获取OHLCV数据的统一接口
    
    支持两种调用方式：
    1. 现有方式：fetch_ohlcv(exchange, symbol, timeframe, limit)
    2. 新方式：fetch_ohlcv(symbol, source='crypto', timeframe='1d', limit=700)
    """
    # 参数重载检测
    if len(args) == 4 and hasattr(args[0], 'fetch_ohlcv'):
        # 现有逻辑：4个参数且第一个是exchange对象
        print("Parameter detection: legacy_call")
        return _fetch_ohlcv_legacy(*args)
    elif len(args) >= 1 and isinstance(args[0], str):
        # 新逻辑：第一个参数是字符串symbol
        print("Parameter detection: new_call")
        return _fetch_ohlcv_new(*args, **kwargs)
    else:
        raise ValueError(f"不支持的参数格式: args={args}, kwargs={kwargs}")


def _fetch_ohlcv_legacy(exchange, symbol, timeframe, limit):
    """原有的crypto数据获取逻辑，保持不变"""
    since = None
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)   # ohlcv六要素：datatime, open, high, low, close, volume
        if len(ohlcv):
            print(f"读取到 {len(ohlcv)} 根蜡烛")
            # 转换为DataFrame with正确列名
            df = pd.DataFrame(ohlcv, columns=['timestamps', 'open', 'high', 'low', 'close', 'volume'])
            # 添加amount列 - KronosPredictor需要6个特征
            df['amount'] = df['volume'] * df[['open', 'high', 'low', 'close']].mean(axis=1)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(type(e).__name__, str(e))
        return pd.DataFrame()


def _fetch_ohlcv_new(symbol, source='crypto', timeframe='1d', limit=700):
    """新的多数据源获取逻辑"""
    try:
        return data_manager.get_data(symbol, source, timeframe, limit)
    except Exception as e:
        print(f"Error fetching data: {type(e).__name__}: {str(e)}")
        return pd.DataFrame()

# 示例调用
if __name__ == "__main__":
    exchange = ccxt.okx({
        'proxies': {
            'http': 'http://localhost:1082',    # 别忘了本地把代理打开
            'https': 'http://localhost:1082',
        },
    })

    # 获取数据
    ohlcv_data = fetch_ohlcv(exchange, 'BTC/USDT', '15m', 200)
    print(ohlcv_data)
