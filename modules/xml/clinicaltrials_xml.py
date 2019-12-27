#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : clinicaltrials_xml.py
# @Author: liukunchi
# @Date  : 2019/12/11

import os
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
    root_store_pre = os.path.abspath(os.path.join(os.getcwd(), '../../collection_pre'))     # 预处理之后存储路径

    mkdir(root_store_pre)

    root_cli = os.path.join(root, 'clinicaltrials_xml')
    root_store_pre_cli = os.path.join(root_store_pre, 'clinicaltrials_xml')
    mkdir(root_store_pre_cli)

    root_cli_ls = os.listdir(root_cli)
    root_cli_ls.sort()
    for i in root_cli_ls:
        root_cli_1 = os.path.join(root_cli, i)
        root_store_pre_cli_1 = os.path.join(root_store_pre_cli, i)
        mkdir(root_store_pre_cli_1)

        root_cli_1_ls = os.listdir(root_cli_1)
        root_cli_1_ls.sort()
        for j in root_cli_1_ls:
            root_cli_2 = os.path.join(root_cli_1, j)
            root_store_pre_cli_2 = os.path.join(root_store_pre_cli_1, j)
            mkdir(root_store_pre_cli_2)

            root_cli_2_ls = os.listdir(root_cli_2)
            root_cli_2_ls.sort()
            for k in root_cli_2_ls:
                root_cli_xml = os.path.join(root_cli_2, k)
                root_store_pre_cli_xml = os.path.join(root_store_pre_cli_2, k)

                xml = parse(root_cli_xml)
                DOC = Element('DOC')
                '''<nct_id>'''
                nct_id = xml.findtext('id_info/nct_id')
                # print(nct_id)

                DOCNO = SubElement(DOC, 'DOC')
                DOCNO.text = nct_id

                '''brief_summary'''
                brief_summary = xml.findtext('brief_summary/textblock')
                # print(brief_summary)
                brief_summary_ = SubElement(DOC, 'brief_summary')
                brief_summary_.text = deleteSpaceNewLine(brief_summary)

                '''brief_title'''
                brief_title = xml.findtext('brief_title')
                # print(brief_title)
                brief_title_ = SubElement(DOC, 'brief_title')
                brief_title_.text = brief_title

                '''detailed_description'''
                detailed_description = xml.findtext('detailed_description/textblock')
                # print(detailed_description)
                detailed_description_ = SubElement(DOC, 'detailed_description')
                detailed_description_.text = deleteSpaceNewLine(detailed_description)

                '''mesh_term'''
                for mesh_term in xml.findall('condition_browse/mesh_term'):
                    # print(mesh_term.text)
                    mesh_term_ = SubElement(DOC, 'mesh_term')
                    mesh_term_.text = mesh_term.text

                for mesh_term in xml.findall('intervention_browse/mesh_term'):
                    # print(mesh_term.text)
                    mesh_term_ = SubElement(DOC, 'mesh_term')
                    mesh_term_.text = mesh_term.text

                '''criteria, gender, minimum_age, maximum_age'''
                for eligibility in xml.iterfind('eligibility'):
                    criteria = eligibility.findtext('criteria/textblock')
                    # criteria.replace(['Inclusion Criteria:','Exclusion Criteria:', '-'],'')
                    for i in ['Inclusion Criteria:', 'Exclusion Criteria:', '-']:
                        if criteria is not None:
                            criteria = criteria.replace(i, '')
                    criteria = deleteSpaceNewLine(criteria)
                    gender = eligibility.findtext('gender')
                    minimum_age = eligibility.findtext('minimum_age')
                    maximum_age = eligibility.findtext('maximum_age')

                    # print(criteria)
                    # print(gender)
                    # print(minimum_age)
                    # print(maximum_age)

                    criteria_ = SubElement(DOC, 'criteria')
                    criteria_.text = criteria

                    gender_ = SubElement(DOC, 'gender')
                    gender_.text = gender

                    minimum_age_ = SubElement(DOC, 'minimum_age')
                    minimum_age_.text = minimum_age

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
                    keyword_.text = keyword.text

                tree = ElementTree(DOC)
                root = tree.getroot()  # 得到根元素，Element类
                prettyXml(root, '\t', '\n')  # 执行美化方法

                tree.write(root_store_pre_cli_xml, encoding='utf-8')
                # print(root_store_pre_cli_xml)
        print(root_store_pre_cli_1 + ' Pre-processing have Completed!')


