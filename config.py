# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认40次/20分钟
READ_NUM = int(os.getenv('READ_NUM') or 40)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'RK': 'oxEY1bTnXf',
    'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
    'pac_uid': '0_e63870bcecc18',
    'iip': '0',
    '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FeEOpSbFh2Mb1bUxMW9Y3FRPfXwWvOLaNlsjWIkcKeeNg6vlVS5kOVuhNKGQ1M8zaggLqMPmpE5qIUdqEXlQgYg%2F132',
    'wr_gender': '0',
    'wr_vid': '22196951',
    'wr_rt': 'web%40ANf9SvhELX9dkJH4wZa_AL',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=dev-1730698697208,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=1ff5a0725f8841088b42f97109c45862',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}


# 书籍
book = [
    "a57325c05c8ed3a57224187","d1c327c0813ab7f74g0152cd","f1232e60813ab9d3fg01378c","f5c32c10813ab9bacg011aa0",
    "10e32ff0813ab9c72g019371","9ea32e40813ab7586g017390","56d32f30813ab9bfdg0197f2","6fb326d071ff64ed6fb0787",
    "6f232b50813ab6ec4g01944d","09d32580727cf78909db8a0","3c032020813ab89efg012c17","f7132830813ab9bc8g016f14"
]

# 章节
chapter = [
    "ecc32f3013eccbc87e4b62e","a87322c014a87ff679a21ea","e4d32d5015e4da3b7fbb1fa","16732dc0161679091c5aeb1",
    "8f132430178f14e45fce0f7","c9f326d018c9f0f895fb5e4","45c322601945c48cce2e120","d3d322001ad3d9446802347",
    "65132ca01b6512bd43d90e3","c20321001cc20ad4d76f5ae","c51323901dc51ce410c121b","aab325601eaab3238922e53",
    "9bf32f301f9bf31c7ff0a60","c7432af0210c74d97b01b1c","70e32fb021170efdf2eca12","6f4322302126f4922f45dec"
]

"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data = {
    'appId': 'wb182564874663h1004883397',
    'b': 'a57325c05c8ed3a57224187',
    'c': '8f132430178f14e45fce0f7',
    'ci': 7,
    'co': 338,
    'sm': '第5章就从这里起步至正十二年(1352)',
    'pr': 0,
    'rt': 5,
    'ts': 1748572606118,
    'rn': 467,
    'sg': '15c1dd66ca1dbffa73062ec12794e694dd05d6b11526fdafc86ebba49d05f8b3',
    'ct': 1748572606,
    'ps': '008321507a6c1c27g016e58',
    'pc': '513328c07a6c1c28g015582',
    's': '73deead2'
}


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
