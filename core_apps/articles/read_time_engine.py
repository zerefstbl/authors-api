class ArticleReadTimeEngine:
    def __init__(self, article):
        self.article = article

        self.word_per_minute = 250

        self.banner_image_adjustment_time = round(1 / 6, 3)

    def check_article_has_banner_image(self):
        has_banner_image = True
        if not self.article.banner_image:
            has_banner_image = False
            self.banner_image_adjustment_time = 0
        return has_banner_image

    def get_title(self):
        return self.article.title
    
    def get_tags(self):
        tag_words = []
        [tag_words.extend]