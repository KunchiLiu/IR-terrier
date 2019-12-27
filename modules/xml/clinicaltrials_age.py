#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : clinicaltrials_xml.py
# @Author: liukunchi
# @Date  : 2019/12/11

import os
import pandas as pd
import re
from xml.etree.ElementTree import parse

# elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
def prettyXml(element, indent, newline, level = 0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    # 此处两行如果把注释去掉，Element的text也会另起一行
    #else:
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        # 对子元素进行递归操作
        prettyXml(subelement, indent, newline, level = level + 1)


def deleteSpaceNewLine(str):
    '''删除字符串换行符和首位空行'''
    if str is not None:
        str = str.strip()
        str = ' '.join(str.split())
    return str


def mkdir(path):
    '''若文件夹不存在，则创建'''
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.getcwd(), '../../collection'))
    root_store_pre = os.path.abspath(os.path.join(os.getcwd(), '../../collection_pre'))  # 预处理之后存储路径
    DOCNO_AgeInfo = []
    mkdir(root_store_pre)

    root_cli = os.path.join(root, 'clinicaltrials_xml')
    root_store_pre_cli = os.path.join(root_store_pre, 'clinicaltrials_AgeInfo.csv')

    root_cli_ls = os.listdir(root_cli)
    root_cli_ls.sort()
    for i in root_cli_ls:
        root_cli_1 = os.path.join(root_cli, i)

        root_cli_1_ls = os.listdir(root_cli_1)
        root_cli_1_ls.sort()
        for j in root_cli_1_ls:
            root_cli_2 = os.path.join(root_cli_1, j)

            root_cli_2_ls = os.listdir(root_cli_2)
            root_cli_2_ls.sort()
            for k in root_cli_2_ls:
                AgeInfo = []
                root_cli_xml = os.path.join(root_cli_2, k)

                xml = parse(root_cli_xml)
                '''<nct_id>'''
                nct_id = xml.findtext('id_info/nct_id')
                # print(nct_id)
                AgeInfo.extend([nct_id])

                '''criteria, gender, minimum_age, maximum_age'''
                for eligibility in xml.iterfind('eligibility'):


                    minimum_age = eligibility.findtext('minimum_age')
                    maximum_age = eligibility.findtext('maximum_age')
                    MinAge = re.findall(r"\d+\.?\d*",minimum_age)
                    MaxAge = re.findall(r"\d+\.?\d*",maximum_age)

                    if not MinAge:
                        AgeInfo.extend([0])
                    else:
                        AgeInfo.extend(MinAge)

                    if not MaxAge:
                        AgeInfo.extend([200])
                    else:
                        AgeInfo.extend(MaxAge)

                DOCNO_AgeInfo.append(AgeInfo)
        print(i + ' AgeInfo Pre-processing have Completed!')
    DOCNO_AgeInfo = pd.DataFrame(DOCNO_AgeInfo, columns=['DOCNO', 'minimum_age', 'maximum_age'])
    print(DOCNO_AgeInfo.shape)
    DOCNO_AgeInfo.to_csv(root_store_pre_cli,index=False)
