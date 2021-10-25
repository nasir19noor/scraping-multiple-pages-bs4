from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = f'{root}/movies'
response = requests.get(website)
content = response.text
soup = BeautifulSoup(content, 'lxml')

pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links = []
for page in range(1, int(last_page)+1)[:2]:
    response = requests.get(f'{website}?page={page}')
    print(f'{website}?page={page}')
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')

    for link in box.select('a', href=True):
        links.append(link['href'])

    for link in links:
        try:
            response = requests.get(f'{root}/{link}')
            content = response.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')
            title = box.find('h1').get_text()
            print(title)
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')
            with open(f'transcripts/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(transcript)
        except:
            print('--------Link not Working--------')
            print(link)

