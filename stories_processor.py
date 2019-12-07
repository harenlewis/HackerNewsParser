import re
import csv
import requests
import unicodedata
from datetime import datetime

from bs4 import BeautifulSoup

from top_page_clean_strat import StoryCleanStrat
from utils.constants import Constants
from utils.csv_utility import CSVUtility


class HNStoryProcessor(object):
    """
    Parses the top page of Hacker News.
    Creates two csv files
    1) Stories sorted by comments.
       - filename: sorted_by_comments_{current_datetime}.csv
    2) List of all the stories rank wise
       - filename: hn_top_page_{current_datetime}.csv
    """
    def __init__(self, url):
        self.parsing_url = hacker_news_url

    def fetch(self):
        hn_html = requests.get(self.parsing_url)
        article_soup = BeautifulSoup(hn_html.content, 'html.parser')
        self.parse_and_clean_top_page(article_soup)

    def parse_and_clean_top_page(self, soup):
        item_ids_list = []
        data = {}
        table = soup.find('table', attrs={'class': 'itemlist'})

        story_clean = StoryCleanStrat(table)
        parsed_stories_data, item_ids_list = story_clean.cleanup()

        self.parse_data_to_csv(parsed_stories_data, item_ids_list)
        self.sort_by_comments(parsed_stories_data, item_ids_list)

    def sort_by_comments(self, data, item_ids_list):
        sorted_stories_by_comment = sorted(item_ids_list, key=lambda x: data[x]['comments_count'], reverse=True)
        header_fields = [
            'item_id', 'title', 'title_link', 'main_site', 'points',
            'comments_count', 'username', 'user_link', 'user_karma_points'
        ]

        CSVUtility.create_csv(header_fields, data, sorted_stories_by_comment, 'sorted_by_comments')

    def parse_data_to_csv(self, data, item_ids_list):
        header_fields = [
            'item_id', 'title', 'title_link', 'main_site', 'points',
            'comments_count', 'username', 'user_link', 'user_karma_points'
        ]

        CSVUtility.create_csv(header_fields, data, item_ids_list, 'hn_top_page')

if __name__ == '__main__':
    hacker_news_url = Constants.BASE_URL
    story = HNStoryProcessor(hacker_news_url)
    story_parser = story.fetch()
    print("Done parsing, pls check the following CSV file")
