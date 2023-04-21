from random import random
import random
import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render
from bs4 import BeautifulSoup
import json
from lxml import etree
import requests
import gopup
# Create your views here.
import time
import json
from datetime import datetime
from pyecharts import options as opts

from pyecharts.charts import Kline, Line, Pie


def ana_data(x):
    json_data = json.loads(x.split('{"result":')[1].split('});}catch(e)')[0])
    data = json_data['data']
    news = []
    for i in data:
        dt = datetime.fromtimestamp(int(i['ctime']))
        crtime = dt.strftime('%Y-%m-%d %H:%M:%S')
        news.append([i['title'], i['url'], crtime])
    df = pd.DataFrame(news, index=None, columns=['标题', '链接', '时间'])

    return df


def show(request):
    return render(request, 'base.html')


def zhihu(request):
    url = 'https://www.zhihu.com/billboard'

    cookies = {
        '_zap': '76b4e9fd-b0ed-4a96-b059-63f807f24d8b',
        'd_c0': 'AADXl3Jg_BWPTrMAaFM-UUNpwH0PbN7vpNc=|1670493969',
        'YD00517437729195%3AWM_TID': 'NSt%2BurD3NGdFVQRUEVfBJb8TD0sam4vN',
        'q_c1': 'e055019b89944fd8acf564f8f16af136|1674959144000|1674959144000',
        '_xsrf': '4YTakvU4KKJVuAMLZ1E7ZugFgJKPCjCH',
        'YD00517437729195%3AWM_NI': 'Fm6qWuLc03S4tG7zf0ud1iiQpXKIdUUu%2FUcQfce%2Fo2CwF3UIgrQc%2BuLSMBMtZcuZ2rzEZNiVRrqJr%2FY7CcpZWbOI9gDYpP7z4N%2B1xNKCIbUu3FCRLJvXe9lNmfTwTuODWFA%3D',
        'YD00517437729195%3AWM_NIKE': '9ca17ae2e6ffcda170e2e6eed1b5698cb08391c45286868ba6c55f939f8fadd141a2ee9891ae25b6b08ed2c82af0fea7c3b92a86b3fa92d67f90bd00d4d240b899f99be53cb7bcff8aec5bb48885aae75f97abe1b6e25ba6bdabd0ee3a81a98ad4d843a5ae9f84aa7f908d83a3d0809abdbbbbb17aba9b96afec5e92aebfabf1259be98d84f35295be81aabc6d8887c0b1b672f892e5d2fb46899d8783d87ff19a8db3cf42b688abdaef46afba9c98d77f8d9c99a7c437e2a3',
        '__snaker__id': 'qULnlEdI96tpChGj',
        'z_c0': '2|1:0|10:1680240226|4:z_c0|80:MS4xaVJnZUVBQUFBQUFtQUFBQVlBSlZUWS1HRTJXbUZMZjBILUxQLU5saDlBMlRCZjJWNVdkdzJnPT0=|c5155fa1b8c4dbc0518a2edfba0eb5e3661437bd4a5a3c4713598e0be04e6a09',
        'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1680852198,1681717848,1681739632,1681781883',
        'tst': 'f',
        'SESSIONID': 'vQ2iOuaGjaxdKrc8758fiQXNTV7sFfw1UtWGyFiKpks',
        'JOID': 'VlATBUKY1AHI7_vDM5o1232VmT4k4oszrq2CrHT_uXesq4SsBfE8Ma7u-c08WXQ73JxABbBW6f53u48ho6B5H10=',
        'osd': 'VF0WC02a2QTG4PnONpQ62XCQlzEm7449oa-PqXrwu3qppYuuCPQyPqzj_MMzW3k-0pNCCLVY5vx6voEuoa18EVI=',
        'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1681909394',
        'KLBRSID': 'fe78dd346df712f9c4f126150949b853|1681909394|1681909352',
    }

    headers = {
        'authority': 'www.zhihu.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_zap=76b4e9fd-b0ed-4a96-b059-63f807f24d8b; d_c0=AADXl3Jg_BWPTrMAaFM-UUNpwH0PbN7vpNc=|1670493969; YD00517437729195%3AWM_TID=NSt%2BurD3NGdFVQRUEVfBJb8TD0sam4vN; q_c1=e055019b89944fd8acf564f8f16af136|1674959144000|1674959144000; _xsrf=4YTakvU4KKJVuAMLZ1E7ZugFgJKPCjCH; YD00517437729195%3AWM_NI=Fm6qWuLc03S4tG7zf0ud1iiQpXKIdUUu%2FUcQfce%2Fo2CwF3UIgrQc%2BuLSMBMtZcuZ2rzEZNiVRrqJr%2FY7CcpZWbOI9gDYpP7z4N%2B1xNKCIbUu3FCRLJvXe9lNmfTwTuODWFA%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed1b5698cb08391c45286868ba6c55f939f8fadd141a2ee9891ae25b6b08ed2c82af0fea7c3b92a86b3fa92d67f90bd00d4d240b899f99be53cb7bcff8aec5bb48885aae75f97abe1b6e25ba6bdabd0ee3a81a98ad4d843a5ae9f84aa7f908d83a3d0809abdbbbbb17aba9b96afec5e92aebfabf1259be98d84f35295be81aabc6d8887c0b1b672f892e5d2fb46899d8783d87ff19a8db3cf42b688abdaef46afba9c98d77f8d9c99a7c437e2a3; __snaker__id=qULnlEdI96tpChGj; z_c0=2|1:0|10:1680240226|4:z_c0|80:MS4xaVJnZUVBQUFBQUFtQUFBQVlBSlZUWS1HRTJXbUZMZjBILUxQLU5saDlBMlRCZjJWNVdkdzJnPT0=|c5155fa1b8c4dbc0518a2edfba0eb5e3661437bd4a5a3c4713598e0be04e6a09; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1680852198,1681717848,1681739632,1681781883; tst=f; SESSIONID=vQ2iOuaGjaxdKrc8758fiQXNTV7sFfw1UtWGyFiKpks; JOID=VlATBUKY1AHI7_vDM5o1232VmT4k4oszrq2CrHT_uXesq4SsBfE8Ma7u-c08WXQ73JxABbBW6f53u48ho6B5H10=; osd=VF0WC02a2QTG4PnONpQ62XCQlzEm7449oa-PqXrwu3qppYuuCPQyPqzj_MMzW3k-0pNCCLVY5vx6voEuoa18EVI=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1681909394; KLBRSID=fe78dd346df712f9c4f126150949b853|1681909394|1681909352',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.zhihu.com/billboard', cookies=cookies, headers=headers)

    html = etree.HTML(response.text)

    script = html.xpath('//script[@id="js-initialData"]/text()')[0]
    items = json.loads(script)['initialState']['topstory']['hotList']

    zhihu_hot = []
    for item in items:
        zhihu_hot.append([
            item['target']['titleArea']['text'],
            item['target']['link']['url'],
            item['target']['metricsArea']['text']])

    df = pd.DataFrame(zhihu_hot, index=None, columns=['标题', '链接', '热度'])

    return render(request, "zhihu.html", {'result': df})


def baidu(request):
    url = 'https://top.baidu.com/board?tab=realtime'

    baidu_hot = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    for i in soup.find(class_='rel container_2VTvm').find(class_='container right-container_2EFJr').findAll(
            class_='category-wrap_iQLoo horizontal_1eKyQ'):
        hot = str(f'{int(i.find(class_="hot-index_1Bl1a").text) / 10000 :.2f}') + "万热度"
        tittle = i.find(class_="c-single-text-ellipsis").text
        url = i.find(class_="img-wrapper_29V76")['href']
        baidu_hot.append([tittle.strip(), url.strip(), hot.strip()])
    df = pd.DataFrame(baidu_hot, index=None, columns=['标题', '链接', '热度'])
    return render(request, "baidu.html", {'result': df})


def weibo(request):
    url = 'https://s.weibo.com/top/summary'

    BASE_URL = 'https://s.weibo.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Cookie': 'SUB=_2AkMVWDYUf8NxqwJRmP0Sz2_hZYt2zw_EieKjBMfPJRMxHRl-yj9jqkBStRB6PtgY-38i0AF7nDAv8HdY1ZwT3Rv8B5e5; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFencmWZyNhNlrzI6f0SiqP'
    }
    response = requests.get(url, headers=headers)
    if response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding if response.apparent_encoding != 'ISO-8859-1' else 'utf-8'
    html = etree.HTML(response.text)

    titles = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/text()')
    hrefs = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/@href')
    hots = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/../span/text()')
    titles = [title.strip() for title in titles]
    hrefs = [BASE_URL + href.strip() for href in hrefs]
    hots = [str(round(int(hot.strip().split(' ')[-1]) / 10000, 2)) + "万热度"
            for hot in hots]
    weibo_hot = []
    for i, title in enumerate(titles):
        weibo_hot.append([title, hrefs[i], hots[i]])
    df = pd.DataFrame(weibo_hot, index=None, columns=['标题', '链接', '热度'])

    return render(request, "weibo.html", {'result': df})


