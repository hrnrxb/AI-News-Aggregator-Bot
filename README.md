# 🤖💡 AI News Aggregator Bot: Your Smart Companion in the World of AI 💡🤖

Tired of struggling to keep up with the latest advancements in the fast-paced world of Artificial Intelligence?
This Python-powered Telegram bot is your ultimate solution!
The **AI News Aggregator Bot** collects the newest and most critical news from the fields of **Artificial Intelligence (AI), Machine Learning (ML), Deep Learning (DL),** and **Natural Language Processing (NLP)** in real-time, delivering it directly to you.

This project is more than just a simple bot; it's a powerful demonstration of **robust data collection, intelligent content curation, and automated deployment practices**. It's an invaluable asset for anyone who wants to stay updated in the constantly evolving AI landscape.

---

## ✨ Standout Features: Why Choose This Bot?

* **Unparalleled Comprehensive Data Aggregation:**
    This bot gathers news and updates from a diverse array of leading and authoritative sources. Imagine having all key information, from the most reputable sources, in one place!
    * **Leading Research Blogs:** Hugging Face, OpenAI, DeepMind, Google AI, Microsoft AI, Meta AI, Amazon Science, Nvidia AI (the latest innovations directly from the source).
    * **Academic & Knowledge Platforms:** arXiv (for the newest NLP papers), Papers With Code (linked code and papers), The Gradient, Jay Alammar's blog (in-depth explanations), machinelearningmastery, Towards Data Science (practical insights), MIT News (general AI & tech news).
    * **Community & Trends:** Reddit (Machine Learning subreddits for community discussions), Hacker News (general CS & tech discussions).
    * **GitHub Trending:** Identifies top trending repositories across relevant languages and topics (Python, Jupyter Notebook, Google Colab, AI, ML, DL, NLP, CV, Data Science, Awesome Lists) – always stay on top of hot projects!

* **Automated & Timely Updates:**
    The bot is configured to run automatically every ~5 hours (or your chosen interval) via **GitHub Actions**. This ensures you consistently receive the freshest news.

* **Intelligent Duplicate Prevention:**
    Using an SQLite database (`sent_links.db`), the bot persistently tracks previously sent news links. This means **no more redundant news!** You'll only receive new, relevant content.

* **Rich and Engaging Telegram Formatting:**
    News is delivered with dynamic, source-specific emojis, **bold titles**, concise summaries, and clear "Read More" hyperlinks for an engaging and user-friendly experience.

* **Scalable & Modular Architecture:**
    Designed with clear separation of concerns (`main.py`, `utils.py`, `db.py`) for easy maintenance, extension, and testing.

* **Secure Credential Handling:**
    Leverages **GitHub Secrets** for secure storage and management of sensitive API tokens. Your information is safe!

---

## 🚀 Technologies Used: The Project's Beating Heart

This bot is built using a powerful stack of technologies:

* **Python 3.x:** The core programming language providing power and flexibility.
* **`python-telegram-bot`:** The official and robust library for seamless communication with the Telegram Bot API.
* **`feedparser`:** For robust parsing of RSS/Atom feeds from various blogs and academic sources.
* **`requests`:** For making HTTP requests to retrieve web content and API data.
* **`BeautifulSoup4`:** For efficient web scraping (e.g., GitHub Trending) and HTML content cleaning.
* **`sqlite3`:** Python's built-in library for local, file-based database management (for persistent storage).
* **GitHub Actions:** The **CI/CD** (Continuous Integration / Continuous Deployment) core of the project, enabling automated, scheduled execution of the bot.

---

## ⚙️ Setup and Installation: How to Get It for Yourself?

To set up and run this bot locally for development or contribution:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/AI-News-Aggregator-Bot.git](https://github.com/your-username/AI-News-Aggregator-Bot.git)
    cd AI-News-Aggregator-Bot
    ```

2.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Telegram Bot Token & Channel ID:**
    * Create a new bot via Telegram's @BotFather and get your `TELEGRAM_BOT_TOKEN`.
    * Create a Telegram channel and add your bot as an administrator. Get your `TELEGRAM_CHANNEL_ID` (e.g., `@YourChannelUsername` or numeric ID).
    * For **local development**, create a `.env` file in the root directory and add your credentials:
        ```
        TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
        TELEGRAM_CHANNEL_ID="@YOUR_CHANNEL_USERNAME_OR_ID_HERE"
        ```
        (Note: For production/GitHub Actions, these are handled via GitHub Secrets.)

5.  **Run the Bot (Local Testing):**
    ```bash
    python src/main.py
    ```
    The bot will run, collect news, and send it to your configured Telegram channel. A `sent_links.db` file will be created locally to track sent links.

---

## 🚀 Seamless Deployment with GitHub Actions: Set It and Forget It!

This bot is designed for automated deployment using GitHub Actions, ensuring consistent updates without manual intervention.

1.  **Push your code to GitHub:** Ensure all your project files, including the `src/` directory, `requirements.txt`, and `.github/workflows/main.yml`, are pushed to your GitHub repository.

2.  **Configure GitHub Secrets:**
    * In your GitHub repository, navigate to `Settings` > `Secrets and variables` > `Actions`.
    * Add two new repository secrets:
        * `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token.
        * `TELEGRAM_CHANNEL_ID`: Your Telegram channel's username (e.g., `@YourChannelUsername`) or its numeric ID.

3.  **Monitor Workflows:**
    * Go to the `Actions` tab in your GitHub repository.
    * You'll see the "AI News Aggregator Bot" workflow. It's scheduled to run automatically (e.g., every 5 hours).
    * You can also manually trigger a run by clicking "Run workflow" from the workflow's page.
    * The `sent_links.db` file will be created and persisted across runs using GitHub Actions' artifact caching.

---

## 🤝 Contribution: We Get Better With Your Help!

Your contributions are highly welcome! If you have suggestions for new news sources, improvements to the scraping logic, or general enhancements, feel free to open an issue or submit a pull request.

---

## 📄 License: Freedom to Use!

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
