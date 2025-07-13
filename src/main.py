import asyncio
import os
import time
from telegram import Bot
from telegram.error import RetryAfter, TimedOut
from telegram.constants import ParseMode

# Import functions from other modules
from src.utils import get_rss_feed_items, get_hacker_news_items, get_github_trending_repos, get_source_emoji
from src.db import load_sent_links, save_sent_link, initialize_db

# --- Configuration Variables ---
# Bot token and channel ID will be read from GitHub Secrets or environment variables.
# For local testing, you can set them here directly or use a .env file.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Initialize the Telegram Bot object with your token.
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Channel ID for display in the Telegram post footer.
TELEGRAM_CHANNEL_ID_FOR_FOOTER = "@AI_Nexus_RSS" # Hardcode this as it's constant for the channel

# --- Function Definitions ---

def format_telegram_post(title, link, summary, source_name_for_emoji_lookup):
    """
    Formats the news item into an HTML string suitable for Telegram.
    Includes a source-specific emoji, title, summary, read more link, and channel ID.

    Args:
        title (str): The title of the news item.
        link (str): The URL of the news item.
        summary (str): A brief summary or description of the news item.
        source_name_for_emoji_lookup (str): The clean source name used to retrieve the specific emoji.

    Returns:
        str: An HTML formatted string for the Telegram post.
    """
    source_emoji = get_source_emoji(source_name_for_emoji_lookup)

    emoji_link = "🔗"
    emoji_channel = "📣"

    if not summary or summary.strip().lower() in [
        "no description available.",
        "click to read more or join the discussion."
    ]:
        summary_text = ""
    else:
        summary_text = f"\n\n{summary}"

    post_content = (
        f"{source_emoji} <b>{title}</b>"
        f"{summary_text}"
        f"\n\n{emoji_link} <a href='{link}'>Read More</a>"
        f"\n\n{emoji_channel} Channel: {TELEGRAM_CHANNEL_ID_FOR_FOOTER}"
    )
    return post_content


