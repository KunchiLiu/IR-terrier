#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : topics2018_XmlAndAge.py
# @Author: liukunchi
# @Date  : 2019/12/25

import os
import re
import pandas as pd
from xml.etree.ElementTree import parse, Element, SubElement, ElementTree

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
    mkdir(root_store_pre)

    root_topics = os.path.join(root, 'topics2018.xml')
    root_store_pre_xml = os.path.join(root_store_pre, 'topics2018.xml')
    root_topics_Age = os.path.join(root_store_pre, 'topics2018_Age.csv')


    xml = parse(root_topics)
    Topics_AgeInfo = []
    xml_all = []
    for i in xml.findall('topic'):
        AgeInfo = []
        TOPIC = Element('TOP')
        NUM = SubElement(TOPIC, 'NUM')
        NUM.text = (i.attrib)['number']
        AgeInfo.extend([NUM.text])

        disease = SubElement(TOPIC,'disease')
        disease.text = i.findtext('disease')

        gene = SubElement(TOPIC, 'gene')
        gene.text = i.findtext('gene')

        demographic = SubElement(TOPIC, 'demographic')
        demographic.text = i.findtext('demographic')
        Age = re.findall(r"\d+\.?\d*", demographic.text)

        if not Age:
            AgeInfo.extend([0])
        else:
            AgeInfo.extend(Age)
        Topics_AgeInfo.append(AgeInfo)

        tree = ElementTree(TOPIC)
        root = tree.getroot()  # 得到根元素，Element类

        prettyXml(root, '\t', '\n')  # 执行美化方法

        '''xml文件是树结构，为了达到一个xml文件里有多棵树，使用追加内容方法，但xml.write不支持追加，
        所以，定义一个字符串，每次生成一个xml文件，即追加到字符串里，最后在写进新的xml文件里'''


        tree.write(root_store_pre_xml, encoding='utf-8')
        with open(root_store_pre_xml,'r') as f:
            # print(f.readlines())
            ls = f.readlines()
            # print(ls)

            xml_all.extend(ls)
            xml_all.extend(['\n'])
            # print(xml_all)
    Topics_AgeInfo = pd.DataFrame(Topics_AgeInfo, columns=['TopicId', 'Age'])
    Topics_AgeInfo.to_csv(root_topics_Age, index=False)
    with open(root_store_pre_xml, 'w') as f:
        f.write(''.join(xml_all))




