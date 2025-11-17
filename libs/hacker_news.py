import requests

# --- Hacker News API Configuration ---
HN_API_BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{HN_API_BASE_URL}/topstories.json"
ITEM_URL = f"{HN_API_BASE_URL}/item"


def get_top_stories(limit=10):
    """Fetches the top stories from Hacker News."""
    try:
        response = requests.get(TOP_STORIES_URL)
        response.raise_for_status()
        story_ids = response.json()

        stories = []
        for story_id in story_ids[:limit]:
            story_response = requests.get(f"{ITEM_URL}/{story_id}.json")
            story_response.raise_for_status()
            stories.append(story_response.json())
        return stories
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Hacker News API: {e}")
        return []
