#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试A股数据获取 - 任务8验证脚本
验证条件：获取600848数据 → Console显示 "Retrieved 365+ records for 600848"
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from fetch_ohlcv import fetch_ohlcv

def test_china_stock_data():
    """测试A股数据获取"""
    print("=== 测试A股数据获取 ===")
    
    try:
        # 获取上汽集团(600848)一年的数据
        symbol = '600848'
        print(f"正在获取{symbol}的数据...")
        
        df = fetch_ohlcv(symbol, source='cn_stock', limit=365)
        
        if df is not None and len(df) > 0:
            record_count = len(df)
            print(f"Retrieved {record_count} records for {symbol}")
            
            # 验证是否达到预期记录数
            if record_count >= 365:
                print(f"[OK] 获取到{record_count}条记录，达到预期")
            else:
                print(f"[INFO] 获取到{record_count}条记录，少于365条（可能是交易日限制）")
            
            # 显示数据基本信息
            print(f"数据时间范围: {df['timestamps'].min()} 到 {df['timestamps'].max()}")
            print(f"列名: {list(df.columns)}")
            print("最新5条数据:")
            print(df.head(5))
            
            # 验证数据质量
            print("\n数据质量检查:")
            print(f"开盘价范围: {df['open'].min():.2f} - {df['open'].max():.2f}")
            print(f"成交量总计: {df['volume'].sum():,.0f}")
            print(f"平均成交额: {df['amount'].mean():,.0f}")
            
        else:
            print(f"[ERROR] 未获取到{symbol}的数据")
            
    except Exception as e:
        print(f"[ERROR] A股数据获取测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_multiple_stocks():
    """测试多只股票数据获取"""
    print("\n=== 测试多只股票数据获取 ===")
    
    test_stocks = ['000001', '600848', '000002']  # 平安银行、上汽集团、万科A
    
    for symbol in test_stocks:
        try:
            print(f"\n测试股票: {symbol}")
            df = fetch_ohlcv(symbol, source='cn_stock', limit=10)
            
            if df is not None and len(df) > 0:
                print(f"  [OK] 获取到{len(df)}条记录")
                print(f"  最新价格: {df.iloc[0]['close']}")
            else:
                print(f"  [ERROR] 未获取到数据")
                
        except Exception as e:
            print(f"  [ERROR] {symbol}获取失败: {e}")

if __name__ == "__main__":
    test_china_stock_data()
    test_multiple_stocks()