def collect_all_news(sent_links):
    """
    Collects and aggregates news items from various sources (RSS, GitHub Trending, Hacker News).
    Ensures uniqueness of news items based on their links.

    Args:
        sent_links (set): A set of previously sent links to avoid duplicates.

    Returns:
        list: A list of tuples, each containing (title, link, summary, source_name_for_emoji_lookup).
    """
    all_news_items = []

    print("\n--- Starting News Collection ---")

    # 1. Collect from RSS Feeds
    all_news_items.extend(get_rss_feed_items("https://hf.co/blog/feed.xml", "Hugging Face Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://jamesg.blog/hf-papers.xml", "Hugging Face Paper", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://www.reddit.com/r/MachineLearning/.rss", "ML Reddit", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://openai.com/blog/rss.xml", "OpenAI Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://thegradient.pub/rss/", "The Gradient", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://jalammar.github.io/feed.xml", "Jay Alammar", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://deepmind.google/blog/rss.xml", "DeepMind Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://news.mit.edu/rss/topic/artificial-intelligence2", "AI From MIT News", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://www.technologyreview.com/feed/", "General News From MIT News", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://blogs.microsoft.com/ai/feed/", "Microsoft AI Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://machinelearningmastery.com/blog/feed/", "machinelearningmastery Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://blogs.nvidia.com/blog/category/ai/feed/", "Nvidia AI Blog", sent_links, limit=10))
    all_news_items.extend(get_rss_feed_items("https://towardsdatascience.com/feed/", "Towards Data Science", sent_links, limit=10))

    # 2. Collect from GitHub Trending
    all_news_items.extend(get_github_trending_repos(language="python", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="jupyter-notebook", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="google colab", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="Artificial Intelligence", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="AI", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="machine-learning", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="deep-learning", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="nlp", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="Natural Language Processing", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="CV", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="Computer Vision", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="Data Science", sent_links=sent_links, limit=10))
    all_news_items.extend(get_github_trending_repos(language="Awesome Lists", sent_links=sent_links, limit=10))

    # 3. Collect from Hacker News API
    all_news_items.extend(get_hacker_news_items(sent_links=sent_links, limit=10))

    unique_news_items = {}
    for title, link, summary, source_name_for_emoji_lookup in all_news_items:
        unique_news_items[link] = (title, link, summary, source_name_for_emoji_lookup)
    
    final_news_list = list(unique_news_items.values())

    print(f"Total unique new items collected: {len(final_news_list)}")
    print("--- News Collection Finished ---")

    return final_news_list


async def send_news_to_telegram(news_items):
    """
    Sends collected news items to the Telegram channel.
    Manages Telegram's Flood Control by waiting when necessary.
    Saves sent links to prevent duplicates.

    Args:
        news_items (list): A list of tuples, each containing
                           (title, link, summary, source_name_for_emoji_lookup).
    """
    print("\n--- Starting to send news to Telegram ---")
    if not news_items:
        print("No new items to send.")
        return

    sent_count = 0

    for title, link, summary, source_name_for_emoji_lookup in news_items:
        # Check if the link has already been sent (using load_sent_links for real-time check against DB)
        # This is a final safeguard, as get_... functions already filter based on the initial sent_links.
        if link in load_sent_links():
            print(f"SKIPPED (already sent in this or previous run): {title}")
            continue
            
        formatted_msg = format_telegram_post(title, link, summary, source_name_for_emoji_lookup) 
        
        try:
            await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=formatted_msg, parse_mode=ParseMode.HTML)
            save_sent_link(link) # Save the link to DB after successful sending.
            print(f"SUCCESS: '{title}' sent to Telegram.")
            sent_count += 1
            await asyncio.sleep(3) # Wait to prevent hitting Telegram's rate limits.
        except RetryAfter as e:
            wait_time = e.retry_after + 1 
            print(f"Telegram Flood Control: Waiting for {wait_time} seconds before retrying...")
            await asyncio.sleep(wait_time)
            
            try:
                await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=formatted_msg, parse_mode=ParseMode.HTML)
                save_sent_link(link)
                print(f"SUCCESS (retry): '{title}' sent to Telegram after waiting.")
                sent_count += 1
                await asyncio.sleep(3)
            except Exception as retry_e:
                print(f"ERROR (retry failed): Could not send '{title}' after waiting: {retry_e}")
        except TimedOut:
            print(f"TIMEOUT: Telegram API connection timed out for '{title}'. Retrying in 5 seconds.")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"ERROR: Could not send '{title}' to Telegram: {e}")
            
    print(f"--- Finished sending news to Telegram ---")
    print(f"Total items sent: {sent_count}")


async def main_bot_run():
    """
    Orchestrates the entire news bot operation:
    1. Initializes the database for sent links.
    2. Loads previously sent links from the database.
    3. Collects news from all configured sources.
    4. Sends new, filtered news items to Telegram.
    5. Measures and prints the total execution time of the run.
    """
    start_time = time.time()

    print(f"\n--- Bot run started at: {time.ctime()} ---")

    # Ensure the database is initialized
    initialize_db()
    
    # Load previously sent links from the database
    # This 'sent_links' will be passed to collection functions to avoid duplicate fetches
    initial_sent_links = load_sent_links() 
    print(f"Number of previously sent links loaded from DB: {len(initial_sent_links)}")

    # Pass the initial_sent_links to the collection function
    collected_news = collect_all_news(initial_sent_links) 
    await send_news_to_telegram(collected_news)

    end_time = time.time()
    duration = end_time - start_time

    print(f"--- Bot run finished at: {time.ctime()} ---")
    print(f"Total execution time: {duration:.2f} seconds")

# This block ensures main_bot_run() is executed when the script is run directly.
if __name__ == "__main__":
    asyncio.run(main_bot_run())
