import os
import sys
import json
import you_get

def flatten_list(inlst:list) -> list:
    res = []
    def flatten_recur(sublst):
        for ele in sublst:
            if type(ele) == list:
                flatten_recur(ele)
            else:
                res.append(ele)

    for ele in inlst:
        if type(ele) == list:
            flatten_recur(ele)
        else:
            res.append(ele)
    return res



class YouGet(object):
    def __init__(self, Savepath):
        self.Savepath = Savepath
        self.url = None
        self.format_list_cmd = "you-get --json {} -s 127.0.0.1:1090"
        self.format_choose = None

    def set_url(self, url):
        self.url = url

    def format_list(self):
        r = os.popen(self.format_list_cmd.format(self.url))
        res = r.read()
        r.close()
        res = json.loads(res)

        title = res['title']
        print("--标题--", title)

        streams = res['streams']

        for k, v in streams.items():
            video_flg = k
            video_format = v['container']
            video_quality = v['quality']
            if "size" in v:
                video_size = int(v['size']) / 1024 / 1024
            else:
                video_size = None
            if "src" in v:
                video_src = flatten_list(v['src'])
            else:
                video_src = []
            print("视频标识：", video_flg)
            print("视频格式：", video_format)
            print("视频质量：", video_quality)
            print("视频大小：", video_size)
            print("视频路径：", video_src)

            print("--"*10)

        return res

if __name__ == '__main__':
    YouGet = YouGet("./")
    YouGet.set_url("https://www.youtube.com/watch?v=XyTcINLKq4c")
    YouGet.format_list()