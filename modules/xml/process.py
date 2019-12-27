#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : porter_xml.py
# @Author: maofenghua
# @Date  : 2019/12/13

import string
import nltk
import os
import re
from xml.etree.ElementTree import parse, Element, SubElement, ElementTree
from nltk.corpus import stopwords,wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer


stopwordsdir = set(stopwords.words('english'))  


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


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def pre_process(text):
    #分词
    text=word_tokenize(text)
    #去停用词
    clean_words=[i for i in text if i not in stopwordsdir]
    #词性标注
    tagged_text=pos_tag(clean_words)
    #词形还原
    wnl = WordNetLemmatizer()
    lemma_text=[]
    for tag in tagged_text:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemma_text.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    str = ' '
    text=str.join(lemma_text)
    return text


    #text=word_tokenize(text)
    #clean_words=[i for i in text if i not in stopwordsdir]
    #tagged_text=pos_tag(clean_words)
    #wnl = WordNetLemmatizer()
    #lemma_text=[]
    #for tag in tagged_text:
        #wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        #lemma_text.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    #str = ' '
    #text=str.join(lemma_text)
if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.getcwd(), '../../collection'))
    root_store_pre = os.path.abspath(os.path.join(os.getcwd(), '../../collection_pre1'))  # 预处理之后存储路径

    mkdir(root_store_pre)

    root_cli = os.path.join(root, 'clinicaltrials_xml') #原始数据
    root_store_pre_cli = os.path.join(root_store_pre, 'clinicaltrials_xml')
    mkdir(root_store_pre_cli)

    root_cli_ls = os.listdir(root_cli)
    root_cli_ls.sort()
    for i in root_cli_ls:
        root_cli_1 = os.path.join(root_cli, i)#一级目录
        root_store_pre_cli_1 = os.path.join(root_store_pre_cli, i)
        mkdir(root_store_pre_cli_1)

        root_cli_1_ls = os.listdir(root_cli_1)
        root_cli_1_ls.sort()
        for j in root_cli_1_ls:#二级目录
            root_cli_2 = os.path.join(root_cli_1, j)
            root_store_pre_cli_2 = os.path.join(root_store_pre_cli_1, j)
            mkdir(root_store_pre_cli_2)

            root_cli_2_ls = os.listdir(root_cli_2)
            root_cli_2_ls.sort()
            for k in root_cli_2_ls:#二级目录下的xml文件
                root_cli_xml = os.path.join(root_cli_2, k)
                root_store_pre_cli_xml = os.path.join(root_store_pre_cli_2, k)

                xml = parse(root_cli_xml)
                DOC = Element('DOC')
                '''<nct_id>'''
                nct_id = xml.findtext('DOC')
                # print(nct_id)

                DOCNO = SubElement(DOC, 'DOCNO')
                DOCNO.text = nct_id

                '''brief_summary'''
                brief_summary = xml.findtext('brief_summary')
                # print(brief_summary)
                brief_summary_ = SubElement(DOC, 'brief_summary')
                brief_summary = deleteSpaceNewLine(brief_summary)
                brief_summary_.text = pre_process(brief_summary)

                '''brief_title'''
                brief_title = xml.findtext('brief_title')
                # print(brief_title)
                brief_title_ = SubElement(DOC, 'brief_title')
                brief_title = deleteSpaceNewLine(brief_title)
                brief_title = brief_title.replace('[','').replace(']','')
                brief_title_.text = pre_process(brief_title)

                '''detailed_description'''
                detailed_description = xml.findtext('detailed_description')
                # print(detailed_description)
                detailed_description_ = SubElement(DOC, 'detailed_description')
                detailed_description = deleteSpaceNewLine(detailed_description)
                detailed_description_.text = pre_process(str(detailed_description))

                '''mesh_term'''
                for mesh_term in xml.findall('mesh_term'):
                    # print(mesh_term.text)
                    mesh_term_ = SubElement(DOC, 'mesh_term')
                    mesh_term_.text = pre_process(mesh_term.text)


                '''criteria, gender, minimum_age, maximum_age'''
                criteria = xml.findtext('criteria')
                criteria_ = SubElement(DOC, 'criteria')
                criteria = deleteSpaceNewLine(criteria)
                criteria_.text = pre_process(str(criteria))

                gender = xml.findtext('gender')
                gender_ = SubElement(DOC, 'gender')
                gender_.text = gender

                minimum_age = xml.findtext('minimum_age')
                minimum_age_ = SubElement(DOC, 'minimum_age')
                minimum_age_.text = minimum_age

                maximum_age = xml.findtext('maximum_age')
                maximum_age_ = SubElement(DOC, 'maximum_age')
                maximum_age_.text = maximum_age

                '''verification_date'''
                verification_date = xml.findtext('verification_date')
                # print(verification_date)
                verification_date_ = SubElement(DOC, 'verification_date')
                verification_date_.text = verification_date

                '''keyword'''
                for keyword in xml.findall('keyword'):
                    # print(keyword.text)
                    keyword_ = SubElement(DOC, 'keyword')
                    keyword_.text = pre_process(keyword.text)

                tree = ElementTree(DOC)
                root = tree.getroot()  # 得到根元素，Element类
                prettyXml(root, '\t', '\n')  # 执行美化方法

                tree.write(root_store_pre_cli_xml, encoding='utf-8')
                # print(root_store_pre_cli_xml)
        print(root_store_pre_cli_1 + ' Pre-processing have Completed!')