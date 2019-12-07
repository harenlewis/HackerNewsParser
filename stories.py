from top_page_clean_strat import *


class Story(object):

    def __init__(self,
                title = '',
                image=None,
                description = '',
                author = '',
                publishedDate = '',
                slug = ''):

        self.title = title
        self.image = image
        self.description = description
        self.author = author
        self.publishedDate = publishedDate
        self.slug = slug

    def __repr__(self):
        print ('test')
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'title': self.title,
            'image': self.image,
            'short_description' : self.description,
            'author' :self.author,
            'publishedDdate' :self.publishedDate
        }

    def image(self, arg):
        pass
