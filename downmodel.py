from model import Kronos, KronosTokenizer, KronosPredictor
import ccxt
import pandas as pd
from fetch_ohlcv import fetch_ohlcv

# Load from local path
tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")

# 验证加载是否成功
print(f"分词器类型: {type(tokenizer)}")
print(f"模型类型: {type(model)}")
print("模型加载完成！")

# Initialize the predictor
predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)

import pandas as pd

# Load your data
exchange = ccxt.okx({
    'proxies': {
        'http': 'http://localhost:1082',    # 别忘了本地把代理打开
        'https': 'http://localhost:1082',
    },
})

# 获取数据
df = fetch_ohlcv(exchange, 'BTC/USDT', '15m', 300)
# df = pd.read_csv("./data/XSHG_5min_600977.csv")
df['timestamps'] = pd.to_datetime(df['timestamps'])

# Define context window and prediction length
lookback = 300
pred_len = 220

# Prepare inputs for the predictor
x_df = df.loc[:lookback-1, ['open', 'high', 'low', 'close', 'volume']]
x_timestamp = df.loc[:lookback-1, 'timestamps']
y_timestamp = df.loc[lookback:lookback+pred_len-1, 'timestamps']

# Generate predictions
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp,
    y_timestamp=y_timestamp,
    pred_len=pred_len,
    T=1.0,          # Temperature for sampling
    top_p=0.9,      # Nucleus sampling probability
    sample_count=1  # Number of forecast paths to generate and average
)

print("Forecasted Data Head:")
print(pred_df.head())