import feedparser
import requests
from bs4 import BeautifulSoup
import time

# Assuming sent_links is passed as an argument or loaded from db.py
# The actual sent_links set will be managed and passed from main.py

def get_source_emoji(source_name):
    """
    Returns an appropriate emoji based on the news source's name.

    Args:
        source_name (str): The clean name of the news source (e.g., "Hugging Face Blog").

    Returns:
        str: An emoji string.
    """
    emoji_map = {
        # RSS Feeds
        "Hugging Face Blog": "🤗",  # Blog posts from Hugging Face
        "Hugging Face Paper": "📝", # Papers/research related to Hugging Face from JamesG's blog
        "ML Reddit": "🤖",          # Machine Learning discussions from Reddit
        "OpenAI Blog": "✨",        # OpenAI's latest breakthroughs
        "The Gradient": "📜",       # In-depth articles and essays on AI
        "Jay Alammar": "💡",        # Visual explanations and deep dives
        "DeepMind Blog": "🔬",       # Scientific research from DeepMind
        "AI From MIT News": "🎓",   # AI news directly from MIT
        "General News From MIT News": "🏛️", # Broader tech/science from MIT
        "Microsoft AI Blog": "💻",  # Microsoft's AI advancements
        "machinelearningmastery Blog": "👨‍🏫", # Practical ML tutorials
        "Nvidia AI Blog": "🚀",     # NVIDIA's AI hardware & software news
        "Towards Data Science": "📊",# Data Science articles and tutorials
        "Hacker News": "🧑‍💻",        # Hacker News latest news
        "The Verge": "🟣",        # The Verge latest articles
        

        # GitHub Trending (using specific language/topic emojis where applicable)
        "GitHub Trending (python)": "🐍",
        "GitHub Trending (jupyter-notebook)": "📓",
        "GitHub Trending (google colab)": "☁️", # Google Colab specific
        "GitHub Trending (Artificial Intelligence)": "🧠",
        "GitHub Trending (AI)": "🧠",
        "GitHub Trending (machine-learning)": "📈",
        "GitHub Trending (deep-learning)": "🌌", # Deep learning, cosmic feel
        "GitHub Trending (nlp)": "🗣️", # Natural Language Processing, talking
        "GitHub Trending (Natural Language Processing)": "🗣️",
        "GitHub Trending (CV)": "👁️", # Computer Vision, eye
        "GitHub Trending (Computer Vision)": "👁️",
        "GitHub Trending (Data Science)": "🧪", # Data Science, lab/experiment
        "GitHub Trending (Awesome Lists)": "⭐", # Curated lists
    }
    return emoji_map.get(source_name, "✨")

# --- Define a common User-Agent header ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}


def get_rss_feed_items(feed_url, source_name, sent_links, limit=15):
    """
    Retrieves new news items from an RSS feed, including title, link, and summary.
    No emoji prefix is added here, as it's handled by format_telegram_post.

    Args:
        feed_url (str): The URL of the RSS feed.
        source_name (str): The name of the source (e.g., "Hugging Face Blog").
        sent_links (set): A set of previously sent links to avoid duplicates.
        limit (int): Maximum number of items to return.

    Returns:
        list: A list of tuples (title, link, summary, source_name_for_emoji_lookup).
    """
    print(f"Retrieving news from RSS: {source_name} ({feed_url})")
    items = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:limit]:
            title = getattr(entry, 'title', "No Title")
            link = getattr(entry, 'link', None)
            summary = getattr(entry, 'summary', getattr(entry, 'description', title))
            
            summary = BeautifulSoup(summary, "html.parser").get_text(separator=' ', strip=True)
            summary = (summary[:200] + '...') if len(summary) > 200 else summary

            # Add a small delay after processing each entry
            time.sleep(0.3)
            
            if link and link not in sent_links:
                items.append((f"{source_name}: {title}", link, summary, source_name))
            else:
                if link:
                    print(f"Duplicate link from {source_name} ignored: {link}")
        return items
    except Exception as e:
        print(f"Error retrieving RSS from {source_name}: {e}")
        return []

def get_hacker_news_items(sent_links, limit=10):
    """
    Retrieves top news items from Hacker News API, including title, link, and a short summary.
    No emoji prefix is added here, as it's handled by format_telegram_post.

    Args:
        sent_links (set): A set of previously sent links to avoid duplicates.
        limit (int): Maximum number of items to return.

    Returns:
        list: A list of tuples (title, link, summary, source_name_for_emoji_lookup).
    """
    source_name = "Hacker News"
    print(f"Retrieving news from Hacker News")
    items = []
    try:
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

        # --- Delay before first request to Hacker News ---
        time.sleep(1)
        
        top_story_ids = requests.get(top_stories_url).json()

        for story_id in top_story_ids[:limit]:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

            # --- Delay before each individual story request ---
            time.sleep(0.5)
            
            story_data = requests.get(item_url).json()

            title = story_data.get('title', "No Title")
            link = story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}")
            summary = story_data.get('text', "Click to read more or join the discussion.")
            summary = BeautifulSoup(summary, "html.parser").get_text(separator=' ', strip=True)
            summary = (summary[:200] + '...') if len(summary) > 200 else summary

            if title and link and link not in sent_links:
                items.append((f"{source_name}: {title}", link, summary, source_name))
            else:
                if link:
                    print(f"Duplicate link from {source_name} ignored: {link}")
        return items
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving Hacker News: {e}")
        return []
    except Exception as e:
        print(f"General error in Hacker News: {e}")
        return []

def get_github_trending_repos(language, sent_links, limit=10):
    """
    Scrapes trending GitHub repositories, including title, link, and description.
    No emoji prefix is added here, as it's handled by format_telegram_post.

    Args:
        language (str): The programming language to search for (e.g., "python").
        sent_links (set): A set of previously sent links to avoid duplicates.
        limit (int): Maximum number of repositories to return.

    Returns:
        list: A list of tuples (title, link, summary, source_name_for_emoji_lookup).
    """
    source_name = f"GitHub Trending ({language})"
    url = f"https://github.com/trending/{language}"
    print(f"Retrieving news from GitHub Trending: {language} ({url})")
    items = []
    try:

        # --- Delay before GitHub Trending request ---
        time.sleep(1)
        
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        for article_tag in soup.select("article.Box-row")[:limit]:
            title_tag = article_tag.select_one("h2 a")
            description_tag = article_tag.select_one("p.col-9")
            
            repo_name = title_tag.text.strip().replace("\n", "").replace(" ", "") if title_tag else "No Repository Name"
            link = "https://github.com" + title_tag["href"] if title_tag and "href" in title_tag.attrs else None
            summary = description_tag.text.strip() if description_tag else "No description available."
            summary = (summary[:200] + '...') if len(summary) > 200 else summary

            if link and link not in sent_links:
                items.append((f"{source_name}: {repo_name}", link, summary, source_name))
            else:
                if link:
                    print(f"Duplicate link from GitHub Trending ignored: {link}")
        return items
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving GitHub Trending: {e}")
        return []
    except Exception as e:
        print(f"General error in GitHub Trending: {e}")
        return []
