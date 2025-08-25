#!/usr/bin/env python3
"""
测试fetch_ohlcv集成接口
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from fetch_ohlcv import fetch_ohlcv

def test_integration():
    """测试集成接口"""
    print("=== 测试fetch_ohlcv集成接口 ===")
    
    # 测试A股数据获取
    print("\n测试A股数据获取:")
    try:
        df = fetch_ohlcv('600848', source='cn_stock', limit=10)
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取A股数据，共{len(df)}条记录")
            print(f"列名: {list(df.columns)}")
            print(f"数据形状: {df.shape}")
            print("前3行数据:")
            print(df.head(3))
            
            # 验证6列数据
            if len(df.columns) == 6:
                print("✅ DataFrame包含6列数据")
            else:
                print(f"❌ DataFrame列数不正确，期望6列，实际{len(df.columns)}列")
                
        else:
            print("❌ 未获取到A股数据")
            
    except Exception as e:
        print(f"❌ A股数据获取失败: {e}")

if __name__ == "__main__":
    test_integration()