import os

from linebot.v3.messaging import (
    ApiClient,
    ApiException,
    BroadcastRequest,
    Configuration,
    MessagingApi,
    TextMessage,
)

from libs.hacker_news import get_top_stories
from libs.vertex import summarize_with_vertex_ai

# --- LINE Configuration ---
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

# --- Vertex AI Configuration ---
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "dev-projects-476011")


def main():
    """
    Fetches, summarizes, and broadcasts top 10 Hacker News stories.
    """
    if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET]):
        print("Error: Please set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET.")
        return

    top_stories = get_top_stories(10)

    if not top_stories:
        print("No stories fetched from Hacker News.")
        return

    message_lines = []
    for story in top_stories:
        title = story.get("title", "No Title")
        url = story.get("url", "No URL")
        message_lines.append(f"- {title}: {url}")

    stories_as_text = "\n".join(message_lines)

    print("Generating summary with Vertex AI...")
    summary_message = summarize_with_vertex_ai(stories_as_text)

    print("Prepared message to broadcast:", summary_message)

    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    api_client = ApiClient(configuration)
    line_bot_api = MessagingApi(api_client)

    try:
        broadcast_request = BroadcastRequest(
            messages=[TextMessage(text=summary_message)]
        )
        line_bot_api.broadcast(broadcast_request)
        print("Successfully broadcasted summary to LINE.")
    except ApiException as e:
        print(f"Error sending message to LINE: {e.body}")


if __name__ == "__main__":
    main()
