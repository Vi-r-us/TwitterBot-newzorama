# Import Required Modules
import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://www.animenewsnetwork.com'
Optimal_News = []
final = []

# get the date of the day , last hour from current time date
# return as a string format: yy-mm-dd
last_hour_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
date = str(last_hour_date_time).split()[0]  # will be change accordingly


# This Function return optimal news
def give_me_news():

    # Opening a connection
    client = requests.get(url)
    page_html = client.text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # Get the html code according to date provided
    try:
        desk = page_soup.find("div", {'data-day': date}).find("div", class_="mainfeed-section herald-boxes")
    except:
        return final

    # Get all type of news and append
    Optimal_News.extend(desk.find_all('div', class_="herald box news"))
    Optimal_News.extend(desk.find_all('div', class_="herald box interest"))
    Optimal_News.extend(desk.find_all('div', class_="herald box news aside_overlap"))
    Optimal_News.extend(desk.find_all('div', class_="herald box reviews"))

    # for each news
    for news in Optimal_News:

        # get the main url and title of the particular news
        main_url = url + news.find('div', class_="wrap").div.h3.a['href']
        title = news.find('div', class_="wrap").div.h3.a.text

        # open a new connection for that particular news main link
        client = requests.get(main_url)
        page_html = client.text
        page_soup = BeautifulSoup(page_html, 'html.parser')

        # get image url if its youtube thumbnail or normal picture
        if news.find('div')['class'] == "herald box reviews":
            image_url = url + page_soup.find('div', class_="KonaBody").find('p', style="clear:right").img['data-src']
        elif news.find('div')['class'] == "herald box news aside_overlap":
            image_url = url + page_soup.find('div', class_="KonaBody").find('p', align="center").img['src']
        else:
            try:
                image_url = url + page_soup.find('div', class_="text-zone easyread-width").find('div', class_="meat").center.img['data-src']
            except:
                try:
                    image_url = url + page_soup.find('div', class_="KonaBody").find('div', class_="meat").find('p', align="center").img['data-src']
                except:
                    try:
                        image_url = url + page_soup.find('div', class_="KonaBody").find('p', style="clear:right").img['data-src']
                    except:
                        try:
                            image_url = url + page_soup.find('div', class_="KonaBody").find('div', class_="meat").p.img['data-src']
                        except:
                            image_url = url + news.find('div', class_="thumbnail")['data-src']

        if '/review/' in main_url:
            temp = page_soup.find('div', class_="KonaBody").find_all('p')
            for ele in temp:
                if ele.find('p', align="center") or ele.find('p', style="clear:right"):
                    temp.remove(ele)
            content = f'{temp[0].text} {temp[1].text}'
        else:
            # get all content included pictures
            temp = page_soup.find('div', class_="KonaBody").find('div', class_='meat').find_all('p')

            # remove unwanted content such as pictures
            for ele in temp:
                if ele.find('p', align="center") or ele.find('p', style="clear:right"):
                    temp.remove(ele)

            # get the content in a string format
            try:
                if temp[0].text is None or temp[1].text is None or temp[2].text is None:
                    content = f'{temp[0]}'
                else:
                    content = f'{temp[0].text} {temp[1].text} {temp[2].text}'
            except:
                content = ""

        # get author name
        try:
            author = page_soup.find('div', id="page-title").text.split('IST')[1].split('\n')[0]
        except:
            author = 'by' + page_soup.find('div', id="page-title").text.split('by')[1].split(',')[0]

        # if the news is from last hour then only append it to final
        last_hour_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        if page_soup.find('div', id="page-title").small.time.text.split(" ")[1].split(":")[0] == last_hour_date_time.strftime("%H"):
            final.append([main_url, image_url, title, author, content])

    return final

