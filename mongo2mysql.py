#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import requests
import json

header = {'Authorization': ' Token 000be7c07d7b07e1fbe7b3e96e696bf5c81ffc63'}
client = pymongo.MongoClient('202.202.5.140')
collection = client['cnki_papers']
db = collection['paper_detail_better_test2']


def getnode(ptext, paperid, parent=0):
    node = {
        "headline":ptext['name'] if 'name' in ptext else '',
        "parent": parent,
        "paper": paperid
    }
    jg = requests.post(url='http://127.0.0.1/paper/content/', data=node, headers=header)
    if jg.status_code == 201:
        nd = json.loads(jg.text)
        for k in ptext['content']:
            if k[0] == 'p':
                paragraph = {
                                "paragraph_content": ptext['content'][k],
                                "paragraph_type": 1,
                                "content": nd['id']
                            }
                jg3=requests.post(url='http://127.0.0.1/paper/paragraph/', data=paragraph, headers=header)
            elif k[0] == 'n':
                getnode(ptext['content'][k], paperid, nd['id'])

flag =False
try:
    for i in db.find():





        paper = {
        "journal": i['tips'].split('\r\n')[0].strip('\n').strip() if 'tips' in i else '',
        "journal_tips": i['tips'].split('\r\n')[1].strip('\n').strip()if 'tips' in i else '',
        "paper_title": i['top-title'].strip()if 'top-title' in i else '',
        "paper_authors": i['h2_author'][0] + i['h2_author'][1]if 'h2_author' in i else '',
        "keywords": i['a_keywords']if 'a_keywords' in i else '',
        "subject": 1,
        "domain": 1,
        'filename':i['filename'].strip()
        }
        print(paper)



        if flag==True:
            jg = requests.post(url='http://127.0.0.1/paper/paper/', data=paper, headers=header)
            if jg.status_code == 201:

                paper = json.loads(jg.text)
                paperid = paper['id']
                print(paperid)
                for j in i:
                    if j[0] == 'n':
                        getnode(i[j], paperid, 0)
        if paper['paper_title']=='面向超媒体链接的RESTful服务隐私建模方法':
            flag=True
except Exception :
    pass