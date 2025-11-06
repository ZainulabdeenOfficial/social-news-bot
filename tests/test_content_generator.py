from src.ai.content_generator import ContentGenerator


def test_content_generator_fallback_without_key(monkeypatch):
    # Ensure no key in env
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    gen = ContentGenerator()
    article = {
        'title': 'Test Title',
        'description': 'Test description',
        'source': 'Test',
        'link': 'http://example.com'
    }
    data = gen.generate_post_content(article, 'linkedin')
    assert 'post_text' in data and data['post_text']


