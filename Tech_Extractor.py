# Import Required Modules
import requests
from bs4 import BeautifulSoup
import datetime
import pytz

url = 'https://gadgets.ndtv.com/news'
Optimal_News = []
final = []

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')

# get the date of the day , last hour from current time date
last_hour_date_time = datetime.datetime.now(IST) - datetime.timedelta(hours=1)
date = str(last_hour_date_time).split()[0]              # return as a string format: yy-mm-dd


# This Function return optimal news
def give_me_news():

    # check for each page
    for page in range(1, 51):

        # Opening a connection
        if page == 1:       # if the page is 1 url is different
            client = requests.get(url)
            page_html = client.text
        else:               # from 2nd page onward url in same format
            client = requests.get(url + "/page-" + str(page))
            page_html = client.text

        page_soup = BeautifulSoup(page_html, 'html.parser')

        # Getting all the news from that particular page
        try:
            All_News = page_soup.find("div", class_="story_list row margin_b30").find_all("li")
        except:
            return final

        # Check Whether any news not belongs to today's date
        i = -1
        for News in All_News:
            try:

                if date != News.find("div", class_="dateline").text.split(", ")[-1]:
                    i = All_News.index(News)
                    break
            except:
                continue

        # if finds any news not belonging to the today's date then stop scraping for other pages
        if i != -1:
            del All_News[i:]
            Optimal_News.extend(All_News)
            break
        else:
            Optimal_News.extend(All_News)

    # every news in optimal news
    for ele in Optimal_News:

        try:
            main_url = ele.div.a['href']        # get main url of the news
            title = ele.find('span', class_="news_listing").text    # get the title of that news
            author = ele.find('div', class_="dateline").text.split(', ')[0]     # get the author name

            # open a new connection for news main url
            client = requests.get(main_url)
            page_html = client.text
            page_soup = BeautifulSoup(page_html, 'html.parser')

            # get the image link
            image_url = page_soup.find('div', class_="fullstoryImage").picture.img['src']

            # get the content of the news
            temp = page_soup.find('div', class_="content_text row description").find_all('p')
            content = f"{temp[0].text} {temp[1].text} {temp[2].text}"

            last_hour_date_time = datetime.datetime.now(IST) - datetime.timedelta(hours=1)

            # if the news is from last hour then only append it to final
            if page_soup.find('div', class_="content_block white_bg row margin_b30").find('div', class_="dateline").span['title'].split(" ")[4].split(":")[0] == last_hour_date_time.strftime("%H"):
                final.append([main_url, image_url, title, author, content])
        except:
            continue

    return final
