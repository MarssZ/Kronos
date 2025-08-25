import ccxt
import pandas as pd
import mplfinance as mpf

def fetch_ohlcv(exchange, symbol, timeframe, limit):
    since = None
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)   # ohlcv六要素：datatime, open, high, low, close, volume
        if len(ohlcv):
            print(f"读取到 {len(ohlcv)} 根蜡烛")
            # 转换为DataFrame with正确列名
            df = pd.DataFrame(ohlcv, columns=['timestamps', 'open', 'high', 'low', 'close', 'volume'])
            return df
        return pd.DataFrame()
    except Exception as e:
        print(type(e).__name__, str(e))
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
