import pytest
from human_screen import human_screen_articles


@pytest.fixture
def sample_articles():
    return [
        {
            "title": "Climate change fund launches in UK",
            "description": "A new ESG fund focused on climate resilience",
            "url": "https://example.com/1"
        },
        {
            "title": "Oil prices rise as demand spikes",
            "description": "Markets show increased activity around fossil fuels",
            "url": "https://example.com/2"
        }
    ]


def test_screen_accept_first_only(monkeypatch, sample_articles):
    inputs = iter(["y", "n"])

    def mock_input(_):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)

    accepted = human_screen_articles(sample_articles)
    assert len(accepted) == 1
    assert accepted[0]["title"] == "Climate change fund launches in UK"


def test_screen_accept_all(monkeypatch, sample_articles):
    inputs = iter(["y", "y"])

    def mock_input(_):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)

    accepted = human_screen_articles(sample_articles)
    assert len(accepted) == 2


def test_screen_exit_early(monkeypatch, sample_articles):
    inputs = iter(["exit"])

    def mock_input(_):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)

    accepted = human_screen_articles(sample_articles)
    assert len(accepted) == 0
