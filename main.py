import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36"
    }
    url = "https://olimpiada.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="news_item_in_full_list")

    news_dict = {}
    for article in articles_cards:
        article_time = str(datetime.now())[:16]
        article_title = article.find("a").text.strip()
        article_url = f'https://olimpiada.ru{article.find("a").get("href")}'

        rr = requests.get(url=article_url, headers=headers)
        info = BeautifulSoup(rr.text, "lxml").find("div", class_="news_left")
        article_info = str(BeautifulSoup(info.text, 'html.parser').get_text)[32:-3]

        article_id = article_url.split("/")[-1]

        #print(f"{article_time} | {article_title} | {article_url} | {article_info}")

        news_dict[article_id] = {
            "article_time" : article_time,
            "article_title": article_title,
            "article_url": article_url,
            "article_info": article_info
        }

    with open("news_dict.json", "w", encoding="utf8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36"
    }
    url = "https://olimpiada.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="news_item_in_full_list")

    fresh_news = {}
    for article in articles_cards:
        article_time = str(datetime.now())[:16]
        article_title = article.find("a").text.strip()
        article_url = f'https://olimpiada.ru{article.find("a").get("href")}'


        article_id = article_url.split("/")[-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("a").text.strip()
            article_id = article_url.split("/")[-1]

            rr = requests.get(url=article_url, headers=headers)
            info = BeautifulSoup(rr.text, "lxml").find("div", class_="news_left")
            article_info = str(BeautifulSoup(info.text, 'html.parser').get_text)[32:-3]

            news_dict[article_id] = {
                "article_time": article_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_info": article_info
            }

            fresh_news[article_id] = {
                "article_time": article_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_info": article_info
            }

    with open("news_dict.json", "w", encoding="utf8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    get_first_news()
    #print(check_news_update())


if __name__ == '__main__':
    main()
