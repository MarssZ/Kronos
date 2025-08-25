from model import Kronos, KronosTokenizer, KronosPredictor

# Load from local path
tokenizer = KronosTokenizer.from_pretrained("./NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("./NeoQuasar/Kronos-small")

# 验证加载是否成功
print(f"分词器类型: {type(tokenizer)}")
print(f"模型类型: {type(model)}")
print("模型加载完成！")