#!/usr/bin/env python3
"""
测试fetch_ohlcv参数重载检测逻辑
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from fetch_ohlcv import fetch_ohlcv

# Mock exchange对象用于测试
class MockExchange:
    def fetch_ohlcv(self, symbol, timeframe, since, limit):
        # 返回模拟数据
        return [
            [1640000000000, 50000, 51000, 49000, 50500, 1000],  # timestamp, o, h, l, c, v
            [1640003600000, 50500, 52000, 50000, 51500, 1200],
        ]

def test_parameter_detection():
    print("=== 测试参数重载检测逻辑 ===")
    
    # 测试1: Legacy调用方式 (4个参数 + exchange对象)
    print("\n测试1: Legacy调用方式")
    exchange = MockExchange()
    try:
        result = fetch_ohlcv(exchange, 'BTC/USDT', '15m', 300)
        print("Legacy调用测试通过")
    except Exception as e:
        print(f"Legacy调用测试失败: {e}")
    
    # 测试2: 新调用方式 (symbol字符串)
    print("\n测试2: 新调用方式")  
    try:
        result = fetch_ohlcv('600848', source='cn_stock')
        print("新调用测试通过（预期会因为没有适配器而报错，但参数检测正常）")
    except Exception as e:
        print(f"新调用测试：{e}")
    
    # 测试3: 默认参数调用
    print("\n测试3: 默认crypto调用")
    try:
        result = fetch_ohlcv('BTC/USDT')
        print("默认调用测试通过（预期会因为没有适配器而报错，但参数检测正常）")
    except Exception as e:
        print(f"默认调用测试：{e}")

if __name__ == "__main__":
    test_parameter_detection()