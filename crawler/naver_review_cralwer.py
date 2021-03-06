import os
import pandas as pd
import requests
import time
from datetime import datetime as dt
from bs4 import BeautifulSoup
from tqdm import tqdm

date = dt.date(dt.now())

PATH = '../review'
FILE_NAME = 'movie_reviews_{}.txt'.format(date)

def review_crawler():
    nv_reviews = pd.DataFrame(columns=["title", "review"])
    ratings_lst = []

    for i in tqdm(range(1, 400+1)):
        url = "https://movie.naver.com/movie/point/af/list.nhn?&page={}".format(i)
        response = requests.get(url)
        dom = BeautifulSoup(response.content, "html.parser")
        reviews_pre = dom.find_all("td", "title")
        ratings = dom.find_all("td", "point")

        for idx, rvw in enumerate(reviews_pre):
            title = rvw.a.text
            review = rvw.text.split('\n')[2].split(' \r')[0]
            nv_reviews.loc[len(nv_reviews)] = {
                "title": title,
                "review": review
            }

        for point in ratings:
            rating = point.text
            ratings_lst.append(rating)

        time.sleep(0.2)

    nv_reviews["rating"] = ratings_lst

    return nv_reviews


df = review_crawler()
df.to_csv(os.path.join(PATH, FILE_NAME),
          index=False, encoding='utf-8')
