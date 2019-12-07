import re
import csv
import json
import string
import requests
import unicodedata
from datetime import datetime

from bs4 import BeautifulSoup

from top_page_clean_strat import StoryCleanStrat
from stories import *


class ArticleProcessor(object):

    def __init__(self, url):
        self.parsing_url = hacker_news_url

    def fetch(self):
        hn_html = requests.get(self.parsing_url)
        article_soup = BeautifulSoup(hn_html.content, 'html.parser')
        cleaned_article = self.parse_and_clean_top_page(article_soup)
        return cleaned_article

    def parse_and_clean_top_page(self, soup):
        item_ids_list = []
        data = {}
        table = soup.find('table', attrs={'class': 'itemlist'})

        rows = table.find_all('tr')

        prev_item_id = ''

        for row in rows:
            tr_class = row.get('class', [])
            if 'athing' in tr_class:
                item_id = row['id']
                data[item_id] = {}

                item_ids_list.append(item_id)
                prev_item_id = item_id

                cols = row.find_all('td')
                for col in cols:
                    td_title_class = col['class']
                    title_tag = col.find('a', attrs={'class': 'storylink'})
                    if 'title' in td_title_class and title_tag is not None:
                        data[item_id]['item_id'] = item_id
                        data[item_id]['title'] = title_tag.text
                        data[item_id]['title_link'] = title_tag['href']

                        main_site_tag = col.find('span', attrs={'class': 'sitestr'})
                        data[item_id]['main_site'] = 'NA'
                        if main_site_tag is not None:
                            data[item_id]['main_site'] = main_site_tag.text

            if len(tr_class) == 0:
                col = row.find('td', attrs={'class': 'subtext'})
                if col is not None:
                    points_tag = col.find('span', attrs={'class': 'score'})
                    if points_tag is not None:
                        clean_points_text = unicodedata.normalize("NFKD", points_tag.text)
                        data[prev_item_id]['points'] = int(clean_points_text.split('points')[0])

                    user_tag = col.find('a', attrs={'class': 'hnuser'})
                    usr_name = 'NA'
                    usr_link = 'NA'
                    usr_karma_points = 0

                    if user_tag is not None:
                        usr_name = user_tag.text
                        usr_link = user_tag.get('href', 'NA')
                        usr_karma_points = self.get_author_karma_points(usr_link)

                    data[prev_item_id]['username'] = usr_name
                    data[prev_item_id]['user_link'] = usr_link
                    data[prev_item_id]['user_karma_points'] = usr_karma_points

                    comments_text = col.find(string=re.compile("comments"))
                    comments_count = 0
                    if comments_text is not None:
                        clean_comment_text = unicodedata.normalize("NFKD", comments_text)
                        comments_count = int(clean_comment_text.split('comments')[0])

                    data[prev_item_id]['comments_count'] = comments_count

        self.create_csv(data, item_ids_list)

        self.sort_by_comments(data, item_ids_list)

    def get_author_karma_points(self, user_link):
        hn_usr_link = self.parsing_url + user_link
        hn_usr_html = requests.get(hn_usr_link)
        hn_usr_soup = BeautifulSoup(hn_usr_html.content, 'html.parser')

        karma_points = 0
        usr_karma_tag = hn_usr_soup.find('td', string="karma:")

        if usr_karma_tag is not None:
            main_usr_karma_tag = usr_karma_tag.next_sibling
            karma_points_text = main_usr_karma_tag.text.strip()
            clean_karma_points_text = unicodedata.normalize("NFKD", karma_points_text)
            karma_points = int(clean_karma_points_text.split('karma')[0])

        return karma_points

    def sort_by_comments(self, data, item_ids_list):
        sorted_stories_by_comment = sorted(item_ids_list, key=lambda x: data[x]['comments_count'], reverse=True)

    def create_csv(self, data, item_ids_list):
        csv_filename = 'hn_top_page_{}.csv'.format(str(datetime.utcnow()))

        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = [
                'item_id', 'title', 'title_link', 'main_site', 'points',
                'comments_count', 'username', 'user_link', 'user_karma_points'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in item_ids_list:
                data_to_write = data[item]
                writer.writerow(data_to_write)


if __name__ == '__main__':
    hacker_news_url = 'https://news.ycombinator.com/'
    article = ArticleProcessor(hacker_news_url)
    article_parser = article.fetch()
    print("Done parsing, pls check the following CSV file")
