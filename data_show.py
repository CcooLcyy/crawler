from email.utils import format_datetime
from numpy import true_divide
import requests
from lxml import etree
import json, csv

import pandas as pd
from pyecharts.charts import Map, Page
from pyecharts import options as opts

class Create_data():
    def __init__(self, url):
        self.__url = url
        self.__province = None
        self.__summary = None

    def __get_data_by_array(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
        }
        response = requests.get(url=self.__url, headers=headers).text
        html = etree.HTML(response)
        json_text_array = html.xpath('//script[@type="application/json"]/text()')
        return json_text_array
    
    def __handle_data(self):
        json_test = self.__get_data_by_array()[0]
        result = json.loads(json_test)
        # 将数据进一步提纯
        result = result['component']
        self.__province = result[0]['caseList']
        self.__summary = result[0]['summaryDataIn']

    def format_data(self):
        self.__handle_data()
        province_rows_list = [["省份", "新增确诊", "现有确诊"]]
        for line in self.__province:
            line_name = [line["area"], line["confirmedRelative"], line["curConfirm"]]
            for ele in line_name:
                if ele == '':
                    ele = 0
            province_rows_list.append(line_name)
        return province_rows_list

    def csv(self, province=False):
        if(province == True):
            data = self.format_data()
            FILENAME = 'data.csv'
            with open(FILENAME, 'w', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        # elif(summary == True):

    # @property
    # def json(self):
    #     FILENAME = 'data.json'
    #     with open(FILENAME, 'w', encoding='utf8') as file:
    #         json.dumps(json_data, file, ensure_ascii=False)



data = Create_data('https://voice.baidu.com/act/newpneumonia/newpneumonia')
data.csv(province=True)


exit()


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