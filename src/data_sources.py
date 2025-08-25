import pandas as pd
from typing import Optional
import tushare as ts
import os
from pathlib import Path


class DataSourceError(Exception):
    """数据源基础异常"""
    pass


class ConfigurationError(DataSourceError):
    """配置错误异常"""
    pass


class NetworkError(DataSourceError):
    """网络请求异常"""
    pass


class DataFormatError(DataSourceError):
    """数据格式异常"""
    pass


class ChinaStockAdapter:
    """A股数据适配器"""
    
    def __init__(self):
        self._setup_token()
        self.pro = ts.pro_api()
    
    def _setup_token(self):
        """设置tushare token"""
        # 从.env文件读取token
        env_file = Path(__file__).parent.parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('TUSHARE_TOKEN='):
                        token = line.strip().split('=')[1]
                        ts.set_token(token)
                        return
        
        raise ConfigurationError("未找到tushare token配置，请在.env文件中设置TUSHARE_TOKEN")
    
    def fetch_data(self, symbol: str, timeframe: str = '1d', limit: int = 700) -> pd.DataFrame:
        """
        获取A股数据
        
        Args:
            symbol: 股票代码 (如: '600848')
            timeframe: 时间周期 (暂时只支持 '1d')
            limit: 数据条数
            
        Returns:
            标准化的DataFrame
        """
        try:
            # 目前先实现日线数据获取
            if timeframe != '1d':
                raise ValueError(f"暂不支持的时间周期: {timeframe}")
            
            # 处理股票代码格式：添加.SH或.SZ后缀
            if '.' not in symbol:
                if symbol.startswith('6'):
                    ts_symbol = f"{symbol}.SH"  # 沪市
                elif symbol.startswith(('0', '3')):
                    ts_symbol = f"{symbol}.SZ"  # 深市
                else:
                    ts_symbol = f"{symbol}.SH"  # 默认沪市
            else:
                ts_symbol = symbol
                
            # 使用tushare pro API获取日线数据
            df = self.pro.daily(ts_code=ts_symbol, limit=limit)
            
            if df is None or len(df) == 0:
                return pd.DataFrame()
            
            return self.normalize_data(df)
            
        except Exception as e:
            raise NetworkError(f"获取A股数据失败: {str(e)}")
    
    def normalize_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        将tushare pro数据格式化为标准格式
        
        Tushare Pro字段: ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount
        标准格式: timestamps, open, high, low, close, volume, amount
        """
        try:
            if raw_data.empty:
                return pd.DataFrame(columns=['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount'])
            
            # 字段映射和选择
            result = pd.DataFrame({
                'timestamps': pd.to_datetime(raw_data['trade_date']),
                'open': raw_data['open'],
                'high': raw_data['high'], 
                'low': raw_data['low'],
                'close': raw_data['close'],
                'volume': raw_data['vol'],  # tushare pro中vol是成交量
                'amount': raw_data['amount']  # tushare pro中amount是成交额
            })
            
            # 按时间排序(从旧到新)
            result = result.sort_values('timestamps')
            
            return result
            
        except Exception as e:
            raise DataFormatError(f"数据格式转换失败: {str(e)}")


class DataSourceManager:
    """数据源管理器 - 统一不同数据源的访问接口"""
    
    def __init__(self):
        self.adapters = {}
    
    def get_data(self, symbol: str, source: str, timeframe: str = '1d', limit: int = 700) -> pd.DataFrame:
        """
        获取数据的统一接口
        
        Args:
            symbol: 标的代码
            source: 数据源类型 ('crypto', 'cn_stock')
            timeframe: 时间周期
            limit: 数据条数
            
        Returns:
            标准化的DataFrame
        """
        if source not in self.adapters:
            raise ValueError(f"不支持的数据源: {source}")
        
        adapter = self.adapters[source]
        return adapter.fetch_data(symbol, timeframe, limit)
    
    def register_adapter(self, source: str, adapter):
        """注册数据源适配器"""
        self.adapters[source] = adapter


# 全局实例和适配器注册
data_manager = DataSourceManager()

# 注册A股适配器
try:
    china_adapter = ChinaStockAdapter()
    data_manager.register_adapter('cn_stock', china_adapter)
    print("A股数据适配器注册成功")
except Exception as e:
    print(f"A股数据适配器注册失败: {e}")