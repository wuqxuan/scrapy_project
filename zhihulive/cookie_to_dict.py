
def string_to_dict(cookie):
    '''
    将从浏览器上Copy来的cookie字符串("Cookie:"后的一串)转化为Scrapy能使用的Dict
    :return:
    '''
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        values = item.split('=')
        value = ''
        # 处理有一个或者多个'='的情况
        for i in range(1, len(values)):
            value = value + values[i]
            cookie_dict[key] = value
    return cookie_dict

if __name__ == "__main__":
    cookie = 'cookie信息'
    print(string_to_dict(cookie))
