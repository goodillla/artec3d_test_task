#!/usr/bin/env python
# -*- coding: cp1251 -*-
import urllib.request
from bs4 import BeautifulSoup
'''
��������� ����, ������� �� ����� �������� ������:
1) �� �������� ������ ����������� ��� <a> ��� ������ �� ������ ��������
2) ��� <a> ����, �� ����� ������ ������, � ������� ���������
3) ��� <a> ����, ����� ����, �� �� �� "Next", � �����-�� ������
4) ��� <a> ����, ����� ����, �� ��� �������� "href", ��-�� ���� ����� ����� ������ ������� ��� ������
5) ��� <a> ����, ����� ����, ������� "href" ����, �� ����� �� �� ��������� ��������
'''

# ����� ���������������� ����� ��������, ������� � 1, ���� �� ����� �� ���������, �� ��� ���������� ��� html-���������:
# <h2>��� ��������� �������� �� ��� ��� ������. ��� ����.</h2>
i = 1
#���� ����� ��������� ������ �������������� �������
warning_pages = []

#for i in range(9995,20000):
while True:
    url = 'https://s3.eu-central-1.amazonaws.com/qa-web-test-task/%s.html' %str(i)  #
    page = urllib.request.urlopen(url).read()
    page = BeautifulSoup (page, features="html.parser")
    # ���� ������� ��� ��������� ��������� - ������� �� �����
    if len(page.find_all('h2')):
        h2 = page.find_all('h2')[0]
        if '��������� ��������' in h2.get_text():
            break

    # ���� ��������� ���, ����������
    all_links = page.find_all('a')

    # ����� ��� �1
    if len(all_links):
        for a in all_links:
            href = a.get('href')
            text = a.get_text()
            # ����� ����� ����� ���� �� 2, 3, 4 � 5
            if href != '%s.html' %str(i+1) or text != 'Next':
                warning_pages.append(i)
                print ('Bug on page: ' +str(i) )
            else:
                #��� alivechecker (��� �� �� �������) �� � ����� �� ������� � ��� - ������� ������� ������ 100 �������
                if i % 100 == 0:
                    print ('We are on page: ' + str(i))
    else:
        warning_pages.append(i)
        print ('Bug on page: ' +str(i) )

    i += 1

print ('We are finished. Bugs on pages: ' + str(warning_pages) )

# Bugs with pages are: [4, 5, 638, 666, 3395, 3471, 8543]