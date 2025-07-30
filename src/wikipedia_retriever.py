import wikipedia
import random

class WikipediaRetriever:
    def __init__(self, language: str = "pt"):
        self.language = language
        self.article_title = None
        self.article_url = None
        self.article_content = None
        wikipedia.set_lang(language)

    def get_random_article(self):
        ai_topics = [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural network",
            "natural language processing",
            "computer vision",
            "reinforcement learning"
        ]
        topic = random.choice(ai_topics)
        try:
            page = wikipedia.page(topic)
            self.article_title = page.title
            self.article_url = page.url
            self.article_content = page.content
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(e.options[0])
            self.article_title = page.title
            self.article_url = page.url
            self.article_content = page.content
        except Exception as e:
            return f"Error retrieving article: {str(e)}"