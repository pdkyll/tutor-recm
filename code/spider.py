# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:57:01 2015
@author: bitjoy.net
"""

from bs4 import BeautifulSoup
import urllib.request
import xml.etree.ElementTree as ET
import re
import configparser

def get_news_pool(root, start, end):
    news_pool = []
    for i in range(start,end,-1):
        page_url = ''
        if i != start:
            page_url = root +'_%d.shtml'%(i)
        else:
            page_url = root + '.shtml'
        try:
            response = urllib.request.urlopen(page_url)
        except Exception as e:
            print("-----%s: %s-----"%(type(e), page_url))
            continue
        html = response.read()
        soup = BeautifulSoup(html,"lxml") # http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        td = soup.find('td', class_="newsblue1")
        a = td.find_all('a')
        span = td.find_all('span')
        for i in range(len(a)):
            date_time = span[i].string
            url = a[i].get('href')
            title = a[i].string
            news_info = ['2016-'+date_time[1:3]+'-'+date_time[4:-1]+':00',url,title]
            news_pool.append(news_info)
    return(news_pool)

def crawl_news(news_pool, min_body_len, doc_dir_path, doc_encoding):
    i = 1
    for news in news_pool:
        try:
            response = urllib.request.urlopen(news[1])
        except Exception as e:
            print("-----%s: %s-----"%(type(e), news[1]))
            continue
        html = response.read()
        soup = BeautifulSoup(html,"lxml") # http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        try:
            body = soup.find('div', class_ = "text clear").find('div').get_text()
        except Exception as e:
            print("-----%s: %s-----"%(type(e), news[1]))
            continue
        if '//' in body:
            body = body[:body.index('//')]
        body = body.replace(" ", "")
        if len(body) <= min_body_len:
            continue
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d"%(i)
        ET.SubElement(doc, "url").text = news[1]
        ET.SubElement(doc, "title").text = news[2]
        ET.SubElement(doc, "datetime").text = news[0]
        ET.SubElement(doc, "body").text = body
        tree = ET.ElementTree(doc)
        tree.write(doc_dir_path + "%d.xml"%(i), encoding = doc_encoding, xml_declaration = True)
        i += 1
    
if __name__ == '__main__':
    #baseurl='http://pg.njupt.edu.cn/2018/0903/c1079a132310/page.htm'#46个导师
    baseurl='http://pg.njupt.edu.cn/2018/0903/c1080a132292/page.htm' #专硕93个导师
    tutors_pool=[]
    response = urllib.request.urlopen(baseurl)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    body=soup.find('div',class_="wp_articlecontent")
    a=body.find_all('a')
    span=body.find_all('span')
    for i in range(len(a)):
        title = span[i].string
        url = a[i].get('href')
        name = a[i].string
        tutor_info = [name, url]
        tutors_pool.append(tutor_info)
    i = 1
    for tutor in tutors_pool:
        response = urllib.request.urlopen(tutor[1])
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        title=soup.select('#container_content > table > tbody > tr:nth-of-type(2) > td > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr > td > table > tbody > tr > td:nth-of-type(2) > table > tbody > tr:nth-of-type(7) > td:nth-of-type(2)')
        body1=soup.select('#container_content > table > tbody > tr:nth-of-type(2) > td > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr > td > p:nth-of-type(4)')
        body2=soup.select('#container_content > table > tbody > tr:nth-of-type(2) > td > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr > td > p:nth-of-type(6)')
        title1=title[0].get_text()
        title2=title[0].get('align')
        doc_dir_path ='../data/news/'
        doc_encoding = 'utf-8'
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d" % (i)
        ET.SubElement(doc, "url").text = tutor[1]
        ET.SubElement(doc, "title").text = tutor[0]
        ET.SubElement(doc, "datetime").text = '2018-09-12'
    #   ET.SubElement(doc, "title1").text = title[0].get_text()
        ET.SubElement(doc, "body").text = body1[0].get_text()
   #    ET.SubElement(doc, "body2").text = body2[0].get_text()
        tree = ET.ElementTree(doc)
        tree.write(doc_dir_path + "%d.xml" % (i), encoding=doc_encoding, xml_declaration=True)
        i += 1

    print('done!')

