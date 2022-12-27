#!/usr/bin/env python
# -*- coding: cp1251 -*-
import urllib.request
from bs4 import BeautifulSoup
'''
Возможные баги, которые мы будем пытаться ловить:
1) на странице вообще отсутствует тэг <a> как ссылка на другие страницы
2) тэг <a> есть, но текст ссылки пустой, а поэтому невидимый
3) тэг <a> есть, текст есть, но он не "Next", а какой-то другой
4) тэг <a> есть, текст есть, но нет атрибута "href", из-за чего текст будет просто текстом без ссылки
5) тэг <a> есть, текст есть, атрибут "href" есть, но ведет не на следующую страницу
'''

# будем инкрементировать номер страницы, начиная с 1, пока не дойдём до последней, по уже известному нам html-заголовку:
# <h2>Это последняя страница на ней нет ссылки. Так надо.</h2>
i = 1
#сюда будем сохранять номера подозрительных страниц
warning_pages = []

#for i in range(9995,20000):
while True:
    url = 'https://s3.eu-central-1.amazonaws.com/qa-web-test-task/%s.html' %str(i)  #
    page = urllib.request.urlopen(url).read()
    page = BeautifulSoup (page, features="html.parser")
    # если находим наш финальный заголовок - выходим из цикла
    if len(page.find_all('h2')):
        h2 = page.find_all('h2')[0]
        if 'последняя страница' in h2.get_text():
            break

    # пока заголовка нет, продолжаем
    all_links = page.find_all('a')

    # ловим баг №1
    if len(all_links):
        for a in all_links:
            href = a.get('href')
            text = a.get_text()
            # здесь сразу ловим баги №№ 2, 3, 4 и 5
            if href != '%s.html' %str(i+1) or text != 'Next':
                warning_pages.append(i)
                print ('Bug on page: ' +str(i) )
            else:
                #как alivechecker (что мы не зависли) но и чтобы не спамить в лог - выводим счетчик каждые 100 страниц
                if i % 100 == 0:
                    print ('We are on page: ' + str(i))
    else:
        warning_pages.append(i)
        print ('Bug on page: ' +str(i) )

    i += 1

print ('We are finished. Bugs on pages: ' + str(warning_pages) )

# Bugs with pages are: [4, 5, 638, 666, 3395, 3471, 8543]