import requests, textwrap, subprocess, sys
from bs4 import BeautifulSoup

# Sources definition
sources = {
    'lmneuquen': {
        'url': 'https://www.lmneuquen.com',
        'link_selector': '.title a',
        'text_selector': 'div.cuerpo p'
    },
    'genbeta': {
        'url': 'https://www.genbeta.com',
        'link_selector': 'h2.abstract-title a',
        'text_selector': 'div.js-post-images-container p'
    }
}

def get_link_list(source):
    if source not in sources:
        print('Source ' + source + ' not found')
        return False

    url = sources[source]['url']
    print(url)

    page = requests.get(url)

    if page.status_code != 200:
        return False

    soup = BeautifulSoup(page.content, 'html.parser')

    # Save in a file
    file = open('__norss_' + source + '.txt', 'w+')

    n = 1
    links = ''

    for link in soup.select(sources[source]['link_selector']):
        print(str(n) + '|' + link.getText())
        links += str(n) + '|' + link.getText()
        file.write(str(n) + '|' + link['href'] + '|' + link.getText() + '\n')

        n = n + 1

    file.close()

    return links


def get_article_by_number(source, number):
    # TODO Check if file exists
    path = '__norss_' + source + '.txt'

    with open(path) as file:
        line = file.readline()
        #print(line)

        while line:
            data = line.split('|')

            if data[0] == str(number):
                url = data[1]
                return get_article(source, url)

            line = file.readline()

    return False


def get_article(source, url):
    # TODO Check if source definition exists
    page = requests.get(url)

    if page.status_code != 200:
        return False

    soup = BeautifulSoup(page.content, 'html.parser')

    content = '# ' + soup.title.string + '\r\n'

    for i in soup.select(sources[source]['text_selector']):
        content += i.text + '\r\n'

    print(content)
    return content

#get_link_list('genbeta')
get_article_by_number('lmneuquen', 20)