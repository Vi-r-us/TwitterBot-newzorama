import Tech_Extractor as tech
import Anime_Extractor as anime
import Game_Extractor as game
import Coding_Extractor as code
import tweepy as tw
from os import environ
import time

time_to_execute = ['01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                   '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
                   '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                   '19:00', '20:00', '21:00', '22:00', '23:00', '00:00']

while True:
    current_time = time.strftime("%H:%M")

    if current_time in time_to_execute:
        print(f"\nAt {current_time}")

        final = code.give_me_news()                      # [[main_url, title, author]]

        consumer_key = environ['consumer_key_coding']
        consumer_secret = environ['consumer_secret_coding']
        access_key = environ['access_key_coding']
        access_secret = environ['access_secret_coding']

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        if len(final) > 10:
            i = 0
            for ele in final[:10]:
                try:
                    api.update_status(status=f"{ele[1]} \n\t\t -{ele[2]} \n{ele[0]}")
                    time.sleep(15)
                    i += 1
                except:
                    final.remove(ele)
            print(f"{len(final)} Coding News Tweeted")
        del final

        final = game.give_me_news()                     # [[main_url, image_url, title, author, content]]
        consumer_key = environ['consumer_key_gaming']
        consumer_secret = environ['consumer_secret_gaming']
        access_key = environ['access_key_gaming']
        access_secret = environ['access_secret_gaming']

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        i = 0
        for ele in final:
            try:
                api.update_status(status=f"{ele[2]} \n\t\t -{ele[3]} \n{ele[0]}")
                time.sleep(15)
                i += 1
            except:
                final.remove(ele)
        print(f"{i} Gaming News Tweeted")
        del final

        final = tech.give_me_news()                     # [[main_url, image_url, title, author, content]]
        consumer_key = environ['consumer_key_tech']
        consumer_secret = environ['consumer_secret_tech']
        access_key = environ['access_key_tech']
        access_secret = environ['access_secret_tech']

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        i = 0
        for ele in final:
            try:
                api.update_status(status=f"{ele[2]}\n\t\t -{ele[3]}\n{ele[0]}")
                time.sleep(15)
                i += 1
            except:
                final.remove(ele)
        print(f"{i} Technology News Tweeted")
        del final

        final = anime.give_me_news()                    # [[main_url, image_url, title, author, content]]

        consumer_key = environ['consumer_key_anime']
        consumer_secret = environ['consumer_secret_anime']
        access_key = environ['access_key_anime']
        access_secret = environ['access_secret_anime']

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        i = 0
        for ele in final:
            try:
                api.update_status(status=f"{ele[2]} \n\t\t -{ele[3]} \n{ele[0]}")
                time.sleep(15)
                i += 1
            except:
                final.remove(ele)
        print(f"{i} Anime News Tweeted")
        del final

        time.sleep(60)
