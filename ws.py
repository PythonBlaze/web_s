import requests
from bs4 import BeautifulSoup
import lxml

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'Microsoft']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get('https://habr.com/ru/feed/', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

matching_articles = ''
articles = soup.find_all('article', class_= 'tm-articles-list__item')

for article in articles:
    title_tag = article.find('h2', class_='tm-title')
    if title_tag:
        title = title_tag.text
        date = article.find('time')['title']
        link = 'https://habr.com' + article.find('a', class_='tm-title__link')['href']

        article_response = requests.get(link, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'lxml')
        article_body = article_soup.find('div', class_='tm-article-body')

        if article_body:
            article_text = article_body.get_text()
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                matching_articles += f'{date} - {title} - {link} (в заголовке)\n'
            if any(keyword.lower() in article_text.lower() for keyword in KEYWORDS):
                matching_articles += f'{date} - {title} - {link} (в тексте)\n'

print(matching_articles)
