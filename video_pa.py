import json

import requests

from mode.movie import Movie

if __name__ == '__main__':
    page = 9382
    pageCount = 9381
    while (page <= pageCount):
        data = requests.get('https://www.siwazyw.tv/api.php/provide/vod/at/json/?ac=detail&pg=' + str(page))
        videos = []
        if data.status_code == 200:
            data_json = data.json()
            pageCount = data_json['pagecount']
            vlist = data_json['list']
            for item in vlist:
                video = Movie()
                video.id = 0
                video.type = item['type_name']
                video.title = item['vod_name']
                video.span = item['type_name']
                video.create_time = item['vod_time_add']
                video.update_time = item['vod_time_add']
                video.play_count = 0
                video.address = item['vod_play_url']
                video.horizontal = None
                video.vertical = item['vod_pic']
                video.actor = None
                video.child_type = None
                video.director = None
                video.region = None
                video.year = None
                video.total_part = None
                video.details = item['vod_content']
                video.source = 'sw'
                videos.append(video.__dict__)
        with open('/Users/yi/project/old/project/pvideo/conf/vjs/v-' + str(page) + '.json', 'w') as f:
            f.write(json.dumps(videos))
        print("page" + str(page))
        page += 1