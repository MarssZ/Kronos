#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试tushare基本功能，看是否需要token
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

import tushare as ts
import pandas as pd
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_tushare_basic():
    """测试tushare基本数据获取"""
    print("=== 测试tushare基本功能 ===")
    
    # 设置token
    token = os.getenv('TUSHARE_TOKEN')
    if token:
        ts.set_token(token)
        print(f"[OK] Token已设置: {token[:10]}...")
    else:
        print("[WARNING] 未找到TUSHARE_TOKEN")
    
    try:
        # 测试1: 使用Pro接口获取数据
        print("\n测试1: 使用Pro接口获取股票数据")
        pro = ts.pro_api()
        
        # 获取单只股票的历史数据
        df = pro.daily(ts_code='000001.SZ', start_date='20240101', end_date='20240110')
        
        if df is not None and len(df) > 0:
            print(f"[OK] 成功获取数据，共{len(df)}条记录")
            print("数据列:", list(df.columns))
            print("前3行数据:")
            print(df.head(3))
            return df
        else:
            print("[ERROR] 未获取到数据")
            
    except Exception as e:
        print(f"[ERROR] 获取数据失败: {e}")
        return None

def test_data_format():
    """测试数据格式"""
    print("\n=== 测试数据格式 ===")
    
    try:
        # 使用Pro接口获取股票基本信息用于格式分析
        pro = ts.pro_api()
        df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        
        if df is not None and len(df) > 0:
            print("原始数据格式:")
            print(f"索引名: {df.index.name}")
            print(f"索引类型: {type(df.index)}")  
            print(f"列名: {list(df.columns)}")
            print(f"数据形状: {df.shape}")
            print("\n原始数据:")
            print(df)
            
            # 模拟我们的normalize_data处理
            print("\n模拟数据标准化:")
            result = df.reset_index()
            print(f"reset_index后列名: {list(result.columns)}")
            print("标准化后前3行:")
            print(result.head(3))
            
        else:
            print("[ERROR] 未获取到测试数据")
            
    except Exception as e:
        print(f"[ERROR] 数据格式测试失败: {e}")

if __name__ == "__main__":
    test_tushare_basic()
    test_data_format()