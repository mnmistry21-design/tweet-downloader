import json
from datetime import datetime

def _format_tweet_for_display(tweet):
    """Formats a single tweet for readable output."""
    text = tweet.text.replace('\n', '\n> ')
    created_at = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
    tweet_url = f"https://x.com/{tweet.author_id}/status/{tweet.id}"

    metrics = tweet.public_metrics or {}
    likes = metrics.get('like_count', 0)
    retweets = metrics.get('retweet_count', 0)
    replies = metrics.get('reply_count', 0)

    return (
        f"**Tweet ID:** {tweet.id}\n"
        f"**Posted at:** {created_at}\n"
        f"**Link:** {tweet_url}\n"
        f"**Metrics:** {likes} Likes, {retweets} Retweets, {replies} Replies\n\n"
        f"> {text}\n"
    )

def export_to_markdown(tweets: list, username: str, filename: str):
    """Exports tweets to a Markdown file."""
    header = (
        f"# Tweets from @{username}\n\n"
        f"Downloaded on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Total tweets: {len(tweets)}\n\n"
        "---\n\n"
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header)
        for tweet in tweets:
            f.write(_format_tweet_for_display(tweet))
            f.write("\n---\n\n")
    print(f"Successfully exported {len(tweets)} tweets to {filename}")

def export_to_json(tweets: list, filename: str):
    """Exports tweets to a JSON file."""
    tweet_list = [tweet.data for tweet in tweets]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweet_list, f, indent=4, ensure_ascii=False)
    print(f"Successfully exported {len(tweets)} tweets to {filename}")

def export_to_txt(tweets: list, username: str, filename: str):
    """Exports tweets to a plain text file."""
    header = (
        f"Tweets from @{username}\n"
        f"Downloaded on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Total tweets: {len(tweets)}\n\n"
        "--------------------\n\n"
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header)
        for tweet in tweets:
            created_at = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"Tweet ID: {tweet.id}\n")
            f.write(f"Posted at: {created_at}\n")
            f.write(f"Text: {tweet.text}\n")
            f.write("\n--------------------\n\n")
    print(f"Successfully exported {len(tweets)} tweets to {filename}")
