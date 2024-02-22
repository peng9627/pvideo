import requests

if __name__ == '__main__':
    res = requests.get('http://127.0.0.1:5555/play_movie/11')
    print(res.text)