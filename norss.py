import requests, textwrap, subprocess, sys
from bs4 import BeautifulSoup

def get_link_list():
    url = 'https://www.lmneuquen.com'

    page = requests.get(url)

    if page.status_code != 200:
        return False

    soup = BeautifulSoup(page.content, 'html.parser')

    # Save in a file
    file = open('__norss_links.txt', 'w+')

    n = 1
    links = ''

    for link in soup.select('.title a'):
        print(str(n) + '|' + link.getText())
        links += str(n) + '|' + link.getText()
        file.write(str(n) + '|' + link['href'] + '|' + link.getText() + '\n')

        n = n + 1

    file.close()

    return links


def get_article_by_number(number):
    path = '__norss_links.txt'

    with open(path) as file:
        line = file.readline()
        #print(line)

        while line:
            data = line.split('|')
            print(data)
            print(str(data[0]) + ' - ' + str(number))

            if data[0] == str(number):
                url = data[1]
                #print("va a pasar por el llamado!")
                #print(url)
                return get_article(url)

            line = file.readline()

    return False


def get_article(url):
    print("pasa por get article")
    page = requests.get(url)

    if page.status_code != 200:
        return False

    soup = BeautifulSoup(page.content, 'html.parser')

    content = '# ' + soup.title.string + '\r\n'

    for i in soup.select('div.cuerpo p'):
        content += i.text + '\r\n'

    print(content)
    return content

get_article_by_number(20)