# AI News Aggregator Bot 🧠🚀

A Python-powered Telegram bot designed for real-time aggregation and delivery of cutting-edge news in Artificial Intelligence (AI), Machine Learning (ML), Deep Learning (DL), and Natural Language Processing (NLP). This project demonstrates robust data collection, intelligent content curation, and automated deployment practices, making it a valuable asset for staying updated in the rapidly evolving AI landscape.

## ✨ Features

* **Comprehensive Data Aggregation:** Gathers news and updates from a diverse array of leading sources including:
    * **Research Blogs:** Hugging Face, OpenAI, DeepMind, Google AI, Microsoft AI, Meta AI, Amazon Science, Nvidia AI.
    * **Academic & Knowledge Platforms:** arXiv (for NLP papers), Papers With Code, The Gradient, Jay Alammar's blog, machinelearningmastery, Towards Data Science, MIT News (AI & General Tech).
    * **Community & Trends:** Reddit (Machine Learning subreddits), Hacker News (general CS & tech discussions).
    * **GitHub Trending:** Identifies top trending repositories across relevant languages and topics (Python, Jupyter Notebook, Google Colab, AI, ML, DL, NLP, CV, Data Science, Awesome Lists).
* **Automated & Timely Updates:** Configured to run automatically every ~3 hours (or chosen interval) via GitHub Actions, ensuring consistent and fresh news delivery.
* **Intelligent Duplicate Prevention:** Utilizes an SQLite database (`sent_links.db`) to persistently track and prevent the re-sending of previously posted news links across multiple runs.
* **Rich Telegram Formatting:** Delivers news with dynamic, source-specific emojis, bold titles, concise summaries, and clear "Read More" hyperlinks for an engaging user experience.
* **Scalable & Modular Architecture:** Designed with clear separation of concerns (`main.py`, `utils.py`, `db.py`) for easy maintenance, extension, and testing.
* **Secure Credential Handling:** Leverages GitHub Secrets for secure storage and management of sensitive API tokens.

## 🚀 Technologies Used

* **Python 3.x:** Core programming language.
* **`python-telegram-bot`:** Official Telegram Bot API wrapper for seamless communication.
* **`feedparser`:** For robust parsing of RSS/Atom feeds from various blogs and academic sources.
* **`requests`:** For making HTTP requests to retrieve web content and API data.
* **`BeautifulSoup4`:** For efficient web scraping (e.g., GitHub Trending) and HTML content cleaning.
* **`sqlite3`:** Built-in Python library for local, file-based database management (for persistent storage).
* **GitHub Actions:** For Continuous Integration/Continuous Deployment (CI/CD), enabling automated, scheduled execution of the bot.

## ⚙️ Setup and Installation

To set up and run this bot locally for development or contribute:

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

## 🚀 Deployment (GitHub Actions)

This bot is designed for automated deployment using GitHub Actions, ensuring consistent updates without manual intervention.

1.  **Push your code to GitHub:** Ensure all your project files, including `src/` directory, `requirements.txt`, and `.github/workflows/main.yml`, are pushed to your GitHub repository.

2.  **Configure GitHub Secrets:**
    * In your GitHub repository, navigate to `Settings` > `Secrets and variables` > `Actions`.
    * Add two new repository secrets:
        * `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token.
        * `TELEGRAM_CHANNEL_ID`: Your Telegram channel's username (e.g., `@YourChannelUsername`) or numeric ID.

3.  **Monitor Workflows:**
    * Go to the `Actions` tab in your GitHub repository.
    * You'll see the "AI News Aggregator Bot" workflow. It's scheduled to run automatically (e.g., every 3 hours).
    * You can also manually trigger a run by clicking "Run workflow" from the workflow's page.
    * The `sent_links.db` file will be created and persisted across runs using GitHub Actions' artifact caching.

## 🤝 Contribution

Contributions are welcome! If you have suggestions for new news sources, improvements to the scraping logic, or general enhancements, feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
