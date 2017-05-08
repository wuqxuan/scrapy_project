import requests
import json
import pymongo


class SendData():

    def send_message(self):
        """新榜"""
        url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle'
        headers = {'authorization': '9FF42ADA-F6A7-3624-0F60-31872533DD16',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
        # 小道消息
        # post_data = {
        #     'flag': 'true',
        #     'uuid': 'C1080392D32744FD45596A58F74C7D84',
        #     'nonce': 'e1a3ef0e3',
        #     'xyz': 'e8688cbd58780b18f9b172308eb39ab7'
        # }

        # 咪蒙
        post_data = {
            'flag': 'true',
            'uuid': '0E4AF33DCB6B9C8E4A207FFF716D590F',
            'nonce': 'f84a048fc',
            'xyz': '9b44348b89f1d04b50c91bb1881ab4d9'
        }
        response_message = requests.post(url, data=post_data, headers=headers)
        print(response_message.text)

if __name__ == "__main__":
    senddata = SendData()
    senddata.send_message()
