import pytest
import tweepy
from unittest.mock import MagicMock, patch
from datetime import datetime
import time

from src.config import get_bearer_token
from src.api_client import TwitterAPIClient
from src.exporter import export_to_markdown, export_to_json, export_to_txt

# Mock tweet data
class MockTweet:
    def __init__(self, tweet_id, text, author_id, created_at, likes, retweets, replies):
        self.id = tweet_id
        self.text = text
        self.author_id = author_id
        self.created_at = created_at
        self.public_metrics = {
            'like_count': likes,
            'retweet_count': retweets,
            'reply_count': replies
        }
        self.data = {
            'id': self.id,
            'text': self.text,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat() + 'Z',
            'public_metrics': self.public_metrics
        }

MOCK_TWEETS = [
    MockTweet(1, "Hello World", 123, datetime(2023, 1, 1), 10, 5, 2),
    MockTweet(2, "This is a test tweet.", 123, datetime(2023, 1, 2), 20, 15, 7),
]

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked TwitterAPIClient."""
    with patch('tweepy.Client') as mock_client_constructor:
        mock_client_instance = MagicMock()
        mock_client_constructor.return_value = mock_client_instance
        yield TwitterAPIClient("dummy_token")

# --- Test config.py ---

@patch('os.environ.get')
def test_get_bearer_token_from_env(mock_os_get):
    """Test that get_bearer_token reads from the environment variable."""
    mock_os_get.return_value = "test_token_from_env"
    assert get_bearer_token() == "test_token_from_env"
    mock_os_get.assert_called_with("BEARER_TOKEN")

@patch('os.environ.get', return_value=None)
@patch('src.config.getpass')
def test_get_bearer_token_from_prompt(mock_getpass, mock_os_get):
    """Test that get_bearer_token prompts for input if env var is not set."""
    mock_getpass.return_value = "test_token_from_prompt"
    assert get_bearer_token() == "test_token_from_prompt"
    mock_getpass.assert_called_once()

# --- Test api_client.py ---

def test_get_user_id_success(mock_api_client):
    """Test successfully fetching a user ID."""
    mock_response = MagicMock()
    mock_response.data.id = "12345"
    mock_api_client.client.get_user.return_value = mock_response

    user_id = mock_api_client.get_user_id("testuser")
    assert user_id == "12345"
    mock_api_client.client.get_user.assert_called_with(username="testuser")

def test_get_user_id_not_found(mock_api_client):
    """Test handling of a user not found."""
    mock_response = MagicMock()
    mock_response.data = None
    mock_api_client.client.get_user.return_value = mock_response

    user_id = mock_api_client.get_user_id("nonexistentuser")
    assert user_id is None

@patch('tweepy.Paginator')
def test_get_all_tweets_pagination(mock_paginator_class, mock_api_client):
    """Test that the client correctly handles pagination."""
    mock_response_page1 = MagicMock()
    mock_response_page1.data = [MOCK_TWEETS[0]]
    mock_response_page2 = MagicMock()
    mock_response_page2.data = [MOCK_TWEETS[1]]

    mock_paginator_instance = mock_paginator_class.return_value
    mock_paginator_instance.__iter__.return_value = iter([mock_response_page1, mock_response_page2])

    tweets = list(mock_api_client.get_all_tweets("12345"))

    assert len(tweets) == 2
    assert tweets[0].id == 1
    assert tweets[1].id == 2

# --- Test exporter.py ---

# --- Test exporter.py ---

def test_export_to_markdown(tmp_path):
    """Test exporting tweets to a Markdown file."""
    filename = tmp_path / "test.md"
    export_to_markdown(MOCK_TWEETS, "testuser", str(filename))

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "# Tweets from @testuser" in content
        assert "Hello World" in content
        assert "This is a test tweet." in content
        assert "**Metrics:** 10 Likes, 5 Retweets, 2 Replies" in content

def test_export_to_json(tmp_path):
    """Test exporting tweets to a JSON file."""
    filename = tmp_path / "test.json"
    export_to_json(MOCK_TWEETS, str(filename))

    with open(filename, 'r', encoding='utf-8') as f:
        import json
        data = json.load(f)
        assert len(data) == 2
        assert data[0]['id'] == 1
        assert data[1]['text'] == "This is a test tweet."

def test_export_to_txt(tmp_path):
    """Test exporting tweets to a TXT file."""
    filename = tmp_path / "test.txt"
    export_to_txt(MOCK_TWEETS, "testuser", str(filename))

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Tweets from @testuser" in content
        assert "Text: Hello World" in content
        assert "Text: This is a test tweet." in content
