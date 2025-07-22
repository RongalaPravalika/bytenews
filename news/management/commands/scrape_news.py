from django.core.management.base import BaseCommand
from news.utils import fetch_news_from_rss
from news.models import Article, Category

class Command(BaseCommand):
    help = 'Scrapes news articles from multiple RSS feeds and saves them.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting multi-source scraping...")

        NEWS_SOURCES = {
            'BBC News': 'https://feeds.bbci.co.uk/news/rss.xml',
            'CNN': 'http://rss.cnn.com/rss/cnn_topstories.rss',
            'Reuters': 'http://feeds.reuters.com/reuters/topNews',
        }

        total_articles_added = 0
        general_category, _ = Category.objects.get_or_create(name='General')

        for source_name, feed_url in NEWS_SOURCES.items():
            self.stdout.write(f"Fetching from {source_name}...")

            articles_data = fetch_news_from_rss(feed_url, source_name)

            if not articles_data:
                self.stdout.write(self.style.WARNING(f"No articles from {source_name}."))
                continue

            articles_added = 0
            for article_data in articles_data:
                if not Article.objects.filter(link=article_data['link']).exists():
                    article = Article.objects.create(
                        title=article_data['title'],
                        content=article_data['content'],
                        link=article_data['link'],
                        publication_date=article_data['publication_date'],
                        author=article_data['source'],  # ✅ author (optional)
                        source=article_data['source'],
                        source_url=article_data['link'],  # Temporary source_url
                        category=general_category,        # Assigning default category
                    )
                    articles_added += 1

            total_articles_added += articles_added
            self.stdout.write(self.style.SUCCESS(f"{articles_added} articles added from {source_name}"))

        self.stdout.write(self.style.SUCCESS(f"Total new articles: {total_articles_added}"))
