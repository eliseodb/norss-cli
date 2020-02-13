import requests, textwrap, subprocess, sys
from bs4 import BeautifulSoup

def get_article(url):
	page = requests.get(url)

	if page.status_code != 200:
		return False

	soup = BeautifulSoup(page.content, 'html.parser')

	content = '# ' + soup.title.string + '\r\n'

	for i in soup.select('div.cuerpo p'):
		content += i.text + '\r\n'

	return content