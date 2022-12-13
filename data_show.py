import requests
from lxml import etree
import json, csv

import pandas as pd
from pyecharts.charts import Map, Page
from pyecharts import options as opts

def handle_data():
    # 爬虫抓取百度疫情数据
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
    }
    response = requests.get(url=url, headers=headers).text
    html = etree.HTML(response)
    json_text_array = html.xpath('//script[@type="application/json"]/text()')

    json_text = json_text_array[0]
    result = json.loads(json_text)
    # 控制生成json文件
    # filename = 'text.json'
    # with open(filename, 'w', encoding='utf8') as f_obj:
    #     json.dump(result, f_obj, ensure_ascii=False)

    result = result["component"]
    # # 数据提取
    province = result[0]['caseList']
    # summary_data = result[0]['summaryDataIn']

    rows_list = [["省份", "新增确诊", "现有确诊"]]
    for line in province:
        line_name = [line["area"], line["confirmedRelative"], line["curConfirm"]]
        for ele in line_name:
            if ele == '':
                ele = 0
        rows_list.append(line_name)
    # print(rows_list)

    with open('data.csv', 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerows(rows_list)

    filename = 'data.csv'
    return filename


def make_map(filename):
    # 整理图标数据集
    # 设置列对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    # 打开文件
    df = pd.read_csv(filename)
    # 对省份进行统计
    data2 = df['省份']
    data2_list = list(data2)
    data3 = df['新增确诊']
    data3_list = list(data3)
    data4 = df['现有确诊']
    data4_list = list(data4)

    # 制作图表
    a = (
        Map()
            .add("新增确诊", [list(z) for z in zip(data2_list, data3_list)], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(),
            visualmap_opts=opts.VisualMapOpts(max_=10000, ),
            )
    )

    b = (
        Map()
            .add("现有确诊", [list(z) for z in zip(data2_list, data4_list)], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(),
            visualmap_opts=opts.VisualMapOpts(max_=10000),
            )
    )

    page = Page(layout=Page.SimplePageLayout)
    page.add(a, b)
    # 生成render.html文件
    page.render()


def main():
    make_map(handle_data())
main()