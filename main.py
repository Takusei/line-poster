import os

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
)

from libs.hacker_news import get_top_stories

# --- LINE Configuration ---
# Get LINE credentials from environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")


def main():
    """
    Fetches top 10 Hacker News stories and broadcasts them to all LINE followers.
    """
    if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET]):
        print("Error: Please set the following environment variables:")
        print(" - LINE_CHANNEL_ACCESS_TOKEN")
        print(" - LINE_CHANNEL_SECRET")
        return

    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    api_client = ApiClient(configuration)
    line_bot_api = MessagingApi(api_client)

    top_stories = get_top_stories(10)

    if not top_stories:
        print("No stories fetched from Hacker News.")
        return

    message_lines = ["Top 10 Hacker News Stories:"]
    for story in top_stories:
        title = story.get("title", "No Title")
        url = story.get("url", "No URL")
        message_lines.append(f"- {title}: {url}")

    message = "\n".join(message_lines)
    print("Prepared message to broadcast:", message)

    # try:
    #     broadcast_request = BroadcastRequest(messages=[TextMessage(text=message)])
    #     line_bot_api.broadcast(broadcast_request)
    #     print("Successfully broadcasted stories to LINE.")
    # except ApiException as e:
    #     print(f"Error sending message to LINE: {e.body}")


if __name__ == "__main__":
    main()