def toutiao(request):
    url = 'https://is-lq.snssdk.com/api/suggest_words/?business_id=10016'
    response = requests.get(url)
    toutiao_hot = []
    for i in json.loads(response.text)['data'][0]['words']:
        toutiao_hot.append(
            [i['word'], f"https://so.toutiao.com/search?keyword={i['word']}",
             str(round(int(i['params']['fake_click_cnt']) / 10000, 2)) + "万热度"])
    df = pd.DataFrame(toutiao_hot, index=None, columns=['标题', '链接', '热度'])

    return render(request, "toutiao.html", {'result': df})


def douyin(request):
    url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/'

    HEADERS = {
        'user-agent': 'okhttp3'
    }
    response = requests.get(url, headers=HEADERS)
    douyin_hot = []

    for i in json.loads(response.text)['data']['word_list']:
        douyin_hot.append([i['word'], f"https://www.douyin.com/search/{i['word']}",
                           str(round(int(i['hot_value']) / 10000, 2)) + "万热度"])
    df = pd.DataFrame(douyin_hot, index=None, columns=['标题', '链接', '热度'])

    return render(request, "douyin.html", {'result': df})


def news(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2509',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)

    df = ana_data(response.text)

    return render(request, "news.html", {'result': df, 'page_obj': page_obj})


def keji(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '372',
        'lid': '2431',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "keji.html", {'result': df, 'page_obj': page_obj})


def guoji(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2511',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "guoji.html", {'result': df, 'page_obj': page_obj})


def caijin(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2516',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "caijin.html", {'result': df, 'page_obj': page_obj})


def shehui(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2669',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "shehui.html", {'result': df, 'page_obj': page_obj})


def junshi(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2514',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "junshi.html", {'result': df, 'page_obj': page_obj})


def yule(request):
    data = [i for i in range(1, 51)]
    paginator = Paginator(data, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    timestamp = int(time.time() * 1000)
    num = random.random()
    headers = {
        'authority': 'feed.mix.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://tech.sina.com.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'pageid': '153',
        'lid': '2513',
        'k': '',
        'num': '50',
        'page': f'{page_number}',
        'r': f'{num}',
        'callback': f'jQuery111207237837844315576_{timestamp}',
        '_': f'{timestamp}',
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    df = ana_data(response.text)

    return render(request, "yule.html", {'result': df, 'page_obj': page_obj})


def tiyu(request):
    df = pd.DataFrame()
    for id in [572, 571, 575, 255, 588, 255, 576, 583]:
        data = [i for i in range(1, 51)]
        paginator = Paginator(data, 1)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        timestamp = int(time.time() * 1000)
        num = random.random()
        headers = {
            'authority': 'feed.mix.sina.com.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://tech.sina.com.cn/',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

        params = {
            'pageid': '13',
            'lid': f'{id}',
            'k': '',
            'num': '50',
            'page': f'{page_number}',
            'r': f'{num}',
            'callback': f'jQuery111207237837844315576_{timestamp}',
            '_': f'{timestamp}',
        }

        response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
        all = ana_data(response.text)
        df = pd.concat([df, all], axis=0)
    df = df.sort_values(by="时间", ascending=[False]).drop_duplicates()

    return render(request, "tiyu.html", {'result': df, 'page_obj': page_obj})


def drawyule(request):
    df = gopup.weibo_index('娱乐', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("娱乐", [int(df.娱乐[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="娱乐话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html,
    }

    return render(request, 'yuledraw.html', context)


def drawguoji(request):
    df = gopup.weibo_index('国际', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("国际", [int(df.国际[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="国际话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html,
    }

    return render(request, 'guojidraw.html', context)


def drawtiyu(request):
    df = gopup.weibo_index('体育', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("体育", [int(df.体育[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="体育话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html,
    }

    return render(request, 'tiyudraw.html', context)


def drawkeji(request):
    df = gopup.weibo_index('科技', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("科技", [int(df.科技[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="科技话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})
    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html,
    }

    return render(request, 'kejidraw.html', context)


def drawcaijin(request):
    df = gopup.weibo_index('财经', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("财经", [int(df.财经[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="财经话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html,
    }

    return render(request, 'caijindraw.html', context)


def drawshehui(request):
    df = gopup.weibo_index('社会', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("社会", [int(df.社会[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="社会话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html
    }

    return render(request, 'shehuidraw.html', context)


def drawjunshi(request):
    df = gopup.weibo_index('军事', '1month')
    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df.index.tolist()])
    close_line.add_yaxis("军事", [int(df.军事[i]) for i in range(len(df))])
    close_line.set_global_opts(
        title_opts=opts.TitleOpts(title="军事话题时间线"),
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})

    )
    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    close_line_html = close_line.render_embed()

    context = {
        'close_line_html': close_line_html
    }

    return render(request, 'junshidraw.html', context)


def home(request):
    dt = datetime.fromtimestamp(int(time.time()) - 3600 * 24)
    crtime = dt.strftime('%Y-%m-%d')
    df1 = gopup.weibo_index('娱乐', '3month')
    df2 = gopup.weibo_index('国际', '3month')
    df3 = gopup.weibo_index('体育', '3month')
    df4 = gopup.weibo_index('科技', '3month')
    df5 = gopup.weibo_index('财经', '3month')
    df6 = gopup.weibo_index('社会', '3month')
    df7 = gopup.weibo_index('军事', '3month')

    data = [
        int(df1.娱乐[-1]),
        int(df2.国际[-1]),
        int(df3.体育[-1]),
        int(df4.科技[-1]),
        int(df5.财经[-1]),
        int(df6.社会[-1]),
        int(df7.军事[-1])]

    index = ['娱乐',
             '国际',
             '体育',
             '科技',
             '财经',
             '社会',
             '军事']

    pie = Pie(init_opts=opts.InitOpts(width="100%")).set_global_opts(
        title_opts=opts.TitleOpts(title=f"{crtime}日新闻话题分布", pos_left="2%"),  # 图的标题
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),  # 图例的位置
    )

    pie.add("", [x for x in zip(index, data)], label_opts=opts.LabelOpts(
        position="outside",
        formatter="{b}:{d}%",
    ))
    pie_html = pie.render_embed()

    close_line = Line(init_opts=opts.InitOpts(width="100%"))
    close_line.add_xaxis([i.strftime('%Y-%m-%d') for i in df1.index.tolist()])
    close_line.add_yaxis("娱乐", [int(df1.娱乐[i]) for i in range(len(df1))])
    close_line.add_yaxis("国际", [int(df2.国际[i]) for i in range(len(df2))])
    close_line.add_yaxis("体育", [int(df3.体育[i]) for i in range(len(df3))])
    close_line.add_yaxis("科技", [int(df4.科技[i]) for i in range(len(df4))])
    close_line.add_yaxis("财经", [int(df5.财经[i]) for i in range(len(df5))])
    close_line.add_yaxis("社会", [int(df6.社会[i]) for i in range(len(df6))])
    close_line.add_yaxis("军事", [int(df7.军事[i]) for i in range(len(df7))])

    close_line.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                               xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50})
                               )

    close_line_html = close_line.render_embed()

    context = {
        'pie_html': pie_html,
        'close_line_html': close_line_html

    }

    return render(request, 'home.html', context)
