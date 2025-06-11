# BriefBot 📰🤖

**Get a daily synthesized summary of top news across sources.**

BriefBot is a Python-based automation tool that pulls the day’s top headlines from categories of interest, identifies clusters of articles covering the same story, and then synthesizes them into a coherent, long-form summary. Finally, it delivers these summaries directly to your inbox in a clean, styled HTML email.

It’s built for people who want to stay informed without drowning in dozens of articles. By pulling from multiple sources and distilling the essential information into readable summaries, BriefBot gives you a clear, unbiased snapshot of the day’s most important stories.

---

## ✨ Features

- 📡 Pulls from a wide set of **RSS feeds** across political and tech news   
- 🔍 **Clusters articles** covering the same story for deeper understanding  
- 📝 Synthesizes **long-form summaries** using the **Mistral AI API**  
- 📬 Sends you a personalized, styled **daily email digest**  
- ⚙️ Fully automated via **GitHub Actions**

---

## 🛠 Tech Stack

- Python  
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) – for sentence embeddings via `sentence-transformers`
- [Sentence-Transformers](https://www.sbert.net/) – semantic text embeddings used in clustering
- [Mistral AI](https://mistral.ai/)  
- [Feedparser](https://pypi.org/project/feedparser/) (RSS parsing)  
- [Trafilatura](https://pypi.org/project/trafilatura/) (article text extraction)  
- Gmail SMTP (for email delivery)  
- GitHub Actions (for daily automation)

---

## 🚀 Getting Started

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/yourusername/briefbot.git
cd briefbot
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Set up your environment variables
Create a `.env` file in the root directory with the following secrets (or use GitHub repository secrets):

```ini
MISTRAL_KEY=your_mistral_api_key
EMAIL_PASSWORD=your_email_smtp_password
EMAIL=youremail@gmail.com
SENDER=BriefBot <youremail@gmail.com>
RECIPIENT=youremail@gmail.com
```

### 3. Run once manually

```bash
python main.py
```
Or let it run automatically every day using GitHub Actions (see `.github/workflows/daily.yml`).

---

## 📌 Notes & Limitations

- ⚠️ Mistral API limits (if using the free tier) may restrict how many summaries you can generate per day
- 📰 Article quality and coverage depends on the RSS feeds you choose
- Currently focused on political and tech news - can be adjusted depending on personal interests (you'll need to find other RSS feeds)
- During development and testing, you can speed up iterations and avoid making lots of API requests by enabling JSON caching of intermediate results. To do this, set `USE_CACHE = True` in `main.py`.

---

## 🧠 Why It’s Useful

- 💤 No more doomscrolling — just one clean daily email with all the context you need
- 🗞️ Synthesized from multiple sources to reduce bias
- 📚 Prioritizes depth over brevity, for people who actually want to understand the news
- 🧩 Fully open-source and customizable

---

## 📄 License

MIT  
