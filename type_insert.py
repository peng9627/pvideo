import json
if __name__ == '__main__':
    infile = open('/Users/pengyi/PycharmProjects/h5video/conf/hg.json')
    videos = json.load(infile)
    infile.close()
    for t in videos:
        for c in t["clsList"]:
            title = c["name"]
            pid = str(t["moduleId"])
            print "INSERT INTO video_type (title, pid) VALUES ('', " + pid + ")"
