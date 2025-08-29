import time
import tweepy

class TwitterAPIClient:
    """A wrapper for the Tweepy client to handle X API v2 interactions."""

    def __init__(self, bearer_token: str):
        """
        Initializes the TwitterAPIClient.

        Args:
            bearer_token: The X API v2 bearer token.
        """
        self.client = tweepy.Client(bearer_token)

    def get_user_id(self, username: str) -> str | None:
        """
        Fetches the user ID for a given username.

        Args:
            username: The X username (without '@').

        Returns:
            The user ID as a string, or None if the user is not found.
        """
        try:
            response = self.client.get_user(username=username)
            if response.data:
                return response.data.id
            return None
        except tweepy.errors.TweepyException as e:
            print(f"Error fetching user '{username}': {e}")
            return None

    def get_all_tweets(
        self,
        user_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
        include_replies: bool = False,
        include_retweets: bool = False,
    ):
        """
        Fetches all public tweets for a given user ID, handling pagination and rate limits.

        Args:
            user_id: The ID of the user whose tweets are to be fetched.
            start_time: The start time for filtering tweets (YYYY-MM-DDTHH:MM:SSZ).
            end_time: The end time for filtering tweets (YYYY-MM-DDTHH:MM:SSZ).
            include_replies: Whether to include replies.
            include_retweets: Whether to include retweets.

        Yields:
            A tweet object from the API response.
        """
        tweet_fields = [
            "id",
            "text",
            "created_at",
            "author_id",
            "public_metrics",
            "entities",
        ]

        exclude = []
        if not include_replies:
            exclude.append("replies")
        if not include_retweets:
            exclude.append("retweets")

        paginator = tweepy.Paginator(
            self.client.get_users_tweets,
            id=user_id,
            start_time=start_time,
            end_time=end_time,
            exclude=exclude if exclude else None,
            tweet_fields=tweet_fields,
            max_results=100,
        )

        wait_time = 1  # Initial wait time for exponential backoff
        page_iterator = iter(paginator)

        while True:
            try:
                response = next(page_iterator)
                if response.data:
                    for tweet in response.data:
                        yield tweet
                # Reset wait time on successful request
                wait_time = 1
            except StopIteration:
                break  # Finished iterating
            except tweepy.errors.TooManyRequests:
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
                # Exponential backoff, max wait time of 15 minutes (900s)
                wait_time = min(wait_time * 2, 900)
                # Continue to retry the same page
                continue
            except tweepy.errors.TweepyException as e:
                print(f"An unexpected API error occurred: {e}")
                break
