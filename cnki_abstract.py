#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import requests
import json
from bs4 import BeautifulSoup
from lxml import etree
from xml.etree import ElementTree

#sj=1 dm=6
header = {'Authorization': ' Token 02d4a080ba052bcee03375cdc215fa0102bcbaf9'}
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getnode(ptext, paperid, parent=0):
    node = {
        "headline":ptext['name'] if 'name' in ptext else '',
        "parent": parent,
        "paper": paperid
    }
    jg = requests.post(url='http://39.100.48.36:3003/paper/content/', data=node, headers=header)
    if jg.status_code == 201:
        nd = json.loads(jg.text)
        for k in ptext['content']:
            if k[0] == 'p':
                paragraph = {
                                "paragraph_content": ptext['content'][k],
                                "paragraph_type": 1,
                                "content": nd['id']
                            }
                jg3=requests.post(url='http://39.100.48.36:3003/paper/paragraph/', data=paragraph, headers=header)
            elif k[0] == 'n':
                getnode(ptext['content'][k], paperid, nd['id'])

flag =False
import MySQLdb
def get_p():

    urls=[]
    db = MySQLdb.connect("localhost", "root", "1701sky", "ll", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * from ps")
    result = dictfetchall(cursor)
    return result

    pass

    pass##ctl00 > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > a

try:
    for i in get_p():
        paper = {
        "journal": i['Source'],
        "journal_tips": 'null',
        "paper_title": i['Title'],
        "paper_authors": i['Author'],
        "keywords": i['Keyword'],
        "subject": 1,
        "domain": 6,
        'filename':'null'
        }
        print(paper)

        if True:
            jg = requests.post(url='http://39.100.48.36:3003/paper/paper/', data=paper, headers=header)
            if jg.status_code == 201:

                paper = json.loads(jg.text)
                paperid = paper['id']
                print(paperid)
                node = {
                    "headline": '摘要',
                    "parent": 0,
                    "paper": paperid
                }
                jg = requests.post(url='http://39.100.48.36:3003/paper/content/', data=node, headers=header)
                nd = json.loads(jg.text)
                paragraph = {
                    "paragraph_content": i['Summary'],
                    "paragraph_type": 1,
                    "content": nd['id']
                }
                jg3 = requests.post(url='http://39.100.48.36:3003/paper/paragraph/', data=paragraph, headers=header)


except Exception :
    pass