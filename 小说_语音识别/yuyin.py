from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '14975947'
API_KEY = 'X9f3qewzCohppMHxlunznUbi'
SECRET_KEY = 'LupWgIIFzZ9kTVNZSH5G0guNGZIqqTom'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#第一个参数是文本数据，第二个参数是语言，第三个参数是平台，第四个参数是声音
result  = client.synthesis('今天天气好好呀。棒棒的', 'zh', 1, {
    'vol': 5,   # 音量
    'spd': 2,   # 语速
    'pit': 9,   # 语调
    'per': 2    # 3 逍遥音  4 萝莉音
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
