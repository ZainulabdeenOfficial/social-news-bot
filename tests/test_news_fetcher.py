from src.services.news_fetcher import NewsFetcher


def test_fetcher_instantiates():
    fetcher = NewsFetcher()
    assert isinstance(fetcher.sources, list)


