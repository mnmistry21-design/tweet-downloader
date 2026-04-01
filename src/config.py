import os
import sys
from getpass import getpass

def get_bearer_token() -> str:
    """
    Retrieves the X API Bearer Token.

    It first checks for the 'BEARER_TOKEN' environment variable.
    If the environment variable is not set, it prompts the user to enter the
    token securely.

    Returns:
        str: The Bearer Token.

    Raises:
        SystemExit: If the token is not provided.
    """
    if token := os.environ.get("BEARER_TOKEN"):
        print("Bearer Token found in environment variables.")
        return token
    else:
        print("BEARER_TOKEN environment variable not found.")
        try:
            token = getpass("Please enter your X API Bearer Token: ")
            if not token:
                sys.exit("Error: No Bearer Token provided. Exiting.")
            return token
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(1)
