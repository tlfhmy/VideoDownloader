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

class VideoInfo(object):
    def __init__(self, video_info_dict: dict):
        self.title = ""
        self.flag = ""
        self.quality = ""
        self.size = ""
        self.container = ""
        self.src = []
        self.extrac_infor(video_info_dict)

    def extrac_infor(self, video_info_dict):
        self.title = video_info_dict['title']
        self.flag = video_info_dict['flag']
        self.quality = video_info_dict['quality']
        self.size = video_info_dict['size']
        self.src = video_info_dict['src']
        self.container = video_info_dict['container']

    def __str__(self):
        res = ""
        res += f"视频标题：{self.title}\n"
        res += f"视频标识：{self.flag}\n"
        res += f"视频格式：{self.container}\n"
        res += f"视频质量：{self.quality}\n"
        res += f"视频大小：{self.size}\n"
        return res

    def __repr__(self):
        return self.__str__()



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

        streams = res['streams']

        res = []

        for k, v in streams.items():
            try:
                video_info_dict = {}
                video_info_dict['title'] = title
                video_info_dict['flag'] = k
                video_info_dict['container'] = v['container']
                video_info_dict['quality'] = v['quality']
                video_info_dict['size'] = '%5.2fMB'%(int(v['size']) / 1024 / 1024)
                video_info_dict['src'] = flatten_list(v['src'])

                res.append(VideoInfo(video_info_dict))

            except:
                pass

        return res

if __name__ == '__main__':
    YouGet = YouGet("./")
    YouGet.set_url("https://www.youtube.com/watch?v=XyTcINLKq4c")
    for ele in YouGet.format_list():
        print(ele)
