from server3.business.seo_article_business import SeoArticleBusiness


class SeoArticleService:
    @classmethod
    def seo_article_list(self):
        article_list = SeoArticleBusiness.get_article_list()
        return article_list

    @classmethod
    def get_article_detail(cls, article_id):
        article = SeoArticleBusiness.get_article(article_id=article_id)
        return article
