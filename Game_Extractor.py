
# Import Required Modules
import requests
from bs4 import BeautifulSoup

# Site URL from which data will be extracted
url = 'https://in.ign.com/'
final = []


# This Function return optimal news
def give_me_news():

    # Check if site is working or not if site is down return None news
    try:
        client = requests.get(url)
        page_html = client.text
        page_soup = BeautifulSoup(page_html, 'html.parser')

        # Get all the html in all broll-wrap
        all_news = page_soup.find_all("div", class_="page-content")[-1].find_all('section', class_="broll wrap")
    except:
        return None

    # For every broll-wrap find news
    for news in all_news:

        # get the news listed from broll-wrap
        bunker = news.find_all('article')

        # for every single news
        for ele in bunker:

            # check if the news at the time of execution is not more than an hour ago
            if 'hour' not in ele.find('div', class_="info").time.text.split(' min')[0]:

                # get the main url of the particular news
                main_url = ele.find('div', class_='m').h3.a['href']
                # get the title of the particular news
                title = ele.find('div', class_='m').h3.a.text

                # open the new request connection for the particular news main url
                client = requests.get(main_url)
                page_html = client.text
                page_soup = BeautifulSoup(page_html, 'html.parser')

                # get the image url
                try:
                    # if find the the image link of full quality on the news main url
                    image_url = page_soup.find('img', class_="hero image")['src']
                except:
                    # otherwise take the image url of thumbnail from the original site
                    image_url = ele.find('img', class_="thumb")['srcset'].split(' ')[1]

                try:
                    # Get the author name
                    author = 'by ' + page_soup.find('section', class_="article-authors").find('a', class_="url").text
                except:
                    # for trailers there is no author return blank string
                    author = ""

                try:
                    # get the description
                    temp = page_soup.find('div', id="id_text").find_all('p')
                    desc = temp[0].text + temp[1].text
                except:
                    try:
                        # for game trailers there is no description
                        desc = page_soup.find('section', class_='video-details').find('div', class_='description').text
                    except:
                        desc = ''

                # append to final as a list in list
                final.append([main_url, image_url, title, author, desc])

    return final
