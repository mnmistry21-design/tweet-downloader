import argparse
import sys
from datetime import datetime

from src.config import get_bearer_token
from src.api_client import TwitterAPIClient
from src.exporter import export_to_markdown, export_to_json, export_to_txt

def main():
    """Main function to run the TweetDownloader."""
    parser = argparse.ArgumentParser(
        description="Download all public tweets from a specified X user's account."
    )
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="The X username of the user whose tweets you want to download.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="The name of the output file (without extension). Defaults to '[username]_tweets'.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="md",
        choices=["md", "json", "txt"],
        help="The format of the output file. Defaults to Markdown ('md').",
    )
    parser.add_argument(
        "--include-replies",
        action="store_true",
        help="Include replies in the download.",
    )
    parser.add_argument(
        "--include-retweets",
        action="store_true",
        help="Include retweets in the download (Note: X API v2 does not return full retweet text).",
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Start date for fetching tweets (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--until",
        type=str,
        help="End date for fetching tweets (YYYY-MM-DD).",
    )

    args = parser.parse_args()

    # Get Bearer Token
    bearer_token = get_bearer_token()

    # Initialize API client
    api_client = TwitterAPIClient(bearer_token)

    # Get user ID
    print(f"Fetching user ID for '{args.username}'...")
    user_id = api_client.get_user_id(args.username)
    if not user_id:
        print(f"User '{args.username}' not found. Exiting.")
        sys.exit(1)
    print(f"User ID found: {user_id}")

    # Format dates for API
    start_time = f"{args.since}T00:00:00Z" if args.since else None
    end_time = f"{args.until}T23:59:59Z" if args.until else None

    # Fetch tweets
    print("Fetching tweets... (This may take a while for users with many tweets)")
    all_tweets = []
    try:
        tweet_iterator = api_client.get_all_tweets(
            user_id,
            start_time=start_time,
            end_time=end_time,
            include_replies=args.include_replies,
            include_retweets=args.include_retweets,
        )
        for i, tweet in enumerate(tweet_iterator):
            all_tweets.append(tweet)
            if (i + 1) % 100 == 0:
                print(f"Fetched {i + 1} tweets so far...")
    except Exception as e:
        print(f"An error occurred during tweet fetching: {e}")
        sys.exit(1)

    if not all_tweets:
        print("No tweets found for the specified criteria.")
        sys.exit(0)

    print(f"\nTotal tweets downloaded: {len(all_tweets)}")

    # Export tweets
    output_file = args.output or f"{args.username}_tweets"
    filename = f"{output_file}.{args.format}"

    if args.format == "md":
        export_to_markdown(all_tweets, args.username, filename)
    elif args.format == "json":
        export_to_json(all_tweets, filename)
    elif args.format == "txt":
        export_to_txt(all_tweets, args.username, filename)

if __name__ == "__main__":
    main()
