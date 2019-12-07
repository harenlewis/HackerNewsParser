import re
import json
import requests
import unicodedata

from bs4 import BeautifulSoup
from utils.constants import Constants


class StoryCleanStrat(object):

    def __init__(self, soup):
        self.soup = soup

    def cleanup(self):
        self.item_ids_list = []
        self.main_data = {}
        
        rows = self.soup.find_all('tr')
        prev_item_id = ''
        for row in rows:
            tr_class = row.get('class', [])
            if 'athing' in tr_class:
                item_id = row.get('id', None)
                self.main_data[item_id] = {}
                self.item_ids_list.append(item_id)
                prev_item_id = item_id

                cols = row.find_all('td')
                for col in cols:
                    header_data, is_data = self.get_story_main_data(col)
                    if is_data:
                        self.main_data[item_id]['item_id'] = item_id
                        self.main_data[item_id]['title'] = header_data['title']
                        self.main_data[item_id]['title_link'] = header_data['title_link']
                        self.main_data[item_id]['main_site'] = header_data['main_site']

            if len(tr_class) == 0:
                col = row.find('td', attrs={'class': 'subtext'})
                if col is not None:
                    self.main_data[prev_item_id]['points'] = self.get_points(col)

                    usr_data = self.get_author_data(col)

                    self.main_data[prev_item_id]['username'] = usr_data['username']
                    self.main_data[prev_item_id]['user_link'] = usr_data['user_link']
                    self.main_data[prev_item_id]['user_karma_points'] = usr_data['user_karma_points']

                    self.main_data[prev_item_id]['comments_count'] = self.get_story_comments(col)

        return self.main_data, self.item_ids_list

    def get_story_main_data(self, col):
        """
        Returns story data:
        - title
        - title
        - main_site
        """
        is_data = False
        data = {}
        td_title_class = col['class']
        title_tag = col.find('a', attrs={'class': 'storylink'})
        if 'title' in td_title_class and title_tag is not None:
            data['title'] = title_tag.text
            data['title'] = title_tag['href']

            main_site_tag = col.find('span', attrs={'class': 'sitestr'})
            data['main_site'] = 'NA'
            if main_site_tag is not None:
                data['main_site'] = main_site_tag.text

            is_data = True
        return data, is_data

    def get_points(self, col):
        """
        Returns number of points on a story
        """
        points_tag = col.find('span', attrs={'class': 'score'})
        if points_tag is not None:
            clean_points_text = unicodedata.normalize("NFKD", points_tag.text)
            return int(clean_points_text.split('points')[0])
        else:
            return 0

    def get_story_comments(self, col):
        """
        Returns number of comments on a story
        """
        comments_text = col.find(string=re.compile("comments"))
        comments_count = 0
        if comments_text is not None:
            clean_comment_text = unicodedata.normalize("NFKD", comments_text)
            comments_count = int(clean_comment_text.split('comments')[0])
        
        return comments_count

    def get_author_data(self, col):
        """
        Returns author data:
        - username
        - user_link
        - user_karma_points
        """
        usr_data = {}
        user_tag = col.find('a', attrs={'class': 'hnuser'})
        usr_name = 'NA'
        usr_link = 'NA'
        usr_karma_points = 0

        if user_tag is not None:
            usr_name = user_tag.text
            usr_link = user_tag.get('href', 'NA')
            usr_karma_points = self.get_author_karma_points(usr_link)

        usr_data['username'] = usr_name
        usr_data['user_link'] = usr_link
        usr_data['user_karma_points'] = usr_karma_points

        return usr_data

    def get_author_karma_points(self, user_link):
        """
        Returns karma points for given author(user_link)
        """
        hn_usr_link = Constants.BASE_URL + user_link

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
