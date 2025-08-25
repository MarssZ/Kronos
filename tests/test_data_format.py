#!/usr/bin/env python3
"""
测试数据格式标准化功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

import pandas as pd
from data_sources import ChinaStockAdapter

def test_data_normalization():
    """测试数据格式标准化"""
    print("=== 测试数据格式标准化 ===")
    
    # 创建模拟的tushare原始数据格式
    dates = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
    mock_tushare_data = pd.DataFrame({
        'open': [10.5, 11.0, 10.8],
        'high': [11.2, 11.5, 11.0], 
        'low': [10.2, 10.8, 10.5],
        'close': [11.0, 10.8, 10.9],
        'volume': [1000000, 1200000, 800000],
        'price_change': [0.5, -0.2, 0.1],
        'p_change': [4.76, -1.82, 0.93],
        'ma5': [10.8, 10.9, 10.85],
        'ma10': [10.7, 10.75, 10.8],
        'ma20': [10.6, 10.65, 10.7],
        'v_ma5': [1000000, 1100000, 1000000],
        'v_ma10': [950000, 1050000, 975000],
        'v_ma20': [900000, 1000000, 950000],
        'turnover': [2.5, 3.0, 2.0]
    }, index=dates)
    
    # 设置索引名为'date'，模拟tushare返回格式
    mock_tushare_data.index.name = 'date'
    
    # 创建适配器实例（模拟模式，跳过token检查）
    try:
        adapter = ChinaStockAdapter()
    except Exception:
        # 如果token检查失败，直接测试normalize_data方法
        adapter = object.__new__(ChinaStockAdapter)  # 绕过__init__
    
    # 测试数据标准化
    try:
        normalized_data = adapter.normalize_data(mock_tushare_data)
        
        print("数据标准化成功！")
        print(f"Columns: {list(normalized_data.columns)}")
        
        # 验证列名
        expected_columns = ['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']
        if list(normalized_data.columns) == expected_columns:
            print("✅ 列名验证通过")
        else:
            print(f"❌ 列名验证失败，期望: {expected_columns}, 实际: {list(normalized_data.columns)}")
        
        # 验证数据类型
        print(f"数据形状: {normalized_data.shape}")
        print("前3行数据:")
        print(normalized_data.head(3))
        
        # 验证amount列计算
        expected_amount = mock_tushare_data['volume'] * mock_tushare_data['close']
        if (normalized_data['amount'] == expected_amount.values).all():
            print("✅ amount列计算正确")
        else:
            print("❌ amount列计算错误")
            
    except Exception as e:
        print(f"数据标准化测试失败: {e}")

if __name__ == "__main__":
    test_data_normalization()