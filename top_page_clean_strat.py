import json
import requests

from bs4 import BeautifulSoup
from stories import Story


class StoryCleanStrat(object):
    # import pdb; pdb.set_trace()

    def __init__(self, soup):
        self.soup = soup

    def cleanup(self):
        # import pdb; pdb.set_trace()
        article = Article()
        article.title = self.get_title()
        article.image = self.get_image()
        article.description = self.get_short_description()
        article.author = self.get_author()
        article.publishedDate = self.get_published_date()
        article.slug = self.get_slug()
        article.keyword_list = self.get_keywords()
        return article

    def get_title(self):
        soup = self.soup
        if soup.article.h1:
            title = soup.find('meta',  property='og:title')
            return title['content']

    def get_image(self):
        soup = self.soup
        if soup.article.img:
            return soup.article.img.get_attribute_list('src')

    def get_short_description(self):
        soup = self.soup
        short_description = soup.find('meta', property = 'og:description')
        return short_description['content']


    def get_author(self):
        soup = self.soup
        scriptData = json.loads(soup.find_all('script' , type =  'application/ld+json')[1].get_text())
        return scriptData['author']['name']


    def get_published_date(self):
        soup = self.soup
        scriptData = json.loads(soup.find_all('script' , type =  'application/ld+json')[1].get_text())
        return scriptData['datePublished']

    def get_slug(self):
        soup = self.soup
        title = soup.find('meta',  property='og:title')
        slug = title['content'].replace(' ','-')
        return slug

    def get_keywords(self):
        soup = self.soup
        keyword_list = []
        for meta in soup.findAll("meta"):
            metaname = meta.get('name', '').lower()
            if 'keywords' == metaname:
                keyword_list.append(meta['content'].strip())
        return keyword_list
