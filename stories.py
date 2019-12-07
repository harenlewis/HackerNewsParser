from top_page_clean_strat import *


class Story(object):

    # def __init__(self,
    #             title_link,
    #             title,
    #             user_karma_points,
    #             points,
    #             main_site,
    #             item_id,
    #             user_link,
    #             comments_count,
    #             username):

        # self.title_link = title_link
        # self.title = title
        # self.user_karma_points = user_karma_points
        # self.points = points
        # self.main_site = main_site
        # self.item_id = item_id
        # self.user_link = user_link
        # self.comments_count = comments_count
        # self.username = username

    def __repr__(self):
        return json.dumps(self.to_dict())

    def story_to_dict(self):
        return {
            "title_link": self.title_link,
            "title": self.title,
            "user_karma_points": self.user_karma_points,
            "points": self.points,
            "main_site": self.main_site,
            "item_id": self.item_id,
            "user_link": self.user_link,
            "comments_count": self.comments_count,
            "username": self.username
        }
