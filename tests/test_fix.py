#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的时间戳处理
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from fetch_ohlcv import fetch_ohlcv
import pandas as pd

def test_timestamp_fix():
    """测试时间戳处理修复"""
    print("=== 测试时间戳处理修复 ===")
    
    # 获取A股数据
    df = fetch_ohlcv('600848', source='cn_stock', limit=3)
    
    print(f"原始timestamps类型: {df['timestamps'].dtype}")
    print("原始数据:")
    print(df[['timestamps', 'open', 'high', 'low', 'close']].head(3))
    
    # 模拟predict.py中的处理逻辑
    if df['timestamps'].dtype == 'int64':  # 毫秒时间戳
        df['timestamps'] = pd.to_datetime(df['timestamps'], unit='ms')
        print("进行了毫秒转换")
    else:
        print("timestamps已经是datetime类型，无需转换")
    
    print("\n处理后数据:")
    print(df[['timestamps', 'open', 'high', 'low', 'close']].head(3))

if __name__ == "__main__":
    test_timestamp_fix()