# Import Required Modules
import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/newest'
Optimal_News = []
final = []

# This Function return optimal news
def give_me_news():

    j = 0
    i = 0
    while j != -1:

        if i == 0:
            client = requests.get(url)
            page_html = client.text
            page_soup = BeautifulSoup(page_html, 'html.parser')
        else:
            client = requests.get(URL)
            page_html = client.text
            page_soup = BeautifulSoup(page_html, 'html.parser')

        try:
            Optimal_News = page_soup.find('table', class_="itemlist").find_all('tr')
        except:
            return None

        next_url = Optimal_News[-1].find('td', class_='title').a['href']
        URL = url.split('newest')[0] + next_url
        i += 1

        del Optimal_News[-1]
        del Optimal_News[-1]

        for ele in Optimal_News:
            if str(ele) == """<tr class="spacer" style="height:5px"></tr>""":
                Optimal_News.remove(ele)

        for news in Optimal_News:
            if Optimal_News.index(news) % 2 == 0:
                main_url = news.find('a', class_="storylink")['href']

                if 'item?id=' in main_url:
                    main_url = url

                title = news.find('a', class_="storylink").text
            else:
                content = news.find('td', class_="subtext").text
                author = 'by ' + content.split(' ')[3]

                if f"{content.split(' ')[4]} {content.split(' ')[5]}" == '1 hour':
                    j=-1
                    break
                else:
                    final.append([main_url, title, author])
    return final
