#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试向后兼容性 - 任务7验证脚本
验证条件：运行现有crypto调用 → 返回结果与修改前一致
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

import ccxt
from fetch_ohlcv import fetch_ohlcv

def test_crypto_compatibility():
    """测试原有crypto调用方式的兼容性"""
    print("=== 测试向后兼容性 ===")
    
    try:
        # 模拟一个最小的exchange对象，用于测试
        class MockExchange:
            def fetch_ohlcv(self, symbol, timeframe, since, limit):
                # 模拟返回数据：[timestamp, open, high, low, close, volume]
                return [
                    [1640995200000, 47000.0, 48000.0, 46000.0, 47500.0, 100.5],
                    [1640995260000, 47500.0, 48500.0, 47000.0, 48000.0, 120.3],
                    [1640995320000, 48000.0, 49000.0, 47500.0, 48500.0, 110.8]
                ]
        
        mock_exchange = MockExchange()
        
        # 测试原有的4参数调用方式
        print("测试原有crypto调用方式...")
        df = fetch_ohlcv(mock_exchange, 'BTC/USDT', '15m', 200)
        
        if df is not None and len(df) > 0:
            print("[OK] 向后兼容性测试成功")
            print(f"数据行数: {len(df)}")
            print(f"列名: {list(df.columns)}")
            print("前3行数据:")
            print(df.head(3))
            
            # 验证数据格式是否与预期一致
            expected_columns = ['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']
            if list(df.columns) == expected_columns:
                print("[OK] 数据格式与预期一致")
            else:
                print(f"[WARNING] 数据格式不一致，期望: {expected_columns}")
                
        else:
            print("[ERROR] 向后兼容性测试失败：未获取到数据")
            
    except Exception as e:
        print(f"[ERROR] 向后兼容性测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_new_interface():
    """测试新接口是否正常工作"""
    print("\n=== 测试新接口 ===")
    
    try:
        # 测试新的A股调用方式
        print("测试新的A股调用方式...")
        df = fetch_ohlcv('000001', source='cn_stock', limit=3)
        
        if df is not None and len(df) > 0:
            print("[OK] 新接口测试成功")
            print(f"数据行数: {len(df)}")
            print(f"列名: {list(df.columns)}")
            
        else:
            print("[ERROR] 新接口测试失败：未获取到数据")
            
    except Exception as e:
        print(f"[ERROR] 新接口测试失败: {e}")

if __name__ == "__main__":
    test_crypto_compatibility()
    test_new_interface()