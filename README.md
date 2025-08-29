# TweetDownloader

TweetDownloader is a Python command-line tool for downloading all public tweets from a specified X (formerly Twitter) user's account and exporting them to a formatted document file. It is designed to be user-friendly, ethically conscious, and robust.

## Features

- **Download All Public Tweets**: Fetches the entire public tweet history of a user (subject to API limitations).
- **Multiple Export Formats**: Export tweets to Markdown, JSON, or plain TXT files.
- **Secure**: Uses environment variables or a secure prompt for your X API Bearer Token. Your keys are never hardcoded or stored.
- **Rate Limit Handling**: Automatically handles API rate limits with exponential backoff.
- **Filtering**: Options to include or exclude replies and retweets.
- **Date Filtering**: Specify a date range (`--since` and `--until`) for the download.
- **User-Friendly**: Clear progress indicators and command-line arguments.

## Ethical Disclaimer

This tool is intended for personal and archival purposes only. By using it, you agree to comply with the [X Developer Agreement and Policy](https://developer.x.com/en/developer-terms/agreement-and-policy). This tool should not be used for scraping, spamming, or any other activity that violates X's terms of service. The developer of this tool is not responsible for any misuse.

---

## Setup and Installation

### 1. Prerequisites

- Python 3.10+
- A free [X Developer Account](https://developer.x.com/en/docs/projects/overview) to get API access.

### 2. Get Your Bearer Token

1.  **Apply for a Developer Account**: Go to the [X Developer Portal](https://developer.x.com/en/portal/dashboard) and sign up for a new account. You may need to describe your intended use case (e.g., "Archiving my own tweets for personal analysis").
2.  **Create a New Project**: Once approved, create a new Project and an App within that project.
3.  **Get Your Keys**: In your App's "Keys and Tokens" section, you will find your **Bearer Token**. This token provides read-only access to the X API v2, which is exactly what this tool needs.

### 3. Install the Tool

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/TweetDownloader.git
    cd TweetDownloader
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set the Bearer Token:**
    It is highly recommended to set your Bearer Token as an environment variable.

    **On macOS/Linux:**
    ```bash
    export BEARER_TOKEN="YOUR_BEARER_TOKEN_HERE"
    ```
    To make this permanent, add the line above to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`).

    **On Windows:**
    ```powershell
    $env:BEARER_TOKEN="YOUR_BEARER_TOKEN_HERE"
    ```
    If you do not set the environment variable, the tool will prompt you to enter the token securely when you run it.

---

## Usage

The main script is `src/tweet_downloader.py`.

### Basic Example

Download all tweets from the user `@x_ai` and save them to `x_ai_tweets.md`:

```bash
python src/tweet_downloader.py --username x_ai
```

### Advanced Example

Download all tweets from `@elonmusk` between January 1, 2023, and December 31, 2023, including replies, and save them to a JSON file named `elon_2023.json`:

```bash
python src/tweet_downloader.py \
  --username elonmusk \
  --since 2023-01-01 \
  --until 2023-12-31 \
  --include-replies \
  --format json \
  -o elon_2023
```

### All Command-Line Arguments

- `--username` (required): The X username.
- `-o`, `--output`: The name of the output file (without extension). Defaults to `[username]_tweets`.
- `--format`: The output format. Choices: `md`, `json`, `txt`. Defaults to `md`.
- `--include-replies`: Flag to include replies.
- `--include-retweets`: Flag to include retweets.
- `--since`: Start date for tweets (YYYY-MM-DD).
- `--until`: End date for tweets (YYYY-MM-DD).

---

## Example Output (`.md` format)

```markdown
# Tweets from @x_ai

Downloaded on: 2023-10-27 10:00:00
Total tweets: 1

---

**Tweet ID:** 1717842233931694237
**Posted at:** 2023-10-27 08:30:00
**Link:** https://x.com/x_ai/status/1717842233931694237
**Metrics:** 1000 Likes, 200 Retweets, 50 Replies

> The most powerful AI in the universe.

---
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
